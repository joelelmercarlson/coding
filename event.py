"""event.py demonstrates asyncio for parallel dependent jobs"""
import asyncio
import os
import time
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
    """async main"""
    filename = 'stage.yaml'
    touch(filename)

    await asyncio.gather(
        stage('input', 2, filename),
        stage('serverdata', 2, filename, {'child': 'input'}),
        stage('powercheck', 2, filename, {'child': 'serverdata'}),
        stage('applybios', 5, filename, {'child': 'powercheck'}),
        stage('raidsetup', 9, filename, {'child': 'powercheck'}),
        stage('poweroff', 2, filename, {'child': 'raidsetup'}),
        stage('isocreate', 2, filename, {'child': 'serverdata'}),
        stage('deploy', 9, filename, {'child': 'poweroff'}),
        stage('ssh', 3, filename, {'child': 'deploy'}),
        stage('secureboot', 2, filename, {'child': 'ssh'}),
        stage('email', 2, filename, {'child': 'secureboot'}),
        stage('alldone', 1, filename, {'child': 'email'}),
    )

def red(message):
    """:returns: (str)"""
    return f'\x1b[31;1m{message}\x1b[0m'

async def stage(name, number, filename, depend=None):
    """stage executes steps

    :param name: (str)
    :param number: (int)
    :param filename: (yaml)
    :param depend: (dict)"""

    # handle dependencies and status
    status = loader(filename)
    if depend is not None:
        ready = 0
        while ready < 1:
            for key, value in status.items():
                if key == depend['child'] and value['end'] > 0:
                    ready = 1
            await asyncio.sleep(5)
            status = loader(filename)

    # status=0: Start
    run = {'name': name,
           'number': number,
           'start': time.time(),
           'end': 0,
           'duration': 0,
           'status': 0,
           'result': 0,
           'depend': depend}
    journal(filename, run)

    # status=1: Run (factorials for fun)
    factorial = 1
    for i in range(2, number + 1):
        await asyncio.sleep(1)
        factorial *= i

        run['status'] = 1
        run['duration'] = time.time() - run['start']
        journal(filename, run)

    # status=2: Done
    run['end'] = time.time()
    run['status'] = 2
    run['result'] = factorial
    journal(filename, run)

def touch(filename, times=None):
    """touch filename"""
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
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
