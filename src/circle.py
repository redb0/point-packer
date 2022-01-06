import math

from figure import Figure


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

    @area.setter
    def area(self):
        return self.area

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
