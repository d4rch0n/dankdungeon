import yaml
import random

from .namerator import make_name_generator
from .character import NPC
from .rand import rand_freqs

DEFAULT_RACE_RATIO = {
    'human': 85,
    'elf': 5,
    'dwarf': 5,
    'half-elf': 2,
    'half-orc': 1,
    'gnome': 1,
    'halfling': 1,
}


def call_if(func, val):
    """
    Return None if falsey, or func(val).
    """
    return (val or None) and func(val)


def make_shop_name(owner_name=None, house=None, goods=None):
    fmts = [
        '{owner_name}\'s {house} of {goods}',
        '{owner_name}\'s {house}',
        '{house} of {goods}',
        '{adj} {house} of {goods}',
        '{adj} {goods}',
        'the {adj} {house}',
        '{goods}',
    ]
    if owner_name:
        fmt = random.choice(fmts)
    else:
        fmt = random.choice([x for x in fmts if '{owner_name}' not in x])
    house = house or random.choice([
        'house', 'shop', 'den', 'outlet', 'store', 'boutique', 'market',
        'establishment', 'warehouse', 'stall', 'mart', 'booth', 'shed',
        'trading post', 'bargain house', 'club', 'reseller',
    ])


class Shop:

    def __init__(
        self,
        owner=None, name=None, npcs=None, rand_npc=None, npc_kwargs=None,
    ):
        if owner is None:
            self.owner = NPC(**npc_kwargs)
        elif owner is False:
            self.owner = None
        else:
            self.owner = owner


class TownConfig(dict):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        defaults = {
            'races': DEFAULT_RACE_RATIO.copy(),
        }
        for key, default in defaults.items():
            data[key] = data.get(key, default)
        data['name_gen'] = call_if(make_name_generator, data.get('names'))
        for del_key in ['names']:
            if del_key in data:
                del data[del_key]
        return cls(**data)


class Town:

    def __init__(self, config=None):
        self.config = config
        self.npcs = [self.make_npc() for _ in range(10)]

    def make_npc(self):
        race = rand_freqs(self.config['races'])
        subrace = None
        if race == 'human' and self.config['human_subraces']:
            subrace = rand_freqs(self.config['human_subraces'])
        return NPC(
            name_gen=self.config['name_gen'],
            race=race,
            subrace=subrace,
        )

    def output(self):
        print(repr(self.config))
        for n in self.npcs:
            n.output()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c', help='path to YAML config for town generation',
    )
    args = parser.parse_args()
    config = TownConfig.load(args.config)
    town = Town(config=config)
    town.output()


if __name__ == '__main__':
    main()
