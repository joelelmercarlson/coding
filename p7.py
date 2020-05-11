"""p7.py"""
import time
import sys

def make_a_guy(name, level, power, pet):
    """make_a_guy

    :param name: (str)
    :param level: (int)
    :param power: (str)
    :param pet: (str)"""
    print("==================================================")
    print(f'{name} is level {level} w/ amazing power {power}')
    print(f'my pet is {pet}')
    print("==================================================")

def action(name, ops):
    """action does ops

    :param name: (str)
    :param ops: (str)"""
    time.sleep(1)
    print(f'{name} is doing {ops}!')

def blood():
    """blood does blood"""
    i = 0
    while i < 3:
        i = i + 1
        print("* BLOOD *")

def dylan():
    """say hello to the creator"""
    say('Dylan')

def say(something):
    """say something

    :param something: (str)"""
    print(f'Hello {something}!')

if __name__ == '__main__':
    NAME = 'fiend'
    PET = 'fang'
    WEAPON = 'blood blaster'
    TABLE = {'a': 'attacks',
             'd': 'defends',
             's': 'pet bites',
             'f': 'bleeds',
             'n': 'jumps',
             'o': 'king attack',
             'p': 'potty time',
             'k': 'kill move',
             'c': 'change to gorilla lava monster',
             '9': 'turn into Drew Brees',
             'q': 'dies'}
    COUNTER = 0
    dylan()
    make_a_guy(NAME, '10', WEAPON, PET)
    while True:
        ACTOR = input('Action> ')
        if len(ACTOR) > 1:
            say(ACTOR)
        else:
            try:
                DOING = TABLE[ACTOR]
            except KeyError:
                DOING = f'ducks, dodge, grab your {WEAPON}!'
            action(NAME, DOING)
        COUNTER = COUNTER + 1
        if COUNTER > 5:
            print(f'Battle over {NAME} and {PET}')
            blood()
            sys.exit()
