#!/bin/bash
while [ "true" ]
do
	VPNNAME=$(nmcli con status)
	if [[ $VPNNAME != *fr.myvpn.com.tcp* ]]; then
		echo "You ar disconnected from the VPN !"
		(sleep 2s && nmcli con up uuid 31445679-af7c-7485-829e-cfd48edf4f59  )
	else
		echo "You are connected to the VPN !"
	fi
	sleep 5
done
