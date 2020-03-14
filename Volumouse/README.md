# Volumouse.py for Linux : Change the volume with the mouse wheel !

[![GitHub license](https://img.shields.io/github/license/pzim-devdata/Tools-for-Debian?style=plastic)](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/LICENSE)    ![](https://img.shields.io/badge/Works%20with-Python%203-red?style=plastic)    [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=plastic)](https://www.python.org/)   [![GitHub issues](https://img.shields.io/github/issues/pzim-devdata/Tools-for-Debian?style=plastic)](https://github.com/pzim-devdata/Tools-for-Debian/issues)    ![GitHub repo size](https://img.shields.io/github/repo-size/pzim-devdata/Tools-for-Debian?style=plastic)    ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/Tools-for-Debian/total?style=plastic)    ![GitHub release (latest by date)](https://img.shields.io/github/v/release/pzim-devdata/Tools-for-Debian?style=plastic)    [![GitHub commits](https://img.shields.io/github/commits-since/pzim-devdata/Tools-for-Debian/v1.0.0.svg?style=plastic)](https://GitHub.com/pzim-devata/Tools-for-Debian/commit/)

[Download :inbox_tray:](https://github.com/pzim-devdata/Tools-for-Linux/releases/download/v1.0.0/Volumouse.zip)


## Description :

A Python 3 program that allows you to change the volume with the mouse wheel using it at the four corners of the screen.

There are two files: one for the LEFT side and one for the RIGHT side of the screen. Like that, if you have two sound systems like an HiFi and an HDMI screen, you can change the volume for both.

The screen size by default is 1920 * 1080 but you can change it by opening Python files with a notepad. You can also change the size of the detection box in the corners of the screen.



![GifVolumouse.gif](GifVolumouse.gif)


## How to install :

1. First you must know the Terminal command which allows you to modify the volume:
    - Open your Terminal and type:
     
        - `amixer set Master 5%+` If this command increases the volume, download the files ***"Volumouse_amixer_right.py"*** and ***"Volumouse_amixer_left.py"***
        - if `amixer set Master 5%+` is not working try `amixer -q sset Master 5%+` If this command increases the volume, download the files ***"Volumouse_amixer_sset_right.py"*** and ***"Volumouse_amixer_sset_left.py"***
        - `pactl set-sink-volume 0 + 5%` If this command increases the volume, download the files ***"Volumouse_pactl_0_right.py"*** and ***"Volumouse_pactl_0_left.py"***
        - `pactl set-sink-volume 1 + 5%` If this command increases the volume, download the files ***"Volumouse_pactl_1_right.py"*** and ***"Volumouse_pactl_1_left.py"***
        - `pactl set-sink-volume 2 + 5%` If this command increases the volume, download the files ***"Volumouse_pactl_2_right.py"*** and ***"Volumouse_pactl_2_left.py"***

2. Download the correct 2 files in your "Home" directory. For example : /home/***your user name***/Volumouse/ (*Replace "your user name" by your username folder)

3. Install python-xlib package:
 Run in your Terminal :
 `sudo apt-get install python3-xlib` or if it's not working `sudo apt-get install python-xlib`

3. If you want to start Volumouse automatically at startup :

   - Enter this ***two Python commands*** in your favorite startup tool : like "gnome-tweak-tool" for Gnome or other startup applications for other desktop environment : https://winaero.com/blog/manage-startup-apps-linux-mint/ 
       - `python3 "Volumouse/#Your file Volumouse_left.py#"`
       - `python3 "Volumouse/#Your file Volumouse_right.py#"` 
       (*Replace "***#Your file Volumouse_left.py#***" by the name of the Python file for the LEFT side and "***#Your file Volumouse_right.py#***" by the name of the Python file for the RIGHT side)

   - Or you can edit "crontab" (not working with me):

        - Tape in your Terminal :
        
            `crontab -e`

        - Then copy this line at the end of the document :

            - `@reboot python3 "Volumouse/#Your file Volumouse_left.py#" & python3 "Volumouse/#Your file Volumouse_right.py#"` (*Replace "***#Your file Volumouse_left.py#***" by the name of the Python file for the LEFT side) and and "***#Your file Volumouse_right.py#***" by the name of the Python file for the RIGHT side)
            
           

        - Tape CTRL + X then y and Enter to save the document


Reboot an enjoy ! :blush:


--------------------------------------------

## - [Licence](https://github.com/pzim-devdata/DATA-developer/raw/master/LICENSE)
MIT License
Copyright (c) 2019 pzim-devdata

--------------------------------------------

## - [Contact :email:](mailto:contact@pzim.fr?subject=Contact%20from%20Github)
Created by [@pzim](https://www.pzim.fr/) - feel free to contact me!




