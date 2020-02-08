import os
import random

from . import rand, template
from .character import NPC

'''
class ShopType(Enum):
    tavern = 'tavern'
    inn = 'inn'
    bakery = 'bakery'
    carpenter = 'carpenter'
    butcher = 'butcher'
    blacksmith = 'blacksmith'
    bronzesmith = 'bronzesmith'
    fletcher = 'fletcher'
    bowyer = 'bowyer'
    potter = 'potter'
    cooper = 'cooper'
'''


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


class Shop:
    SHOP_TYPES = {}

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
        npc_kwargs = npc_kwargs or {}
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
        fn = f'{self.shop_type}_{template.to_filename(self.name)}.txt'
        path = os.path.join(out_dir, fn)
        template.dump('shop.txt', path, obj=self)
        return path

    @classmethod
    def register(cls, name):
        def decorator(klass):
            cls.SHOP_TYPES[name] = klass
            return klass
        return decorator

    @classmethod
    def rand(cls, shop_type, name=None, **kwargs):
        klass = cls.SHOP_TYPES[shop_type]
        owner = kwargs.get('owner') or NPC(**(kwargs.get('npc_kwargs') or {}))
        name = name or klass.rand_name(owner.name)
        kwargs['name'] = name
        kwargs['owner'] = owner
        kwargs['shop_type'] = shop_type
        return klass(**kwargs)


@Shop.register('tavern')
class TavernShop(Shop):

    @classmethod
    def rand_name(self, owner_name):
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


@Shop.register('inn')
class InnShop(Shop):

    @classmethod
    def rand_name(self, owner_name):
        house = random.choice([
            'inn', 'hotel', 'lodge', 'guest house', 'boarding house',
            'bed and breakfast',
        ])
        if rand.uflip():
            return rand.rand_adj_noun_inn(suffix=house)
        else:
            return make_shop_name(owner_name=owner_name, house=house)


@Shop.register('bakery')
class BakeryShop(Shop):

    @classmethod
    def rand_name(self, owner_name):
        goods = random.choice([
            'breads', 'cakes', 'rolls', 'sweetrolls',
            'cookies', 'baked goods', 'buns', 'muffins',
        ])
        house = random.choice([
            'bakery', 'house', 'den', 'shop', 'shed', 'kitchen',
            'bakehouse', 'cookhouse', 'cookery',
        ])
        return make_shop_name(
            goods=goods,
            owner_name=owner_name,
            house=house,
        )
