#!/bin/bash
while [ "true" ]
do
	VPNNAME=$(nmcli con show --active)
	if [[ $VPNNAME != *fr.myvpn.com.tcp* ]]; then
		echo "You are disconnected from the VPN ! HELP !!!!!!!!!!!!!!!!!!!!"
		(sleep 2s && nmcli con up uuid 31445679-af7c-7485-829e-cfd48edf4f59         )
	else
		echo "You are connected to the VPN ! All seems good :-)"
	fi
	sleep 5
done
