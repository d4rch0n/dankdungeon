import os
import json


ROOT = os.path.dirname(__file__)
DATADIR = os.path.join(ROOT, 'data')
MONSTERS_PATH = os.path.join(DATADIR, 'monsters.json')

# Easy, Medium, Hard, Deadly
XP_THRESH = [
    (0, 0, 0, 0),
    # 1st
    (25, 50, 75, 100),
    (50, 100, 150, 200),
    (75, 150, 225, 400),
    (125, 250, 375, 500),
    # 5th
    (250, 500, 750, 1100),
    (300, 600, 900, 1400),
    (350, 750, 1100, 1700),
    (450, 900, 1400, 2100),
    (550, 1100, 1600, 2400),
    # 10th
    (600, 1200, 1900, 2800),
    (800, 1600, 2400, 3600),
    (1000, 2000, 3000, 4500),
    (1100, 2200, 3400, 5100),
    (1250, 2500, 3800, 5700),
    # 15th
    (1400, 2800, 4300, 6400),
    (1600, 3200, 4800, 7200),
    (2000, 3900, 5900, 8800),
    (2100, 4200, 6300, 9500),
    (2400, 4900, 7300, 10900),
    # 20th!
    (2800, 5700, 8500, 12700),
]


def scale_enc(num):
    if num == 0:
        return 0.0
    if num == 1:
        return 1.0
    if num == 2:
        return 1.5
    if 3 <= num <= 6:
        return 2.0
    if 7 <= num <= 10:
        return 2.5
    if 11 <= num <= 14:
        return 3.0
    return 4.0


class Monster:
    MONSTERS = {}
    MONSTER_DATA = []

    def __repr__(self):
        return self.data['name']

    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        if attr in self.data:
            val = self.data[attr]
        else:
            raise AttributeError('{!r} has no {!r}'.format(self, attr))
        if isinstance(val, str):
            if val.isdigit():
                return int(val)
            try:
                return float(val)
            except:
                return val
        return val

    @property
    def tags(self):
        if 'tags' not in self.data:
            return set()
        return set(self.data['tags'])

    @classmethod
    def load(cls):
        with open(MONSTERS_PATH) as f:
            cls.MONSTER_DATA = json.load(f)
        cls.MONSTERS = [cls(x) for x in cls.MONSTER_DATA]

    @classmethod
    def find(cls, include=None, exclude=None):
        mons = [v for v in cls.MONSTERS]
        if include is not None:
            if isinstance(include, str):
                include = {include}
            include = set(include)
            mons = [v for v in mons if include & v.tags]
        if exclude is not None:
            if isinstance(exclude, str):
                exclude = {exclude}
            exclude = set(exclude)
            mons = [v for v in mons if not (exclude & v.tags)]
        return mons


def calc_threshold(player_levels):
    thresh = [0, 0, 0, 0]
    for lvl in player_levels:
        for i in range(4):
            thresh[i] += XP_THRESH[lvl][i]
    return thresh
