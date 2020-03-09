# Sartminimized.py for Linux : Start any program minimized

[![GitHub license](https://img.shields.io/github/license/pzim-devdata/Tools-for-Debian?style=plastic)](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/LICENSE)    ![](https://img.shields.io/badge/Works%20with-Python%203-red?style=plastic)    [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=plastic)](https://www.python.org/)   [![GitHub issues](https://img.shields.io/github/issues/pzim-devdata/Tools-for-Debian?style=plastic)](https://github.com/pzim-devdata/Tools-for-Debian/issues)    ![GitHub repo size](https://img.shields.io/github/repo-size/pzim-devdata/Tools-for-Debian?style=plastic)    ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/Tools-for-Debian/total?style=plastic)    ![GitHub release (latest by date)](https://img.shields.io/github/v/release/pzim-devdata/Tools-for-Debian?style=plastic)    [![GitHub commits](https://img.shields.io/github/commits-since/pzim-devdata/Tools-for-Debian/v1.0.0.svg?style=plastic)](https://GitHub.com/pzim-devata/Tools-for-Debian/commit/)

[Download :inbox_tray:](https://github.com/pzim-devdata/Tools-for-Linux/releases/download/v1.0.0/Startminimized.zip)

## Description :

A Python 3 program that allows you to start a program minimized. For exemple Thunderbird.

![Presentation__gif](Gifstartminimized.gif)

To execute it tap :

```bash
python3 "/PATH/TO/THE/PROGRAM/Startminimized.py" thunderbird
```
## How to install :

1. Download Startminimized.py in your `~Home` directory in a folder called `Startminimized` : 

```bash
cd ~
wget https://raw.githubusercontent.com/pzim-devdata/Tools-for-Debian/master/Startminimized/Startminimized.py -P Startminimized

```

2. Download dependencies :

```bash
sudo apt-get update && sudo apt-get install wmctrl && sudo apt-get install xdotool && sudo apt-get update
```

3. Then open your Terminal in the folder where "Startminimized.py" is located and make it executable by typing :

```bash
chmod +x /path/to/my/program/Startminimized.py
```

For example in our case :

```sh
cd ~
chmod +x Startminimized/Startminimized.py
``` 

4. Now execute it at startup (In this exemple with Thunderbird) :

    - Enter this ***command*** in your favorite startup tool (like "gnome-tweak-tool" for Gnome or other startup applications for other desktop environment : https://winaero.com/blog/manage-startup-apps-linux-mint/ :
       
       For exemple for starting ***Thunderbird*** at startup :
       
        ```
        python3 "/PATH/TO/THE/PROGRAM/Startminimized.py" thunderbird
        ``` 
       
       or in our case :
       
       ```
       python3 "Startminimized/Startminimized.py" thunderbird
       ``` 

    - Or you can edit "crontab" (doesn't work for me):

        Tape in your Terminal :

        ```
        sudo crontab -e
        ```

        Then copy this line at the end of the document :

        ```
        @reboot python3 "/path/to/my/program/Startminimized.py" thunderbird
        ```

        or in our example :

        ```
        @reboot python3 "Startminimized/Startminimized.py" thunderbird
        ```

        Tape CTRL + X then y and Enter to save the document


Reboot an enjoy ! :blush:
