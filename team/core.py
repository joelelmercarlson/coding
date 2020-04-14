"""core.py -- contains class"""
from . import helpers

__author__ = 'Joel E Carlson'
__credits__ = ['joel.elmer.carlson@gmail.com']
__email__ = __credits__[0]
__pylint__ = '10.00/10'

class ExampleClass():
    """ExampleClass -- default core.py, helpers.py"""
    def __init__(self, name):
        self.my_name = name
        self.first_name = helpers.first(self.my_name)
        self.last_name = helpers.last(self.my_name)
        self.name_array = helpers.make_parts(self.my_name)
        self.name_dict = helpers.make_dict(self.my_name)
    def __repr__(self):
        return (f'ExampleClass({self.my_name!r}'
                f', {self.first_name!r}'
                f', {self.last_name!r}'
                f', {self.name_array!r}'
                f', {self.name_dict!r}'
                ')')

    def pick_array(self):
        """pick_array -- return array"""
        return self.name_array
    def pick_dict(self):
        """pick_dict -- return dictionary"""
        return self.name_dict
    @classmethod
    def example(cls):
        """example -- cls example"""
        return cls('Joel Carlson')
