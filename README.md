## Update 2017/2/9

All of the softwares are up-to-date. (It indecates that you can use pip to install the selenium instead of downloading the package.)

In `downloader.py`:

- Python: **Python 3.6.0** (default, Jan 16 2017, 12:12:55) [GCC 6.3.1 20170109] on linux

- Selenium: 3.0.2

- Phantomjs: 2.1.1-4

For the Windows user, you can still use the `downloader-v2.py`.

## About this project

This project aim to download the lecture videos @rvc.ust.hk.

Of course, you have to provide 

- your ITSC account name

- password

- the lecture URL

- the browser can be ``PhantomJS``(recommended) or ``Firefox``

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

- configparser

- requests

- urllib

## Test OS

Windows 10 64-bit & Linux x86_64

Python ~~2.7.12~~ 3.6.0

selenium ~~2.52.0~~ 3.0.2

PhantomJS 2.1.1-4

## Common Questions

In windows system, Selenium 3.x use the geckodriver, so if you are using the version 3, there will be an error:`WebDriverException:Message:'geckodriver'executable needs to be in Path`, and [here](http://blog.163.com/tracy_ly_8/blog/static/263060033201691931046880/) is the solution.

Firefox 46.0.1 & [PhantomJS](http://phantomjs.org/)

Because there still exist [bugs](https://github.com/SeleniumHQ/selenium/issues/2645) for Firefox 47 and above version, please use [Firefox 46.0.1](https://ftp.mozilla.org/pub/firefox/releases/46.0.1/) and colse the auto update in the `about:config` to avoid the bug.
