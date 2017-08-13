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


And generate encounters according to player levels!

Just a medium encounter with 4 players of level 1, showing abbreviated stats for each monster type::

	$ dankdungeon encounter
	XP=300.0 (200 <= xp <= 300):
	 - 3 Giant Lizard

	Giant Lizard (beast) CR:1/4 XP:50
	AC:12 HP:19 (3d10)
	S:15 D:12 C:13 I:2 W:10 CH:5
	Size: Large
	Speed: 30 ft., climb 30 ft.
	Senses: darkvision 30 ft., passive Perception 10
	Action "Bite": Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 6 (1d8 + 2) piercing damage.
	Ability "Variant: Hold Breath": The lizard can hold its breath for 15 minutes. (A lizard that has this trait also has a swimming speed of 30 feet.)
	Ability "Variant: Spider Climb": The lizard can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check.

Players of levels 2, 2, 2 and 3::

	$ dankdungeon encounter -p 2,2,2,3
	XP=450.0 (450 <= xp <= 675):
	 - 1 Gargoyle

	... stats ...

Restrict it to these monsters. Each monster is tagged with its name, so this selects everything in the set of monsters that have dire wolf or wolf in its tags::

	$ dankdungeon encounter -p 4,3,3,1 -O 'dire wolf,wolf' -d hard
	XP=900.0 (900 <= xp <= 1400):
	 - 2 Dire Wolf
	 - 1 Wolf

	... stats ...

Restrict it to only undead, hard difficulty::
	
	$ dankdungeon encounter -p 3,3,3 -d hard -A undead
	XP=1100.0 (675 <= xp <= 1200):
	 - 1 Ghost

	$ dankdungeon encounter -p 3,3,3 -d hard -A undead
	XP=1200.0 (675 <= xp <= 1200):
	 - 1 Shadow
	 - 1 Wight

Deadly encounter for four 5th level players::

	$ dankdungeon encounter -p 5,5,5,5 -d deadly -A undead
	XP=5400.0 (4400 <= xp <= 6500):
	 - 2 Ghast
	 - 1 Wraith

Deadly with hellish (found in lower planes) or cave beasts::

	$ dankdungeon encounter -p 5,5,5,5 -d deadly -O cave,underdark,hell
	XP=5600.0 (4400 <= xp <= 6500):
	 - 2 Nightmare
	 - 2 Hell Hound

Werewolves are tagged with "cave", because it makes a bit of sense that they could be found there.
These are just rough guesses at where it might make sense to see some monsters, with these location tags: plains, tundra, desert, mountain, forest, swamp, jungle, cave, underdark, city, ruins::

	$ dankdungeon encounter -p 10,8,10,9 -d deadly -O cave,underdark,hell
	XP=12250.0 (10100 <= xp <= 15050):
	 - 7 Werewolf

2 bone devils will be just deadly enough for this group... good boss fight possibly::

	$ dankdungeon encounter -p 10,8,10,9 -d deadly -O hell
	XP=15000.0 (10100 <= xp <= 15050):
	 - 2 Bone Devil


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

:0.0.1:
    Project created
