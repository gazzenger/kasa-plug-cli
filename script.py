#!/usr/bin/env python3

import os
from dotenv import load_dotenv
load_dotenv()
device_ip = os.getenv('DEVICE_IP')


import asyncio
from kasa import SmartPlug


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--action')
parser.add_argument('--state', action='store_true')
parser.add_argument('--status', action='store_true')
parser.add_argument('--schedule', action='store_true')
parser.add_argument('--add-schedule')
parser.add_argument('--remove-schedule')
#parser.add_argument('--set-timer', )
args = parser.parse_args()

action_arg = args.action or ''
status_arg = args.status
state_arg = args.state
schedule_arg = args.schedule
add_schedule_arg = args.add_schedule or ''
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
        print('test')
    elif remove_schedule_arg:
        await dev._query_helper('schedule','delete_rule', {'id': remove_schedule_arg})

if __name__ == "__main__":
    asyncio.run(main())

