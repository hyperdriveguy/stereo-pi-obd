#!/usr/bin/python

import obd
import systemd.daemon


# This doesn't pair your obd reader for you. You have to do that yourself.
# Use async connections for continous updates.
# TODO: A lot. Main loop, retry connecting, warning and importing tts
connection = obd.Async(fast=False, timeout=30)
