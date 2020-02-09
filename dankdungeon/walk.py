import itertools
import collections

from . import config, util
from .namerator import make_name_generator
from .character import NPC


class WalkConfig(config.Config):
    DEFAULTS = {}

    @classmethod
    def load(cls, path):
        conf = super().load(path)
        conf.name_gen = util.call_if(make_name_generator, conf.get('names'))
        if 'names' in conf:
            del conf['names']
        conf.rand_race = util.race_freq_gen(conf['race_freq'])
        conf._rand_chain = {}
        for group, group_d in conf['group_chain'].items():
            if group == 'default':
                continue
            race, subrace = util.split_race(group)
            for key, val in conf['group_chain']['default'].items():
                if key not in group_d:
                    group_d[key] = val
            conf._rand_chain[race, subrace] = util.race_freq_gen(group_d)
        conf.rand_chain = lambda x, y: conf._rand_chain[x, y]()
        return conf


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c',
        help='path to YAML config',
    )
    parser.add_argument(
        '--out', '-o', default='walk_npcs',
        help='path to dump NPC verbose output, default: %(default)s',
    )
    args = parser.parse_args()
    conf = WalkConfig.load(args.config)
    npcs = []
    for i in range(100):
        race, subrace = conf.rand_race()
        npc = NPC(name_gen=conf.name_gen, race=race, subrace=subrace)
        npcs.append(npc)
    groups = collections.defaultdict(list)
    for npc1, npc2 in itertools.combinations(npcs, 2):
        race, subrace = conf.rand_chain(npc1.race, npc1.subrace)
        if npc2.race == race and npc2.subrace == subrace:
            groups[repr(npc1)].append(repr(npc2))
    for npc, friends in groups.items():
        print(f'- {npc!r}')
        for friend in friends:
            print(f'  - {friend!r}')


if __name__ == '__main__':
    main()
