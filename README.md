## About this project

This project aim to download the lecture videos @rvc.ust.hk.

Of course, you have to provide 

- your ITSC account name

- password 

- the lecture URL

in the config file.

You can see more details [here](http://firiceguo.xyz/web/python/2016/09/29/downloader-rvc/)(Chinese).

## You are welcome to ...

- give me pull requests and become a countributor of this project

- raising issues to me.

## What you could do

There are some options you can configure.

- account: You have to input your ITSC account name here.

- password: You have to input your ITSC account password here.

- url: You have to provide the video url.

- save_dir: The route you want to save the video.

- threads: The number of threads you want to use.

## Required libraries

- [selenium](https://github.com/SeleniumHQ/selenium)

- requests

## Test OS

Windows 10 64-bit & Linux Mint 18 x86_64

Python 2.7.12

selenium 2.52.0

Firefox 46.0.1 & [PhantomJS](http://phantomjs.org/)

Note: Because there still exist [bugs](https://github.com/SeleniumHQ/selenium/issues/2645) for Firefox 47 and above version, please use [Firefox 46.0.1](https://ftp.mozilla.org/pub/firefox/releases/46.0.1/) and colse the auto update in the `about:config` to avoid the bug.


