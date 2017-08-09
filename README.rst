dankdungeon
===========

generate monster encounters and look up stats

Credit for JSON monsters goes mainly to::

    https://www.reddit.com/r/dndnext/comments/43a09o/srd_monsters_in_json_format/

I added tags, but all the monster data is otherwise from there, created by reddit user droiddruid.


Installation
------------

From the project root directory::

    $ python setup.py install

Or from pip::

	$ pip install dankdungeon


Usage
-----

Use --help/-h to view info on the arguments::

	$ dankdungeon -h
	usage: dankdungeon [-h] {monster,encounter} ...

	positional arguments:
	  {monster,encounter}

	optional arguments:
	  -h, --help           show this help message and exit


	$ dankdungeon monster -h
	usage: dankdungeon monster [-h] name

	positional arguments:
	  name        select a monster by name

	optional arguments:
	  -h, --help  show this help message and exit


	$ dankdungeon encounter -h
	usage: dankdungeon encounter [-h] [--players PLAYERS]
								 [--difficulty {easy,medium,hard,deadly}]
								 [--and AND_TAGS] [--or OR_TAGS] [--not NOT_TAGS]

	optional arguments:
	  -h, --help            show this help message and exit
	  --players PLAYERS, -p PLAYERS
							the player levels, default 1,1,1,1
	  --difficulty {easy,medium,hard,deadly}, -d {easy,medium,hard,deadly}
	  --and AND_TAGS, -A AND_TAGS
							require monsters have all of these, eg:
							underdark,undercommon_lang
	  --or OR_TAGS, -O OR_TAGS
							only include monsters with one or more, eg:
							dragon,reptile
	  --not NOT_TAGS, -N NOT_TAGS
							exclude monsters with one of these, eg: undead,fire


Show stats for a creature (fuzzy search on name)::

	$ dankdungeon monster gobl
	Goblin
	Name: Goblin
	Xp: 50
	Type: humanoid
	Subtype: goblinoid
	Alignment: neutral evil
	Size: Small
	Speed: 30 ft.
	Senses: darkvision 60 ft., passive Perception 9
	Strength: 8
	Dexterity: 14
	Constitution: 10
	Intelligence: 10
	Wisdom: 8
	Charisma: 8
	Tags: darkvision, evil, cave, plains, goblin_lang, cavevision, common_lang, swamp, jungle, desert, mountain, walk, city, forest, tundra, goblin, humanoid
	Related monsters: Goblin, Hobgoblin, Bugbear, Orc, Kobold, Werewolf, Wererat, Wereboar, Worg, Oni

	Actions:
	  Scimitar
		Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage.
	  Shortbow
		Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage.

	Special Abilities:
	  Nimble Escape
		The goblin can take the Disengage or Hide action as a bonus action on each of its turns.


And generate encounters according to player levels::

	# Just a medium encounter with 4 players of level 1
	$ dankdungeon encounter
	XP=300.0 (200 <= xp <= 300):
	 - 3 Giant Lizard

	# players of levels 2, 2, 2 and 3
	$ dankdungeon encounter -p 2,2,2,3
	XP=450.0 (450 <= xp <= 675):
	 - 1 Gargoyle

	# restrict it to these monsters (each monster is tagged with its name, so this selects
	# everything in the set of monsters that have dire wolf or wolf in its tags.
	$ dankdungeon encounter -p 4,3,3,1 -O 'dire wolf,wolf' -d hard
	XP=900.0 (900 <= xp <= 1400):
	 - 2 Dire Wolf
	 - 1 Wolf

	# Restrict it to only undead, hard difficulty
	$ dankdungeon encounter -p 3,3,3 -d hard -A undead
	XP=1100.0 (675 <= xp <= 1200):
	 - 1 Ghost

	$ dankdungeon encounter -p 3,3,3 -d hard -A undead
	XP=1200.0 (675 <= xp <= 1200):
	 - 1 Shadow
	 - 1 Wight

	# deadly encounter for four 5th level players
	$ dankdungeon encounter -p 5,5,5,5 -d deadly -A undead
	XP=5400.0 (4400 <= xp <= 6500):
	 - 2 Ghast
	 - 1 Wraith

	# deadly with hellish or cave beasts
	$ dankdungeon encounter -p 5,5,5,5 -d deadly -O cave,underdark,hell
	XP=5600.0 (4400 <= xp <= 6500):
	 - 2 Nightmare
	 - 2 Hell Hound

	# werewolves are tagged with "cave", because it makes sense you could encounter them there.
	# Most monsters are tagged with several tags like plains,tundra,desert,mountain,forest,swamp,jungle
	$ dankdungeon encounter -p 10,8,10,9 -d deadly -O cave,underdark,hell
	XP=12250.0 (10100 <= xp <= 15050):
	 - 7 Werewolf

	# 2 bone devils will be just deadly enough for this group... good boss fight possibly.
	$ dankdungeon encounter -p 10,8,10,9 -d deadly -O hell
	XP=15000.0 (10100 <= xp <= 15050):
	 - 2 Bone Devil

	# A strange combination, but could be some hellish warlock's pets
	$ dankdungeon encounter -p 10,8,10,9 -d deadly -O hell
	XP=12600.0 (10100 <= xp <= 15050):
	 - 1 Spirit Naga
	 - 1 Magma Mephit
	 - 1 Vrock



Release Notes
-------------

:0.0.1:
    Project created
