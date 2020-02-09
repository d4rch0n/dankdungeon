from . import rand


def call_if(func, val):
    """
    Return None if falsey, or func(val).
    """
    return (val or None) and func(val)


def split_race(race_str):
    if ',' in race_str:
        race, subrace = race_str.split(',')
        return race.strip(), subrace.strip()
    return race_str.strip(), None


def race_freq_gen(freqs):

    def random_race():
        choice = rand.rand_freqs(freqs)
        return split_race(choice)

    return random_race
