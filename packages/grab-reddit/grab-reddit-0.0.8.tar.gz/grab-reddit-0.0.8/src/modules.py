#!/usr/bin/env python3
"""
@author: RealStickman
"""
import configparser
import multiprocessing
import sys
import praw
import prawcore
import requests
import os
from datetime import date
import argparse
from pathlib import Path
from PIL import Image

# import variables
import progvars

# config initialisation
progvars.config = configparser.ConfigParser()

# read the config file
def readconf():
    print("Reading Config file")
    progvars.config.read('grab.ini')
    progvars.lim = int(progvars.config['CONFIG']['limit'])
    progvars.category = progvars.config['CONFIG']['category']
    progvars.subl = progvars.config['CONFIG']['subs']
    progvars.sublist = progvars.subl.replace('.empty.', '')
    progvars.sublf = list(filter(None, progvars.sublist.split(';')))
    progvars.path = progvars.config['CONFIG']['path']
    progvars.seltheme = progvars.config['CONFIG']['theme']

# Write the configuration file
def writeconf():
    print("Writing config file")
    progvars.config['CONFIG'] = {'limit': progvars.lim,
                        'category': progvars.category,
                        'subs': progvars.sublist,
                        'path': progvars.path,
                        'theme': progvars.seltheme}
    with open('grab.ini', 'w') as configfile:
        progvars.config.write(configfile)

# Download stuff from reddit
def dl(subvar):
    # make path choosable
    pathdl = str(os.path.join(progvars.path, subvar, progvars.date))
    if not os.path.exists(pathdl):
        os.makedirs(pathdl)
    pathtxt = str(os.path.join(progvars.path, subvar))
    os.chdir(pathtxt)

    reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                         client_secret=None,
                         user_agent="grab, a Reddit download bot by /u/RealStickman_")

    # setting subreddit and variable for the first few posts in the hot category of it
    subreddit = reddit.subreddit(subvar)

    if progvars.category == 'controversial':
        print(progvars.category)
        posts = subreddit.controversial(limit=progvars.lim)
    elif progvars.category == 'gilded':
        print(progvars.category)
        posts = subreddit.gilded(limit=progvars.lim)
    elif progvars.category == 'hot':
        print(progvars.category)
        posts = subreddit.hot(limit=progvars.lim)
    elif progvars.category == 'new':
        print(progvars.category)
        posts = subreddit.new(limit=progvars.lim)
    elif progvars.category == 'rising':
        print(progvars.category)
        posts = subreddit.rising(limit=progvars.lim)
    elif progvars.category == 'top':
        print(progvars.category)
        posts = subreddit.top(limit=progvars.lim)
    else:
        print('This category is not implemented or does not exist')

    #test whether the subreddit exists
    try:
        subreddit.title
    except prawcore.exceptions.Redirect:
        print(progvars.CRED + subreddit.display_name + " is no subreddit" + progvars.CEND)
        return

    #creates downloaded.txt in the subreddit's directory
    try:
        downloaded = open("downloaded.txt")
        print("File exists")
        print("Downloading from " + subreddit.display_name)
    except IOError:
        print("Creating file")
        downloaded = open("downloaded.txt", "w")
        downloaded.write("")
        print("Downloading from " + subreddit.display_name)
    finally:
        downloaded.close()

    #searches the specified number of posts
    for post in posts:
        url = post.url
        filename = post.author.name + " - " + post.title + ".png"
        filetest = post.title
        downloaded = open("downloaded.txt", "r")
        string = str(downloaded.read())
        downloaded.close()
        if filetest not in string:
            print(progvars.CGRE + filename + progvars.CEND)
            reddit = requests.get(url)
            #download files from reddit
            os.chdir(pathdl)
            try:
                with open(filename, "wb") as file:
                    file.write(reddit.content)
                try:
                    Image.open(filename)
                except:
                    os.remove(filename)
                    print("Removed " + filename + ", because it is not an image.")
            except IOError:
                print("Couldn't find any picture, skipping.")
            #appends the filenames
            os.chdir(pathtxt)
            with open("downloaded.txt", "a") as downloaded:
                downloaded.write(post.title)
                downloaded.write(" ")
        else:
            print(progvars.CYEL + filename + " is already present in downloaded.txt" + progvars.CEND)

def multiprocdl():
    # number of subreddits
    progvars.numsubs = len(progvars.sublf)
    #creates a pool of processes
    try:
        p = multiprocessing.Pool(progvars.numsubs)
        #processes are started with the arguments contained in the list
        p.map(dl, progvars.sublf)
    except ValueError:
        print(progvars.CRED + "Please specify a subreddit." + progvars.CEND)
    #exit(0)
