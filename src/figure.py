import random
import numpy as np


class Figure:

    def __init__(self, num_points, method_first_gen='seq'):
        self.num_points = num_points
        self.points = self.random_generate()

    def generate_seq_points(self):
        x = [0]
        y = np.zeros(self.num_points)
        for i in range(1, self.num_points):
            x.append(x[i - 1] + i)
        return np.array(list(zip(x, y)))

    def random_generate(self):
        right_border = sum([i for i in range(1, self.num_points + 1)])
        #x = np.linspace(0, right_border, self.num_points)
        #y = np.linspace(0, right_border, self.num_points)
        x = [random.randint(0, right_border) for i in range(self.num_points)]
        y = [random.randint(0, right_border) for i in range(self.num_points)]
        return np.array(list(zip(x, y)))

    def check_distance(self):
        res = set()
        for i in range(len(self.points)):
            point = self.points[i]
            for x, y in self.points[i + 1:]:
                res.add(np.sqrt(np.sum(np.square(point - (x, y)))))
        return len(res) == len(self.points)

    def search_point(self):
        max_dist = 0
        for i in range(len(self.points)):
            point = self.points[i]
            for x, y in self.points[i + 1:]:
                distance = np.sqrt(np.sum(np.square(point - (x, y))))
                if distance > max_dist:
                    max_dist = distance
                    points_max_dist = (point, (x, y))
        return np.array(points_max_dist), max_dist
