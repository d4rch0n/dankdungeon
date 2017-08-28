import random
from enum import Enum
from .character import NPC

BAD_ALIGNMENTS = ['chaotic evil', 'neutral evil', 'lawful evil', 'true neutral']


class Villain(NPC):

    def __init__(self, alignment=None, **kwargs):
        if alignment is None:
            alignment = random.choice(BAD_ALIGNMENTS)
        super().__init__(alignment=alignment, **kwargs)
        self.evil_bond = self.random_bond()
        self.bond = self.evil_bond.value
        self.evil_ideal = self.random_ideal()
        self.ideal = self.evil_ideal.value

    def random_bond(self):
        return random.choice(list(EvilBond))

    def random_ideal(self):
        return random.choice(list(EvilIdeal))


def main_villain():
    vln = Villain()
    vln.output()


class EvilBond(Enum):
    evil_god = 'My dark gods are my purpose in life and I must appease them.'
    revenge = 'I was wronged and I must exact revenge upon them.'
    hatred = 'I feel an intense hatred and will do anything to ruin them.'
    evil_patron = 'A dark fiend is the source of my power and I am its vessel.'
    envy = 'I envy something they have that I dont and it drives me mad.'
    despair = 'I feel intense despair and I will make others share my pain.'
    vanity = 'I am a god among men and they all must worship me or die.'
    plans = 'Nothing must get in the way of my dark plans, or they will die.'
    science = 'My experiments are all that matter, even if it causes pain.'
    arcana = 'I must learn ever dark arcane secret no matter what it involves.'
    insanity = 'I have been losing my mind and I know it, and I love the chaos.'
    undeath = 'I must live forever, even if that means undeath.'
    sadism = 'Inflicting pain in others gives me great joy, and I am addicted.'
    broken_heart = 'I lost the one I love and now I live to make others hurt.'
    greed = 'My love is for gold, and I will do anything for it.'
    power = 'Power is all that matters, and I will do anything for it.'
    duality = 'I am the Evil counterpart to some other Good.'
    service = 'Service to my Master calls for unspeakable but necessary evils.'
    capability = 'I am capable of horrible evils, and the temptation is great.'
    slave = 'I am powerless to escape the binds of my master.'
    death = 'Someone close to me died, and it drove me insane.'
    murder = "The more I kill, the more I love it... and the more I can't stop."
    purity = 'The world has become impure and it is my duty to purify it.'


class EvilIdeal(Enum):
    domination = 'Domination. Taking control of others is what I do.'
    greed = 'Wealth. The only things that matter are gold and silver.'
    power = 'Power. I do whatever I can to be the most powerful I can become.'
    service = "Service. The reason for my existence is to do my Master's will."
    arcana = 'Arcana. True power lies in mastery of the arcane.'
    undeath = 'Undeath. Immortality through undeath is the ultimate power.'
    murder = 'Murder. There is a beauty in causing the death of others.'
    fear = 'Fear. True power comes from inflicting terror in others.'
    pain = 'Pain. The pain and torment of others is our purpose.'
