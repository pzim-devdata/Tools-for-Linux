# VPNautoconnect.sh for Linux : Automatically connect to the VPN at startup and reconnect if connection is lost.

A script to automatically connect to the VPN at startup (if you lauch this script at startup) and reconnect  every 5 seconds if connection is lost.


## How to install :



1. Download the file "VPNautoconnect.sh" in a folder called `VPN` in your `Home` directory :

`wget https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/VPNautoconnect.sh -P VPN`



2. You must first know your UUID for the VPN connection and the name of this connection:

    - Type in the Terminal **when you are connected to the VPN** :

`nmcli con`



3. Copy the VPN name and UUID:


![Image of the nmcli con command](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/Image1.png)



4. Paste the VPN name and UUID in the "VPNautoconnect.sh" file :

To open "VPNautoconnect.sh" tape in your terminal :

`sudo gedit ~home/VPN/VPNautoconnecte.sh` 

![Image of the UUID in the file VPNautoconnect.sh](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/Image2.png)



5. Then open your Terminal in the folder where "VPNautoconnect.sh" is located and type :

`chmod +x ~home/VPN/VPNautoconnect.sh` 



6. Connect to the VPN at startup :

If you want to connect to the VPN automatically at startup :

   - Enter the address of the script "VPNautoconnect.sh" (which is `~home/VPN/VPNautoconnect.sh`)  in your favorite startup tool : like "gnome-tweak-tool" for Gnome or other startup applications for other desktop environment : https://winaero.com/blog/manage-startup-apps-linux-mint/

   - Or you can edit "crontab" (doesn't work for me):

        - Tape in your Terminal :
        
            `sudo crontab -e`

        - Then copy this line at the end of the document :

            `@reboot /path/to/my/script/VPNautoconnect.sh`

            or in our example :

            `@reboot ~home/VPN/VPNautoconnect.sh` 


        - Tape CTRL + X then y and Enter to save the document

Reboot an enjoy ! :-)



   
