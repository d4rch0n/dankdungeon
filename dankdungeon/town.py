import os

from . import rand
from .config import Config
from .namerator import make_name_generator
from .character import NPC
from .shop import Shop
from .util import call_if

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
    'inn': 10,
}


class TownConfig(Config):
    DEFAULTS = {
        'race_freq': DEFAULT_RACE_FREQ,
        'shop_freq': DEFAULT_SHOP_FREQ,
    }

    @classmethod
    def load(cls, path):
        conf = super().load(path)
        conf['name_gen'] = call_if(make_name_generator, conf.get('names'))
        if 'names' in conf:
            del conf['names']
        return conf


class Town:

    def __init__(self, config=None):
        self.config = config
        self.npcs = []
        self.shops = []
        for _ in range(self.config['shops']['random']):
            while True:
                shop = self.make_shop()
                if self.config.get('interactive'):
                    shop.output()
                    print()
                    inp = input('Keep? [Y/n]  ')
                    if inp.lower() == 'n':
                        continue
                break
            self.shops.append(shop)

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
