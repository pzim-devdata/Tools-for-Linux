# Start_in_another_workspace
[![GitHub license](https://img.shields.io/github/license/pzim-devdata/Tools-for-Debian?style=plastic)](https://github.com/pzim-devdata/Tools-for-Debian/blob/master/LICENSE)    [![GitHub issues](https://img.shields.io/github/issues/pzim-devdata/Tools-for-Debian?style=plastic)](https://github.com/pzim-devdata/Tools-for-Debian/issues)    ![GitHub repo size](https://img.shields.io/github/repo-size/pzim-devdata/Tools-for-Debian?style=plastic)    ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/Tools-for-Debian/total?style=plastic)    ![GitHub release (latest by date)](https://img.shields.io/github/v/release/pzim-devdata/Tools-for-Debian?style=plastic)    [![GitHub commits](https://img.shields.io/github/commits-since/pzim-devdata/Tools-for-Debian/v1.0.0.svg?style=plastic)](https://GitHub.com/pzim-devata/Tools-for-Debian/commit/)


[Download :inbox_tray:](https://github.com/pzim-devdata/Tools-for-Linux/releases/download/v1.0.0/Start_in_another_workspace.zip)

Here is a script for starting a program in another worhspace for Linux. Works with wmctrl.
1. Install wmctrl
```command
sudo apt install wmctrl
```

2. And create a script (in this example thunderbird on the second workspace (```-t 1```)):

```bash
#!/bin/sh

 (thunderbird &)  & sleep 5 && 
sh -c "wmctrl -i -r `wmctrl -l | grep Thunderbird` -t 1"
```

To know your application name on wmctrl you can view it by taping on your terminal :
```command
wmctrl -l
```
And replace it with the correct name in the script.

Be carrefull with the capital letter ("Thunderbird" not "thunderbird") !!

Other example with firefox on the 3d workspace (```-t 2```):

```bash
#!/bin/sh
(firefox &)  & sleep 5 && 
sh -c "wmctrl -i -r `wmctrl -l | grep Firefox` -t 2"
```
3. Bonus :
Here is the command to execute at start-up :
```bash
sh -c "thunderbird  & sleep 5 && wmctrl -i -r `wmctrl -l | grep Thunderbird` -t 1"
```

Works on Debain 10 with Cinnamon. But should works for all.



--------------------------------------------

## - [Licence](https://github.com/pzim-devdata/DATA-developer/raw/master/LICENSE)
MIT License
Copyright (c) 2019 pzim-devdata

--------------------------------------------

## - [Contact :email:](mailto:pizim@posteo.net?subject=Contact%20from%20Github)
Created by [@pzim](https://www.pzim.fr/) - feel free to contact me!





