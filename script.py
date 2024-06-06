#!/usr/bin/env python3

import os
from dotenv import load_dotenv
load_dotenv()
device_ip = os.getenv('DEVICE_IP')

from datetime import datetime

import asyncio
from kasa import SmartPlug

# Define a custom argument type for a list of integers
# https://www.geeksforgeeks.org/how-to-pass-a-list-as-a-command-line-argument-with-argparse/
def list_of_ints(arg):
    return list(map(int, arg.split(',')))

import argparse
parser = argparse.ArgumentParser(description='Kasa Plug CLI tool')
subparsers = parser.add_subparsers()
parser.add_argument('--action')
parser.add_argument('--state', action='store_true')
parser.add_argument('--status', action='store_true')
parser.add_argument('--schedule', action='store_true')

add_schedule_parser = subparsers.add_parser('add-schedule')
add_schedule_parser.add_argument('--name')
add_schedule_parser.add_argument('--disable', action='store_true', default=False)
add_schedule_parser.add_argument('--dow', type=list_of_ints, default=[1,1,1,1,1,1,1], help='Days of Week, Sun - Sat')
add_schedule_parser.add_argument('--no-repeat', action='store_true', default=False)
add_schedule_parser.add_argument('--set-state', default=True)
add_schedule_parser.add_argument('--trigger-sunrise', action='store_true', default=False)
add_schedule_parser.add_argument('--trigger-sunset', action='store_true', default=False)
add_schedule_parser.add_argument('--trigger-time', default=0)

parser.add_argument('--remove-schedule')
#parser.add_argument('--set-timer', )
args = parser.parse_args()

action_arg = args.action or ''
status_arg = args.status
state_arg = args.state
schedule_arg = args.schedule

add_schedule_arg = add_schedule_parser
add_schedule_name_arg = args.name
add_schedule_disable_arg = args.disable
add_schedule_dow_arg = args.dow
add_schedule_no_repeat_arg = args.no_repeat
add_schedule_set_state_arg = args.set_state
add_schedule_trigger_sunrise_arg = args.trigger_sunrise
add_schedule_trigger_sunset_arg = args.trigger_sunset
add_schedule_trigger_time_arg = args.trigger_time

remove_schedule_arg = args.remove_schedule or ''



async def main():
    dev = SmartPlug(device_ip)  # We create the instance inside the main loop
    await dev.update()

    sys_info = dev.sys_info

    if state_arg:
        print('ON' if sys_info['relay_state'] else 'OFF')
    elif action_arg.upper() == 'ON':
        await dev.turn_on()
    elif action_arg.upper() == 'OFF':
        await dev.turn_off()
    elif status_arg:
        print(sys_info)
    elif schedule_arg:
        schedule = await dev._query_helper('schedule','get_rules')
        print(schedule['rule_list'])
    elif add_schedule_arg:
        print(f'test {add_schedule_name_arg}')
        print(f'test {add_schedule_disable_arg}')
        print(f'test {add_schedule_dow_arg}')
        print(f'test {add_schedule_no_repeat_arg}')
        print(f'test {add_schedule_set_state_arg}')
        print(f'test {add_schedule_trigger_sunrise_arg}')
        print(f'test {add_schedule_trigger_sunset_arg}')

        print(f'test {add_schedule_trigger_time_arg}')
        time_object = datetime.strptime(add_schedule_trigger_time_arg, '%H:%M:%S').time()
        print(type(time_object))
        print(time_object)
        min_value = time_object.hour * 60 + time_object.minute + time_object.second / 60
        print(min_value)

        if add_schedule_trigger_time_arg:
            # trigger time
        elif add_schedule_trigger_sunrise_arg:
            
        elif add_schedule_trigger_sunset_arg:
            
        elif add_schedule_no_repeat_arg:
            # ensure dow are all 0's
            # must also set year, month, day values
        else:
            # repeating, and either nominated DOW or default DOWs

    elif remove_schedule_arg:
        await dev._query_helper('schedule','delete_rule', {'id': remove_schedule_arg})

if __name__ == "__main__":
    asyncio.run(main())

