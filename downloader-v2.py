# -*- coding: utf-8 -*-

import ConfigParser
from selenium import webdriver
import time
import requests
import urllib
import os
import platform
import copy
import sys
import threading

# load config file
cf = ConfigParser.ConfigParser()
cf.read("config")
account = cf.get("ITSC", "account")
pwd = cf.get("ITSC", "password")
url = cf.get("lecture", "url")
save_dir = cf.get("local", "save_dir") + '/'
threads = cf.getint("local", "threads")
browser = cf.get("local", "browser")

system = platform.system()

print browser


def GetRVC():
    '''log in the rvc.ust.hk and get the PlaylistUrl url'''
    print 'Opening the browser......'

    # config the browser
    if "Firefox" in browser:
        sel = webdriver.Firefox()
    elif "PhantomJS" in browser:
        sel = webdriver.PhantomJS()
    else:
        print 'I donnot know the browser!'
    # open the login in page
    sel.get(url)
    time.sleep(5)

    # sign in the username
    try:
        # sel.find_element_by_name("UsernameField").send_keys(account)
        sel.find_element_by_id("username").send_keys(account)
        print 'user success!'
    except:
        print 'user error!'
    time.sleep(1)
    # sign in the pasword
    try:
        # sel.find_element_by_name("PasswordField").send_keys(pwd)
        sel.find_element_by_id("password").send_keys(pwd)
        print 'pw success!'
    except:
        print 'pw error!'
    time.sleep(1)
    # click to login
    try:
        # sel.find_element_by_name("EnterButton").click()
        sel.find_element_by_name("submit").click()
        print 'click success!'
    except:
        print 'click error!'
    time.sleep(3)

    # get the play list url
    source = sel.page_source.encode('ascii', 'ignore')
    try:
        rtsp_idx = source.index('rvcprotected')
        sour = source[rtsp_idx:]
        idx = sour.index('http')
        i = idx
        while sour[i] is not "'":
            i += 1
        PlaylistUrl_0 = sour[idx:i]
        try:
            amp_idx = PlaylistUrl_0.index('amp')
            PlaylistUrl = PlaylistUrl_0[:amp_idx] + PlaylistUrl_0[amp_idx+4:]
        except:
            PlaylistUrl = PlaylistUrl_0
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
    # for i in xrange(5):  # just for test
    for i in xrange(len(Videolist)):
        idx = GetCurrentFileIdx(Videolist[i])
        try:
            r = urllib.urlopen(Videolist[i])
            if idx==-1:
                print Videolist[i]," failed"
                continue
            filename = save_dir + str(idx) + '.ts'
            if os.path.isfile(filename):
                filesize = os.path.getsize(filename)
                if filesize==int(r.headers.dict["content-length"]):
                    print idx,", it has been downloaded"
                    continue
            print '%d' % (idx),
            content = r.read()
            VideoName.append(str(i) + '.ts')
            with open(filename, 'wb') as f:
                f.write(content)
        except Exception as e:
            print idx,",failed"
            print e.message


def MergeTS(VideoName, dir):
    num = len(VideoName)
    os.chdir(dir)
    print 'Merging videos ......'
    if system is 'Windows':
        for i in xrange(1, num):
            cmd = 'copy /b %s+%s %s' % (VideoName[0], VideoName[i], VideoName[0])
            os.system(cmd)
            os.remove(VideoName[i])
    else:
        for i in xrange(1, num):
            try:
                cmd = 'cat %s >> %s' % (VideoName[i], VideoName[0])
                os.system(cmd)
                os.remove(VideoName[i])
            except:
                if i == 1:
                    print 'Sorry, it seems that I donnot know how to merge .ts file in your system.'
                    break
    os.chdir('../')

def Merge_TS_ONE(src,dst):
    if system is 'Windows':
        try:
            cmd = 'copy /b %s+%s %s' % (dst, src, dst)
            os.system(cmd)
            os.remove(src)
            return True
        except Exception as e:
            print e
            return False
    else:
        try:
            cmd = 'cat %s >> %s' % (src, dst)
            os.system(cmd)
            os.remove(src)
            return True
        except:
            return False

def Merge_TS_Quick(VideoName, dir):
    os.chdir(dir)
    templist = copy.copy(VideoName)
    print 'Merging videos ......'
    while len(templist)>1:
        listlen = len(templist)
        i = 0
        middlelist = []
        while i<listlen:
            if i+1>=listlen:
                middlelist.append(VideoName[i])
                break
            if not Merge_TS_ONE(templist[i+1],templist[i]):
                print "merge error , os error"
                return False
            middlelist.append(VideoName[i])
            i += 2
        templist = middlelist
    os.chdir('../')
    return True

def GetCurrentFileIdx(VideoUrl):
    idx=-1
    try:
        ts = VideoUrl.split('.')[-2]
    except:
        pass
    try:
        idx = int(ts.split('_')[-1])
    except:
        pass
    return(idx)
def getsortedlist():
    # sort the VideoName according to the number not the ascii code
    VideoName = os.listdir(save_dir)
    for i in xrange(len(VideoName)):
        VideoName[i] = int(VideoName[i].split('.')[0])
    VideoName = sorted(VideoName)
    for i in xrange(len(VideoName)):
        VideoName[i] = str(VideoName[i]) + '.ts'
    return VideoName
if __name__ == '__main__':
    if len(sys.argv)==1:
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
        # establish threads
        thr = []
        for i in xrange(threads):
            t = threading.Thread(target=GetVideo, args=(thrVideolist[i],))
            thr.append(t)
            t.start()

        # wait every threads to complete tasks
        for i in xrange(threads):
            thr[i].join()
        VideoName = getsortedlist()
        # merge the videos downloaded into one file
        while not Merge_TS_Quick(VideoName, save_dir):
            VideoName = getsortedlist()
            print u"merge failed,if occur many times,shut down it"
        try:
            os.remove("ghostdriver.log")
        except:
            pass
    else:
        VideoName = getsortedlist()
        # merge the videos downloaded into one file
        while not Merge_TS_Quick(VideoName, save_dir):
            VideoName = getsortedlist()
            print u"merge failed,if occur many times,shut down it"
        try:
            os.remove("ghostdriver.log")
        except:
            pass
