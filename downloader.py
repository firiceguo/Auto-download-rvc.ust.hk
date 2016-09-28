# -*- coding: utf-8 -*-

import ConfigParser
from selenium import webdriver
import time
import requests
import urllib
import os
import platform
import threading

# load config file
cf = ConfigParser.ConfigParser()
cf.read("config")
account = cf.get("ITSC", "account")
pwd = cf.get("ITSC", "password")
url = cf.get("lecture", "url")
save_dir = cf.get("local", "save_dir")
threads = cf.getint("local", "threads")

system = platform.system()


def GetRVC():
    '''log in the rvc.ust.hk and get the PlaylistUrl url'''
    print 'Opening the browser......'

    sel = webdriver.Firefox()

    # open the login in page
    sel.get(url)
    time.sleep(5)

    # sign in the username
    try:
        sel.find_element_by_name("UsernameField").send_keys(account)
        print 'user success!'
    except:
        print 'user error!'
    time.sleep(1)
    # sign in the pasword
    try:
        sel.find_element_by_name("PasswordField").send_keys(pwd)
        print 'pw success!'
    except:
        print 'pw error!'
    time.sleep(1)
    # click to login
    try:
        sel.find_element_by_name("EnterButton").click()
        print 'click success!'
    except:
        print 'click error!'
    time.sleep(3)

    # get the play list url
    source = sel.page_source.encode('ascii', 'ignore')
    try:
        rtsp_idx = source.index('rtsp')
        sour = source[rtsp_idx:]
        idx = sour.index('http')
        i = idx
        while sour[i] is not "'":
            i += 1
        PlaylistUrl_0 = sour[idx:i]
        amp_idx = PlaylistUrl_0.index('amp')
        PlaylistUrl = PlaylistUrl_0[:amp_idx] + PlaylistUrl_0[amp_idx+4:]
        print 'Get playlist url:', PlaylistUrl
    except:
        print 'Cannot find playlist source!'

    sel.close()
    return(PlaylistUrl)


def GetVideoList(PlaylistUrl):
    r = requests.get(PlaylistUrl).text.encode('ascii', 'ignore')
    Chunklist_idx = r.index('chunk')
    ChunklistUrl = PlaylistUrl[:PlaylistUrl.index('playlist')] + r[Chunklist_idx:]
    print 'Get chunk list url:', ChunklistUrl

    Chunklist = requests.get(ChunklistUrl).text.encode('ascii', 'ignore')
    Videolist = []
    while 'media' in Chunklist:
        idx = Chunklist.index('media')
        i = idx
        while Chunklist[i] is not '#':
            i += 1
        Videolist.append(PlaylistUrl[:PlaylistUrl.index('playlist')] + Chunklist[idx:i-1])
        Chunklist = Chunklist[i:]
    print 'Get video list success!'
    print 'There are %d chunks' % (len(Videolist))
    return(Videolist)


def GetVideo(Videolist):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    VideoName = []
    for i in xrange(len(Videolist)):
        print 'Downloading the video %d...' % (GetCurrentFileIdx(Videolist[i]))
        r = urllib.urlopen(Videolist[i]).read()
        filename = save_dir + str(GetCurrentFileIdx(Videolist[i])) + '.ts'
        VideoName.append(str(i) + '.ts')
        with open(filename, 'wb') as f:
            f.write(r)


def MergeTS(VideoName, dir):
    num = len(VideoName)
    os.chdir(dir)
    print 'Merging videos ......'
    if system is 'Windows':
        for i in xrange(1, num):
            cmd = 'copy /b %s+%s %s' % (VideoName[0], VideoName[i], VideoName[0])
            os.system(cmd)
            os.remove(VideoName[i])
    elif system is 'Linux':
        for i in xrange(1, num):
            cmd = 'cat %s %s > %s' % (VideoName[0], VideoName[i], VideoName[0])
            os.system(cmd)
            os.remove(VideoName[i])
    else:
        print 'Sorry, it seems that I donnot know how to merge .ts file in your system.'
    os.chdir('../')


def GetCurrentFileIdx(VideoUrl):
    ts = VideoUrl.split('.')[-2]
    idx = int(ts.split('_')[-1])
    return(idx)

if __name__ == '__main__':
    PlaylistUrl = GetRVC()
    Videolist = GetVideoList(PlaylistUrl)

    # assign each threads' workload
    if threads > len(Videolist):
        threads = len(Videolist)
    num = len(Videolist) / threads
    mod = len(Videolist) % threads
    thrVideolist = [[]]*threads
    x = 0
    for i in xrange(threads):
        thrVideolist[i] = Videolist[x:x+num]
        x += num
        if i < mod:
            thrVideolist[i].append(Videolist[x:x+1])
            x += 1
    print thrVideolist

    # establish threads
    thr = []
    for i in xrange(threads):
        t = threading.Thread(target=GetVideo, args=(thrVideolist[i],))
        thr.append(t)
        t.start()

    # wait every threads to complete tasks
    for i in xrange(threads):
        thr[i].join()

    # sort the VideoName according to the number not the ascii code
    VideoName = os.listdir(save_dir)
    for i in xrange(len(VideoName)):
        VideoName[i] = int(VideoName[i].split('.')[0])
    VideoName = sorted(VideoName)
    for i in xrange(len(VideoName)):
        VideoName[i] = str(VideoName[i])+'.ts'

    # merge the videos downloaded into one file
    MergeTS(VideoName, save_dir)
