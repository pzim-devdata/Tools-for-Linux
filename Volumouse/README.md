# Volumouse.py for Linux : Change the volume with the mouse wheel !

[![Licence](https://camo.githubusercontent.com/2b5c48821f22738887c98a07f95852b610fb555b/68747470733a2f2f696d672e736869656c64732e696f2f61706d2f6c2f61746f6d69632d64657369676e2d75692e7376673f)](https://raw.githubusercontent.com/pzim-devdata/Tools-for-Debian/master/LICENSE)    [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)    [![GitHub issues](/bitbucket/issues-raw/pzim-devdata/Tools-for-Debian)](https://github.com/pzim-devdata/Tools-for-Debian/issues)

A Python 3 program that allows you to change the volume with the mouse wheel using it at the four corners of the screen.
There are two files: one for the LEFT side and one for the RIGHT side of the screen. Like that, if you have two sound systems like an HiFi and an HDMI screen, you can change the volume for both.
The screen size by default is 1920 * 1080 but you can change it by opening Python files with a notepad. You can also change the size of the detection box in the corners of the screen.



![GifVolumouse.gif](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/Volumouse/GifVolumouse.gif)


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
