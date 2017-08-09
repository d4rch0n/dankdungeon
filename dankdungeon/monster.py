import os
import sys
import json
from fuzzywuzzy import fuzz


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
    MONSTERS = []
    TAG_GROUPS = {}
    MONSTER_GROUPS = {}
    MONSTER_DATA = []
    MONSTER_D = {}
    TAGS = set()

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

    def __sub__(self, mon):
        if not isinstance(mon, Monster):
            raise ValueError('cant calculate the difference between anything '
                             'except other monsters')
        s = 0.0
        if self.name == mon.name:
            return 999999
        langs = {x for x in self.tags if x.endswith('_lang')}
        mlangs = {x for x in mon.tags if x.endswith('_lang')}
        tags = self.tags - langs
        mtags = mon.tags - mlangs
        s += 2 * len(langs & mlangs)
        areas = {'plains', 'desert', 'mountain', 'swamp', 'forest', 'jungle',
                 'tundra'}
        if tags & mtags & areas:
            s += 1
        for t in {'insect', 'arachnid', 'reptile', 'cave', 'city', 'sea',
                  'fresh', 'fish'}:
            if tags & {t} and mtags & {t}:
                s *= 2
        for t in {'underdark', 'fire', 'ice', 'lightning', 'water', 'earth',
                  'air', 'water', 'hell', 'fly', 'swim', 'were'}:
            if tags & {t} and mtags & {t}:
                s *= 3
        align = {'good', 'evil'}
        if len(align & tags) == 1 and len(align & mtags) == 1:
            if align & tags & mtags:
                s *= 7
            else:
                s /= 7
        if self.type == mon.type:
            if self.subtype and self.subtype == mon.subtype:
                s *= 8
            else:
                s *= 3
        for bad in {'were', 'dragon', 'reptile', 'arachnid', 'insect'}:
            if bad not in tags | mtags:
                continue
            if {bad} & tags & mtags != {bad}:
                s /= 5
            else:
                s *= 5
        return s

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
        tags = set()
        for mon in cls.MONSTERS:
            tags |= mon.tags
        cls.TAGS = tags.copy()
        for tag in cls.TAGS:
            arr = []
            for mon in cls.MONSTERS:
                if mon.tags & {tag}:
                    arr.append(mon)
            cls.TAG_GROUPS[tag] = arr
        for mon in cls.MONSTERS:
            arr = []
            for mon2 in cls.MONSTERS:
                diff = mon - mon2
                if diff > 1.0:
                    arr.append((diff, mon2))
            arr = sorted(arr, reverse=True, key=lambda x: (x[0], x[1].name))
            arr = [v for k, v in arr]
            cls.MONSTER_GROUPS[mon] = arr
        cls.MONSTER_D = {m.name.lower().strip(): m for m in cls.MONSTERS}

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

    @classmethod
    def get(cls, name):
        mon = cls.MONSTER_D.get(name.strip().lower())
        if mon:
            return mon
        mons = []
        for mon in cls.MONSTERS:
            ratio = fuzz.ratio(mon.name.lower().strip(), name)
            mons.append((ratio, mon))
        mons = [b for a, b in sorted(mons, key=lambda x: x[0], reverse=True)]
        return mons[0]

    def related(self):
        return Monster.MONSTER_GROUPS[self]


def calc_threshold(player_levels):
    thresh = [0, 0, 0, 0]
    for lvl in player_levels:
        for i in range(4):
            thresh[i] += XP_THRESH[lvl][i]
    return thresh


Monster.load()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--monster', '-m', help='select a monster by name')
    parser.add_argument('--related', '-r', action='store_true',
                        help='print related monsters')
    parser.add_argument('--players', '-p', help='the player levels')
    args = parser.parse_args()
    if args.players:
        players = [int(x.strip()) for x in args.players.split(',')]
    else:
        players = [1, 1, 1, 1]
    if args.monster:
        mon = Monster.get(args.monster)
        if args.related:
            rel = mon.related()[:10]
            for m in rel:
                print(m.name)
    else:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
