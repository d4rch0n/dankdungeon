import random
from math import floor
from PIL import Image

random.seed()


class Noise:

    def __init__(self, octave, size):
        self.w = size[0]
        self.h = size[1]
        self.s = 2**octave
        self.m = []
        p = 1 / self.s
        for x in range(self.s):
            n = []
            for y in range(self.s):
                n.append(random.randint(0, 1) * p)
            self.m.append(n)

    def __call__(self, x, y):
        xx = x / self.w
        yy = y / self.h
        px = floor(self.s * xx)
        py = floor(self.s * yy)
        return self.m[px][py]

    @classmethod
    def random(cls, octave, size):
        return cls(octave, size)


class WorldMap:

    def __init__(self, width=256, height=256):
        self.size = (width, height)
        self.im = Image.new('RGB', self.size)
        self.px = self.im.load()

    def generate(self):
        self.funcs = []
        for o in range(1, 10):
            f = Noise.random(o, self.size)
            self.funcs.append(f)
        w, h = self.size
        for x in range(w):
            for y in range(h):
                self.px[x, y] = self.calc_pt_color(x, y)

    def calc_pt(self, x, y):
        vals = [f(x, y) for f in self.funcs]
        return sum(vals)

    def calc_pt_color(self, x, y):
        ht = self.calc_pt(x, y)
        # if ht > 0.7:
        #     ht = 1.0
        # else:
        #     ht = 0
        return (
            256 - floor(256 * ht),
            256 - floor(256 * ht),
            256 - floor(256 * ht),
        )

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
    parser.add_argument('--out', '-o', default='worldmap.png')
    args = parser.parse_args()
    wm = WorldMap()
    wm.generate()
    if args.debug:
        wm.debug()
    wm.show()
    wm.save(args.out)


if __name__ == '__main__':
    main_worldmap()
