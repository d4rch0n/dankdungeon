import os
import json
from dankdungeon import Monster

ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dankdungeon')
DATADIR = os.path.join(ROOT, 'data')
MONSTERS_PATH = os.path.join(DATADIR, 'monsters.json')

tags_path = os.path.join(DATADIR, 'tags.json')
tag_groups_path = os.path.join(DATADIR, 'tag_groups.json')
type_groups_path = os.path.join(DATADIR, 'type_groups.json')
subtype_groups_path = os.path.join(DATADIR, 'subtype_groups.json')
related_path = os.path.join(DATADIR, 'related.json')

with open(MONSTERS_PATH) as f:
    monster_data = json.load(f)
monsters = [Monster(x) for x in monster_data]

tags = set()
for mon in monsters:
    tags |= mon.tags
with open(tags_path, 'w') as f:
    json.dump(sorted(tags), f)

tag_groups = {}
for tag in tags:
    arr = []
    for mon in monsters:
        if mon.tags & {tag}:
            arr.append(mon.name.strip().lower())
    tag_groups[tag] = arr
with open(tag_groups_path, 'w') as f:
    json.dump(tag_groups, f)

type_groups = {}
for mon in sorted(monsters, key=lambda x: x.name):
    typ = mon.type
    if typ not in type_groups:
        type_groups[typ] = []
    type_groups[typ].append(mon.name.strip().lower())
with open(type_groups_path, 'w') as f:
    json.dump(type_groups, f)

subtype_groups = {}
for mon in sorted(monsters, key=lambda x: x.name):
    if mon.type not in subtype_groups:
        subtype_groups[mon.type] = {}
    typ = mon.subtype or None
    if typ not in subtype_groups[mon.type]:
        subtype_groups[mon.type][typ] = []
    subtype_groups[mon.type][typ].append(mon.name.strip().lower())

with open(subtype_groups_path, 'w') as f:
    json.dump(subtype_groups, f)

print('calculating related...')
related = {}
for mon in monsters:
    arr = []
    for mon2 in monsters:
        diff = mon - mon2
        if diff > 1.0:
            arr.append((diff, mon2))
    arr = sorted(arr, reverse=True, key=lambda x: (x[0], x[1].name))
    arr = [v.name.strip().lower() for k, v in arr]
    related[mon.name.strip().lower()] = arr
with open(related_path, 'w') as f:
    json.dump(related, f)
print('done!')
