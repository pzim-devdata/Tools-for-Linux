# VPNautoconnect.sh

A script to automatically connect to the VPN at startup (if you lauch this script at startup) and reconnect  every 5 seconds if connection is lost.


## How to install :



1. Download the file "VPNautoconnect.sh" in a folder in your Home directory. For exemple /home/***your user name***/VPN (*Replace "your user name" by your username folder
)



2. You must first know your UUID for the VPN connection and the name of this connection:

    - Type in the Terminal **when you are connected to the VPN** :

`nmcli con`



3. Copy the VPN name and UUID:


![Image of the nmcli con command](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/Image1.png)



4. Paste the VPN name and UUID in the "VPNautoconnect.sh" file :

To open "VPNautoconnect.sh" tape in your terminal :

`sudo gedit /path/to/my/script/VPNautoconnecte.sh`

or in our case :

`sudo gedit /home/your user name/VPN/VPNautoconnecte.sh` (*Replace "your user name" by your username's folder)

![Image of the UUID in the file VPNautoconnect.sh](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/Image2.png)



5. Then open your Terminal in the folder where "VPNautoconnect.sh" is located and type :

`chmod +x /path/to/my/script/VPNautoconnect.sh`

For exemple in our case :

`chmod +x /home/your user name/VPN/VPNautoconnect.sh` (*Replace "your user name" by your username's folder)



6. Connect to the VPN at startup :

If you want to connect to the VPN automatically at startup :

   - Enter the address of the script "VPNautoconnect.sh" in your favorite startup tool

   - Or you can edit "crontab" :

        - Tape in your Terminal :
        
            `crontab -e`

        - Then copy this line at the end of the document :

            `@reboot /path/to/my/script/VPNautoconnect.sh`

            or in our exemple :

            `@reboot /home/your user name/VPN/VPNautoconnect.sh` (*Replace "your user name" by your username's folder)


        - Tape CTRL + X then y and Enter to save the document

Reboot an enjoy ! :-)



   
