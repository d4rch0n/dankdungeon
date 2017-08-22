import math
import random
from collections import namedtuple
from .namerator import make_name


def roll_stat():
    nums = [random.randint(1, 6) for _ in range(4)]
    return sum(nums) - min(nums)


VALID_SUBRACES = {
    'dwarf': ['hill', 'mountain'],
    'elf': ['high', 'wood', 'dark'],
    'halfling': ['lightfoot', 'stout'],
    'human': ['calishite', 'chondathan', 'damaran', 'illuskan', 'mulan',
              'rashemi', 'shou', 'tethyrian', 'turami'],
    'dragonborn': ['black', 'blue', 'brass', 'bronze', 'copper', 'gold',
                   'green', 'red', 'silver', 'white'],
    'gnome': ['forest', 'rock'],
}

HIT_DICE = {
    'barbarian': 12,
    'bard': 8,
    'cleric': 8,
    'druid': 8,
    'fighter': 10,
    'monk': 8,
    'paladin': 10,
    'ranger': 10,
    'rogue': 8,
    'sorcerer': 6,
    'warlock': 8,
    'wizard': 6,
    None: 8,
}

DESIRED_STATS = {
    'barbarian': ('str', 'con'),
    'bard': ('cha', 'dex'),
    'cleric': ('wis',),
    'druid': ('wis',),
    'fighter': ('str', 'con'),
    'monk': ('dex', 'wis'),
    'paladin': ('str', 'cha'),
    'ranger': ('dex', 'wis'),
    'rogue': ('dex',),
    'sorcerer': ('cha',),
    'warlock': ('cha',),
    'wizard': ('int',),
    None: [],
}


Stats = namedtuple('Stats', ['str', 'dex', 'con', 'int', 'wis', 'cha'])


def modifier(stat):
    return math.floor((stat - 10) / 2)


class NPC:

    def __init__(self, name=None, klass=None, gender=None, race=None,
                 subrace=None, stats=None, level=1, hp=None, ac=10):
        self.gender = gender or random.choice(['male', 'female'])
        self.race = race or random.choice([
            'human', 'elf', 'half-elf', 'dwarf', 'gnome', 'half-orc',
            'halfling',
        ])
        self.name = name or make_name(self.race, gender=self.gender)
        self.subrace = subrace
        if self.subrace is None:
            self._random_subrace()
        self.klass = klass
        if stats is None:
            self.roll_stats(klass=klass)
        else:
            self.stats = Stats(**stats)
            attrs = DESIRED_STATS[self.klass]
            self.stats = self._add_racial_stats(attrs=attrs)
        self.level = level
        self.ac = ac
        self.hp = hp or self._calc_hp()

    def _random_subrace(self):
        if self.race in VALID_SUBRACES:
            self.subrace = random.choice(VALID_SUBRACES[self.race])

    def _calc_hp(self):
        base = HIT_DICE[self.klass]
        auto = (base / 2) + 1
        mod = modifier(self.con)
        hp = base + mod
        for _ in range(1, self.level):
            hp += auto + mod
        return hp

    def roll_stats(self, klass=None):
        stats = sorted([roll_stat() for _ in range(6)], reverse=True)
        attrs = DESIRED_STATS[self.klass]
        if klass is None:
            random.shuffle(stats)
            self.stats = Stats(*stats)
        else:
            self.stats = self._setup_stats(stats, attrs)
        self.stats = self._add_racial_stats(attrs=attrs)

    def _add_racial_stats(self, attrs=None):
        self.speed = 30
        self.senses = []
        self.size = 'medium'
        kwargs = dict(**self.stats._asdict())
        if self.race == 'dwarf':
            kwargs['con'] += 2
            self.speed = 25
            self.senses = ['darkvision']
            if self.subrace == 'hill':
                kwargs['wis'] += 1
            elif self.subrace == 'mountain':
                kwargs['str'] += 2
        elif self.race == 'elf':
            kwargs['dex'] += 2
            self.senses = ['darkvision']
            if self.subrace == 'high':
                kwargs['int'] += 1
            elif self.subrace == 'wood':
                self.speed = 35
                kwargs['wis'] += 1
            elif self.subrace in ('dark', 'drow'):
                kwargs['cha'] += 1
        elif self.race == 'halfling':
            kwargs['dex'] += 2
            self.size = 'small'
            self.speed = 25
            if self.subrace == 'lightfoot':
                kwargs['cha'] += 1
            elif self.subrace == 'stout':
                kwargs['con'] += 1
        elif self.race == 'human':
            for key in kwargs:
                kwargs[key] += 1
        elif self.race == 'dragonborn':
            kwargs['str'] += 2
            kwargs['cha'] += 1
        elif self.race == 'gnome':
            kwargs['int'] += 2
            self.size = 'small'
            self.senses = ['darkvision']
            if self.subrace == 'forest':
                kwargs['dex'] += 1
            elif self.subrace == 'rock':
                kwargs['con'] += 1
        elif self.race == 'half-elf':
            kwargs['cha'] += 2
            remaining = {'str', 'dex', 'con', 'int', 'wis'}
            added = 0
            for attr in (attrs or [])[:2]:
                if attr in remaining:
                    kwargs[attr] += 1
                    remaining.remove(attr)
                    added += 1
            while added < 2:
                key = random.choice(list(remaining))
                kwargs[key] += 1
                added += 1
                remaining.remove(key)
        elif self.race == 'half-orc':
            kwargs['str'] += 2
            kwargs['con'] += 1
            self.senses = ['darkvision']
        elif self.race == 'tiefling':
            kwargs['int'] += 1
            kwargs['cha'] += 2
            self.senses = ['darkvision']
        return Stats(**kwargs)

    def _setup_stats(self, stats, attrs):
        stats = sorted(stats, reverse=True)
        kwargs = {}
        for attr in attrs:
            kwargs[attr] = stats[0]
            stats = stats[1:]
        remaining = list(
            {'str', 'dex', 'con', 'int', 'wis', 'cha'} - set(attrs)
        )
        random.shuffle(remaining)
        for key in remaining:
            kwargs[key] = stats[0]
            stats = stats[1:]
        return Stats(**kwargs)

    def __getattr__(self, attr):
        if attr in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
            return getattr(self.stats, attr)
        raise AttributeError('no attribute {!r}'.format(attr))

    def _random_appearance(self):
        pass

    def output(self):
        print(self.name)
        if self.subrace:
            racestr = '{} {}'.format(self.subrace, self.race)
        else:
            racestr = self.race
        print('{} {}'.format(racestr, self.gender))
        if self.klass:
            print('Level {} {}'.format(self.level, self.klass.title()))
        print('')
        print('HP:  {}'.format(self.hp))
        print('AC:  {}'.format(self.ac))
        print('SPD: {}'.format(self.speed))
        print('')
        print('STR: {}'.format(self.str))
        print('DEX: {}'.format(self.dex))
        print('CON: {}'.format(self.con))
        print('INT: {}'.format(self.int))
        print('WIS: {}'.format(self.wis))
        print('CHA: {}'.format(self.cha))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--class', '-c', dest='klass')
    parser.add_argument('--race', '-r', choices=('human', 'dwarf', 'elf',
                                                 'half-elf', 'half-orc',
                                                 'gnome', 'halfling'))
    parser.add_argument('--subrace', '-s')
    parser.add_argument('--gender', '-g', choices=('male', 'female'))
    parser.add_argument('--name', '-n')
    args = parser.parse_args()

    npc = NPC(klass=args.klass, race=args.race, gender=args.gender,
              name=args.name, subrace=args.subrace)
    npc.output()
