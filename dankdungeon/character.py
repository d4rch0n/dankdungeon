import random


def roll_stat():
    nums = [random.randint(1, 6) for _ in range(4)]
    return sum(nums) - min(nums)


class NPC:

    def __init__(self):
        self.roll_stats()

    def roll_stats(self):
        self.str = roll_stat()
        self.dex = roll_stat()
        self.con = roll_stat()
        self.int = roll_stat()
        self.wis = roll_stat()
        self.cha = roll_stat()

    def output(self):
        print('STR: {}'.format(self.str))
        print('DEX: {}'.format(self.dex))
        print('CON: {}'.format(self.con))
        print('INT: {}'.format(self.int))
        print('WIS: {}'.format(self.wis))
        print('CHA: {}'.format(self.cha))
