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
	usage: dankdungeon [-h] {monster,encounter,threshold} ...

	positional arguments:
	  {monster,encounter,threshold}

	optional arguments:
	  -h, --help            show this help message and exit

Show monster stats::

	$ dankdungeon monster -h
	usage: dankdungeon monster [-h] [--short] name

	positional arguments:
	  name         select a monster by name

	optional arguments:
	  -h, --help   show this help message and exit
	  --short, -s  print short stats
	
Generate encounters::

	$ dankdungeon encounter -h
	usage: dankdungeon encounter [-h] [--players PLAYERS]
								 [--difficulty {easy,medium,hard,deadly}]
								 [--and AND_TAGS] [--or OR_TAGS] [--not NOT_TAGS]
								 [--custom CUSTOM] [--max-num MAX_NUM]

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
	  --custom CUSTOM, -c CUSTOM
							specify custom set of monsters with name=xp notation,
							eg. elfmage=500,treeperson=1500,goblin,goblinmage=200
	  --max-num MAX_NUM, -m MAX_NUM
							for custom encounters, the maximum number of one
							type,eg. "--max-num 5" if you only want up to 5 of
							each type, default: 10

Check player level XP thresholds::

	$ dankdungeon threshold -h
	usage: dankdungeon threshold [-h] [--players PLAYERS]

	optional arguments:
	  -h, --help            show this help message and exit
	  --players PLAYERS, -p PLAYERS
							the player levels, default 1,1,1,1



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


Or for abbreviated output for making notes for combat::

    $ dankdungeon monster 'goblin' -s
    Goblin (humanoid goblinoid) CR:1/4 XP:50
    AC:15 HP:7 (2d6)
    S:8 D:14 C:10 I:10 W:8 CH:8
    Size: Small
    Speed: 30 ft.
    Senses: darkvision 60 ft., passive Perception 9
    Langs: Common, Goblin
    Action "Scimitar": Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage.
    Action "Shortbow": Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage.
    Ability "Nimble Escape": The goblin can take the Disengage or Hide action as a bonus action on each of its turns.

    $ dankdungeon monster 'wraith' -s
    Wraith (undead) CR:5 XP:1800
    AC:13 HP:67 (9d8)
    S:6 D:16 C:16 I:12 W:14 CH:15
    Size: Medium
    Speed: 0 ft., fly 60 ft. (hover)
    Senses: darkvision 60 ft., passive Perception 12
    Immune: necrotic, poison
    Cond.Immune: charmed, exhaustion, grappled, paralyzed, petrified, poisoned, prone, restrained
    Resist: acid, cold, fire, lightning, thunder; bludgeoning, piercing, and slashing from nonmagical weapons that aren't silvered
    Langs: the languages it knew in life
    Action "Life Drain": Melee Weapon Attack: +6 to hit, reach 5 ft., one creature. Hit: 21 (4d8 + 3) necrotic damage. The target must succeed on a DC 14 Constitution saving throw or its hit point maximum is reduced by an amount equal to the damage taken. This reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0.
    Action "Create Specter": The wraith targets a humanoid within 10 feet of it that has been dead for no longer than 1 minute and died violently. The target's spirit rises as a specter in the space of its corpse or in the nearest unoccupied space. The specter is under the wraith's control. The wraith can have no more than seven specters under its control at one time.
    Ability "Incorporeal Movement": The wraith can move through other creatures and objects as if they were difficult terrain. It takes 5 (1d10) force damage if it ends its turn inside an object.
    Ability "Sunlight Sensitivity": While in sunlight, the wraith has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight.


Easily calculate the XP threshold requirements for players::

	$ dankdungeon threshold -p 4,4,3,3
	Easy: 400 to 799
	Medium: 800 to 1199
	Hard: 1200 to 1799
	Deadly: 1800+

And generate encounters according to player levels!

Just a medium encounter with 4 players of level 1, showing abbreviated stats for each monster type::

	$ dankdungeon encounter
	found 138 possible monsters
	trying to build with types: Giant Wolf Spider, Spider, Giant Spider, Swarm of Spiders, Scorpion, Stirge
	iterating through 1000000 possible encounter permutations...
	198 of those match allowed XP values
	XP=300.0 (200 <= xp <= 300):
	 - 5 Spider
	 - 2 Scorpion
	 - 2 Stirge

	Spider (beast) CR:0 XP:10
	AC:12 HP:1 (1d4)
	S:2 D:14 C:8 I:1 W:10 CH:2
	Size: Tiny
	Speed: 20 ft., climb 20 ft.
	Senses: darkvision 30 ft., passive Perception 12
	Action "Bite": Melee Weapon Attack: +4 to hit, reach 5 ft., one creature. Hit: 1 piercing damage, and the target must succeed on a DC 9 Constitution saving throw or take 2 (1d4) poison damage.
	Ability "Spider Climb": The spider can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check.
	Ability "Web Sense": While in contact with a web, the spider knows the exact location of any other creature in contact with the same web.
	Ability "Web Walker": The spider ignores movement restrictions caused by webbing.

	Scorpion (beast) CR:0 XP:10
	AC:11 HP:1 (1d4)
	S:2 D:11 C:8 I:1 W:8 CH:2
	Size: Tiny
	Speed: 10 ft.
	Senses: blindsight 10 ft., passive Perception 9
	Action "Sting": Melee Weapon Attack: +2 to hit, reach 5 ft., one creature. Hit: 1 piercing damage, and the target must make a DC 9 Constitution saving throw, taking 4 (1d8) poison damage on a failed save, or half as much damage on a successful one.

	Stirge (beast) CR:1/8 XP:25
	AC:14 HP:2 (1d4)
	S:4 D:16 C:11 I:2 W:8 CH:6
	Size: Tiny
	Speed: 10 ft., fly 40 ft.
	Senses: darkvision 60 ft., passive Perception 9
	Action "Blood Drain": Melee Weapon Attack: +5 to hit, reach 5 ft., one creature. Hit: 5 (1d4 + 3) piercing damage, and the stirge attaches to the target. While attached, the stirge doesn't attack. Instead, at the start of each of the stirge's turns, the target loses 5 (1d4 + 3) hit points due to blood loss.
	The stirge can detach itself by spending 5 feet of its movement. It does so after it drains 10 hit points of blood from the target or the target dies. A creature, including the target, can use its action to detach the stirge.

Players of levels 2, 2, 2 and 3::

	$ dankdungeon encounter -p 2,2,2,3
	found 181 possible monsters
	trying to build with types: Griffon, Hippogriff, Harpy, Darkmantle, Cockatrice, Worg
	iterating through 1000000 possible encounter permutations...
	20 of those match allowed XP values
	XP=600.0 (450 <= xp <= 675):
	 - 1 Hippogriff
	 - 1 Harpy

	Hippogriff (monstrosity) CR:1 XP:200
	AC:11 HP:19 (3d10)
	...

	Harpy (monstrosity) CR:1 XP:200
	AC:11 HP:38 (7d8)
	...


Restrict it to these monsters. -c or --custom will allow you to specify named types or custom monsters with XP values, eg. --custom wolf,wolfman=200 . This just uses standard wolf and direwolf::

	$ dankdungeon encounter -p 4,3,3,1 -c 'dire wolf,wolf'
	iterating through 100 possible encounter permutations...
	8 of those match allowed XP values
	XP=600.0 (600 <= xp <= 900):
	 - 2 Dire Wolf (xp=200)

	$ dankdungeon encounter -p 4,3,3,1 -c 'dire wolf,wolf'
	iterating through 100 possible encounter permutations...
	8 of those match allowed XP values
	XP=800.0 (600 <= xp <= 900):
	 - 1 Dire Wolf (xp=200)
	 - 4 Wolf (xp=50)


Restrict it to only undead, hard difficulty, for 3 player 3's::

	$ dankdungeon encounter -p 3,3,3 -d hard -A undead
	found 13 possible monsters
	trying to build with types: Zombie, Shadow, Wight, Warhorse Skeleton, Specter, Ogre Zombie
	iterating through 1000000 possible encounter permutations...
	130 of those match allowed XP values
	XP=1200.0 (675 <= xp <= 1200):
	 - 2 Zombie
	 - 1 Shadow
	 - 2 Warhorse Skeleton
	 - 1 Specter

	... stats ...

Deadly encounter for four 5th level players, the evil dead::

	$ dankdungeon encounter -p 5,5,5,5 -d deadly -A evil,undead
	found 14 possible monsters
	trying to build with types: Vampire Spawn, Zombie, Wraith, Shadow, Wight, Warhorse Skeleton
	iterating through 1000000 possible encounter permutations...
	1205 of those match allowed XP values
	XP=4750.0 (4400 <= xp <= 6500):
	 - 2 Zombie
	 - 4 Shadow
	 - 2 Wight

Deadly with hellish (found in lower planes) or cave beasts::

	$ dankdungeon encounter -p 5,5,5,5 -d deadly -O cave,underdark,hell
	found 141 possible monsters
	trying to build with types: Vrock, Succubus/Incubus, Hezrou, Glabrezu, Dretch, Nightmare
	iterating through 1000000 possible encounter permutations...
	46 of those match allowed XP values
	XP=4500.0 (4400 <= xp <= 6500):
	 - 3 Dretch
	 - 3 Nightmare

Mummies are tagged with "desert" because it makes sense to find them there, and werewolf might be tagged "cave" as well as "forest".
These are just rough guesses at where it might make sense to see some monsters, with these location tags: plains, tundra, desert, mountain, forest, swamp, jungle, cave, underdark, city, ruins::

	$ dankdungeon encounter -p 10,8,10,9 -d deadly -A tundra,evil
	found 46 possible monsters
	trying to build with types: Spirit Naga, Oni, Minotaur, Chimera, Winter Wolf, Rakshasa
	iterating through 1000000 possible encounter permutations...
	93 of those match allowed XP values
	XP=14800.0 (10100 <= xp <= 15050):
	 - 1 Minotaur
	 - 2 Chimera
	 - 3 Winter Wolf

2 bone devils will be just deadly enough for this group... good boss fight possibly::

	$ dankdungeon encounter -p 10,8,10,9 -d deadly -O hell
	found 24 possible monsters
	trying to build with types: Barbed Devil, Ice Devil, Horned Devil, Erinyes, Chain Devil, Bone Devil
	iterating through 1000000 possible encounter permutations...
	9 of those match allowed XP values
	XP=15000.0 (10100 <= xp <= 15050):
	 - 2 Bone Devil
 
And if you want custom monsters with personally known XP values, use the --custom flag::

	$ dankdungeon encounter -c 'mushroomer=250,mushroomer pet dog=100,mushroomer mage=600,violet fung,bugbear' -p 8,8,8 -d hard
	iterating through 100000 possible encounter permutations...
	2538 of those match allowed XP values
	XP=5100.0 (4200 <= xp <= 6300):
	 - 4 mushroomer (xp=250)
	 - 5 mushroomer pet dog (xp=100)
	 - 4 Violet Fungus (xp=50)
	
	$ dankdungeon encounter -c 'mushroomer=250,mushroomer pet dog=100,mushroomer mage=600,violet fung,bugbear' -p 8,8,8 -d hard
	iterating through 100000 possible encounter permutations...
	2538 of those match allowed XP values
	XP=5550.0 (4200 <= xp <= 6300):
	 - 1 mushroomer (xp=250)
	 - 9 mushroomer pet dog (xp=100)
	 - 1 mushroomer mage (xp=600)
	 - 2 Violet Fungus (xp=50)

	$ dankdungeon encounter -c 'mushroomer=250,mushroomer pet dog=100,mushroomer mage=600,violet fung,bugbear' -p 8,8,8 -d hard
	iterating through 100000 possible encounter permutations...
	2538 of those match allowed XP values
	XP=4950.0 (4200 <= xp <= 6300):
	 - 2 mushroomer pet dog (xp=100)
	 - 5 Violet Fungus (xp=50)
	 - 6 Bugbear (xp=200)


The following monsters have been incorporated from the Standard Reference Document::

    Aboleth
    Acolyte
    Adult Black Dragon
    Adult Blue Dracolich
    Adult Blue Dragon
    Adult Brass Dragon
    Adult Bronze Dragon
    Adult Copper Dragon
    Adult Gold Dragon
    Adult Green Dragon
    Adult Red Dragon
    Adult Silver Dragon
    Adult White Dragon
    Air Elemental
    Ancient Black Dragon
    Ancient Blue Dragon
    Ancient Brass Dragon
    Ancient Bronze Dragon
    Ancient Copper Dragon
    Ancient Gold Dragon
    Ancient Green Dragon
    Ancient Red Dragon
    Ancient Silver Dragon
    Ancient White Dragon
    Androsphinx
    Animated Armor
    Ankheg
    Ape
    Archmage
    Assassin
    Awakened Shrub
    Awakened Tree
    Axe Beak
    Azer
    Baboon
    Badger
    Balor
    Bandit
    Bandit Captain
    Barbed Devil
    Basilisk
    Bat
    Bearded Devil
    Behir
    Berserker
    Black Bear
    Black Dragon Wyrmling
    Black Pudding
    Blink Dog
    Blood Hawk
    Blue Dragon Wyrmling
    Boar
    Bone Devil
    Brass Dragon Wyrmling
    Bronze Dragon Wyrmling
    Brown Bear
    Bugbear
    Bulette
    Camel
    Carrion Crawler
    Cat
    Cave Bear
    Centaur
    Chain Devil
    Chimera
    Chuul
    Clay Golem
    Cloaker
    Cloud Giant
    Cockatrice
    Commoner
    Constrictor Snake
    Copper Dragon Wyrmling
    Couatl
    Crab
    Crocodile
    Cult Fanatic
    Cultist
    Darkmantle
    Death Dog
    Deep Gnome (Svirfneblin)
    Deer
    Deva
    Dire Wolf
    Djinni
    Doppelganger
    Draft Horse
    Dragon Turtle
    Dretch
    Drider
    Drow
    Druid
    Dryad
    Duergar
    Dust Mephit
    Eagle
    Earth Elemental
    Efreeti
    Elephant
    Elk
    Erinyes
    Ettercap
    Ettin
    Fire Elemental
    Fire Giant
    Flesh Golem
    Flying Snake
    Flying Sword
    Frog
    Frost Giant
    Gargoyle
    Gelatinous Cube
    Ghast
    Ghost
    Ghoul
    Giant Ape
    Giant Badger
    Giant Bat
    Giant Boar
    Giant Centipede
    Giant Constrictor Snake
    Giant Crab
    Giant Crocodile
    Giant Eagle
    Giant Elk
    Giant Fire Beetle
    Giant Frog
    Giant Goat
    Giant Hyena
    Giant Lizard
    Giant Octopus
    Giant Owl
    Giant Poisonous Snake
    Giant Rat
    Giant Rat (Diseased)
    Giant Scorpion
    Giant Sea Horse
    Giant Shark
    Giant Spider
    Giant Toad
    Giant Vulture
    Giant Wasp
    Giant Weasel
    Giant Wolf Spider
    Gibbering Mouther
    Glabrezu
    Gladiator
    Gnoll
    Goat
    Goblin
    Gold Dragon Wyrmling
    Gorgon
    Gray Ooze
    Green Dragon Wyrmling
    Green Hag
    Grick
    Griffon
    Grimlock
    Guard
    Guardian Naga
    Gynosphinx
    Half-Red Dragon Veteran
    Harpy
    Hawk
    Hell Hound
    Hezrou
    Hill Giant
    Hippogriff
    Hobgoblin
    Homunculus
    Horned Devil
    Hunter Shark
    Hydra
    Hyena
    Ice Devil
    Ice Mephit
    Imp
    Invisible Stalker
    Iron Golem
    Jackal
    Killer Whale
    Knight
    Kobold
    Kraken
    Lamia
    Lemure
    Lich
    Lion
    Lizard
    Lizardfolk
    Mage
    Magma Mephit
    Magmin
    Mammoth
    Manticore
    Marilith
    Mastiff
    Medusa
    Merfolk
    Merrow
    Mimic
    Minotaur
    Minotaur Skeleton
    Mule
    Mummy
    Mummy Lord
    Nalfeshnee
    Night Hag
    Nightmare
    Noble
    Ochre Jelly
    Octopus
    Ogre
    Ogre Zombie
    Oni
    Orc
    Otyugh
    Owl
    Owlbear
    Panther
    Pegasus
    Phase Spider
    Pit Fiend
    Planetar
    Plesiosaurus
    Poisonous Snake
    Polar Bear
    Pony
    Priest
    Pseudodragon
    Purple Worm
    Quasit
    Quipper
    Rakshasa
    Rat
    Raven
    Red Dragon Wyrmling
    Reef Shark
    Remorhaz
    Rhinoceros
    Riding Horse
    Roc
    Roper
    Rug of Smothering
    Rust Monster
    Saber-Toothed Tiger
    Sahuagin
    Salamander
    Satyr
    Scorpion
    Scout
    Sea Hag
    Sea Horse
    Shadow
    Shambling Mound
    Shield Guardian
    Shrieker
    Silver Dragon Wyrmling
    Skeleton
    Solar
    Specter
    Spider
    Spirit Naga
    Sprite
    Spy
    Steam Mephit
    Stirge
    Stone Giant
    Stone Golem
    Storm Giant
    Succubus/Incubus
    Swarm of Bats
    Swarm of Beetles
    Swarm of Centipedes
    Swarm of Insects
    Swarm of Poisonous Snakes
    Swarm of Quippers
    Swarm of Rats
    Swarm of Ravens
    Swarm of Spiders
    Swarm of Wasps
    Tarrasque
    Thug
    Tiger
    Treant
    Tribal Warrior
    Triceratops
    Troll
    Tyrannosaurus Rex
    Unicorn
    Vampire
    Vampire Spawn
    Veteran
    Violet Fungus
    Vrock
    Vulture
    Warhorse
    Warhorse Skeleton
    Water Elemental
    Weasel
    Werebear
    Wereboar
    Wererat
    Weretiger
    Werewolf
    White Dragon Wyrmling
    Wight
    Will-o'-Wisp
    Winter Wolf
    Wolf
    Worg
    Wraith
    Wyvern
    Xorn
    Young Black Dragon
    Young Blue Dragon
    Young Brass Dragon
    Young Bronze Dragon
    Young Copper Dragon
    Young Gold Dragon
    Young Green Dragon
    Young Red Dragon
    Young Silver Dragon
    Young White Dragon
    Zombie

Release Notes
-------------

:0.2.0:
    Instead of calculating everything at runtime, I cached it and saved new json files... runs way quicker!
:0.1.2:
    Fixed include for monster json
:0.1.1:
    Ready for consumption
:0.0.1:
    Project created
