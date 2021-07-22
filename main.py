#!/usr/bin/python3.9

import subprocess
import time
import sys
import os
from shlex import quote 
import eyed3

def readPlaylist(filename):
    songList = []
    with open(filename,"r") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                songList.append("/storage/"+line.rstrip())
    return songList

def getMetadataFromDevice(paths):
    global badPaths
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
                badPaths.append(path)
        if len(tags) > 0:
            metadata.append(tags)
    return badPaths,metadata

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


filename = 'playlist.m3u8'
badPaths = []

paths = readPlaylist(filename)
songs = getMetadataFromDevice(paths)
print(songs)
youtubeLogin(
createPlaylist(name)
videos = searchForVideos(songs)
addVideos(videos,name)
