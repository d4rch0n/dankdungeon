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
        self.evil_flaw = self.random_flaw()
        self.flaw = self.evil_flaw.value
        self.evil_trait = self.random_trait()
        self.trait = self.evil_trait.value

    def random_bond(self):
        return random.choice(list(EvilBond))

    def random_ideal(self):
        return random.choice(list(EvilIdeal))

    def random_trait(self):
        return random.choice(list(EvilTrait))

    def random_flaw(self):
        return random.choice(list(EvilFlaw))


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


class EvilTrait(Enum):
    laugh = 'I have a tendency to laugh at awkward times.'
    idolize = 'I idolize someone and try my best to imitate them.'
    theatric = 'I love a theatrical display and try to give a show.'
    gambler = 'I am not afraid to take large risks.'
    survivor = 'I often find a way to survive with the worst of odds.'
    macguyver = 'I can escape a prison cell with a toothpick and a string.'
    logical = 'I will always follow the most logical path.'
    sloth = 'The easiest road to victory is the best road.'
    hardworker = 'I will work all day and night to get what I want.'
    pessimist = 'I tend to obsess over the worst of my situation.'
    optimist = 'I tend to look at the bright side even in the worst situations.'
    rude = 'I will act extremely inappropriate when I can get away with it.'
    polite = 'No matter who we are and what we do, we must follow etiquette.'
    talker = 'I love to hear the sound of my voice, and force it upon others.'
    hermit = 'I prefer solitude, and am best when alone.'
    famous = 'I love being famous, and will try to make a name for myself.'
    boredom = 'I get bored very easily, and love excitement.'
    smooth = 'I can usually smoothtalk my way out of bad situations.'
    skeptic = 'There is no reason to trust the narrative being presented.'
    anger = 'I am quick to anger, and will throw tantrums.'
    trustworthy = 'People know I keep my word, and that gives me power.'
    backstabber = 'I will stab anyone in the back.'
    sociopath = 'I have no empathy whatsoever.'
    narcissist = 'I obsess over how wonderful I am, and love flattery.'
    moody = 'I find myself brooding more often than not.'
    judgmental = 'I am quick to judge others for their mistakes.'
    feared = 'People know to fear me, and avoid my wrath.'
    grudge = 'I will hold a grudge until the person is dead.'
    tinker = 'I love a little machinery and lay traps when I can.'
    strategy = 'I obsess over the strategic details.'
    ignoble = 'I was not born into nobility and hate those who were.'
    noble = 'I am of noble birth and peasants are below me.'


class EvilFlaw(Enum):
    phobia = 'I have an unfortunate phobia which causes me to act irrationally.'
    coward = 'In truth, I am a coward and will flee when threatened.'
    greed = 'My greed is my weakness, and I will make bad decisions for gold.'
    planner = "I don't think too far ahead and improvise if possible."
    impulsive = 'I often make impulsive decisions, for better or worse.'
    vanity = 'Appealing to my vanity will cause me to make bad judgments.'
    gullible = 'I often fall for stupid tricks that others might see through.'
    chaotic = 'Sometimes I act without reason just to shake things up.'
    sadness = 'I feel a great sadness, and sometimes lose hope.'
    master = 'I am extremely dependent on my master and feel weak without them.'
    fear = 'If I do not cause fear in someone it troubles me greatly.'
    motivation = 'I lose motivation easily and have trouble following through.'
    failure = 'I cannot cope with failure and do anything to win.'
    mistake = 'I am not very meticulous and make many small mistakes.'
    meticulous = 'I am extremely meticulous and obsess over minor details.'
    confidence = 'I lose confidence with myself very easily.'
    overconfidence = 'I am overconfident, and overestimate my abilities.'
    intuition = 'I cannot see the big picture sometimes.'
    beauty = 'I obsess over my own beauty and hate to see imperfection.'
