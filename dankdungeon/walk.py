from . import config, template
from .character import NPC


class WalkConfig(config.Config):
    DEFAULTS = {}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c', default='./walk.yaml',
        help='path to YAML config, default: %(default)s',
    )
    parser.add_argument(
        '--out', '-o', default='walk_npcs',
        help='path to dump NPC verbose output, default: %(default)s',
    )
    args = parser.parse_args()
    conf = WalkConfig.load(args.config)
    for i in range(100):
        race, subrace = conf.rand_race()
        npc = NPC(name_gen=conf.name_gen, race=race, subrace=subrace)
        print(template.render('npc.oneline', obj=npc))


if __name__ == '__main__':
    main()
