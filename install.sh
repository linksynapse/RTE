#!/bin/bash

sudo rm -rf /opt/tas
sudo rm -rf /var/log/tas
sudo rm -rf /var/cache/tas
sudo rm -rf /etc/supervisord/conf.d/*

sudo mkdir /var/cache/tas
sudo mkdir /var/log/tas
sudo mkdir /var/log/tas/rrc.d
sudo mkdir /var/log/tas/asyc.d
sudo mkdir /var/log/tas/hsyc.d

sudo mkdir /opt/tas

sudo mv asyc.d/ /opt/tas
sudo mv hsyc.d/ /opt/tas
sudo mv rrc.d/ /opt/tas
sudo mv scripts/ /opt/tas

sudo mv rrc.conf /etc/supervisor/conf.d/
sudo mv hsyc.conf /etc/supervisor/conf.d/
sudo mv asyc.conf /etc/supervisor/conf.d/

dbr=$(sudo python3 /opt/tas/scripts/crtdb.py -o /var/cache/tas/history.dat)
echo $dbr

cpuid=$(sudo python3 /opt/tas/scripts/gcpuid.py)
printf "you'r device cpuid is '%s'\n" ${cpuid}

sudo systemctl restart supervisor.service
