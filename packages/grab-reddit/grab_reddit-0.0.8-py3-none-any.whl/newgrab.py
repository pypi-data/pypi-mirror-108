#!/usr/bin/env python3

import newgrabmod
import argparse
import sys
import praw
import prawcore
import os
from pathlib import Path

# terminal colors
CRED = '\033[91m'
CYEL = '\033[33m'
CGRE = '\033[92m'
CEND = '\033[0m'

# testing config file
try:
    lim, path, category, sublist = newgrabmod.readconf()
except (FileNotFoundError, KeyError):
    print("Creating default config file")
    lim = 10
    # import os
    # import pathlib
    path = str(os.path.join(Path.home(), "Downloads", "grab-download"))
    category = "hot"
    sublist = []
    newgrabmod.writeconf(lim, path, category, sublist)

# read config file and get all variables
lim, path, category, sublist = newgrabmod.readconf()

# from here we can handle keyboard interrupts
try:
    # argparser
    # NOTE the arguments stuff was copied from the old program
    # import argparse
    parser = argparse.ArgumentParser(description='CLI-options for grab.py.', formatter_class=argparse.RawDescriptionHelpFormatter)
    arggroup = parser.add_argument_group(title='information options',
    description =
    '''-a, --add <subreddit>       Add subreddits (Multiple allowed)
    -r, --remove <subreddit>    Remove subreddits (Multiple allowed). Program will exit
    -l, --lim <limit>           Set the limit of posts
    -c, --category <category>   Set the category
    -p, --path <path>           Set the download path
    -s, --show                  Shows the configuration file. Program will exit''')

    parser.add_help

    # argument settings
    arggroup.add_argument("-a", "--add", dest="addsub", type=str, nargs='+', required=False, help=argparse.SUPPRESS)
    arggroup.add_argument("-l", "--lim", dest="limit", type=int, required=False, help=argparse.SUPPRESS)
    arggroup.add_argument("-c", "--category", dest="category", type=str, required=False, help=argparse.SUPPRESS)
    arggroup.add_argument("-p", "--path", dest="path", type=str, required=False, help=argparse.SUPPRESS)
    arggroup.add_argument("-s", "--show", action="store_true", dest="show", required=False, help=argparse.SUPPRESS)
    arggroup.add_argument("-r", "--remove", dest="removesub", type=str, nargs='+', required=False, help=argparse.SUPPRESS)

    # less to write every time
    args = parser.parse_args()

    # -s or --show
    if args.show:
        lim, path, category, sublist = newgrabmod.readconf()
        # create a comma separated string of subreddits
        substr = ", ".join(sublist)
        # print everything
        print("Subreddits: " + substr,
              "Limit: " + str(lim),
              "Path: " + path,
              "Category: " + category,
              sep="\n")
        # import sys
        sys.exit(0)

    # REVIEW
    # -r or --remove
    if args.removesub:
        for sub in args.removesub:
            # compare lowercase to prevent annoying issues with upper/lowercase
            for i, subvar in enumerate(sublist):
                if sub.lower() == subvar.lower():
                    print("Removed " + subvar)
                    del sublist[i]
        # save changes
        newgrabmod.writeconf(lim, path, category, sublist)
        sys.exit(0)

    # REVIEW
    # -a or --add
    if args.addsub:
        # compare lowercase to prevent doubles
        # e.g. re_zero while Re_Zero is already present
        sublist_lower = [item.lower() for item in sublist]
        addsub = [item.lower() for item in args.addsub]
        # diff the two lists
        subnew = [x for x in args.addsub if x not in sublist_lower]
        for sub in subnew:
            try:
                # import praw
                reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                                     client_secret=None,
                                     user_agent="grab, a Reddit picture download bot by u/RealStickman_")

                # this triggers the exception if it can't be found
                subtitle = reddit.subreddit(sub).title
                # to prevent inconsistencies between the reddit URL and this program, use the url name
                suburl = reddit.subreddit(sub).url
                # cut the "/r/" and trailing "/"
                subname = suburl[3:-1]

                # add to array
                sublist.append(subname)
                print(CGRE + "Added " + subname + CEND)
            # import prawcore
            except prawcore.exceptions.Redirect:
                print(CRED + sub + " does not exist" + CEND)
        """
        for sub in args.addsub:
            # this is needed, so you can start adding subs.
            if len(sublist) == 0:
                try:
                    # import praw
                    reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                                         client_secret=None,
                                         user_agent="grab, a Reddit picture download bot by u/RealStickman_")

                    # this triggers the exception if it can't be found
                    subtitle = reddit.subreddit(sub).title
                    # to prevent inconsistencies between the reddit URL and this program, use the url name
                    suburl = reddit.subreddit(sub).url
                    # cut the "/r/" and trailing "/"
                    subname = suburl[3:-1]

                    # add to array
                    sublist.append(subname)
                    print(CGRE + "Added " + subname + CEND)
                    sublist_lower = lowsublist(sublist)
                # import prawcore
                except prawcore.exceptions.Redirect:
                    print(CRED + sub + " does not exist" + CEND)
            else:
                for subvar in sublist_lower:
                    if sub in sublist_lower:
                        print(CYEL + subvar + " has already been added" + CEND)
                    else:
                        try:
                            # import praw
                            reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                                                 client_secret=None,
                                                 user_agent="grab, a Reddit picture download bot by u/RealStickman_")

                            # this triggers the exception if it can't be found
                            subtitle = reddit.subreddit(sub).title
                            # to prevent inconsistencies between the reddit URL and this program, use the url name
                            suburl = reddit.subreddit(sub).url
                            # cut the "/r/" and trailing "/"
                            subname = suburl[3:-1]

                            # add to array
                            sublist.append(subname)
                            print(CGRE + "Added " + subname + CEND)
                            sublist_lower = lowsublist(sublist)
                            break
                        # import prawcore
                        except prawcore.exceptions.Redirect:
                            print(CRED + sub + " does not exist" + CEND)
        """

    # -l or --lim
    if args.limit:
        lim = args.limit

    # -c or --category
    if args.category:
        category = args.category

    # -p or --path
    if args.path:
        path = args.path

    # write potential changes to the config file
    newgrabmod.writeconf(lim, path, category, sublist)

    def main():
        newgrabmod.main()

    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    newgrabmod.writeconf(lim, path, category, sublist)
    print("Exiting program")
    # return default linux SIGINT code
    exit(130)
