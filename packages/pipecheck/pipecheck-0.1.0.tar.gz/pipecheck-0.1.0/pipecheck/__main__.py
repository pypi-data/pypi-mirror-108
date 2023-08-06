#!/usr/bin/env /usr/bin/python3

import concurrent.futures
import time
from icecream import ic
from termcolor import colored
from periscope.cli import get_commands_and_config_from_args, parse_args
from periscope.cmdfile import get_config_from_yamlfile, get_commands_from_config
from periscope.checks import Ok, Warn, Err, CheckResult, checks
from prometheus_client import start_http_server, Summary, Enum

REQUEST_TIME = Summary('checks_processing_seconds', 'Time spent processing all checks')

CHECK_STATE_LABLES = ['url', 'host', 'port', 'name']
CHECK_STATES = {}
for check in checks:
    labels = [x for x in checks[check]['args'] if x in CHECK_STATE_LABLES]
    CHECK_STATES[check] = Enum(f'{check}_check_state', f'State of check {check}',
                               labels, states=['Ok', 'Warn', 'Err'])

commands = []
results = []

def print_result(result: CheckResult):
    if isinstance(result, Warn):
        print(colored('[WARN]  ', 'yellow'), result.msg)
    elif isinstance(result, Ok):
        print(colored('[OK]    ', 'green'), result.msg)
    elif isinstance(result, Err):
        print(colored('[ERROR] ', 'red'), result.msg)

def launch_checks(commands):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for cmd in commands:
            yield (cmd, executor.submit(cmd[0], **cmd[1]))

def gen_calls(args):
    (commands, config) = get_commands_and_config_from_args(args)
    if 'file' in args and args['file']:
        c = ic(get_config_from_yamlfile(args['file']))
        commands.extend(ic(get_commands_from_config(c)))

    for command in commands:
        yield gen_call(command, config)

def gen_call(command, config):
    f_name = command.pop('type')
    if f_name not in checks:
        raise Exception(f"can't find check of type '{f_name}'")
    f = checks[f_name]['f']
    call_args = {}
    l_config = {**config, **command}
    for check_arg in checks[f_name]['args']:
        if check_arg not in l_config:
            continue
        if l_config[check_arg]:
            call_args[check_arg] = l_config[check_arg]
    return (f, call_args)


@REQUEST_TIME.time()
def run(calls):
    launched_checks = ic(list(launch_checks(calls)))
    return_code = 0
    for (cmd, future) in launched_checks:
        result = future.result()
        print_result(result)
        labels = {k: v for k, v in cmd[1].items() if k in CHECK_STATE_LABLES}
        CHECK_STATES[cmd[0].__name__].labels(**labels).state(result.__class__.__name__)
        if isinstance(result, Err):
            return_code = 1

    return return_code


if __name__ == '__main__':
    args = parse_args()

    if not ('verbose' in args and args['verbose']):
        ic.disable()
    ic(args)

    calls = list(gen_calls(args))
    ic(calls)

    if 'interval' in args and args['interval']:
        start_http_server(args['port'])
        while(True):
            run(calls)
            time.sleep(float(args['interval']))
    else:
        exit(run(calls))
