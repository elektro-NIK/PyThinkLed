#!/usr/bin/env python3
from time import sleep
import argparse


ledctrl = '/proc/acpi/ibm/led'
diskstat = '/proc/diskstats'
commands = ['on', 'off', 'blink']


def set_led(command, led=0):
    if command not in commands:
        raise ValueError('Commands are', str(commands))
    if type(led) is not int:
        raise TypeError('led is int from 0 to 15', str(commands))
    with open(ledctrl, 'w') as file:
        file.write(str(led) + ' ' + command)


# return int - I/Os in progress, 0 - unused now
def disk_stat(dev):
    with open(diskstat, 'r') as file:
        filelines = file.read().split('\n')
    for i in filelines:
        if dev in i:
            return int(i.split()[11])  # I/Os currently in progress


def disk_led(dev):
    while True:
        if disk_stat(dev):
            set_led('off')
            sleep(0.08)
            set_led('on')
            sleep(0.02)
        else:
            sleep(0.1)

if __name__ == "__main__":
    with open(diskstat, 'r') as f:
        lines = f.read().split('\n')
        hddlist = [i.split()[2] for i in lines[:-1]]
    parser = argparse.ArgumentParser(description='Alternative realization ThinkPad LED functional')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--on', help='set ThinkLED on', action='store_true')
    group.add_argument('--off', help='set ThinkLED off', action='store_true')
    group.add_argument('--blink', help='set ThinkLED blink', action='store_true')
    group.add_argument('--hdd', help='use hdd indicator')
    group.add_argument('--hdd-list', dest='hdd_list', help='list of possible HDD', action="store_true")
    args = parser.parse_args()
    if args.hdd in hddlist:
        disk_led(args.hdd)
    elif args.hdd_list:
        for i in hddlist[:-1]:
            print(i, end='\t')
        print(hddlist[-1])
    elif args.on:
        set_led('on')
    elif args.off:
        set_led('off')
    elif args.blink:
        set_led('blink')
    elif not any(vars(args).values()):
        print('main.py -h for help')
