# scrshot

A screenshot utility written in Python 3 using the `pyautogui` module and my `monopng` class.

## Consider something else

If you are looking for a Windows screenshot utility then consider
a well established program like Greenshot, LightShot or Snagit.

## So what is `scrshot.py` all about then?

I wanted something that did the following:

* Saved grayscale images in PNG format to save space
* Excluded the taskbar region at the bottom of the screen
* Allowed a remote system to trigger a screenshot

I am sure there is an existing screenshot program that does all this - I just could not
find one and the more I searched the more I thought I would write it myself.

Some might call this "Not invented here syndrome" and frown but I call
this "software diversity" instead.  Anyway, I like writing and sharing code :-)

## Pre-requisites

This is for Windows 10.

You will need:

* Python 3
* The 'pyautogui' module - [click here](https://pyautogui.readthedocs.io/en/latest/introduction.html)
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

By default the program stores the screenshots in the subdirectory called:

```
Pictues
```

in the directory pointed to by the environment variable:

```
USERPROFILE
```

On my Windows 10 laptop this directory is:

```
C:\Users\Andy C\Pictures
```

Your set up will vary.

If you want them stored somewhere else then look at the `--dir` command line option.

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

If a UDP port number was specified using the `--port` command line
option on the local system then append a the ':' character and the port
number to the IP address.  Foe example if the UDP port number was 9444 and the remote
IP address was `192.168.8.53` then type:

```
python scrtrigger.py 192.168.8.53:9444
```



## Command line options

The following sections document the various command line options.

### --dir

The `--dir` command line option specifies a directory to store
the screenshot files in.  For example:

```
python scrshot.py --dir C:\Windows\Temp
```

will save the screenshot files to the `C:\Windows\Temp` directory.

Note that you must have access rights to create files in the specified directory.

### -fs

The `--fs` command line option will make the `scrshot.py` program take screenshots
of the entire screen ('fs' meaning Full Screen).

For example:

```
python scrshot.py --fs
```

will take full screen screenshots.

### --region

The `--region` command line option allows you to precisely specifiy exactly what part of the screen
to screenshot.  The argument value is a list of four integers separated by commas such as:

```
100,200,500,350
```

The first number specifies how many pixels across the region sparts.  The second number
specifies how many pixels down the region starts.  The third number specfies
the width of the screenshot area.  The fourth number specifies the height of the screenshot area.

So the following:

```
python scrshot.py --region 100,200,500,350
```

takes a screenshot starting 100 pixels across and 200 pixels down with a width of 500 pixels and height
of 350 pixels.

### --tbw

The `--tbw` command line option stands for `task bar width`.  It is the number of pixels wide that
the taskbar is.  The default value is 40 pixels wide but if your task bar is a different width like
72 pixels then use:

```
python scrshot.py --tbw 72
```

### --tbp

The `--tbp` command line option stands for `task bar position`.  The allowable values for the
task bar position are:

* top
* bottom
* left
* right

These can be abbrevisted to 't', 'b', 'l' and 'r' respectively.

The default value is 'bottom'.

So if your task bar is on the left hand side of the screen use:

```
python scrshot.py --tbp left
```

or:

```
python scrshot.py --tbp l
```

### --noremote

If you do not want screenshots to be triggered remotely by the `scrtrigger.py` program
then specify the `--noremote` command line option as follows:

```
python scrshot.py --noremote
```

This disables the remote screenshot functionality.

### --port

The `--port` command line option specifies a different UDP port number
to listen on for remorte screenshot trigger messages from remote hosts.
The UDP port number defaults to 8333 but if a different port number is required
such as 9444 then use:

```
python scrshot.py --port 9444
```

to listen on post number 9444 instead.

### All together now ...

The command line options can be mixed and matched as required.  For example:

```
python scrshot.py --dir C:\Windows\Temp --fs --noremote
```

will take full screen screenshots to directory `C:\Windows\Temp` and not allow remote
screenshot triggering.

As another example:

```
python scrshot.py --tbw 72 --tbp right --port 9444
```

Will take screenshots that exclude the taskbar on the right hand of the screen.  The task bar is
72 pixels wide and remote screenshots are allowed but the `scrtrigger.py` program must specify
port 9444.

Note: only one of the  `--region`, `--fs` and '--tbp` command line options should be specified.  The
program does not enforce this.  Instead the `--region` option overrides `--fs` and `--tbp`.  The `--fs` option
overrides `--tbp'.  However, do not rely on this behaviour as it may change.  Instead only ever used one of 
`--region`, `--fs` and '--tbp`.

## To Do

Things left to do ...

* Have a Solaris style "spinner" instead of the "Waiting for screenshot..." message scrolling up the command prompt window
* Investigate having the program "daemonize" into the background

---------------------------------------------------

End of README.md
