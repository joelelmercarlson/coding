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
    filename = sandbox()

    await asyncio.gather(
        stage('init', 1, filename, None, sandbox_check),
        stage('input', 2, filename, {'parent': 'init'}),
        stage('serverdata', 2, filename, {'parent': 'input'}),
        stage('powercheck', 2, filename, {'parent': 'serverdata'}),
        stage('applybios', 5, filename, {'parent': 'powercheck'}),
        stage('raidsetup', 9, filename, {'parent': 'powercheck'}),
        stage('poweroff', 2, filename, {'parent': 'raidsetup'}),
        stage('isocreate', 2, filename, {'parent': 'serverdata'}),
        stage('deploy', 9, filename, {'parent': 'poweroff'}),
        stage('ssh', 3, filename, {'parent': 'deploy'}),
        stage('secureboot', 2, filename, {'parent': 'ssh'}),
        stage('email', 2, filename, {'parent': 'secureboot'}),
        stage('alldone', 1, filename, {'parent': 'email'}),
    )

def red(message):
    """:returns: (str)"""
    return f'\x1b[31;1m{message}\x1b[0m'

def sandbox():
    """sandbox

    :param filename: (str)
    :returns sandbox: (str)"""
    path = '/var/tmp'
    filename = path + '/stage.yaml'
    os.chdir(path)
    touch(filename)
    return filename

def sandbox_check(filename):
    """sandbox_check check the sandbox

    :param filename: (str)"""
    print('***')
    os.system('uname -a')
    os.system('df -h /var/tmp')
    print('***')

async def stage(name, number, filename, dependent=None, *args, **kwargs):
    """stage executes functions in *args

    :param name: (str)
    :param number: (int)
    :param filename: (yaml)
    :param dependent: (dict)"""
    # handle dependencies and status
    status = loader(filename)
    if dependent is not None and status is not None:
        ready = 0
        while ready < 1:
            for key, value in status.items():
                if key == dependent['parent'] and value['end'] > 0:
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
           'dependent': dependent}
    journal(filename, run)

    # status=1: Run (factorials for fun)
    for k in args:
        k(filename)
        await asyncio.sleep(1)

    # factorials simulate something that takes time
    # replace in production code w/ IO functions
    factorial = 1
    for i in range(2, number + 1):
        factorial *= i
        await asyncio.sleep(1)

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
