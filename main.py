#!/usr/bin/python

import time
import obd
import systemd.daemon
import tts_wrapper

last_time = int(round(time.time()))
gal_notify = [100, 75, 50, 25, 10, 5, 2]
gal_notify_this_trip = False


def time_since_last_notification(reset=False):
    if reset is True:
        global last_time
        last_time = int(round(time.time()))
        return int(round(time.time()) - round(last_time))


def rpm_callback(rpms):
    # Watch for excessively high RPMS, anything above 3500
    if rpms.value.magnitude > 3500:
        # 30 second grace period
        if time_since_last_notification() > 30:
            tts_wrapper.speak('Agressive Driving. '
                              'This violation will be logged.')
            print('Violation: Agressive Driving on ' + time.ctime())
            time_since_last_notification(reset=True)


def speed_callback(speed):
    # Watch for excessive speed. Capped at 85 MPH
    # Raw unit is KPH
    mph_speed = speed.value.to('mph').magnitude
    if mph_speed > 85:
        # 15 second grace period
        if time_since_last_notification() > 15:
            tts_wrapper.speak('Excessive Speed. '
                              'This violation will be logged.')
            print('Violation: Excessive Speed on ' + time.ctime())
            time_since_last_notification(reset=True)


def fuel_level_callback(fuel_lvl):
    # Dodge Grand Caravan has a 20 gallon fuel tank
    # Avg 20 MPG
    # This value is a percentage. Use (fuel_lvl / 100) * 20
    gals_left = (fuel_lvl.value.magnitude / 100) * 20
    if fuel_lvl.value.magnitude in gal_notify:
        if not gal_notify_this_trip:
            tts_wrapper.speak(str(gals_left) + ' gallons left.')
            global gal_notify_this_trip
            gal_notify_this_trip = True
            time_since_last_notification(reset=True)


def main():
    systemd.daemon.notify(systemd.daemon.Notification.READY)
    # This doesn't pair your obd reader for you. You have to do that yourself.
    while True:
        # Use async connections for continous updates.
        connection = obd.Async(fast=False, timeout=30)
        if connection.is_connected():
            break
        print('Failed to connect to OBD. Trying again in 30 seconds...')
        time.sleep(30)
    tts_wrapper.speak('Connected to OBD')

    connection.watch(obd.commands.RPM, callback=rpm_callback)

    connection.watch(obd.commands.SPEED, callback=speed_callback)
    connection.watch(obd.commands.FUEL_LEVEL, callback=fuel_level_callback)

    connection.start()

    # Stop the script on disconnect. Systemd will restart it for us.
    while True:
        if not connection.is_connected():
            connection.stop()
            print('Connection lost.')
            break
        time.sleep(30)



if __name__ == "__main__":
    main()
