#!/usr/bin/env python3

ledctrl = '/proc/acpi/ibm/led'
diskstat = '/proc/diskstats'
commands = ['on', 'off', 'blink']


def set_led(command, led=0):
    if command not in commands:
        raise ValueError('Commands are', str(commands))
    if type(led) is not int:
        raise TypeError('led is int from 0 to 15', str(commands))
    with open(ledctrl, 'w') as f:
        f.write(str(led) + ' ' + command)


# return int - I/Os in progress, 0 - unused now
def disk_stat(dev):
    with open(diskstat, 'r') as f:
        lines = f.read().split('\n')
    for i in lines:
        if dev in i:
            return int(i.split()[11])  # I/Os currently in progress

def disk_led(dev):
    while(True):
        if main.disk_stat('sda'):
            main.set_led('off')
            time.sleep(0.08)
            main.set_led('on')
            time.sleep(0.02)
       else:
            time.sleep(0.1)
