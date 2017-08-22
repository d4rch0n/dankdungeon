import random
from collections import namedtuple
from .namerator import make_name


def roll_stat():
    nums = [random.randint(1, 6) for _ in range(4)]
    return sum(nums) - min(nums)


Stats = namedtuple('Stats', ['str', 'dex', 'con', 'int', 'wis', 'cha'])


class NPC:

    def __init__(self, name=None, klass=None, gender=None, race=None):
        self.gender = gender or random.choice(['male', 'female'])
        self.race = race or random.choice([
            'human', 'elf', 'half-elf', 'dwarf', 'gnome', 'half-orc',
            'halfling',
        ])
        self.name = name or make_name(self.race, gender=self.gender)
        self.klass = klass
        self.roll_stats(klass=klass)

    def roll_stats(self, klass=None):
        stats = sorted([roll_stat() for _ in range(6)], reverse=True)
        if klass is None:
            random.shuffle(stats)
            self.stats = Stats(*stats)
        elif klass == 'barbarian':
            self.stats = self._take_top_stats(stats, ('str', 'con'))
        elif klass == 'bard':
            self.stats = self._take_top_stats(stats, ('cha', 'dex'))
        elif klass == 'cleric':
            self.stats = self._take_top_stats(stats, ('wis',))
        elif klass == 'druid':
            self.stats = self._take_top_stats(stats, ('wis',))
        elif klass == 'fighter':
            self.stats = self._take_top_stats(stats, ('str', 'con'))
        elif klass == 'monk':
            self.stats = self._take_top_stats(stats, ('dex', 'wis'))
        elif klass == 'paladin':
            self.stats = self._take_top_stats(stats, ('str', 'cha'))
        elif klass == 'ranger':
            self.stats = self._take_top_stats(stats, ('dex', 'wis'))
        elif klass == 'rogue':
            self.stats = self._take_top_stats(stats, ('dex',))
        elif klass == 'sorcerer':
            self.stats = self._take_top_stats(stats, ('cha',))
        elif klass == 'warlock':
            self.stats = self._take_top_stats(stats, ('cha',))
        elif klass == 'wizard':
            self.stats = self._take_top_stats(stats, ('int',))

    def _take_top_stats(self, stats, attrs):
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

    def output(self):
        print(self.name)
        if self.klass is None:
            print('{} {}'.format(self.race, self.gender))
        else:
            print('{} {} {}'.format(self.race, self.gender, self.klass))
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
    parser.add_argument('--gender', '-g', choices=('male', 'female'))
    parser.add_argument('--name', '-n')
    args = parser.parse_args()

    npc = NPC(klass=args.klass, race=args.race, gender=args.gender,
              name=args.name)
    npc.output()
