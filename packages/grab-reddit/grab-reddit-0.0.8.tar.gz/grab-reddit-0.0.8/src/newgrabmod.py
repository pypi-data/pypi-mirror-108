#!/usr/bin/env python3

import os
import praw
import prawcore
from datetime import date
import requests
import json
import re
from multiprocessing.pool import ThreadPool
from functools import partial

# import datetime
date = str(date.today())

# terminal colors
CRED = '\033[91m'
CYEL = '\033[33m'
CGRE = '\033[92m'
CEND = '\033[0m'

# read config options
def readconf():
    with open("grab-config.ini", "r") as conffile:
        jsonvars = conffile.read()
    progvars = json.loads(jsonvars)
    lim = progvars["limit"]
    path = progvars["path"]
    category = progvars["category"]
    sublist = progvars["sublist"]
    return lim, path, category, sublist

# write config options to json
def writeconf(lim, path, category, sublist):
    progvars = {"limit": lim,
                "path": path,
                "category": category,
                "sublist": sublist}
    # import json
    jsonvars = json.dumps(progvars)
    with open("grab-config.ini", "w") as conffile:
        conffile.write(jsonvars)

def download(lim, path, category, subvar):
    # import os
    pathdl = str(os.path.join(path, subvar, date))
    if not os.path.exists(pathdl):
        os.makedirs(pathdl)
    # go into download directory
    pathroot = str(os.path.join(path, subvar))
    os.chdir(pathroot)

    # create reddit instance
    # import praw
    reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                         client_secret=None,
                         user_agent="grab, a Reddit picture download bot by u/RealStickman_")

    # set subreddit
    subreddit = reddit.subreddit(subvar)

    # test existence of subreddit
    try:
        subreddit.title
    # import prawcore
    except prawcore.exceptions.Redirect:
        print(subreddit.display_name + " is no subreddit")
        return

    # TODO implement multiple ways of sorting here
    if category == "hot":
        submissions = subreddit.hot(limit=lim)
    elif category == "top":
        submissions = subreddit.top(limit=lim)
    elif category == "new":
        submissions = subreddit.new(limit=lim)
    else:
        print("Invalid category")


    # REVIEW
    # creates downloaded.txt in the subreddit's directory
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

    # go through the posts
    # NOTE distinguishes text-posts from image posts
    # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    for submission in submissions:
        # checks if the submission contains text. If it does, it should be skipped
        if not submission.selftext:
            # if the submission does not directly link to an image, it is discarded
            if "i." in submission.url:
                url = submission.url

                # check variables before passing them to regex
                # otherwise the program fails
                try:
                    author = submission.author.name
                except AttributeError:
                    author = "[deleted]"
                try:
                    title = submission.title
                except AttributeError:
                    title = "No title provided"

                # import re
                # NOTE removes illegal characters from filenames
                # Windows illegal characters https://gist.github.com/doctaphred/d01d05291546186941e1b7ddc02034d3
                filename = re.sub("<|>|:|\"|\/|\\|\||\?|\*", " ", author + " - " + title + ".png")
                # open the "downloaded" file and check if this submission exists already
                downloaded = open("downloaded.txt", "r")
                string = str(downloaded.read())
                downloaded.close()
                # do this if the post does not already exist in the downloaded file
                if url not in string:
                    print(CGRE + filename + CEND)
                    # import requests
                    # download the file
                    post = requests.get(url)
                    os.chdir(pathdl)
                    # write image to file
                    with open(filename, "wb") as file:
                        file.write(post.content)
                    # go back to subreddit folder
                    os.chdir(pathroot)
                    # add url to downloaded.txt
                    with open("downloaded.txt", "a") as downloaded:
                        downloaded.write(url)
                        downloaded.write(";")
                else:
                    print(CYEL + filename + " is already present in downloaded.txt" + CEND)

# NOTE look at multithreaded execution in the docs
# https://praw.readthedocs.io/en/latest/getting_started/multiple_instances.html#multiple-threads
# import multiprocessing.pool
def multiprocdownload(lim, path, category, sublist):
    # import functools
    downloadpart = partial(download, lim, path, category)
    # using 4 processes, to not stay far away from reddit rate limiting
    with ThreadPool(processes=4) as pool:
        # NOTE this has to be the last argument
        pool.map(downloadpart, sublist)

def main():
    lim, path, category, sublist = readconf()
    if len(sublist) == 0:
        print(CRED + "Please provide at least one subreddit" + CEND)
        exit(1)
    multiprocdownload(lim, path, category, sublist)
    exit(0)

if __name__ == "__main___":
    main()
