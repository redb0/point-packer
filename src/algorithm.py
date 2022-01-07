import random
from operator import attrgetter

import numpy as np

from figure import Figure
from circle import Circle
from visualization import vizualizate


class GeneticAlgorithm:

    def __init__(self, max_iter, num_points, num_agents, draw=False):
        self.max_iter = max_iter
        self.num_points = num_points
        self.num_agents = num_agents
        self.draw = draw
        self.population = []
        self.circles = []

    def initialization(self):
        self.population = self.get_population()
        self.circles = self.get_circles()

    def get_population(self):
        return [Figure(self.num_points) for _ in range(self.num_agents)]

    def get_circles(self):
        return sorted([Circle(agent) for agent in self.population], key=attrgetter('area'))

    def start(self):
        self.initialization()
        for _ in range(self.max_iter):
            self.selection()
            child = self.crossing()
            # проверяем уникальность расстояний
            not_success_child = [agent for agent in child if agent.check_distance()]
            success_child = [agent for agent in child if not agent.check_distance()]
            mutated = self.mutation(not_success_child)
            self.population = list(self.population) + list(success_child) + mutated
            self.population = [agent for agent in self.population if not agent.check_distance()]
            self.circles = self.get_circles()
            if self.draw:
                for circle in self.circles[:2]:
                    vizualizate(circle.figure.points, circle.center, circle.radius)
        if self.circles:
            return self.circles[0]

    def selection(self):
        # выбираем самых перспективных агентов
        border = self.num_agents // 2
        # пересчитываем популяцию и остальные параметры
        self.circles = self.circles[:border]
        flag = False
        for circle in self.circles:
            flag = False
            while not flag:
                flag = circle.check_points()
        self.population = [circle.figure for circle in self.circles]

    def crossing(self):
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
        # до какой точки меняем
        right = random.randint(1, self.num_points - num_genes)
        # скрещиваем выбранные пары
        child = []
        for idx in indexes:
            parent1 = list(self.population[idx[0]].points)
            parent2 = list(self.population[idx[1]].points)
            child.extend([parent1[:right] + parent2[right:],
                         parent2[:right] + parent1[right:]])
        child = [Figure(self.num_points, points=el) for el in child]
        return child

    def mutation(self, child):
        circles = [Circle(agent) for agent in child]
        mutated = []
        max_iter = 5
        for circle in circles:
            result = circle.figure.check_distance()
            iterations = 5
            while iterations and result:
                for i, point in enumerate(circle.figure.points):
                    if all(point == result[0][0]):
                        idx = i
                idx = 0
                point = circle.figure.points[idx]
                x, y = abs(point - circle.center)
                if x > y:
                    point[0] += 1 if point[0] < circle.center[0] else -1
                else:
                    point[1] += 1 if point[1] < circle.center[1] else -1
                result = circle.figure.check_distance()
                iterations -= 1
            if not result:
                mutated.append(circle.figure)
        return mutated



