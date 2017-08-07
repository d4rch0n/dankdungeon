import re
import json

RE_LAND = re.compile(r'^\d+\s+\w+')
RE_LANG_COMMON = re.compile(r'.*\bcommon\b')
RE_LANG_UNCOMMON = re.compile(r'.*\bundercommon\b')
RE_LANG_GIANT = re.compile(r'.*(giant(?:\s\w+)?)')


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


with open('monsters.json') as f:
    mons = json.load(f)


for mon in mons:
    if 'tags' not in mon:
        continue
    ltags = lang_tags(mon)
    if ltags:
        print('should add these to {!r}? {!r}'.format(mon['name'], ltags))
        y = input('(Y|n) ').strip().lower()
        if y == 'n':
            continue
        else:
            mon['tags'] = sorted(set(mon['tags']) | ltags)


with open('monsters.json', 'w') as f:
    json.dump(mons, f, indent=4, sort_keys=True)
