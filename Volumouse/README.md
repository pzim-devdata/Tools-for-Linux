# Volumouse.py

A Python 3 program that allows you to change the volume with the mouse wheel by using it in the four corners of the screen

## How to install :

1. First you must know the Terminal command which allows you to modify the volume:
    - Open your Terminal and type:
     
        - `amixer set Master 5%+` If this command increases the volume, download the files ***"Volumouse_amixer_right.py"*** and ***"Volumouse_amixer_left.py"***
        - if `amixer set Master 5%+` is nor working try `amixer -q sset Master 5%+` If this command increases the volume, download the files ***"Volumouse_amixer_sset_right.py"*** and ***"Volumouse_amixer_sset_left.py"***
        - `pactl set-sink-volume 0 + 5%` If this command increases the volume, download the files ***"Volumouse_pactl_0_right.py"*** and ***"Volumouse_pactl_0_left.py"***
        - `pactl set-sink-volume 1 + 5%` If this command increases the volume, download the files ***"Volumouse_pactl_1_right.py"*** and ***"Volumouse_pactl_1_left.py"***
        - `pactl set-sink-volume 2 + 5%` If this command increases the volume, download the files ***"Volumouse_pactl_2_right.py"*** and ***"Volumouse_pactl_2_left.py"***

2. Download the correct 2 files in your "Home" directory. For exemple : /home/***your user name***/Volumouse/ (*Replace "your user name" by your username folder)

3. Install python-xlib package:
 Run in your Terminal :
 `sudo apt-get install python3-xlib` or if it's not working `sudo apt-get install python-xlib`

3. If you want to start Volumouse automatically at startup :

   - Enter the ***command*** of the Python files in your favorite startup tool :
       - `python3 "/home/***your user name***/Volumouse/***Your file Volumouse_left.py***" ` (*Replace "***your user name***" by your username folder and "***Your file Volumouse_left.py***" by the name of the Python file for the LEFT side)
       - `python3 "/home/***your user name***/Volumouse/***Your file Volumouse_right.py***" ` (*Replace "***your user name***" by your username folder and "***Your file Volumouse_right.py***" by the name of the Python file for the RIGHT side)

   - Or you can edit "crontab" :

        - Tape in your Terminal :
        
            `crontab -e`

        - Then copy this two lines at the end of the document :

            - `@reboot python3 "/home/***your user name***/Volumouse/***Your file Volumouse_left.py***" ` (*Replace "***your user name***" by your username folder and "***Your file Volumouse_left.py***" by the name of the Python file for the LEFT side) 
            - `@reboot python3 "/home/***your user name***/Volumouse/***Your file Volumouse_right.py***" ` (*Replace "***your user name***" by your username folder and "***Your file Volumouse_left.py***" by the name of the Python file for the RIGHT side) 

           

        - Tape CTRL + X then y and Enter to save the document

Reboot an enjoy ! :-)
