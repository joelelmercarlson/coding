"""helpers.py -- contains helper functions"""
from collections import defaultdict

__author__ = 'Joel E Carlson'
__credits__ = ['joel.elmer.carlson@gmail.com']
__email__ = __credits__[0]
__pylint__ = '10.00/10'

def make_parts(name):
    """make_parts --  return parts"""
    parts = name.split(' ')
    if len(parts) < 2:
        parts.append('')
    return parts

def first(name):
    """first -- return first element"""
    return make_parts(name)[0]

def last(name):
    """last -- return last element"""
    return make_parts(name)[1]

def make_dict(name):
    """make_dict -- return dictionary"""
    dictionary = defaultdict(list)
    parts = make_parts(name)
    dictionary['first'].append(parts[0])
    dictionary['last'].append(parts[1])
    dictionary['name'].append(name)
    return dictionary
