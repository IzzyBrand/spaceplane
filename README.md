# spaceplane
The aim of this project is to release a glider from a high altitude weather balloon and have the glider autonomously navigate back to a target landing spot where it can be recovered.

## SETUP
### RASPI-CONFIG
- enable ssh
- disable serial
- expand os
- disable gui
- set hostname to droneberry
- set password to *********
- reboot

### DEPENDENCIES
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim python-pip python-dev libxml2-dev libxslt-dev tmux
sudo pip install requests monotonic future mavproxy dronekit pyserial pymavlink 
```

### DRONEKIT
Dronekit was edited according to ticket 585 to avoid receiving problematic messages from a GCS
```
sudo mv /usr/lib/python2.7/site-packages/dronekit/test/__init.py__ /usr/lib/python2.7/site-packages/dronekit/test/__init.py__.original
sudo cp ~/dro.ne/droneberry/dronekit_util/__init.py /usr/lib/python2.7/site-packages/dronekit/test/__init.py__
```
