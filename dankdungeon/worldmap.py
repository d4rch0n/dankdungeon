import math
from math import floor
import random
from PIL import Image


class Sin3D:

    def __init__(self, coefx, coefy, subx, suby):
        self.coefx = coefx
        self.coefy = coefy
        self.subx = subx
        self.suby = suby

    def __call__(self, x, y):
        return (
            math.sin(self.coefx * (x - self.subx)) +
            math.sin(self.coefy * (y - self.suby))
        )

    @classmethod
    def random(cls, octave):
        p = 1 / (2**octave)
        subx = random.uniform(0, math.pi * 2)
        suby = random.uniform(0, math.pi * 2)
        return cls(p, p, subx, suby)


class WorldMap:

    def __init__(self, width=1024, height=1024):
        self.size = (width, height)
        self.im = Image.new('RGB', self.size)
        self.px = self.im.load()

    def generate(self):
        self.funcs = []
        for o in range(1, 7):
            f = Sin3D.random(o)
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
        return (floor(256 * ht), floor(256 * ht), floor(256 * ht))

    def debug(self):
        pass

    def show(self):
        self.im.show()


def main_worldmap():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()
    wm = WorldMap()
    wm.generate()
    if args.debug:
        wm.debug()
    wm.show()


if __name__ == '__main__':
    main_worldmap()
