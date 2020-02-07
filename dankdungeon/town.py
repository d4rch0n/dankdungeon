import random

import yaml

from . import rand
from .namerator import make_name_generator
from .character import NPC

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


def make_goods_shop_name(goods, owner_name=None, house=None):
    fmts = {
        '{owner_name}\'s {house} of {goods}': 20,
        '{owner_name}\'s {house}': 20,
        '{house} of {goods}': 15,
        '{adj} {house} of {goods}': 15,
        'the {adj} {house}': 15,
        '{adj} {goods}': 10,
        '{goods}': 5,
    }
    if owner_name:
        fmt = rand.rand_freqs(fmts)
    else:
        fmt = rand.rand_freqs({
            k: v for k, v in fmts.items()
            if '{owner_name}' not in k
        })
    house = house or rand.rand_goods_shop_house()
    adj = rand.rand_goods_shop_adj()
    return fmt.format(
        owner_name=owner_name, house=house, adj=adj, goods=goods,
    ).title().replace("'S", "'s")


def rand_tavern_name(owner_name=None):
    r = random.randint(1, 2)
    if r == 1:
        return rand.rand_inn_name()
    elif r == 2:
        booze = rand.rand_freqs({
            'ale': 15,
            'wine': 10,
            'mead': 10,
            'whiskey': 5,
            'rum': 5,
            'vodka': 5,
            'gin': 5,
            'brandy': 3,
            'liquor': 3,
            'booze': 3,
            'beer': 2,
            'hops': 1,
        })
        return make_goods_shop_name(booze, owner_name=owner_name)


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
        self.name = name
        self.npcs = npcs or []
        self.npcs.extend(NPC(**npc_kwargs) for _ in range(rand_npc or 0))

    def output(self):
        print(f'Name\n====\n{self.name}')
        if self.owner:
            print('Owner\n=====')
            self.owner.output()
        if self.npcs:
            print('NPCS\n====')
            for npc in self.npcs:
                npc.output()
                print()

    @classmethod
    def rand_tavern(cls, name=None, **kwargs):
        owner = kwargs.get('owner') or NPC(**(kwargs.get('npc_kwargs') or {}))
        name = name or rand_tavern_name(owner_name=owner.name)
        kwargs['name'] = name
        kwargs['owner'] = owner
        return cls(**kwargs)


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
        race = rand.rand_freqs(self.config['races'])
        subrace = None
        if race == 'human' and self.config['human_subraces']:
            subrace = rand.rand_freqs(self.config['human_subraces'])
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
