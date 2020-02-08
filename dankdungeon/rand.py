import re
import random

from .namerator import NAMES

RE_ROLL = re.compile(
    r'^(?P<num>\d+)d(?P<sides>\d+)\s*(?:(?P<sign>[+-])\s*(?P<plus>\d+))?$'
)


def roll(s):
    if isinstance(s, int):
        return s
    m = RE_ROLL.match(s)
    if not m:
        if s.isdigit():
            return int(s)
        raise ValueError(
            'not a valid roll string (eg "2d8+2"): {!r}'.format(s)
        )
    if m.group('sign') is not None:
        s = int('{}{}'.format(m.group('sign'), m.group('plus')))
    else:
        s = 0
    for _ in range(int(m.group('num'))):
        s += random.randint(1, int(m.group('sides')))
    return s


def rand_freqs(d):
    total = sum(d.values())
    sort = sorted(d.items(), key=lambda x: x[1], reverse=True)
    totaled_freq = []
    rolling_total = 0
    for key, prob in sort:
        rolling_total += prob
        totaled_freq.append((key, rolling_total))
    rnd = random.randint(1, total)
    for key, prob in totaled_freq:
        if rnd <= prob:
            return key
    raise ValueError(
        f'{rnd} cant be <= to any of: {totaled_freq!r} from input {d!r}'
    )


def rand_goods_shop_adj():
    return random.choice([
        'happy', 'glorious', 'mysterious', 'tantalizing', 'fine', 'superior',
        'quality', 'excellent', 'superb', 'outstanding', 'magnificent',
        'exceptional', 'marvelous', 'wonderful', 'splendid', 'worthy',
        'sterling', 'super', 'great', 'terrific', 'fantastic', 'awesome',
        'jolly', 'radiant', 'peculiar', 'strange', 'weird', 'bizarre',
        'mystifying', 'inexplicable', 'unexplainable', 'secret', 'mystical',
    ])


def rand_goods_shop_house():
    return random.choice([
        'house', 'shop', 'den', 'outlet', 'store', 'boutique', 'market',
        'establishment', 'warehouse', 'stall', 'mart', 'booth', 'shed',
        'trading post', 'bargain house', 'club',
    ])


def rand_animal_name():
    return random.choice(NAMES['animals'])


def rand_item_name():
    return random.choice(NAMES['items'])


def rand_adj():
    return random.choice(NAMES['adjs'])


def uflip():
    return random.uniform(0, 1) <= 0.5


def rand_adj_noun_inn(suffix='inn'):
    name = ''
    if uflip():
        name = 'the '
    name += random.choice([
        f'{rand_adj()} {rand_animal_name()}',
        f'{rand_adj()} {rand_item_name()}',
    ])
    if uflip():
        name = f'{name} {suffix}'
    return name.title()
