import os
import sys
import json
import random
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


def csv_set(s):
    if not s:
        return None
    if isinstance(s, (list, tuple, set)):
        return set(s)
    if isinstance(s, str):
        return {x.strip().lower() for x in s.split(',')}
    raise ValueError('bad type for splitting on comma: {!r}'.format(s))


class Monster:
    MONSTERS = []
    TAG_GROUPS = {}
    TYPE_GROUPS = {}
    SUBTYPE_GROUPS = {}
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
        return set(self.data['tags']) | {self.name.strip().lower()}

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
        for mon in sorted(cls.MONSTERS, key=lambda x: x.name):
            typ = mon.type
            if typ not in cls.TYPE_GROUPS:
                cls.TYPE_GROUPS[typ] = []
            cls.TYPE_GROUPS[typ].append(mon)
        for mon in sorted(cls.MONSTERS, key=lambda x: x.name):
            if mon.subtype:
                typ = (mon.type, mon.subtype)
            else:
                typ = (mon.type, None)
            if typ not in cls.SUBTYPE_GROUPS:
                cls.SUBTYPE_GROUPS[typ] = []
            cls.SUBTYPE_GROUPS[typ].append(mon)
        cls.MONSTER_D = {m.name.lower().strip(): m for m in cls.MONSTERS}

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

    @staticmethod
    def select_and(grp1, grp2):
        return [x for x in grp1 if x in grp2]

    @staticmethod
    def select_or(grp1, grp2):
        g1 = [x for x in grp1 if x not in grp2]
        g2 = [x for x in grp2 if x not in grp1]
        return g1 + g2

    @classmethod
    def random_encounter(cls, min_xp, max_xp, or_tags=None, and_tags=None,
                         not_tags=None):
        mons = cls.find(or_tags=or_tags, and_tags=and_tags, not_tags=not_tags)
        if not mons:
            raise ValueError('filters too restrictive! no monsters found')
        mons = [x for x in mons if x.xp <= max_xp]
        if not mons:
            raise ValueError('none of these monsters are <= max xp threshold')
        mon = random.choice(mons)
        enc = [[1, mon]]

        def total_xp():
            nonlocal enc
            xp = 0
            c = 0
            for ct, mon in enc:
                xp += ct * mon.xp
                c += ct
            xp *= scale_enc(c)
            return xp

        rel = cls.select_and(mon.related(), mons)
        variety = random.randint(1, 3)

        if not rel or variety == 1:
            while total_xp() < min_xp:
                enc[0][0] += 1
            if total_xp() > max_xp:
                enc[0][0] -= 1
            return enc, total_xp()

        rel = list(set(rel) - {mon})
        if variety >= 2 and rel:
            other = random.choice(rel)
            enc.append([1, other])
            if total_xp() > max_xp:
                enc = enc[:-1]
            rel = list(set(rel) - {other})

        if variety >= 3 and rel:
            other = random.choice(rel)
            enc.append([1, other])
            if total_xp() > max_xp:
                enc = enc[:-1]
            rel = list(set(rel) - {other})

        while total_xp() < min_xp:
            random.shuffle(enc)
            for lst in enc:
                lst[0] += 1
                if total_xp() > max_xp:
                    lst[0] -= 1
                    continue
                else:
                    break
        return enc, total_xp()

    @classmethod
    def find(cls, or_tags=None, and_tags=None, not_tags=None):
        or_tags = csv_set(or_tags)
        and_tags = csv_set(and_tags)
        not_tags = csv_set(not_tags)
        mons = cls.MONSTERS[:]
        if or_tags is not None:
            mons = [x for x in mons if x.tags & or_tags]
        if and_tags is not None:
            mons = [x for x in mons if x.tags & and_tags == and_tags]
        if not_tags is not None:
            mons = [x for x in mons if not bool(x.tags & not_tags)]
        return mons

    def short_output(self):
        print('{} ({}{}) XP: {} CR: {}'.format(
            self.name, self.type, ' ' + self.subtype if self.subtype else '',
            self.xp, self.challenge_rating))
        print('AC: {} HP: {} ({})'.format(self.armor_class, self.hit_points,
                                          self.hit_dice))
        print('STR: {} DEX: {} CON: {} INT: {} WIS: {} CHA: {}'.format(
            self.strength, self.dexterity, self.constitution, self.intelligence,
            self.wisdom, self.charisma))
        print('Size: {}'.format(self.size))
        print('Speed: {}'.format(self.speed))
        print('Senses: {}'.format(self.senses))
        print('Immune: {}'.format(self.damage_immunities or 'none'))
        print('Cond.Immune: {}'.format(self.condition_immunities or 'none'))
        print('Resist: {}'.format(self.damage_resistances or 'none'))
        print('Vulnerable: {}'.format(self.damage_vulnerabilities or 'none'))
        print('Langs: {}'.format(self.languages))
        if 'actions' in self.data:
            for act in self.actions:
                print('Action "{act[name]}": {act[desc]}'.format(act=act))
        if 'special_abilities' in self.data:
            for abi in self.special_abilities:
                print('Ability "{abi[name]}": {abi[desc]}'.format(abi=abi))

    def output(self):
        print(self.name)
        for x in (
            'name',
            'challenge rating',
            'xp',
            'type',
            'subtype',
            'alignment',
            'size',
            'hit points',
            'hit dice',
            'armor class',
            'speed',
            'senses',
            'languages'
            'damage immunities',
            'damage resistances',
            'damage vulnerabilities',
            'condition immunities',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
        ):
            if x not in self.data:
                continue
            print('{}: {}'.format(x.title(), self.data[x]))
        print('Tags: {}'.format(', '.join(self.tags)))
        if self.subtype:
            print('Same Subtype: {}'.format(', '.join([
                x.name for x in self.same_subtype()
            ])))
        print('Same Type: {}'.format(', '.join([
            x.name for x in self.same_type()
        ])))
        print('Related: {}'.format(', '.join([
            x.name for x in self.related()[:10]
        ])))
        if 'actions' in self.data:
            print('\nActions:')
            for act in self.actions:
                print('  ' + act['name'])
                print('    ' + act['desc'])
        if 'special_abilities' in self.data:
            print('\nSpecial Abilities:')
            for act in self.special_abilities:
                print('  ' + act['name'])
                print('    ' + act['desc'])

    def same_type(self):
        return self.TYPE_GROUPS[self.type]

    def same_subtype(self):
        return self.SUBTYPE_GROUPS[(self.type, self.subtype or None)]


def calc_threshold(player_levels):
    thresh = [0, 0, 0, 0, 0]
    for lvl in player_levels:
        for i in range(4):
            thresh[i] += XP_THRESH[lvl][i]
    # make deadly span between itself and a new number, 1.5 times diff between
    # the hard and deadly difficulty difference
    d = thresh[3] - thresh[2]
    thresh[4] = int(thresh[3] + (1.5 * d))
    return thresh


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')
    p = subs.add_parser('monster')
    p.add_argument('name', help='select a monster by name')
    p.add_argument('--short', '-s', action='store_true',
                   help='print short stats')

    p = subs.add_parser('encounter')
    p.add_argument('--players', '-p', help='the player levels, default 1,1,1,1')
    p.add_argument('--difficulty', '-d', default='medium',
                   choices=('easy', 'medium', 'hard', 'deadly'))
    p.add_argument('--and', '-A', dest='and_tags',
                   help='require monsters have all of these, '
                   'eg: underdark,undercommon_lang')
    p.add_argument('--or', '-O', dest='or_tags',
                   help='only include monsters with one or more, eg: '
                   'dragon,reptile')
    p.add_argument('--not', '-N', dest='not_tags',
                   help='exclude monsters with one of these, eg: undead,fire')

    args = parser.parse_args()

    if args.cmd == 'encounter':
        Monster.load()
        if args.players:
            players = [int(x.strip()) for x in args.players.split(',')]
        else:
            players = [1, 1, 1, 1]
        thresh = calc_threshold(players)
        diff = {'easy': 0, 'medium': 1, 'hard': 2, 'deadly': 3}[args.difficulty]
        thresh = (thresh[diff], thresh[diff + 1])
        try:
            enc, xp = Monster.random_encounter(
                thresh[0],
                thresh[1],
                or_tags=args.or_tags,
                and_tags=args.and_tags,
                not_tags=args.not_tags,
            )
        except ValueError as e:
            sys.exit(str(e))
        print('XP={} ({} <= xp <= {}):'.format(xp, *thresh))
        for ct, mon in enc:
            print(' - {} {!r}'.format(ct, mon))
        print('')
        for ct, mon in enc:
            mon.short_output()
            print('')
    elif args.cmd == 'monster':
        Monster.load()
        mon = Monster.get(args.name)
        if not mon:
            sys.exit('cant find this monster')
        if args.short:
            mon.short_output()
        else:
            mon.output()
    else:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
