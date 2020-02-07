import yaml

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


class TownConfig(dict):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        new = cls(
            races=data.get('races') or DEFAULT_RACE_RATIO.copy(),
            name_gen=data.get('names') and make_name_generator(data['names']),
            human_subraces=data.get('human_subraces')
        )
        return new


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
