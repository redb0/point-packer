import random

from figure import Figure
from circle import Circle
from visualization import vizualizate


class GeneticAlgorithm:

    def __init__(self, num_points, num_agents):
        self.max_iter = 10
        self.num_points = num_points
        self.num_agents = num_agents
        self.population = self.get_population()
        self.circles = self.get_circles()
        self.start()

    def get_population(self):
        return [Figure(self.num_points) for _ in range(self.num_agents)]

    def get_circles(self):
        return sorted([Circle(agent) for agent in self.population], key=Circle.calc_area)

    def start(self):
        for _ in range(self.max_iter):
            # выбираем самых перспективных агентов
            border = self.num_agents // 2
            # пересчитываем популяцию и остальные параметры
            self.circles = self.circles[:border]
            for circle in self.circles:
                # после этого ничего не изменяется
                circle.check_points()
            self.population = [circle.figure for circle in self.circles]
            # создаем новое поколение
            # рандомно выбираем индексы пар для слияния
            count = len(self.population)
            indexes = []
            for i in range(count):
                indexes.append([random.randint(0, count - 1),
                                random.randint(0, count - 1)])
                while indexes[i][0] == indexes[i][1]:
                    indexes[i][1] = random.randint(0, count - 1)
            # выбираем сколько генов (точек) будем менять
            num_genes = self.num_points // 2
            # какие точки меняем
            right = random.randint(1, self.num_points - num_genes)
            # скрещиваем выбранные пары
            child = []
            for idx in indexes:
                parent1 = list(self.population[idx[0]].points)
                parent2 = list(self.population[idx[1]].points)
                child.append(parent1[0:right] + parent2[right:])
                child.append(parent2[0:right] + parent1[right:])
            self.population = [Figure(self.num_points, points=el) for el in child]
            # проверяем уникальность расстояний, удаляем неподходящие
            # в планах делать над ними мутацию, уменьшать координаты
            self.population = [agent for agent in self.population if agent.check_distance() is True]
            self.circles = self.get_circles()
            for circle in self.circles[:2]:
                print(circle.area)
                vizualizate(circle.figure.points, circle.center, circle.radius)
