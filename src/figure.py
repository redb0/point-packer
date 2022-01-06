import itertools
import random
import numpy as np


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
        flag = False
        while not flag:
            self.points = self.random_generate()
            flag = self.check_distance()

    def random_generate(self):
        """ Генерация точек в рандомном месте в заданном интервале
        :return: массив точек
        """
        right_border = sum([1, self.num_points + 1])
        x = np.random.randint(0, right_border, self.num_points)
        y = np.random.randint(0, right_border, self.num_points)
        return np.array(list(zip(x, y)))

    def check_distance(self):
        """ Проверка условия, расстояния между всеми парами точек
        должны быть уникальны
        :return: True в случае выполнения условия
                 False в противном случае
        """
        res = set()
        comb = itertools.combinations(self.points, 2)
        size = 0
        for pair in comb:
            size += 1
            res.add(np.linalg.norm(pair[0] - pair[1]))
        return len(res) == size

    def search_point(self):
        """ Поиск двух наиболее удаленных друг от друга точек
        :return: массив с координатами двух точек и расстояние между ними
        """
        max_dist = 0
        comb = itertools.combinations(self.points, 2)
        for pair in comb:
            distance = np.linalg.norm(pair[0] - pair[1])
            if distance > max_dist:
                max_dist = distance
                points_max_dist = (pair[0], pair[1])
        return np.array(points_max_dist), max_dist
