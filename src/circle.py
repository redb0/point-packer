import math
import numpy as np

from figure import Figure
from visualization import vizualizate


class Circle:
    """ Класс окружности

    Атрибуты класса:
        figure  : экземпляр класса Figure, многоугольник вокруг которого
                  необходимо описать окружность
        radius  : радиус окружности
        center  : центр окружности
        area    : площадь окружности

    Методы класса:
        calc_radius():
            Расчет радиуса окружности
        calc_center():
            Расчет центра окружности
        calc_area():
            Расчет площади окружности
    """

    def __init__(self, figure):
        self.figure = figure
        self.radius = self.calc_radius()
        self.center = self.calc_center()

    @property
    def area(self):
        return self.radius ** 2 * math.pi

    def calc_radius(self):
        """ Расчет радиуса окружности
        :return: радиус окружности
        """
        _, max_dist = self.figure.search_point()
        return max_dist / 2

    def calc_center(self):
        """ Расчет центра окружности
        :return: центр окружности
        """
        points, _ = self.figure.search_point()
        return ((points[0][0] + points[1][0]) / 2,
                (points[0][1] + points[1][1]) / 2)

    def check_points(self):
        """ Проверять на попадание в окружность всех точек """
        flag = True
        for point in self.figure.points:
            distance = np.linalg.norm(point - self.center)
            if distance > self.radius:
                x, y = abs(point - self.center)
                if x > y:
                    point[0] += 1 if point[0] < self.center[0] else -1
                else:
                    point[1] += 1 if point[1] < self.center[1] else -1
                flag = False
        return flag
