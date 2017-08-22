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

Stats = namedtuple('Stats', ['str', 'dex', 'con', 'int', 'wis', 'cha'])


class NPC:

    def __init__(self, name=None, klass=None, gender=None, race=None,
                 subrace=None):
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
        self.roll_stats(klass=klass)

    def _random_subrace(self):
        if self.race in VALID_SUBRACES:
            self.subrace = random.choice(VALID_SUBRACES[self.race])

    def roll_stats(self, klass=None):
        stats = sorted([roll_stat() for _ in range(6)], reverse=True)
        if klass is None:
            random.shuffle(stats)
            self.stats = Stats(*stats)
        elif klass == 'barbarian':
            self.stats = self._setup_stats(stats, ('str', 'con'))
        elif klass == 'bard':
            self.stats = self._setup_stats(stats, ('cha', 'dex'))
        elif klass == 'cleric':
            self.stats = self._setup_stats(stats, ('wis',))
        elif klass == 'druid':
            self.stats = self._setup_stats(stats, ('wis',))
        elif klass == 'fighter':
            self.stats = self._setup_stats(stats, ('str', 'con'))
        elif klass == 'monk':
            self.stats = self._setup_stats(stats, ('dex', 'wis'))
        elif klass == 'paladin':
            self.stats = self._setup_stats(stats, ('str', 'cha'))
        elif klass == 'ranger':
            self.stats = self._setup_stats(stats, ('dex', 'wis'))
        elif klass == 'rogue':
            self.stats = self._setup_stats(stats, ('dex',))
        elif klass == 'sorcerer':
            self.stats = self._setup_stats(stats, ('cha',))
        elif klass == 'warlock':
            self.stats = self._setup_stats(stats, ('cha',))
        elif klass == 'wizard':
            self.stats = self._setup_stats(stats, ('int',))

    def _setup_stats(self, stats, attrs):
        stats = sorted(stats, reverse=True)
        self.speed = 30
        self.size = 'medium'
        self.senses = []
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
            elif self.subrace == 'dark':
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
            for attr in attrs[:2]:
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

    def __getattr__(self, attr):
        if attr in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
            return getattr(self.stats, attr)
        raise AttributeError('no attribute {!r}'.format(attr))

    def output(self):
        print(self.name)
        if self.subrace:
            racestr = '{} {}'.format(self.subrace, self.race)
        else:
            racestr = self.race
        if self.klass is None:
            print('{} {}'.format(racestr, self.gender))
        else:
            print('{} {} {}'.format(racestr, self.gender, self.klass))
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
