import sys
import pywintypes
import win32gui
 
import win32con

import time


'''
 '''

def _settotop():
    print("Select the window to bring to front ")

    loading = True  # a simple var to keep the loading status
    loading_speed = 4  # number of characters to print out per second
    loading_string = "." * 6  # characters to print out one by one (6 dots in this example)
    loading_seconds = 0 #4 seconds to load 

    # while loading:
    while loading_seconds < 4:
        loading_seconds += 1
        #  track both the current character and its index for easier backtracking later
        for index, char in enumerate(loading_string):
            # you can check your loading status here
            # if the loading is done set `loading` to false and break
            sys.stdout.write(char)  # write the next char to STDOUT
            sys.stdout.flush()  # flush the output
            time.sleep(1.0 / loading_speed)  # wait to match our speed
        index += 1  # lists are zero indexed, we need to increase by one for the accurate count
        sys.stdout.flush()  # flush the output
    #WE COULD make this so that as soon as we click, it sets it. instead of waiting 4 seconds
    activewindow=win32gui.GetForegroundWindow()
    print(f" \n set window to top (process id : {activewindow})\
        \
        ")
    win32gui.SetWindowPos(activewindow, win32con.HWND_TOPMOST, 900, 100, 800, 800, 0) #these last are position pixel x, y.. then size width ,height.. not sure what 0 is


def showDoc():
    print(
        """Help Documentation
this is a tool used for selecting a window and bringing it to the top of other applications.

For eg. if you want to set a window on top , click the window with your cursor and wait for the timer 


Tested on Windows 10/Python3
Feel free to contribute or report any issues at https://github.com/swordysrepo/settotop"""
        )

def main():
    """
    Argument Parsing and help documentation
    """
    if len(sys.argv) != 2:
        print("Incorrect number of arguments. Use -h for help")
    else:
        if sys.argv[1] in ["-h", "--h", "-help"]:
            showDoc()
        elif sys.argv[1] in ["select", "Select"]:
            _settotop()

if __name__ == '__main__':
    main()
