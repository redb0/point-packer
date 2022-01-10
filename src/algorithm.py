import math
import random

from copy import deepcopy
from operator import attrgetter, itemgetter
from itertools import product, groupby

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
        res = []
        for i in range(self.max_iter):
            self.selection()
            child = self.crossing()
            mutated = self.mutation(child)
            self.population = list(self.population) + child + mutated
            self.population = [agent for agent in self.population if not agent.check_distance()]
            self.circles = self.get_circles()
            self.permutation()
            self.circles = self.get_circles()
            if self.circles:
                if self.draw:
                    vizualizate(self.circles[0].figure.points,
                                self.circles[0].center,
                                self.circles[0].radius)
                print(f"Итерация {i} - {self.circles[0].area}")
                res.append(deepcopy(self.circles[0]))
        res = sorted(res, key=attrgetter('area'))
        return res[0]

    def selection(self):
        circles = []
        # выбираем самых перспективных агентов
        border = self.num_agents // 2
        # пересчитываем популяцию и остальные параметры
        self.circles = self.circles[:border]
        for _, group in groupby(self.circles, key=attrgetter('area')):
            circles.extend(list(group)[:1])
        self.circles = circles
        self.population = [circle.figure for circle in self.circles]

    def crossing(self):
        # создаем новое поколение
        # рандомно выбираем индексы пар для слияния
        count = len(self.population)
        indexes = []
        child = []
        # выбираем сколько генов (точек) будем менять
        num_genes = self.num_points // 2
        # до какой точки меняем
        border = random.randint(1, self.num_points - num_genes)
        if count > 1:
            for i in range(count):
                indexes.append([random.randint(0, count - 1),
                                random.randint(0, count - 1)])
                while indexes[i][0] == indexes[i][1]:
                    indexes[i][1] = random.randint(0, count - 1)
            # скрещиваем выбранные пары
            for idx in indexes:
                parent1 = deepcopy(list(self.population[idx[0]].points))
                parent2 = deepcopy(list(self.population[idx[1]].points))
                child.extend([parent1[:border] + parent2[border:],
                              parent2[:border] + parent1[border:]])
            child = [Figure(self.num_points, points=el) for el in child]
        return child

    def mutation(self, child):
        circles = [Circle(agent) for agent in child if not agent.check_distance()]
        mutated = []
        for circle in circles:
            flag = False
            old_figure = [deepcopy(circle.figure)]
            points = list([(np.linalg.norm(point - circle.center), point)
                           for point in circle.figure.points])
            old_point = sorted(points, key=itemgetter(0), reverse=True)[0]
            diameter = int(circles[0].radius * 2)
            # все возможные точки внутри круга
            all_points = list(product(list(range(0, diameter)),
                                      list(range(0, diameter))))
            # удаляем те, которые уже заняты чтобы избежать наложения
            all_points = [point for point in all_points
                          if not any([all(point == p) for p in circle.figure.points])]
            idx = 0
            for i, point in enumerate(circle.figure.points):
                if all(point == old_point[1]):
                    idx = i
            for point in all_points:
                circle.figure.points[idx] = np.array(point)
                result = circle.figure.check_distance()
                if not result:
                    mutated.append(circle.figure)
                    flag = True
                    break
            if not flag:
                idx = random.randint(0, self.num_points - 1)
                for point in all_points:
                    old_figure[0].points[idx] = np.array(point)
                    res = old_figure[0].check_distance()
                    if not res:
                        mutated.append(old_figure[0])
        return mutated

    def permutation(self):
        count = 0
        circles = [deepcopy(self.circles[0])]
        diameter = int(circles[0].radius * 2)
        # все возможные точки внутри круга
        all_points = list(product(list(range(0, diameter + 1)),
                                  list(range(0, diameter + 1))))
        for _ in range(len(self.circles)):
            flag = True
            iterations = len(all_points)
            while iterations:
                iterations -= 1
                points_idx = np.random.choice(range(len(all_points)), self.num_points)
                points = np.array([list(all_points[i]) for i in points_idx])
                figure = Figure(self.num_points, points)
                if not figure.check_distance():
                    circles.append(Circle(figure))
                    break
        circles = [circle for circle in circles if circle.area <= circles[0].area]
        agents = [circle.figure for circle in circles]
        self.population = list(self.population) + agents
        self.circles = self.get_circles()
