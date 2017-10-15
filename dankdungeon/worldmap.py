import random
from enum import Enum
from PIL import Image
from opensimplex import OpenSimplex

DEFAULT_SIZE = 256
OCTAVES = 8


class Terrain(Enum):
    sea = (26, 67, 232)
    river = (0x66, 0xcc, 0xff)
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
        self.simp = OpenSimplex(seed=random.randint(0, 2**20))

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


class Point:
    SIZE = (1024, 1024)

    def __init__(self, pos, altitude=None, forest=None, river=None):
        self.altitude = altitude
        self.forest = forest
        self.river = river
        self.pixel = self.calc_terrain()
        self.pos = pos

    def calc_terrain(self):
        if self.altitude >= 0.998:
            return Terrain.tundra
        elif self.altitude >= 0.95:
            return Terrain.mountain
        elif self.altitude >= 0.7:
            if (
                self.forest >= 0.85 or
                self.forest <= 0.15 or
                self.altitude > 0.9
            ):
                return Terrain.forest
            else:
                return Terrain.land
        else:
            return Terrain.sea

    def color(self):
        return self.pixel.value

    def make_river(self):
        self.pixel = Terrain.river
        self.river = True

    def neighbors(self):
        x, y = self.pos
        ns = []
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                p = (x + ix, y + iy)
                if p == self.pos:
                    continue
                if (
                    p[0] >= 0 and p[1] >= 0 and
                    p[0] < self.SIZE[0] and p[1] < self.SIZE[1]
                ):
                    ns.append(p)
        return ns


class WorldMap:

    def __init__(self, width=DEFAULT_SIZE, height=DEFAULT_SIZE):
        self.size = (width, height)
        Point.SIZE = self.size
        self.im = Image.new('RGB', self.size)
        self.px = self.im.load()
        self.m = []
        for x in range(width):
            new = []
            for y in range(height):
                new.append(None)
            self.m.append(new)

    def generate(self):
        w, h = self.size
        print('Generating altitude map...')
        self.altitude = Noise(width=w, height=h, mod=2)
        self.altitude.generate()
        print('Generating forest map...')
        self.forest = Noise(width=w, height=h, mod=12)
        self.forest.generate()
        for x, y in self.coords():
            ht = self.altitude[x, y]
            htf = self.forest[x, y]
            self[x, y] = Point((x, y), altitude=ht, forest=htf)
        self.generate_rivers()
        for x, y in self.coords():
            self.px[x, y] = self[x, y].color()

    def generate_rivers(self):
        roots = []
        for x, y in self.coords():
            p = self[x, y]
            if 0.95 <= p.altitude < 0.998:
                roots.append((x, y))
        random.shuffle(roots)
        roots = roots[:len(roots) // 50]
        for root in roots:
            self.create_river(root)

    def create_river(self, pos):
        self[pos].make_river()


    def __getitem__(self, pos):
        x, y = pos
        return self.m[x][y]

    def __setitem__(self, pos, val):
        x, y = pos
        self.m[x][y] = val

    def debug(self):
        pass

    def show(self):
        if self.size[0] < 1024:
            self.im = self.im.resize((1024, 1024))
        self.im.show()

    def save(self, path):
        self.im.save(path)

    def coords(self):
        w, h = self.size
        for x in range(w):
            for y in range(h):
                yield x, y


def main_worldmap():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--profile', '-p', choices=('tottime', 'cumtime'),
                        default=None)
    parser.add_argument('--out', '-o', default='worldmap.png')
    parser.add_argument('--size', '-s', type=int, default=512)
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
