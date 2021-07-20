#!/usr/bin/python3

import subprocess
import time
import sys
import os

tracks = importPlaylist(filename)
songs = getMetadataFromDevice(tracks)
createPlaylist(name)
videos = searchForVideos(songs)
addVideos(videos,name)
