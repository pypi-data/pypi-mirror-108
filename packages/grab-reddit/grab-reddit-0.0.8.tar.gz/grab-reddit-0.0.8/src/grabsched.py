#!/usr/bin/env python3
"""
@author: RealStickman
"""
import time

# import modules
import modules

import progvars

# FIXME Does not appear to work on windows
def main():
    # This line translates the minutes entered in schedtime into seconds
    schedtimes = progvars.schedtime * 60
    
    starttime = time.time()
    while True:
        # The appropriate functions are called
        modules.readconf()
        modules.multiprocdl()
        # Sleep for the right amount of time
        time.sleep(schedtimes - ((time.time() - starttime) % schedtimes))
