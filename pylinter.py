"""pylinter -- report pylint scores on our .py"""
import os
import re

__author__ = 'Joel E Carlson'
__credits__ = ['joel.elmer.carlson@gmail.com']
__email__ = __credits__[0]
__pylint__ = '10.00/10'

def banner(message):
    """banner -- print a banner"""
    counter = len(message)
    rule = "="
    while counter > 0:
        counter -= 1
        rule += "="
    print(message)
    print(rule)

def pylint(filename):
    """pylint -- call pylint command"""
    if filename is None:
        return
    cmd = "%s %s" %('pylint', filename)
    banner(filename)
    os.system(cmd)

def py_filter(filename):
    """py_filter -- return *.py"""
    match = re.search(r'.*.py$', filename)
    if match:
        return match.group()
    return None

def walk(directory):
    """walk -- pylint a directory"""
    dir_list = os.listdir(directory)
    files = []
    for i in dir_list:
        path = "%s/%s" %(directory, i)
        filename = py_filter(path)
        files.append(filename)
    for i in files:
        pylint(i)

def run():
    """run -- add to walk(directory) when ready"""
    walk('.')
    walk('team')

if __name__ == '__main__':
    banner("pylint scores. Goal is 8.0/10 or better.")
    run()
