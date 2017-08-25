'''
namerator
=========

Name generator, by generating characters based on frequencies of letter patterns

Usage:
    $ python namerator.py -n 5 elf_names.txt
    egil-gonamilin
    taedhorilie
    lalorahinduil
    cirduiel
    amrothrie

'''
import sys
import os
from math import sqrt
from random import gauss, seed, choice
from collections import Counter

NAME_ROOT = os.path.join(os.path.dirname(__file__), 'names')


def load(path):
    with open(path) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def load_names():
    names = {}
    files = os.listdir(NAME_ROOT)
    for f in files:
        name, _ = os.path.splitext(f)
        path = os.path.join(NAME_ROOT, f)
        names[name.replace('_', '-')] = load(path)
    return names


def load_frequencies():
    freq = {}
    for fname, names in NAMES.items():
        freq[fname] = calc_frequencies(names)
    return freq


def chop_name(name):
    lst = [x for x in name.lower().strip().split()[0]]
    return ['', '', '', ''] + lst + ['$']


def inc_frequencies(chop, freqs):
    freqs[0] = freqs.get(0, Counter())
    for i in range(1, 5):
        freqs[i] = freqs.get(i, {})
    for i in range(3, len(chop)):
        a, b, c, d = chop[i-4], chop[i-3], chop[i-2], chop[i-1]
        char = chop[i]
        freqs[0].update([char])
        freqs[1][d] = freqs[1].get(d, Counter())
        freqs[1][d].update([char])
        freqs[2][c + d] = freqs[2].get(c + d, Counter())
        freqs[2][c + d].update([char])
        freqs[3][b + c + d] = freqs[3].get(b + c + d, Counter())
        freqs[3][b + c + d].update([char])
        freqs[4][a + b + c + d] = freqs[4].get(a + b + c + d, Counter())
        freqs[4][a + b + c + d].update([char])
    return freqs


def calc_frequencies(names):
    freqs = {'len': Counter()}
    for name in names:
        freqs['len'].update([len(name)])
        chop = chop_name(name)
        inc_frequencies(chop, freqs)
    return freqs


def combined_frequencies(freqs, last1, last2, last3, last4):
    freq = Counter()
    freq.update(freqs[1][last1])
    for i in range(5):
        freq.update(freqs[2].get(last2, []))
    for i in range(10):
        freq.update(freqs[3].get(last3, []))
    for i in range(25):
        freq.update(freqs[4].get(last4, []))
    return freq.most_common()


def choose(common, over=0, letter_freqs=None):
    lst = []
    for char, num in common:
        if over < 0 and char == '$':
            continue
        lst += [char] * num
    if over >= 0:
        lst += ['$'] * dict(common).get('$', 1) * (over + 1)
    if not lst:
        return choose(letter_freqs, over=over)
    return choice(lst)


def calc_gauss(lens):
    expanded = []
    for l, num in lens:
        expanded += [l] * num
    mean = sum(expanded) / len(expanded)
    sigma = sum((mean - x)**2 for x in expanded)
    sigma /= len(expanded) - 1
    sigma = sqrt(sigma)
    return mean, sigma


def generate(freqs):
    if isinstance(freqs, str):
        freqs = FREQS[freqs]
    name = ''
    last1 = ''
    last2 = ''
    last3 = ''
    last4 = ''
    shortest = min(x for x, y in freqs['len'].most_common())
    # longest = max(x for x, y in freqs['len'].most_common())
    mean, sigma = calc_gauss(freqs['len'].most_common())
    namelen = int(max(gauss(mean, sigma), shortest))
    while True:
        combined = combined_frequencies(freqs, last1, last2, last3, last4)
        while True:
            next_letter = choose(combined, over=len(name) - namelen,
                                 letter_freqs=freqs[0].most_common())
            if last2 and last2 == (next_letter + next_letter):
                continue
            else:
                break
        if next_letter == '$':
            break
        name += next_letter
        last4 = last3 + next_letter
        last3 = last2 + next_letter
        last2 = last1 + next_letter
        last1 = next_letter
    return name


def make_name(race, gender=None):
    if not isinstance(race, str):
        race = race.NAME
    if gender is not None and race in ('human', 'halfling', 'tiefling',
                                       'dragonborn'):
        race = '{}-{}'.format(race, gender)
    if race == 'human-male':
        first = generate('human-first-male')
        last = generate('human-last')
        return '{} {}'.format(first, last).title()
    elif race == 'human-female':
        first = generate('human-first-female')
        last = generate('human-last')
        return '{} {}'.format(first, last).title()
    elif race == 'dragonborn-male':
        first = generate('dragonborn-first-male')
        last = generate('dragonborn-last')
        return '{} {}'.format(first, last).title()
    elif race == 'dragonborn-female':
        first = generate('dragonborn-first-female')
        last = generate('dragonborn-last')
        return '{} {}'.format(first, last).title()
    elif race == 'human-first-male':
        return generate('human-first-male').title()
    elif race == 'human-first-female':
        return generate('human-first-female').title()
    elif race == 'tiefling-male':
        return '{}'.format(generate('tiefling-first-male').title())
    elif race == 'tiefling-female':
        return '{}'.format(generate('tiefling-first-female').title())
    elif race == 'tiefling-first-male':
        return generate('tiefling-first-male').title()
    elif race == 'tiefling-first-female':
        return generate('tiefling-first-female').title()
    elif race == 'human2':
        return generate('human-last').title()
    elif race == 'elf':
        return '{} {}'.format(generate('elf'), generate('elf')).title()
    elif race == 'half-elf':
        first = generate('elf')
        last = generate('human-last')
        return '{} {}'.format(first, last).title()
    elif race == 'dwarf':
        first = generate('dwarf')
        part1 = choice(NAMES['dwarf-part1'])
        n2 = sorted(set(NAMES['dwarf-part2']) - set(part1))
        part2 = choice(n2)
        last = part1 + part2
        return '{} {}'.format(first, last).title()
    elif race == 'gnome':
        first = generate('dwarf')
        last = choice(NAMES['dwarf-part1']) + generate('dwarf-part2')
        return '{} {}'.format(first, last).title()
    elif race == 'dwarf-first':
        return generate('dwarf').title()
    elif race == 'dwarf-last':
        return choice(NAMES['dwarf-part1']) + choice(NAMES['dwarf-part2'])
    elif race == 'orc':
        return generate('orc').title()
    elif race == 'half-orc':
        first = generate('orc').title()
        last = generate('human-last')
        return '{} {}'.format(first, last).title()
    elif race == 'halfling-male':
        first = generate('human-first-male')
        last = generate('halfling-last')
        return '{} {}'.format(first, last).title()
    elif race == 'halfling-female':
        first = generate('human-first-female')
        last = generate('halfling-last')
        return '{} {}'.format(first, last).title()
    else:
        raise NotImplementedError('cant generate name for {}'.format(race))


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--num', '-n', type=int, default=10)
    parser.add_argument('--output', '-o')
    parser.add_argument('--freq-output', '-f')
    args = parser.parse_args()
    if os.path.isfile(args.path):
        names = load(args.path)
        freqs = calc_frequencies(names)
    else:
        sys.exit('Please pass a path to the name file or one of "human", '
                 '"elf", "dwarf" or "orc"')
    if args.freq_output:
        dump = {}
        dump['len'] = freqs['len'].most_common()
        dump['frequency'] = freqs[0].most_common()
        dump['first'] = {k: v.most_common() for k, v in freqs[1].items()}
        dump['second'] = {k: v.most_common() for k, v in freqs[2].items()}
        dump['third'] = {k: v.most_common() for k, v in freqs[3].items()}
        dump['fourth'] = {k: v.most_common() for k, v in freqs[4].items()}
        with open(args.freq_output, 'w') as f:
            json.dump(dump, f, indent=4)
        print('Dumped frequencies to {args.freq_output}'.format(args=args))
    names = set(names)
    ct = 0
    if args.output is None:
        while ct < args.num:
            name = generate(freqs)
            if name in names:
                seed()
                continue
            names.add(name)
            print(name)
            ct += 1
        return
    with open(args.output, 'w') as f:
        while ct < args.num:
            name = generate(freqs)
            if name in names:
                seed()
                continue
            names.add(name)
            f.write(name + '\n')
            ct += 1
            if ct % 100 == 0:
                perc = float(ct) / args.num
                print('{:.2%} done'.format(perc))


NAMES = load_names()
FREQS = load_frequencies()


if __name__ == '__main__':
    main()
