# Sartminimized.py for Linux : Start any program minimized
A Python 3 program that allows you to start a program minimized. For exemple Thunderbird.
To execute it tap :
`python3 "/PATH/TO/THE/PROGRAM/Startminimized.py" thunderbird`
## How to install :

1. Download Startminimized.py in your `~Home` directory. For exemple : /home/***your user name***/Startminimized/ (*Replace ***"your user name"*** by your username folder)

2. Download dependencies :
`sudo apt-get update && sudo apt-get install wmctrl && sudo apt-get install xdotool && sudo apt-get update`

3. Then open your Terminal in the folder where "Startminimized.py" is located and make it executable by typing :

`chmod +x /path/to/my/program/Startminimized.py`

For example in our case :

`chmod +x ~home/Startminimized/Startminimized.py` 

4. Now execute it at startup (In this exemple with Thunderbird) :

    - Enter this ***command*** in your favorite startup tool (like "gnome-tweak-tool" for Gnome or other startup applications for other desktop environment : https://winaero.com/blog/manage-startup-apps-linux-mint/) :
       
       For exemple for starting ***Thunderbird*** at startup :
       
        `python3 "/PATH/TO/THE/PROGRAM/Startminimized.py" thunderbird` 
       
       or in our case :
       
       `python3 "~home/Startminimized/Startminimized.py" thunderbird` 

    - Or you can edit "crontab" (doesn't work for me):

        Tape in your Terminal :

        `sudo crontab -e`

        Then copy this line at the end of the document :

        `@reboot python3 "/path/to/my/program/Startminimized.py" thunderbird`

        or in our example :

        `@reboot python3 "~home/Startminimized/Startminimized.py" thunderbird`

        Tape CTRL + X then y and Enter to save the document

Reboot an enjoy ! :-)
