import random
from operator import attrgetter

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
            self.crossing()
            if self.draw:
                for circle in self.circles[:2]:
                    vizualizate(circle.figure.points, circle.center, circle.radius)
        print(f"Минимальная площадь - {self.circles[0].area}")

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
        # какие точки меняем
        right = random.randint(1, self.num_points - num_genes)
        # скрещиваем выбранные пары
        child = []
        parents = list(self.population)
        for idx in indexes:
            parent1 = list(self.population[idx[0]].points)
            parent2 = list(self.population[idx[1]].points)
            child.extend([parent1[:right] + parent2[right:],
                         parent2[:right] + parent1[right:]])
        self.population = [Figure(self.num_points, points=el) for el in child]
        # проверяем уникальность расстояний, удаляем неподходящие
        # в планах делать над ними мутацию, уменьшать координаты
        self.population = [agent for agent in self.population if agent.check_distance()]
        self.population = parents + self.population
        self.circles = self.get_circles()
