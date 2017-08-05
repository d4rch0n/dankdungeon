import random
import networkx
import matplotlib.pyplot as plt


class Dungeon:

    def __init__(self, num_rooms=None):
        num_rooms = num_rooms or (7, 14)
        self.graph = networkx.Graph()
        if isinstance(num_rooms, (list, tuple)):
            self.num_rooms = random.randint(*num_rooms)
        else:
            self.num_rooms = num_rooms
        self.labels = {}
        self.create()

    def create(self):
        self.labels[0] = 'entry'
        self.graph.add_node(0)
        for i, room in enumerate(range(self.num_rooms - 1)):
            self.graph.add_node(i + 1)
            self.labels[i + 1] = 'room{}'.format(i + 1)


    def save(self, path='out.png'):
        import networkx
        import matplotlib.pyplot as plt
        pos = networkx.spring_layout(self.graph)
        nodelist = list(range(self.num_rooms))
        networkx.draw_networkx_nodes(self.graph, pos, nodelist=nodelist)
        networkx.draw_networkx_edges(self.graph, pos)
        networkx.draw_networkx_labels(self.graph, pos, self.labels)
        plt.savefig(path)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rooms', '-r', type=int, default=None)
    parser.add_argument('--output', '-o', default='out.png')
    args = parser.parse_args()
    dung = Dungeon(num_rooms=args.rooms)
    dung.save(path=args.output)


if __name__ == '__main__':
    main()
