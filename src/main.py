from figure import Figure
from circle import Circle
from visualization import vizualizate
from algorithm import GeneticAlgorithm


def main():
    gen = GeneticAlgorithm(max_iter=3, num_points=10, num_agents=50)
    circle = gen.start()
    if circle:
        vizualizate(circle.figure.points, circle.center, circle.radius)
        print(f"Минимальная площадь - {circle.area}")

if __name__ == "__main__":
    main()
