#!/usr/bin/env python3
import subprocess
import sys
import time
#sudo apt-get update && sudo apt-get install wmctrl && sudo apt-get install xdotool && sudo apt-get update
#Trust in Pzim ! :-)

command = sys.argv[1]
command_check = command.split("/")[-1]

subprocess.Popen(["/bin/bash", "-c", command])

t = 1
while t < 30:
    try:
        w_list = [l.split() for l in subprocess.check_output(["wmctrl", "-lp"]).decode("utf-8").splitlines()]
        proc = subprocess.check_output(["pgrep", "-f", command_check]).decode("utf-8").strip().split()
        match = sum([[l[0] for l in w_list if p in l] for p in proc], [])
        subprocess.Popen(["xdotool", "windowminimize", match[0]])
        break
    except (IndexError, subprocess.CalledProcessError):
        pass
    t += 1
    time.sleep(1)


