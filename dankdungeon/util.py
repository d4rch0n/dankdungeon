from . import rand, namerator


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


def race_dict(dct):
    result = {}
    if 'default' in dct:
        result[None, None] = dct['default']
    for key, val in dct.items():
        if key == 'default':
            continue
        race, subrace = split_race(key)
        result[race, subrace] = val
    return result


def make_race_name_gen(race_names):
    default = race_names[None, None]
    gen_dct = {None: namerator.make_name_generator(default)}
    for (race, subrace), names in race_names.items():
        if race is None:
            continue
        gen_dct[race, subrace] = namerator.make_name_generator(names)

    def name_gen(race, subrace=None, gender=None):
        nonlocal gen_dct
        if (race, subrace) in gen_dct:
            return gen_dct[race, subrace](gender=gender)
        return gen_dct[None](gender=gender)

    return name_gen
