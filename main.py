#!/usr/bin/env python3

import subprocess
import time
import sys
import os
from shlex import quote 
from pathlib import Path

import eyed3 #install with pip, for ID3v2 music tag parsing
from ytmusicapi import YTMusic
from difflib import SequenceMatcher as fuzzy

def readPlaylist(filename):
    songList = []
    with open(filename,"r") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                songList.append("/storage/"+line.rstrip())
    return songList

def getMetadataFromDevice(paths):
    global failures
    metadata = []
    for path in paths:
        tags = {}
        escapedPath = quote(path)
        if(escapedPath[0]=="'"):
            escapedPath='"'+escapedPath[1:-1]+'"'

        footerCommand = "adb shell 'tail -c 128 "+escapedPath+" |cat -v'"
        footer = subprocess.check_output(footerCommand,shell=True)
        if footer.decode()[0:3] == "TAG":
            #This should be faster, try this first
            tags = parseV1(footer)
        else:
            #pull is different than shell for escaping, ig
            # path = path.replace("'\"'\"'","\\'")
            headerCommand = "adb pull \""+path+"\" tmp.mp3; head -c 3 tmp.mp3"
            headerTag = subprocess.check_output(headerCommand,shell=True)
            if(headerTag.decode()[-3:] == "ID3"):
                tags = parseV2('tmp.mp3')
                subprocess.run(['rm','tmp.mp3'])
            else:
                failures.append(path)
        if len(tags) > 0:
            metadata.append(tags)
    return metadata

def parseV1(adbOutput):
    '''Parses info from a ID3v1 tag.'''
    rawMetadata = adbOutput.decode().replace("^@"," ")
    title=rawMetadata[3:32]
    artist=rawMetadata[33:62]
    album=rawMetadata[63:92]
    year=rawMetadata[93:97]
    return {
        "title": title.strip(),
        "artist": artist.strip(),
        "album": album.strip()
    }

def parseV2(path):
    song = eyed3.load(path)
    return {
        "title": song.tag.title,
        "artist": song.tag.artist,
        "album": song.tag.album
    }

def searchForSongs(yt,songs):
    global searchResults
    global failures

    ids = []
    for song in songs:
        found = False
        results = yt.search((song['title']+" by "+song['artist']), "songs",searchResults)
        if len(results) == 0:
            results = yt.search((song['title']+" by "+song['artist']), "videos",searchResults)
            if len(results) == 0:
                failures.append(song)
                continue
        for result in results:
         #    try:
                # doesntmatch(result,song)
            # except:
                # print(fuzzy(None, result['title'], song['title']).ratio())
                # print(result)
                # # print(fuzzy(None, result['artists'][0]['name'], song['artist']).ratio())
                # print(fuzzy(None, result['album']['name'], song['album']).ratio())
                # exit("fuck")
            if doesntmatch(result,song):
                continue
            else:
                ids.append(result['videoId'])
                found = True
                break
        if not found:
            choice = getInput(song,results)
            if choice == "v":
                theChosenOne = searchForVideos(yt,song)
                if theChosenOne != 0:
                    ids.append(theChosenOne)
            elif choice == "s":
                failures.append(song)
            else:
                ids.append(results[int(choice)]['videoId'])
    return ids

def searchForVideos(yt,song):
    global searchResults
    results = yt.search((song['title']+" by "+song['artist']), "videos",searchResults)
    choice = getInput(song, results)
    if choice == "s":
        return 0
    return results[int(choice)]['videoId']

def getInput(song,results):
    print("\n\nImperfect match found.\n")
    print("Search terms: "+str(song)+"\n")
    print("Results:")

    if results[0]['resultType'] == 'video':
        for i in range(0,len(results)):
            print(str(i)+": "+results[i]['title']+" - "
                +(results[i]['artists'][0]['name'] 
                    if len(results[i]['artists'])>0 else "Unknown"))
    else:
        for i in range(0,len(results)):
            print(str(i)+": "+results[i]['title']+" - "
                +(results[i]['artists'][0]['name'] 
                    if len(results[i]['artists'])>0 else "Unknown")+" - "
                +results[i]["album"]['name'])
        print("\n Or type 'v' to search by videos, s to skip.")
    return input("Pick a result by index: ") #todo: validation here maybe

def doesntmatch(result,song):
    global matchThreshold
    resultTitle = result['title'][0:28].lower()
    songTitle = song['title'][0:28].lower()
    resultAlbum = result['album']['name'][0:28].lower()
    songAlbum = song['album'][0:28].lower()
    resultArtist = (result['artists'][0]['name'][0:28].lower() 
            if len(result['artists']) > 0 else 1
    songArtist = song['artist'][0:28].lower()

    titleRatio = fuzzy(None, resultTitle, songTitle).ratio()
    albumRatio = fuzzy(None, resultAlbum, songAlbum).ratio()
    artistRatio = fuzzy(None, resultArtist, songArtist).ratio()

    meanRatio = (titleRatio + albumRatio + artistRatio) / 3
    return meanRatio < matchThreshold

    return ((fuzzy(None, result['title'][0:28], song['title'][0:28]).ratio()) < matchThreshold
        or ((fuzzy(None, result['artists'][0]['name'][0:28], 
            song['artist'][0:28]).ratio() < matchThreshold) 
            if len(result['artists'])>0 else False)
        or (fuzzy(None, result['album']['name'][0:28], song['album'][0:28]).ratio() < matchThreshold))

if __name__ == '__main__':
    failures=[]
    filename = input('Type in the playlist path: ')
    name = Path(filename).stem

    description = "Playlist generated from M3U by Ella."
    matchThreshold = .7 #1 means perfect match
    searchResults = 28

    paths = readPlaylist(filename)
    songs = getMetadataFromDevice(paths)
    if not os.path.isfile("auth.json"):
        YTMusic.setup("auth.json")
    youtube = YTMusic("auth.json")
    videos = searchForSongs(youtube,songs)
    playlistId = youtube.create_playlist(name,description)
    print(playlistId)
    print(videos)
    with open("videoIds","a") as f:
        f.write(str(videos))
    youtube.add_playlist_items(playlistId,videos)

    print("All done! These are the ones that failed: \n")
    print(failures)
