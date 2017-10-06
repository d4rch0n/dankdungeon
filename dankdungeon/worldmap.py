import random
from enum import Enum
from PIL import Image
from opensimplex import OpenSimplex

DEFAULT_SIZE = 256
OCTAVES = 8

random.seed()


class Terrain(Enum):
    sea = (26, 67, 232)
    land = (196, 178, 141)
    forest = (5, 110, 5)
    mountain = (117, 88, 30)
    tundra = (255, 255, 255)


class NoiseLevel:

    def __init__(self, octave, size, mod):
        self.w = size[0]
        self.h = size[1]
        self.s = 2**octave / mod
        self.mvx = random.uniform(0, 2**30)
        self.mvy = random.uniform(0, 2**30)
        self.simp = OpenSimplex()

    def __call__(self, x, y):
        xx = (x / self.w * 4) + self.mvx
        yy = (y / self.h * 4) + self.mvy
        val = self.simp.noise2d(x=xx * self.s, y=yy * self.s)
        return (val + 1) / self.s

    @classmethod
    def random(cls, octave, size, mod):
        return cls(octave, size, mod)


class Noise:

    def __init__(self, width=DEFAULT_SIZE, height=DEFAULT_SIZE, mod=2):
        self.size = (width, height)
        self.vals = []
        self.norm = None
        self.m = []
        self.mod = mod

    def generate(self):
        self.funcs = []
        for o in range(1, OCTAVES):
            f = NoiseLevel.random(o, self.size, self.mod)
            self.funcs.append(f)
        w, h = self.size
        i = 0.10
        for x in range(w):
            new = []
            for y in range(h):
                val = self._calc_pt(x, y)
                self.vals.append(val)
                new.append(val)
            self.m.append(new)
            progress = x / w
            if progress >= i:
                print('{:.0%} done'.format(progress))
                i += 0.10
        self.normalize()

    def normalize(self):
        self.vals = sorted(self.vals)
        mx = max(self.vals)
        mn = min(self.vals)
        self.adder = -mn
        self.divider = mx + self.adder
        self.vals = [x + self.adder for x in self.vals]
        self.vals = [x / self.divider for x in self.vals]
        l = len(self.vals)
        self.thresholds = []
        for i in range(1000):
            n = int(l / 1000 * i)
            self.thresholds.append(self.vals[n])
        w, h = self.size
        for x in range(w):
            for y in range(h):
                self.m[x][y] = self.normal(x, y)

    def normal(self, x, y):
        val = self.calc_pt(x, y)
        a, b = 0, 1000
        while True:
            i = ((b - a) // 2) + a
            if i + 1 == len(self.thresholds):
                return 1.0
            elif self.thresholds[i] <= val < self.thresholds[i + 1]:
                return i / 1000
            elif self.thresholds[i] > val:
                b = i
            else:
                a = i

    def _calc_pt(self, x, y):
        vals = [f(x, y) for f in self.funcs]
        return sum(vals)

    def calc_pt(self, x, y):
        return (self.m[x][y] + self.adder) / self.divider

    def __getitem__(self, pos):
        x, y = pos
        return self.m[x][y]


class WorldMap:

    def __init__(self, width=DEFAULT_SIZE, height=DEFAULT_SIZE):
        self.size = (width, height)
        self.im = Image.new('RGB', self.size)
        self.px = self.im.load()

    def generate(self):
        w, h = self.size
        print('Generating altitude map...')
        self.altitude = Noise(width=w, height=h, mod=2)
        self.altitude.generate()
        print('Generating forest map...')
        self.forest = Noise(width=w, height=h, mod=12)
        self.forest.generate()
        for x in range(w):
            for y in range(h):
                self.px[x, y] = self.calc_pt_color(x, y)

    def calc_pt_terrain(self, x, y):
        ht = self.altitude[x, y]
        htf = self.forest[x, y]
        if ht >= 0.998:
            return Terrain.tundra
        elif ht >= 0.98:
            return Terrain.mountain
        elif ht >= 0.7:
            if (
                htf >= 0.95 or
                htf <= 0.15 or
                ht > 0.9
            ):
                return Terrain.forest
            else:
                return Terrain.land
        else:
            return Terrain.sea

    def calc_pt_color(self, x, y):
        terrain = self.calc_pt_terrain(x, y)
        return terrain.value

    def debug(self):
        pass

    def show(self):
        self.im.show()

    def save(self, path):
        self.im.save(path)


def main_worldmap():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--profile', '-p', choices=('tottime', 'cumtime'),
                        default=None)
    parser.add_argument('--out', '-o', default='worldmap.png')
    parser.add_argument('--size', '-s', type=int, default=256)
    args = parser.parse_args()
    if args.profile:
        from cProfile import run
        run('from dankdungeon.worldmap import WorldMap\n'
            'wm = WorldMap(width=256, height=256)\n'
            'wm.generate()', sort=args.profile)
    else:
        wm = WorldMap(width=args.size, height=args.size)
        wm.generate()
        if args.debug:
            wm.debug()
        wm.show()
        wm.save(args.out)


if __name__ == '__main__':
    main_worldmap()
