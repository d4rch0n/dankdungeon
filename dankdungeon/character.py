import re
import math
import yaml
import random
import argparse
from collections import namedtuple, Counter
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

RE_ROLL = re.compile(
    r'^(?P<num>\d+)d(?P<sides>\d+)\s*(?:(?P<sign>[+-])\s*(?P<plus>\d+))?$'
)


Stats = namedtuple('Stats', ['str', 'dex', 'con', 'int', 'wis', 'cha'])


def modifier(stat):
    return math.floor((stat - 10) / 2)


def roll(s):
    if isinstance(s, int):
        return s
    m = RE_ROLL.match(s)
    if not m:
        if s.isdigit():
            return int(s)
        raise ValueError('not a valid roll string (eg "2d8+2"): {!r}'.format(s))
    if m.group('sign') is not None:
        s = int('{}{}'.format(m.group('sign'), m.group('plus')))
    else:
        s = 0
    for _ in range(int(m.group('num'))):
        s += random.randint(1, int(m.group('sides')))
    return s


class Warrior:

    def roll_initiative(self):
        self.initiative = roll('1d20') + modifier(self.dex)

    def roll_attack(self, enemy_ac):
        d20 = roll('1d20') + self.attack
        return d20 >= enemy_ac

    def roll_damage(self):
        return roll(self.damage)

    def is_dead(self):
        return self.current_hp <= 0

    def reset(self):
        self.current_hp = self.hp


class NPC(Warrior):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.load(f)
        players = []
        for p in data['players']:
            players.append(cls(**p))
        return players

    def __init__(self, name=None, klass=None, gender=None, race=None,
                 subrace=None, stats=None, level=1, hp=None, ac=10,
                 damage=None, attack=None):
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
            self._add_racial_stats(attrs=attrs)
        self.level = level
        self.ac = ac
        self.hp = hp or self._calc_hp()
        self.current_hp = self.hp
        self.damage = damage
        self.attack = attack

    def _random_subrace(self):
        if self.race in VALID_SUBRACES:
            self.subrace = random.choice(VALID_SUBRACES[self.race])

    def _calc_hp(self):
        base = HIT_DICE[self.klass]
        auto = (base / 2) + 1
        mod = modifier(self.con)
        hp = base + mod
        if (self.race, self.subrace) == ('dwarf', 'hill'):
            hp += 1
        for _ in range(1, self.level):
            hp += auto + mod
            if (self.race, self.subrace) == ('dwarf', 'hill'):
                hp += 1
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


class MonsterEntity(Warrior):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.load(f)
        monsters = []
        for m in data:
            for i in range(m['num']):
                mon = cls(**m)
                mon.name = '{}{}'.format(mon.race, i + 1)
                monsters.append(mon)
        return monsters

    def __init__(self, **data):
        self.race = data['name']
        self.stats = Stats(**data['stats'])
        self.hp = roll(data['hp'])
        self.current_hp = self.hp
        self.ac = data['ac']
        self.damage = data['damage']
        self.attack = data['attack']

    def __getattr__(self, attr):
        if attr in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
            return getattr(self.stats, attr)
        raise AttributeError('no attribute {!r}'.format(attr))


class TestEncounter:

    def __init__(self, players_path, encounter_path):
        self.players = NPC.load(players_path)
        self.monsters = MonsterEntity.load(encounter_path)
        with open(encounter_path) as f:
            self.monster_data = yaml.load(f)

    def alive_players(self):
        return [x for x in self.players if not x.is_dead()]

    def alive_monsters(self):
        return [x for x in self.monsters if not x.is_dead()]

    def dead_players(self):
        return [x for x in self.players if x.is_dead()]

    def dead_monsters(self):
        return [x for x in self.monsters if x.is_dead()]

    def reset(self):
        for i in self.players + self.monsters:
            i.reset()

    def run(self):
        for i in self.players:
            i.roll_initiative()
        for m in self.monster_data:
            init = roll('1d20') + modifier(m['stats']['dex'])
            for mon in self.monsters:
                if m['name'] == mon.race:
                    mon.initiative = init
        order = sorted(self.players + self.monsters, key=lambda x: x.initiative,
                       reverse=True)
        while bool(self.alive_players()) and bool(self.alive_monsters()):
            for o in order:
                if not self.alive_players():
                    break
                if not self.alive_monsters():
                    break
                if o.is_dead():
                    continue
                if isinstance(o, NPC):
                    enemy = random.choice(self.alive_monsters())
                elif isinstance(o, MonsterEntity):
                    enemy = random.choice(self.alive_players())
                if not o.roll_attack(enemy.ac):
                    continue
                dmg = o.roll_damage()
                enemy.current_hp -= dmg

    def run_many(self, ct):
        c = Counter()
        for _ in range(ct):
            self.reset()
            self.run()
            c.update([
                x.name for x in
                self.dead_players() + self.dead_monsters()
            ])
        for ent, total in c.most_common():
            print('{} died {:.3%} of the time out of {} simulations'.format(
                ent, total / ct, ct,
            ))


def main_simulate():
    parser = argparse.ArgumentParser()
    parser.add_argument('players_yml')
    parser.add_argument('encounter_yml')
    parser.add_argument('--count', '-c', type=int, default=100)
    args = parser.parse_args()
    enc = TestEncounter(args.players_yml, args.encounter_yml)
    enc.run_many(args.count)


def main_npc():
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


def main_roll():
    import sys
    s = ' '.join(sys.argv[1:])
    r = roll(s)
    print(r)
