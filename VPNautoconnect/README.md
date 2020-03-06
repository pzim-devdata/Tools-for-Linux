# VPNautoconnect.sh

A script to automatically connect to the VPN at startup (if you lauch this script at startup) and reconnect if connection is lost.


## How to install :

1. Download the file "VPNautoconnecte.sh" in a folder in your Home directory. For exemple /home/***your user name***/VPN

2. You must first know your UUID for the VPN connection :

    - Type in the Terminal **when you are connected to the VPN** :

`nmcli con`

3. Copy the VPN UUID:

![Image of the nmcli con command](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/Image1.png)

4. Paste the UUID in the "VPNautoconnecte.sh" file :

![Image of the UUID in the file VPNautoconnect.sh](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/VPNautoconnect/Image2.png)

5. Then open your Terminal in the folder where "VPNautoconnecte.sh" is located and type :

`chmod + x /path/to/my/script/VPNautoconnecte.sh`

For exemple in our case :

`chmod + x /home/your user name/VPN/VPNautoconnecte.sh`

Now when you disconnect from the VPN it will automatically reconnect ;-)

6. Connect to the VPN at startup :

If you want to connect to the VPN automatically at startup, enter the address of this script on your favorite startup tool.

Or you can edit "crontab" :

    - Tape in your Terminal :
   
`crontab -e`

    - Then copy this line at the end of the document :

`@reboot /path/to/my/script/VPNautoconnecte.sh`

or in our exemple :

`@reboot /home/your user name/VPN/VPNautoconnecte.sh`


    - Tape CTRL + X then y and Enter to save the document
   
