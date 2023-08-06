#!/usr/bin/env python3
"""
@author: RealStickman
"""
import configparser
import os
import subprocess
import tkinter as tk
import sys
from pathlib import Path
from tkinter import messagebox, filedialog, ttk
import praw
import prawcore
from multiprocessing import Process

# variables
import progvars
# modules
import modules

import grab

def addfr():
    #remove add/remove subreddit buttons
    butaddsub.destroy()
    butremsub.destroy()

    #Frame for adding subs
    global addsub
    addsub = ttk.Frame(normal)
    addsub.grid(row=1, column=0, sticky="W")

    #Label
    ttk.Label(addsub, text="Enter subreddit:").grid(row=0, column=0, sticky="W")

    #textbox
    global txtent
    txtent = ttk.Entry(addsub)
    txtent.grid(row=1, column=0, sticky="W")

    #abort
    ttk.Button(addsub, text="Cancel", command=cancel).grid(row=2, column=0, sticky="W")

    #try to add
    ttk.Button(addsub, text="Add", command=save).grid(row=2, column=0, sticky="E")

#kills the add subreddit window
def cancel():
    addsub.destroy()

    # add new subreddits
    global butaddsub
    butaddsub = ttk.Button(normal, text="+", command=addfr)
    butaddsub.grid(row=1, column=0, sticky="W", padx=2)

    # remove subreddits
    global butremsub
    butremsub = ttk.Button(normal, text="-", command=listbox)
    butremsub.grid(row=1, column=0, sticky="E")

#for saving subreddits
def save():
    #reddit stuff
    reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                         client_secret=None,
                         user_agent="grab, a Reddit download bot by /u/RealStickman_")

    #hope the user wrote something
    try:
        txte = txtent.get()
        #check if what the user wrote makes sense
        try:
            subreddit = reddit.subreddit(txte)
            subreddit.title

            #read the config
            modules.readconf()
            #add entered subreddit
            progvars.sublist += subreddit.display_name + ";"
            #that's were we're gonna put it
            modules.writeconf()
            print("Added " + subreddit.display_name)

            #reformatting list of subs
            progvars.sublf = progvars.sublist.split(";")
            labelsublist = [x for x in progvars.sublf if x]
            # displays list of subreddits
            lbox.delete(0, 'end')
            for i in range(len(labelsublist)):
                lbox.insert('end', labelsublist[i])

            #destroy window
            addsub.destroy()
        #if the subreddit can't be found
        except prawcore.exceptions.Redirect:
            messagebox.showerror("Wrong Subreddit", subreddit.display_name + " does not exist")
        # add new subreddits
        global butaddsub
        butaddsub = ttk.Button(normal, text="+", command=addfr)
        butaddsub.grid(row=1, column=0, sticky="W", padx=2)

        # remove subreddits
        global butremsub
        butremsub = ttk.Button(normal, text="-", command=listbox)
        butremsub.grid(row=1, column=0, sticky="E")
    #if the user didn't type anything
    except TypeError:
        messagebox.showerror("No Subreddit", "Please fill in a subreddit")

#closes the window and stops the program
def stop():
    root.destroy()
    sys.exit()
    exit()

# showing info message and have it be interactable
def runprog():
    print("works runprog")
    messagebox.showinfo("Running", "Program is running")
    main.update_idletasks()

# process that executes the download
def rundl():
    print("works rundl")
    # to make sure the number of subs is correct
    modules.readconf()
    # download images from reddit
    modules.multiprocdl()

# runs the program
def run():
    # set up processes
    procprog = Process(target = runprog())
    procrundl = Process(target = rundl())

    # start processes
    procrundl.start()
    procprog.start()

    # make sure both processes are finished
    procprog.join()
    procrundl.join()

    messagebox.showinfo("Finished", "Program has finished")

def listbox():
    result = tk.messagebox.askyesno("Delete", "Remove selected subreddit from list?", icon='warning')
    if result == True:
        #read the config
        modules.readconf()
        selec = lbox.curselection()
        val = lbox.get(selec)
        global sublist
        progvars.sublist = progvars.sublist.replace(";" + val, '')
        modules.writeconf()
        print("Deleted " + val)
        updatlist()
    else:
        print("Nothing deleted")

def updatlist():
    #read the config
    modules.readconf()
    lcusubl = progvars.sublist.split(";")
    labsubl = [x for x in lcusubl if x]
    lbox.delete(0, 'end')
    for i in range(len(labsubl)):
        lbox.insert(0, labsubl[i])

def catsel():
    modules.readconf()
    #sets category based on the radiobutton selected
    if catvar.get() == 1:
        progvars.category = "controversial"
        modules.writeconf()
        print("Setting category to controversial")
    # elif catvar.get() == 2:
    #     progvars.category = "gilded"
    #     writeconf()
    #     print("Setting category to gilded")
    elif catvar.get() == 3:
        progvars.category = "hot"
        modules.writeconf()
        print("Setting category to hot")
    elif catvar.get() == 4:
        progvars.category = "new"
        modules.writeconf()
        print("Setting category to new")
    elif catvar.get() == 5:
        progvars.category = "rising"
        modules.writeconf()
        print("Setting category to rising")
    elif catvar.get() == 6:
        progvars.category = "top"
        modules.writeconf()
        print("Setting category to top")
    else:
        print("Something went wrong")

#save the limit
def savelim():
    modules.readconf()
    print("New limit: " + limspin.get())
    global lim
    progvars.lim = limspin.get()
    modules.writeconf()

#expands the window to show all settings
def winexp():
    global extend
    extend = ttk.Frame(main)
    extend.grid(row=0, column=2, sticky="W")
    modules.readconf()

    #destroy button to expand window
    butexp.destroy()

    #other settings
    setfr = ttk.Frame(extend)
    setfr.grid(row=0, column=1, sticky="W")

    #change theme
    ttk.Label(setfr, text="Change theme").grid(row=0, column=0, sticky="W")
    ttk.Button(setfr, text="light", command=setlight).grid(row=1, column=0, sticky="E")
    ttk.Button(setfr, text="dark", command=setdark).grid(row=1, column=1, sticky="W")

    #frame for various settings
    global varfr
    varfr = ttk.Frame(extend)
    varfr.grid(row=1, column=0, sticky="W")

    # Path
    global pathlab
    pathlab = ttk.Label(varfr, text="Path: " + progvars.path)
    pathlab.grid(row=0, column=1, sticky="W")
    global butpath
    butpath = ttk.Button(varfr, text="...", command=dirdialog)
    butpath.grid(row=0, column=2, sticky="W")

    # Limit
    global limspin
    limspin = tk.Spinbox(varfr, from_=0, to=100, width=5, bg=background, fg=foreground)
    limspin.grid(row=1, column=1, sticky="W")
    # show currently set limit
    i = 0
    while i < progvars.lim:
        limspin.invoke(element="buttonup")
        i += 1

    # limit save button
    global butsave
    butsave = ttk.Button(varfr, text="Save", command=savelim)
    butsave.grid(row=1, column=1, sticky="W", padx="55")

    #frame for categories
    global categ
    categ = ttk.Frame(extend)
    categ.grid(row=0, column=0, sticky="W")
    # Category label
    global labcateg
    labcateg = ttk.Label(categ, text="Category:")
    labcateg.grid(row=0, column=0, sticky="W")

    # category buttons for selection
    global catvar
    catvar = tk.IntVar()

    global catcont
    catcont = tk.Radiobutton(categ, text="controversial", variable=catvar, value=1, command=catsel, bg=background, fg=foreground, relief="ridge")
    catcont.grid(row=1, column=0, sticky="W")

    # global catgil
    # catgil = tk.Radiobutton(categ, text="gilded", variable=catvar, value=2, command=catsel, bg=background, fg=foreground, relief="ridge")
    # catgil.grid(row=1, column=1, sticky="W")

    global cathot
    cathot = tk.Radiobutton(categ, text="hot", variable=catvar, value=3, command=catsel, bg=background, fg=foreground, relief="ridge")
    cathot.grid(row=1, column=2, sticky="W")

    global catnew
    catnew = tk.Radiobutton(categ, text="new", variable=catvar, value=4, command=catsel, bg=background, fg=foreground, relief="ridge")
    catnew.grid(row=2, column=0, sticky="W")

    global catris
    catris = tk.Radiobutton(categ, text="rising", variable=catvar, value=5, command=catsel, bg=background, fg=foreground, relief="ridge")
    catris.grid(row=2, column=1, sticky="W")

    global cattop
    cattop = tk.Radiobutton(categ, text="top", variable=catvar, value=6, command=catsel, bg=background, fg=foreground, relief="ridge")
    #cattop.grid(row=2, column=2, sticky="W")
    cattop.grid(row=1, column=1, sticky="W")

    # selects appropriate button to show which one is active
    if progvars.category == 'controversial':
        print("Current selected category is " + progvars.category)
        catcont.select()
    # elif progvars.category == 'gilded':
    #     print("Current selected category is " + progvars.category)
    #     catgil.select()
    elif progvars.category == 'hot':
        print("Current selected category is " + progvars.category)
        cathot.select()
    elif progvars.category == 'new':
        print("Current selected category is " + progvars.category)
        catnew.select()
    elif progvars.category == 'rising':
        print("Current selected category is " + progvars.category)
        catris.select()
    elif progvars.category == 'top':
        print("Current selected category is " + progvars.category)
        cattop.select()

    #close expanded view
    global butshr
    butshr = ttk.Button(main, text="<", command=winshr)
    butshr.grid(row=1, column=1, sticky="W")

#setlight and setdark could maybe be integrated into one function.
def setlight():
    modules.readconf()
    if progvars.seltheme != "light":
        progvars.seltheme = "light"
        print("Setting " + progvars.seltheme + " theme")
        changetheme()
    else:
        print("Program is already using the " + progvars.seltheme + " theme")

def setdark():
    modules.readconf()
    if progvars.seltheme != "dark":
        progvars.seltheme = "dark"
        print("Setting " + progvars.seltheme + " theme")
        changetheme()
    else:
        print("Program is already using the " + progvars.seltheme + " theme")

#code pulled out of setlight and setdark in order to avoid huge blocks of duplicate code
def changetheme():
    modules.writeconf()
    root.destroy()
    try:
        subprocess.Popen('grab-reddit-gui', shell=True, text=True)
    except:
        subprocess.Popen('python3 gui.py', shell=True, text=True)

#shrinks the window back to original size
def winshr():
    #destroy extended view frame & everything in it
    extend.destroy()
    #recreate button to expand window
    global butexp
    butexp = ttk.Button(main, text=">", command=winexp)
    butexp.grid(row=1, column=1, sticky="W")

def dirdialog():
    modules.readconf()
    #explicitly assign path variable, otherwise it complains about the variable being called before assignment
    progvars.path = tk.filedialog.askdirectory(parent=root, initialdir=progvars.path, title="Download directory")
    modules.writeconf()
    global pathlab
    pathlab.destroy()
    pathlab = ttk.Label(varfr, text="Path: " + progvars.path)
    pathlab.grid(row=0, column=1, sticky="W")

def main():
    ############
    #Initialise#
    ############

    global pathdef
    #choose default path
    pathdef = str(os.path.join(Path.home(), "Downloads", "grab-bot"))

    #make sure the config file is present and correct
    try:
        progvars.config.read('grab.ini')
        progvars.lim = progvars.config['CONFIG']['limit']
        progvars.category = progvars.config['CONFIG']['category']
        progvars.config['CONFIG']['subs']
        progvars.path = progvars.config['CONFIG']['path']
        progvars.seltheme = progvars.config['CONFIG']['theme']
        print("Config is present and correct")
    except KeyError:
        progvars.config['CONFIG'] = {'limit': '10',
                            'category': 'hot',
                            'subs': '.empty.;',
                            'path': pathdef,
                            'theme': 'light'}
        with open('grab.ini', 'w') as configfile:
            progvars.config.write(configfile)
        print("Created config or fixed missing options")

    #read config
    modules.readconf()

    global root
    #main window
    root = tk.Tk()
    root.title("grab - Reddit download bot")

    global theme
    #define theme
    theme = ttk.Style()

    global background
    global foreground
    print("Using " + progvars.seltheme + " theme")
    if progvars.seltheme == "light":
        root.configure(bg="#ffffff")
        #light theme
        theme.theme_create('light')
        theme.theme_settings('light', {
            "TFrame": {
                "configure": {
                    "background": ["#ffffff"],
                    "foreground": ["#1e1e1e"]
                }
            },
            "TLabel": {
                "configure": {
                    "background": ["#ffffff"],
                    "foreground": ["#1e1e1e"]
                }
            },
            "TButton": {
                "configure": {
                    "relief": ["ridge"],
                    "padding": [8, 1],
                    "background": ["#dedede"],
                    "foreground": ["#1e1e1e"]
                },
                "map": {
                    "relief": [("pressed", "sunken")],
                    "background": [("active", "#f0f0f0")]
                }
            },
            "TEntry": {

            }
        })
        #set background and foreground
        background = "#ffffff"
        foreground = "#1e1e1e"
        #use light theme
        theme.theme_use('light')

    elif progvars.seltheme == "dark":
        root.configure(bg="#000000")
        #dark theme
        theme.theme_create('dark')
        theme.theme_settings('dark', {
            "TFrame": {
                "configure": {
                    "background": ["#000000"],
                    "foreground": ["#e1e1e1"]
                }
            },
            "TLabel": {
                "configure": {
                    "background": ["#000000"],
                    "foreground": ["#e1e1e1"]
                }
            },
            "TButton": {
                "configure": {
                    "relief": ["ridge"],
                    "padding": [8, 1],
                    "background": ["#212121"],
                    "foreground": ["#e1e1e1"]
                },
                "map": {
                    "relief": [("pressed", "sunken")],
                    "background": [("active", "#0f0f0f")]
                }
            },
            "TEntry": {

            }
        })
        #set background and foreground
        #problems with visibility of selection from radiobuttons and spinbox up/down arrows
        #change color radiobuttons have when the mouse is hovering over them.
        background = "#000000"
        foreground = "#e1e1e1"
        #use dark theme
        theme.theme_use('dark')
    else:
        print("Sorry, this theme could not be found")

    global main
    #main frame
    main = ttk.Frame(root)
    main.grid(row=0, column=0, sticky="W", padx=5, pady=5)

    global normal
    #frame for listbox and main buttons
    normal = ttk.Frame(main)
    normal.grid(row=0, column=0, sticky="W")

    global var
    #subs label
    ttk.Label(normal, text="Active subreddits:", font="none 16").grid(row=0, column=0)
    var = tk.StringVar()

    global cnnsublist
    global labelsublist
    #change the list of subs to fit
    cnnsublist = progvars.sublist.replace(';', '\n')
    progvars.sublf = progvars.sublist.split(";")
    labelsublist = [x for x in progvars.sublf if x]

    global lbox
    #multiple doesn't work with my method
    #lbox = tk.Listbox(window, listvariable=var, selectmode="multiple", width=24)
    #create a listbox with the proper theme
    lbox = tk.Listbox(normal, listvariable=var, selectmode="single", width=26, bg=background, fg=foreground)

    #insert subreddits into listbox
    for y in range(len(labelsublist)):
        lbox.insert('end', labelsublist[y])
    lbox.grid(row=2, column=0, sticky="W")

    #add new subreddits
    global butaddsub
    butaddsub = ttk.Button(normal, text="+", command=addfr)
    butaddsub.grid(row=1, column=0, sticky="W")

    #remove subreddits
    global butremsub
    butremsub = ttk.Button(normal, text="-", command=listbox)
    butremsub.grid(row=1, column=0, sticky="E")

    #y += 1
    #close the program
    ttk.Button(main, text="Exit", command=stop).grid(row=1, column=0, sticky="W")

    #run the program
    ttk.Button(main, text="Run", command=run).grid(row=1, column=0, sticky="E")

    global butexp
    #expand
    butexp = ttk.Button(main, text=">", command=winexp)
    butexp.grid(row=1, column=1, sticky="W")

    root.mainloop()

if __name__ == '__main__':
    main()
