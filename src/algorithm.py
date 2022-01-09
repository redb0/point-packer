import random

from copy import deepcopy
from collections import Counter
from operator import attrgetter, itemgetter
from itertools import product

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
            for circle in self.circles:
                flag = False
                while not flag:
                    flag = circle.check_points()
            self.population = [circle.figure for circle in self.circles
                               if not circle.figure.check_distance()]
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
        # выбираем самых перспективных агентов
        border = self.num_agents // 2
        # пересчитываем популяцию и остальные параметры
        circles = self.circles[:border]
        flag = False
        # начинаем проверку, чтобы все точки лежали в окружности
        for circle in circles:
            flag = False
            while not flag:
                flag = circle.check_points()
        # после перестроения точек снова проверяем уникальность расстояний
        circles = [circle for circle in circles if not circle.figure.check_distance()]
        # все удачные построения становятся популяцией
        self.population = [circle.figure for circle in circles]

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
        border = random.randint(1, self.num_points - num_genes)
        # скрещиваем выбранные пары
        child = []
        for idx in indexes:
            parent1 = deepcopy(list(self.population[idx[0]].points))
            parent2 = deepcopy(list(self.population[idx[1]].points))
            child.extend([parent1[:border] + parent2[border:],
                          parent2[:border] + parent1[border:]])
        child = [Figure(self.num_points, points=el) for el in child]
        return child

    def mutation(self, child):
        circles = [Circle(agent) for agent in child]
        mutated = []
        unmutated = []
        for circle in circles:
            iterations = 5
            old_figure = [deepcopy(circle.figure)]
            while iterations:
                iterations -= 1
                points = list([(np.linalg.norm(point - circle.center), point)
                               for point in circle.figure.points])
                point = sorted(points, key=itemgetter(0), reverse=True)[0]
                x, y = abs(point[1] - circle.center)
                if x > y:
                    point[1][0] += 1 if point[1][0] < circle.center[0] else -1
                else:
                    point[1][1] += 1 if point[1][1] < circle.center[1] else -1
                result = circle.figure.check_distance()
                if not result:
                    mutated.append(circle.figure)
                    break
                elif not iterations:
                    unmutated.append(old_figure[0])
        # мутация для немутировавших
        circles = [Circle(agent) for agent in unmutated]
        for circle in circles:
            x = int(circle.center[0] - circle.radius)
            y = int(circle.center[1] - circle.radius)
            diameter = int(circle.radius * 2)
            # все возможные точки внутри круга
            all_points = list(product(list(range(x, x + diameter)),
                                      list(range(y, y + diameter))))
            # удаляем те, которые уже заняты чтобы избежать наложения
            all_points = [point for point in all_points
                          if not any([all(point == p) for p in circle.figure.points])]
            idx = random.randint(0, self.num_points - 1)
            for point in all_points:
                circle.figure.points[idx] = np.array(point)
                res = circle.figure.check_distance()
                if not res:
                    mutated.append(circle.figure)
        return mutated

    def permutation(self):
        count = 0
        circles = [deepcopy(self.circles[0])]
        x = int(circles[0].center[0] - circles[0].radius)
        y = int(circles[0].center[1] - circles[0].radius)
        diameter = int(circles[0].radius * 2)
        # все возможные точки внутри круга
        all_points = list(product(list(range(x, x + diameter)),
                                  list(range(y, y + diameter))))
        for i in range(len(self.circles)):
            flag = True
            iterations = len(all_points)
            while flag and iterations:
                points_idx = np.random.choice(range(len(all_points)), self.num_points)
                points = np.array([list(all_points[i]) for i in points_idx])
                figure = Figure(self.num_points, points)
                flag = figure.check_distance()
                iterations -= 1
            circles.append(Circle(figure))
        circles = [circle for circle in circles if circle.area < circles[0].area]
        agents = [circle.figure for circle in circles]
        self.population = list(self.population) + agents
        self.circles = self.get_circles()
