"""event.py demonstrates asyncio for parallel dependent jobs"""
import asyncio
import os
import time
import sys
import yaml

def checkpoint(status):
    """checkpoint display informative journal message

    :param status: (dict)"""
    name = status['name']
    result = status['result']
    stat = status['status']
    if not stat:
        verb = red('Start')
        when = status['start']
    if stat > 0:
        verb = yellow('Run')
        when = time.time()
    if stat > 1:
        verb = green('Done')
        when = status['end']
    elapsed = "%02.2f" %(status['duration'])
    print(f'[ {verb} ] {name} at {when}... elapsed={elapsed}, result={result}')

def factorial(filename, number=0):
    """factorial

    :param filename: (str)
    :param number: (int)
    :returns: (int)"""
    touch(filename)
    fact = 1
    for i in range(2, number + 1):
        fact *= i
        time.sleep(1)
    return fact

def green(message):
    """:returns: (str)"""
    return f'\x1b[32;1m{message}\x1b[0m'

def journal(filename, status):
    """journal status to screen and disk

    :param filename: (str)
    :param status: (dict)"""
    try:
        name = status['name']
    except KeyError:
        name = 'nil'
    checkpoint(status)
    entry = {name: {}}
    entry[name] = status
    writer(filename, entry)

def loader(filename):
    """loader reads yaml

    :param filename: (str)
    :returns: contents (yaml)"""
    contents = ''
    with open(filename, 'r') as stream:
        contents = yaml.load(stream, Loader=yaml.FullLoader)
    return contents

async def main():
    """async main builds sandbox and calls functions"""
    filename = sandbox()

    await asyncio.gather(
        stage('init', filename, sandbox_check),
        stage('input', filename, factorial, kwargs={'parent': 'init', 'number': 2}),
        stage('serverdata', filename, factorial, kwargs={'parent': 'input', 'number': 2}),
        stage('powercheck', filename, factorial, kwargs={'parent': 'serverdata', 'number': 3}),
        stage('applybios', filename, factorial, kwargs={'parent': 'powercheck', 'number': 5}),
        stage('raidsetup', filename, factorial, kwargs={'parent': 'powercheck', 'number': 9}),
        stage('poweroff', filename, factorial, kwargs={'parent': 'raidsetup', 'number': 3}),
        stage('isocreate', filename, factorial, kwargs={'parent': 'serverdata', 'number': 5}),
        stage('deploy', filename, factorial, kwargs={'parent': 'poweroff', 'number': 9}),
        stage('ssh', filename, factorial, kwargs={'parent': 'deploy', 'number': 2}),
        stage('secureboot', filename, factorial, kwargs={'parent': 'ssh', 'number': 2}),
        stage('email', filename, factorial, kwargs={'parent': 'secureboot', 'number': 2}),
        stage('alldone', filename, factorial, kwargs={'parent': 'email', 'number': 2}),
    )

def red(message):
    """:returns: (str)"""
    return f'\x1b[31;1m{message}\x1b[0m'

def sandbox(path='/var/tmp/', filename='stage.yaml'):
    """sandbox creates journalfile

    :param path: (str)
    :param filename: (str)
    :returns journalfile: (str)"""
    journalfile = path + filename
    try:
        os.remove(journalfile)
    except FileNotFoundError:
        pass
    os.chdir(path)
    touch(journalfile)
    return journalfile

def sandbox_check(filename, number=0):
    """sandbox_check check the sandbox

    :param filename: (str)
    :returns: (bool)"""
    print('*** sandbox_check ***')
    os.system('df -h ' + filename)
    print('*********************')
    time.sleep(number)
    return True

async def stage(name, filename, *args, **kwargs):
    """stage executes *args w/ **kwargs

    :param name:      (str)  unique name of our step
    :param filename:  (yaml) journal our events
    :param *args:     [str]  function to process
    :param **kwargs:  (dict)"""

    # Process *args, **kwargs
    number = 0
    parent = None
    process = None
    if len(args) > 0:
        process = args[0]
    else:
        print(f'async def stage({name}, {filename}, {args}, {kwargs}) error')
        sys.exit(1)
    for key, value in kwargs.items():
        if key == 'kwargs':
            number = value['number']
            parent = value['parent']

    # Manage dependencies and start time
    status = loader(filename)
    if parent is not None and status is not None:
        ready = 0
        while ready < 1:
            for key, value in status.items():
                if key == parent and value['end'] > 0:
                    ready = 1
            await asyncio.sleep(5)
            status = loader(filename)

    # status=0: Start
    run = {'name': name,
           'start': time.time(),
           'end': 0,
           'duration': 0,
           'status': 0,
           'result': 0,
           'kwargs': kwargs}
    journal(filename, run)

    # status=1: Run
    result = process(filename, number)
    await asyncio.sleep(1)

    run['status'] = 1
    run['duration'] = time.time() - run['start']
    run['result'] = result
    journal(filename, run)

    # status=2: Done
    run['status'] = 2
    run['end'] = time.time()
    journal(filename, run)

def touch(filename, times=None):
    """touch filename"""
    with open(filename, 'a'):
        os.utime(filename, times)

def writer(filename, contents):
    """writer writes yaml

    :param filename: (str)
    :param: contents (dict)"""
    with open(filename, 'a') as stream:
        yaml.dump(contents, stream)

def yellow(message):
    """:returns: (str)"""
    return f'\x1b[33;1m{message}\x1b[0m'

if __name__ == '__main__':
    asyncio.run(main())
