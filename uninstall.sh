#!/bin/bash
sudo echo "!!!Please run as root!!!"
sudo rm -r /bin/serpent
sudo rm -r /usr/serpent
sudo rm -r /var/serpent
systemctl stop serpent.service
systemctl disable serpent.service
rm /etc/systemd/system/serpent.service
systemctl daemon-reload
systemctl reset-failed