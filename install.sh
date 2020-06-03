#!/usr/bin/bash
# For logs use
# journalctl --unit obd_monitor
sudo cp obd_monitor.service /etc/systemd/system/
sudo chown root:root /etc/systemd/system/obd_monitor.service
sudo chmod 644 /etc/systemd/system/obd_monitor.service

sudo mkdir /usr/local/lib/stereo-pi-obd
sudo cp *.py /usr/local/lib/stereo-pi-obd/
sudo chown root:root /usr/local/lib/stereo-pi-obd/*.py
sudo chmod 644 /usr/local/lib/stereo-pi-obd/*.py
