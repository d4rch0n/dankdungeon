from . import config, template, rand
from .character import NPC


class WalkConfig(config.Config):
    DEFAULTS = {}


def walk(conf):
    event = rand.rand_freqs(conf['walk'])
    if event == 'hawk':
        size = 1
    elif event == 'preach':
        size = rand.randint(1, 3)
    else:
        size = rand.randint(1, 5)
    text = []
    for _ in range(size):
        race, subrace = conf.rand_race()
        npc = NPC(name_gen=conf.name_gen, race=race, subrace=subrace)
        text.append(template.render('npc.short', obj=npc))
    print(f'Event: {event}\n')
    for t in text:
        print(t)
        print()


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
    walk(conf)


if __name__ == '__main__':
    main()
