#!/bin/bash
sudo echo "!!!Please run as root!!!"
chmod +x ./cli.py
cp ./cli.py /bin/serpent
mkdir /usr/serpent/
cp ./runner.py /usr/serpent/runner.py
mkdir /var/serpent/
cp ./jobs.db /var/serpent/
chmod 777 /var/serpent/jobs.db
cp ./serpent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable serpent.service
sudo systemctl restart serpent.service