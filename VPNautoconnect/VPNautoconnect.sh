#!/bin/bash
while [ "true" ]
do
	VPNCON=$(nmcli con status)
	if [[ $VPNCON != *fr-uk5.nordvpn.com.tcp* ]]; then
		echo "Disconnected, trying to reconnect..."
		(sleep 1s && nmcli con up uuid 31445679-af7c-7884-829e-cfd48edf4f59)
	else
		echo "Already connected !"
	fi
	sleep 30
done
