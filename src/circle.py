import math

from figure import Figure
from visualization import vizualizate
from find_circle import make_circle


class Circle:
    """ Класс окружности

    Атрибуты класса:
        figure  : экземпляр класса Figure, многоугольник вокруг которого
                  необходимо описать окружность
        radius  : радиус окружности
        center  : центр окружности
        area    : площадь окружности

    Методы класса:
        area():
            Расчет площади окружности
    """

    def __init__(self, figure):
        self.figure = figure
        self.center, self.radius = make_circle(self.figure.points)

    @property
    def area(self):
        return self.radius ** 2 * math.pi
