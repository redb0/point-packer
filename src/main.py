from figure import Figure
from circle import Circle
from visualization import vizualizate
from algorithm import GeneticAlgorithm


def main():
    gen = GeneticAlgorithm(max_iter=5, num_points=6, num_agents=6)
    gen.start()

if __name__ == "__main__":
    main()
