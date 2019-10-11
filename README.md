# scrshot

A screenshot utility written in Python 3 using my `monopng` class.

## Consider something else

If you are looking for a Windows screenshot utility then consider
a well established program like Greenshot, LightShot or Snagit.

## So what is `scrshot.py` all about then?

I wanted something that did the following:

* Saved images in grayscale in PNG files
* Excluded the taskbar region at the bottom of the screen
* Allowed a remote system to trigger a screenshot

I am sure there is an existing screenshot program that does all this - I just could not
find one and the more I searched the more I just thought I would write it myself.

Some might call this "Not invented here syndrome" and frown but I will offer the feeble
defense of calling this "software diversity" instead.  Anyway, I like writing code :-)

## Pre-requisites

This is for Windows 10.

You will need:

* Python 3
* The 'pyautogui' module
* My 'monopng' class - [click here](https://github.com/andycranston/monopng)

## Running

Open a Windows command prompt and change to the directory that contains
the `scrshot.py` file.  Then type:

```
python scrshot.py
```

Every couple of seconds the following message will be printed:

```
Waiting for screenshot trigger action
```

If you get an error saying the `monopng.py` file cannot be found
make sure you have downloaded my `monopng.py`file and copied it to one of:

* The same directory the `scrshot.py` file is in
* A directory in one of the directories listed in the PYTHONPATH environment variable

## Taking a screenshot

Move the mouse pointer to the very top and roughly in the middle of the screen.  Then move the mouse pointer
down at least a few pixels.  This will trigger a screenshot.

## Where are the screenshots saved?

By default the program stores the screenshots in the following directory:

```
C:\andyc\00tmp
```

If you want them stored somewhere else then edit the `scrshot.py` file.

## Remote screenshots

NB: Remote screenshots only work if both the local and remote systems can communicate
with each over using IPv4 addresses using UDP port 8333.

Copy the `scrtrigger.py` Python 3 program to a remote system that has Python 3 installed.

On the remote system type:

```
python scrtrigger.py IP.AD.DR.ESS
```

where IP.AD.DR.ESS is the IPv4 address of the local system.

For example if the local system has a IP address of `192.168.8.53` then type:

```
python scrtrigger.py 192.168.8.53
```

This should trigger a screenshot on the local system.

## To Do

Add command line arguments to specify the following:

* A directory to save the screenshots in
* A flag to toggle if the task bar is included or excluded from screenshots
* The width in pixels of the task bar
* The position of the task bar (bottom, top, left or right)
* A flag to permit/forbid remote screenshot triggering

----------------------------

End of README.md
