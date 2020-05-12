"""event.py demonstrates asyncio for parallel dependent jobs"""
import asyncio
import os
import time
import yaml

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
            now = time.time()
            for key, value in status.items():
                if key == depend['child'] and value['end'] > 0:
                    print(f'Stage: {name} starting at {now}...')
                    ready = 1
            await asyncio.sleep(5)
            status = loader(filename)

    # starting
    entry = {name: {}}
    run = {'name': name,
           'number': number,
           'start': time.time(),
           'end': 0,
           'status': 0,
           'result': 0,
           'depend': depend}

    # running (factorials for fun)
    factorial = 1
    for i in range(2, number + 1):
        # write out the entry
        run['status'] = 1
        entry[name] = run
        writer(filename, entry)

        await asyncio.sleep(1)
        factorial *= i

    # done
    run['end'] = time.time()
    run['status'] = 2
    run['result'] = factorial
    entry[name] = run
    writer(filename, entry)


def loader(filename):
    """loader reads yaml

    :param filename: (str)
    :returns: contents (yaml)"""
    contents = ''
    with open(filename, 'r') as stream:
        contents = yaml.load(stream, Loader=yaml.FullLoader)
    return contents

def writer(filename, contents):
    """writer writes yaml

    :param filename: (str)
    :param: contents (dict)"""
    with open(filename, 'a') as stream:
        yaml.dump(contents, stream)

def touch(filename, times=None):
    """touch filename"""
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    with open(filename, 'a'):
        os.utime(filename, times)

async def main():
    """async main"""
    filename = 'stage.yaml'
    touch(filename)

    await asyncio.gather(
        stage('input', 1, filename),
        stage('serverdata', 2, filename, {'child': 'input'}),
        stage('powercheck', 2, filename, {'child': 'serverdata'}),
        stage('applybios', 5, filename, {'child': 'powercheck'}),
        stage('raidsetup', 7, filename, {'child': 'powercheck'}),
        stage('poweroff', 2, filename, {'child': 'raidsetup'}),
        stage('isocreate', 2, filename, {'child': 'serverdata'}),
        stage('deploy', 7, filename, {'child': 'poweroff'}),
        stage('ssh', 2, filename, {'child': 'deploy'}),
        stage('secureboot', 2, filename, {'child': 'ssh'}),
        stage('email', 2, filename, {'child': 'secureboot'}),
        stage('alldone', 1, filename, {'child': 'email'}),
    )

if __name__ == '__main__':
    asyncio.run(main())
