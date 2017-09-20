from PIL import Image


class WorldMap:

    def __init__(self, width=1024, height=1024):
        self.size = (width, height)
        self.im = Image.new('RGB', self.size)
        self.px = self.im.load()

    def generate(self):
        pass

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
