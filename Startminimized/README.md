# Sartminimized.py
A Python 3 program that allows you to start a program minimized. For exemple Thunderbird.
To execute it tap :
`python3 "/PATH/TO/THE/PROGRAM/Startminimized.py" thunderbird`
## How to install :
1. Download Startminimized.py in your Home directory. For exemple : /home/***your user name***/Startminimized/ (*Replace ***"your user name"*** by your username folder)
2. Download dependencies :
`sudo apt-get update && sudo apt-get install wmctrl && sudo apt-get install xdotool && sudo apt-get update`
3. Then open your Terminal in the folder where "Startminimized.py" is located and make it executable by typing :

`chmod +x /path/to/my/program/Startminimized.py`

For exemple in our case :

`chmod +x /home/[your user name]/Startminimized/Startminimized.py` #(* Replace ***[your user name]*** by your username folder)

4. Now execute it at startup (for exemple Thunderbird) :

    - Enter this ***command*** in your favorite startup tool : like "gnome-tweak-tool" for Gnome or other startup applications for other desktop environment : https://winaero.com/blog/manage-startup-apps-linux-mint/
       For exemple for starting Thunderbird at startup :
       
       `python3 "/home/[your username folder]/Startminimized/Startminimized.py" thunderbird` #(* Replace ***"[your user name folder]"*** by your username's folder)

    - Or you can edit "crontab" (doesn't work for me):

        Tape in your Terminal :

        `sudo crontab -e`

        Then copy this line at the end of the document :

        `@reboot python3 "/path/to/my/program/Startminimized.py" thunderbird`

        or in our exemple :

        `@reboot python3 "/home/[your username folder]/Startminimized/Startminimized.py" thunderbird` #(*Replace ***[your user name]*** by your username folder)

        Tape CTRL + X then y and Enter to save the document

Reboot an enjoy ! :-)
