# Start_in_another_workspace
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

