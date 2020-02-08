import os
import random
from enum import Enum

import yaml

from . import rand, template
from .namerator import make_name_generator
from .character import NPC

DEFAULT_RACE_FREQ = {
    'human': 85,
    'elf': 5,
    'dwarf': 5,
    'half-elf': 2,
    'half-orc': 1,
    'gnome': 1,
    'halfling': 1,
}

DEFAULT_SHOP_FREQ = {
    'tavern': 10,
    'goods': 10,
    'inn': 10,
}


def call_if(func, val):
    """
    Return None if falsey, or func(val).
    """
    return (val or None) and func(val)


def make_shop_name(goods=None, owner_name=None, house=None):
    fmts = {
        '{owner_name}\'s {house} of {goods}': 20,
        '{owner_name}\'s {house}': 20,
        '{house} of {goods}': 15,
        '{adj} {house} of {goods}': 15,
        'the {adj} {house}': 15,
        '{adj} {goods}': 10,
        '{goods}': 5,
    }
    if not owner_name:
        fmts = {k: v for k, v in fmts.items() if '{owner_name}' not in k}
    if not goods:
        fmts = {k: v for k, v in fmts.items() if '{goods}' not in k}
    fmt = rand.rand_freqs(fmts)
    house = house or rand.rand_goods_shop_house()
    adj = rand.rand_goods_shop_adj()
    return fmt.format(
        owner_name=owner_name, house=house, adj=adj, goods=goods,
    ).title().replace("'S", "'s")


def rand_tavern_name(owner_name=None):
    if rand.uflip():
        suffix = random.choice([
            'tavern', 'alehouse', 'taproom', 'bar', 'pub', 'parlor',
            'taphouse', 'drinkroom',
        ])
        return rand.rand_adj_noun_inn(suffix=suffix)
    else:
        booze = rand.rand_freqs({
            'ale': 15,
            'wine': 10,
            'mead': 10,
            'whiskey': 5,
            'rum': 5,
            'vodka': 5,
            'gin': 5,
            None: 5,
            'brandy': 3,
            'liquor': 3,
            'booze': 3,
            'beer': 2,
            'hops': 1,
        })
        return make_shop_name(goods=booze, owner_name=owner_name)


def rand_inn_name(owner_name=None):
    house = random.choice([
        'inn', 'hotel', 'lodge', 'guest house', 'boarding house',
        'bed and breakfast',
    ])
    if rand.uflip():
        return rand.rand_adj_noun_inn(suffix=house)
    else:
        return make_shop_name(owner_name=owner_name, house=house)


class ShopType(Enum):
    tavern = 'tavern'
    inn = 'inn'


class Shop:

    def __init__(
        self,
        owner=None, name=None, npcs=None, rand_npc=None, npc_kwargs=None,
        shop_type=None,
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
        self.shop_type = shop_type

    def output(self):
        print(f'Name\n====\n{self.name}\n')
        if self.owner:
            print('Owner\n=====')
            self.owner.output()
            print()
        if self.npcs:
            print('NPCs\n====')
            for npc in self.npcs:
                npc.output()
                print()

    def dump(self, out_dir):
        fn = f'{self.shop_type.value}_{template.to_filename(self.name)}.txt'
        path = os.path.join(out_dir, fn)
        template.dump('shop.txt', path, obj=self)
        return path

    @classmethod
    def rand(cls, shop_type, **kwargs):
        if isinstance(shop_type, str):
            shop_type = ShopType[shop_type]
        if shop_type is ShopType.tavern:
            return cls.rand_tavern(**kwargs)
        elif shop_type is ShopType.inn:
            return cls.rand_tavern(**kwargs)
        else:
            raise ValueError(f'cant instanciate {shop_type!r}')

    @classmethod
    def rand_tavern(cls, name=None, **kwargs):
        owner = kwargs.get('owner') or NPC(**(kwargs.get('npc_kwargs') or {}))
        name = name or rand_tavern_name(owner_name=owner.name)
        kwargs['name'] = name
        kwargs['owner'] = owner
        kwargs['shop_type'] = ShopType.tavern
        return cls(**kwargs)

    @classmethod
    def rand_inn(cls, name=None, **kwargs):
        owner = kwargs.get('owner') or NPC(**(kwargs.get('npc_kwargs') or {}))
        name = name or rand_inn_name(owner_name=owner.name)
        kwargs['name'] = name
        kwargs['owner'] = owner
        kwargs['shop_type'] = ShopType.inn
        return cls(**kwargs)


class TownConfig(dict):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        defaults = {
            'race_freq': DEFAULT_RACE_FREQ.copy(),
            'shop_freq': DEFAULT_SHOP_FREQ.copy(),
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
        self.npcs = []
        self.shops = []
        for _ in range(self.config['shops']['random']):
            self.shops.append(self.make_shop())

    def make_npc(self):
        race = rand.rand_freqs(self.config['race_freq'])
        subrace = None
        if race == 'human' and self.config['human_subrace_freq']:
            subrace = rand.rand_freqs(self.config['human_subrace_freq'])
        return NPC(
            name_gen=self.config['name_gen'],
            race=race,
            subrace=subrace,
        )

    def make_shop(self):
        shop_type = rand.rand_freqs(self.config['shop_freq'])
        owner = self.make_npc()
        return Shop.rand(shop_type, owner=owner)

    def output(self):
        print('*** SHOPS ***')
        for shop in self.shops:
            shop.output()
            print()
        print('*** NPCs ***')
        for npc in self.npcs:
            npc.output()
            print()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c', help='path to YAML config for town generation',
    )
    parser.add_argument(
        '--out', '-o', default='./town',
        help='path to dump town data',
    )
    args = parser.parse_args()
    config = TownConfig.load(args.config)
    town = Town(config=config)
    town.output()
    if not os.path.exists(args.out):
        os.makedirs(args.out)
    for shop in town.shops:
        path = shop.dump(args.out)
        print(f'dumped to {path}')


if __name__ == '__main__':
    main()
