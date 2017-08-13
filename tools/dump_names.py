from dankdungeon import Monster


Monster.load()


for mon in sorted(Monster.MONSTERS, key=lambda x: x.name):
    print(mon.name)
