import random
import numpy as np
from itertools import product, combinations


class Figure:
    """ Класс фигуры (многоугольника)

    Атрибуты класса:
        num_points      : количество точек многоугольника
        points          : координаты точек многоугольника

    Методы класса:
        generate():
            Генерирует точки по заданному методу
        random_generate():
            Генерация точек в рандомном месте в заданном интервале
        check_distance():
            Проверка условия, расстояния между всеми парами точек
            должны быть уникальны
        search_point():
            Поиск двух наиболее удаленных друг от друга точек
    """

    def __init__(self, num_points, points=None):
        self.num_points = num_points
        self.points = points
        if self.points is None:
            self.generate()

    def generate(self):
        """ Генерирует точки по заданному методу """
        flag = True
        k = 1
        while flag:
            self.points = self.random_generate()
            flag = self.check_distance()
            # print('k =', k)
            k += 1

    def random_generate(self):
        """ Генерация точек в рандомном месте в заданном интервале
        :return: массив точек
        """
        right_border_dist = []
        for i in range(1, self.num_points + 1):
            if right_border_dist:
                d = right_border_dist + [sum(item) for item in combinations(right_border_dist, 2)]
                while i in d:
                    i += 1
                right_border_dist.append(i)
            else:
                right_border_dist.append(i)
        right_border = sum(right_border_dist)
        # right_border = sum([1, self.num_points * 2])
        # points = np.zeros((self.num_points, 2))
        # points = np.full((self.num_points, 2), fill_value=np.nan)
        all_points = list(product(list(range(right_border)), repeat=2))
        points_idx = np.random.choice(range(len(all_points)), self.num_points)
        points = np.array([list(all_points[i]) for i in points_idx])
        # for i in range(self.num_points):
        #     x = np.random.randint(0, right_border)
        #     y = np.random.randint(0, right_border)
        # x = np.random.randint(0, right_border, self.num_points)
        # y = np.random.randint(0, right_border, self.num_points)
        # print(points)
        # return np.array(list(zip(x, y)))
        return points

    def check_distance(self):
        """ Проверка условия, расстояния между всеми парами точек
        должны быть уникальны
        :return: True в случае выполнения условия
                 False в противном случае
        """
        distances = set()
        comb = combinations(self.points, 2)
        pairs = []
        for pair in comb:
            distance = np.linalg.norm(pair[0] - pair[1])
            if distance:
                if distance in distances:
                    pairs.append(pair)
                distances.add(distance)
        if not pairs:
            return None
        return pairs

    def search_point(self):
        """ Поиск двух наиболее удаленных друг от друга точек
        :return: массив с координатами двух точек и расстояние между ними
        """
        max_dist = 0
        comb = combinations(self.points, 2)
        for pair in comb:
            distance = np.linalg.norm(pair[0] - pair[1])
            if distance > max_dist:
                max_dist = distance
                points_max_dist = (pair[0], pair[1])
        return np.array(points_max_dist), max_dist
