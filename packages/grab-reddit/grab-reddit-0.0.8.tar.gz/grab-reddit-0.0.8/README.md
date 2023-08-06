# grab - a Reddit download bot

This is a simple Python script to download submissions containing images from any specified subreddit.  
All images are placed in the ~/Downloads/grab-bot/[subreddit]/[date] by default. The download path however can be changed through the GUI or config file.  
"grab.ini" is the configuration file used by the program. It will be generated with default values in case it is not present when the program is run. This file will be created in your home directory.  
"downloaded.txt" lists all previously downloaded images from their subreddit. This was done to avoid downloading images multiple times in an effort to save bandwidth and make subsequent executions of the program faster.  

*This program supports mainly Linux. Windows support is still in testing.*  

## Table of Contents

1. [TODO](#todo)
2. [How to use](#howto)
3. [Problems](#problems)
4. [Installation](#install)
    1. [Arch](#instarch)
    2. [Debian](#instdeb)
    3. [Fedora](#instfed)
    4. [Windows](#instwin)
5. [Known Bugs](#bugs)
6. [Cron](#cron)

## TODO <a name="todo"></a>

- [ ] GUI for selecting subreddits
- [ ] Change download location through GUI
- [X] Change the download limit
- [X] Change the category
- [ ] CLI option for launching the gui. Done through grab-reddit-gui.
- [ ] Make the GUI look better
- [X] Create CLI options for newgrab.py to create config files in the terminal 
- [ ] Automatically schedule program execution (Can be done manually with cron)


## How to use <a name="howto"></a>

Follow the [installation instructions](#install).  
~~To add subreddits open the gui, click on the "+" Button and type in the subreddit you want to add.  
To remove a subreddit, select one from the list and click on the "-" in the top right. Click yes in the following dialog.  
Clicking ">" will expand the window to change the category, limit and download path. Clicking "Run" in the GUI will execute grab.py.  
The theme can be changed by clicking on "light" or "dark". The dark theme is still work in progress.~~  

To run the program in the terminal use `grab-download <args>`. ~~If you want the gui version, run `grab-reddit-gui`.~~  
Help for arguments taken by `grab-download` can be found by executing `grab-download -h`.  

Setting up cron for repeated executions is [covered below](#cron).  

## Problems <a name="problems"></a>

This program relies on a stable internet connection when adding new subreddits, as each subreddit is checked for whether it can be reached. ~~If your connection is unstable or very slow this can lead to hanging in the GUI.~~  

## Installation <a name="install"></a>

To install all requirements follow the instructions for your distribution shown below.  

### Arch <a name="instarch"></a>

Open a terminal and execute the following commands.  
`sudo pacman -S python-pip`  
`sudo pip install grab-reddit`  

If you want to install the program to your local user, make sure to add your .local/bin directory to your PATH.  
`pip install --user grab-reddit`  

### Debian <a name="instdeb"></a>

Open a terminal and execute the following commands.  
`sudo apt-get install python3-pip python3-tk`  
`pip3 install grab-reddit`  

### Fedora <a name="instfed"></a>

Open a terminal and execute the following commands.  
`sudo dnf install python3 python3-wheel python3-tkinter`  
`pip install --user grab-reddit`  

### Windows <a name="instwin"></a>

*Program still undergoing testing*  

Install python from the [python homepate](https://www.python.org/).  
I suggest you to check "Add to my PATH".  

After a reboot open a terminal and execute the following command.  
`pip install grab-reddit`  

To use the CLI run `grab-reddit <args>`. For the gui version use `grab-reddit-gui`.  

## Known Bugs <a name="bugs"></a>


## Cron <a name="cron"></a>

~~This program comes with its own little execution scheduler included. It can be called with `grab-reddit-sched` in the terminal.~~

To execute this program it is best to specify the full path to the binary executable  
On Linux you should be able to find the path with `which grab-reddit`  

Example setup for hourly execution  
`0 * * * * /home/marc/.local/bin/grab-reddit`  
