#!/usr/bin/python3

import subprocess
import time
import sys
import os

def readPlaylist(filename):
    songList=[]
    with open(filename,"r") as f:
        songList=f.read().splitlines()
    return songList

def getMetadataFromDevice(paths):
    for path in paths:
        #Idk if I can do this from adb.
        #Making a helper app I guess. 
        #Who knows, maybe in the future I can port this to all-Android.
        metadata = subprocess.Popen('adb shell run com.ella.helperapp MainActivity');

filename='playlist.m3u8'

paths = readPlaylist(filename)
songs = getMetadataFromDevice(paths)
createPlaylist(name)
videos = searchForVideos(songs)
addVideos(videos,name)
