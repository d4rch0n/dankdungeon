import random
from enum import Enum


class CivState(Enum):
    mixture = 'mixture'
    gestation = 'gestation'
    expansion = 'expansion'
    conflict = 'conflict'
    empire = 'empire'
    decay = 'decay'
    invasion = 'invasion'

    @classmethod
    def random(cls):
        return random.choice([x for x in cls])


class Civ:

    def __init__(self, state=CivState.gestation):
        self.state = state


class History:

    def __init__(self):
        pass

    def generate(self):
        pass


def main_history():
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    hist = History()
    hist.generate()
