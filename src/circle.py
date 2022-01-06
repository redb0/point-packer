import math

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
        delta_x = self.center[0] + self.radius
        delta_y = self.center[1] + self.radius
        count = 0
        for point in self.figure.points:
            if point[0] > delta_x:
                point[0] = round(point[0] - (point[0] - delta_x), 0)
                vizualizate(self.figure.points, self.center, self.radius)
            elif point[1] > delta_y:
                point[1] = round(point[1] - (point[1] - delta_y), 0)
                vizualizate(self.figure.points, self.center, self.radius)
