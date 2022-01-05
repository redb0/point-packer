import random
import numpy as np


class Figure:
    """ Класс фигуры (многоугольника)

    Атрибуты класса:
        num_points      : количество точек многоугольника
        method_generate : способ первой генерации точек на плоскости
                          (рандом или последовательность точек на прямой)
    Методы класса:
        choice_method_generate():
            Генерирует точки по заданному методу
        generate_seq():
            Генерация точек на прямой
        random_generate():
            Генерация точек в рандомном месте в заданном интервале
        check_distance():
            Проверка условия, расстояния между всеми парами точек
            должны быть уникальны
        search_point():
            Поиск двух наиболее удаленных друг от друга точек
    """

    def __init__(self, num_points, method_generate='r'):
        self.num_points = num_points
        self.method_generate = method_generate
        self.choice_method_generate()

    def choice_method_generate(self):
        """ Генерирует точки по заданному методу """
        if self.method_generate == 'r':
            self.points = self.random_generate()
        else:
            self.points = self.generate_seq()

    def generate_seq(self):
        """ Генерация точек на прямой
        :return: массив точек
        """
        x = [0]
        y = np.zeros(self.num_points)
        for i in range(1, self.num_points):
            x.append(x[i - 1] + i)
        return np.array(list(zip(x, y)))

    def random_generate(self):
        """ Генерация точек в рандомном месте в заданном интервале
        :return: массив точек
        """
        right_border = sum([i for i in range(1, self.num_points + 1)])
        x = [random.randint(0, right_border) for i in range(self.num_points)]
        y = [random.randint(0, right_border) for i in range(self.num_points)]
        return np.array(list(zip(x, y)))

    def check_distance(self):
        """ Проверка условия, расстояния между всеми парами точек
        должны быть уникальны
        :return: True в случае выполнения условия
                 False в противном случае
        """
        res = set()
        for i, point in enumerate(self.points):
            for x, y in self.points[i + 1:]:
                res.add(np.sqrt(np.sum(np.square(point - (x, y)))))
        return len(res) == len(self.points)

    def search_point(self):
        """ Поиск двух наиболее удаленных друг от друга точек
        :return: массив с координатами двух точек и расстояние между ними
        """
        max_dist = 0
        for i, point in enumerate(self.points):
            for x, y in self.points[i + 1:]:
                distance = np.sqrt(np.sum(np.square(point - (x, y))))
                if distance > max_dist:
                    max_dist = distance
                    points_max_dist = (point, (x, y))
        return np.array(points_max_dist), max_dist
