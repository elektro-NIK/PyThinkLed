#!/usr/bin/env python3

ledctrl = '/proc/acpi/ibm/led'
commands = ['on', 'off', 'blink']


def set_led(command, led=0):
    if command not in commands:
        raise ValueError('Commands are', str(commands))
    if type(led) is not int:
        raise TypeError('led is int from 0 to 15', str(commands))
    with open(ledctrl, 'w') as f:
        f.write(str(led) + ' ' + command)


