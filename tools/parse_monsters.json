#!/usr/bin/env python3
import re
import json

RE_LAND = re.compile(r'^\d+\s+\w+')
RE_LANG_COMMON = re.compile(r'.*\bcommon\b')
RE_LANG_UNCOMMON = re.compile(r'.*\bundercommon\b')
RE_LANG_GIANT = re.compile(r'.*(giant(?:\s\w+)?)')


with open('monsters.json') as f:
    mons = json.load(f)


mons = sorted(mons, key=lambda x: (x['xp'], x['name']))


def move_tags(mon):
    spd = mon['speed'].lower()
    tags = set()
    if 'burrow' in spd:
        tags.add('burrow')
    if 'fly' in spd or 'hover' in spd:
        tags.add('fly')
    if 'swim' in spd:
        tags.add('swim')
    if RE_LAND.match(spd) or 'hover' in spd:
        tags.add('walk')
    return tags


def alignment_tags(mon):
    al = mon['alignment']
    tags = set()
    if 'lawful' in al:
        tags.add('lawful')
    if 'chaotic' in al:
        tags.add('chaotic')
    if 'good' in al:
        tags.add('good')
    if 'evil' in al:
        tags.add('evil')
    return tags


def sense_tags(mon):
    s = mon['senses']
    tags = set()
    if 'blindsight' in s:
        tags.add('blindsight')
        tags.add('cavevision')
    if 'darkvision' in s:
        tags.add('darkvision')
        tags.add('cavevision')
    if 'truesight' in s:
        tags.add('truesight')
        tags.add('cavevision')
    if 'tremorsense' in s:
        tags.add('tremorsense')
        tags.add('cavevision')
    return tags


def lang_tags(mon):
    langs = mon['languages'].strip().lower()
    tags = set()
    # giant
    # common/undercommon
    for l in ('abyssal', 'infernal', 'aquan', 'ignan', 'terran', 'auran',
              'deep speech', 'primordial', 'telepathy',
              'draconic', 'celestial', 'elvish', 'sylvan', 'druidic', 'goblin',
              'orc', 'sphinx', 'undercommon', 'gnoll', 'worg', 'gnomish',
              'thieves', 'otyugh', 'sahuagin'):
        if l in langs:
            l = '{}_lang'.format(l.replace(' ', '_'))
            tags.add(l)
    if RE_LANG_COMMON.match(langs):
        tags.add('common_lang')
    if RE_LANG_UNCOMMON.match(langs):
        tags.add('undercommon_lang')
    m = RE_LANG_GIANT.match(langs)
    if m:
        if m.group(1) == 'giant but':
            tags.add('giant')
        else:
            tags.add(m.group(1).replace(' ', '_'))
    if 'aquan' in tags:
        tags.add('water')
    if 'terran' in tags:
        tags.add('earth')
    if 'ignan' in tags:
        tags.add('fire')
    if 'auran' in tags:
        tags.add('air')
    return tags


def modify_monster(mon):
    print(mon['name'])

    tags = set()
    print('adding: {!r}'.format(mon['type']))
    tags.add(mon['type'])

    mv = move_tags(mon)
    print('adding from {!r}: {!r}'.format(mon['speed'], mv))
    tags |= mv

    atags = alignment_tags(mon)
    print('adding from {!r}: {!r}'.format(mon['alignment'], atags))
    tags |= atags

    stags = sense_tags(mon)
    print('adding from {!r}: {!r}'.format(mon['senses'], stags))
    tags |= stags

    ltags = lang_tags(mon)
    print('adding from {!r}: {!r}'.format(mon['languages'], ltags))
    tags |= ltags

    old_tags = (mon.get('attr') and set(mon['attr'])) or set()
    if old_tags:
        print('old tags were: {!r}'.format(old_tags))

    print('\ncurrent tags: {!r}'.format(tags))
    attr = input('\n{!r} , add tags: '.format(mon['name']))
    if attr.strip():
        allenvs = {'forest', 'swamp', 'jungle', 'plains', 'mountain', 'tundra',
                   'desert'}
        attr = {x.strip() for x in attr.strip().split()}
        if 'any' in attr:
            attr.remove('any')
            attr |= allenvs
        if 'anytree' in attr:
            attr.remove('anytree')
            attr |= {'forest', 'swamp', 'jungle'}
        if 'anycold' in attr:
            attr.remove('anycold')
            attr |= {'tundra', 'mountain'}
        if 'anyhot' in attr:
            attr.remove('anyhot')
            attr |= {'plains', 'desert'}
        if 'anytemp' in attr:
            attr.remove('anytemp')
            attr |= {'forest', 'plains', 'mountain'}
        for at in attr:
            if at.startswith('!'):
                attr.remove(at)
                attr -= {at[1:]}
        tags |= attr

    print('\ncurrent tags are: {!r}'.format(tags))
    attr = input('remove tags: ')
    if attr.strip():
        tags -= {x.strip() for x in attr.strip().split()}

    if 'attr' in mon:
        del mon['attr']

    mon['tags'] = sorted(tags)
    print('{!r} tags: {!r}'.format(mon['name'], mon['tags']))


try:
    for mon in mons:
        if 'tags' in mon:
            continue
        modify_monster(mon)
except KeyboardInterrupt:
    print('skipping!')
except:
    import traceback
    print(traceback.format_exc())
    print('Failed! Saving work...')


with open('monsters.json', 'w') as f:
    json.dump(mons, f, indent=4, sort_keys=True)
