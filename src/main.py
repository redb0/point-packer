from figure import Figure
from circle import Circle
from visualization import vizualizate


def main():
    fig = Figure(4)
    circle = Circle(fig)
    vizualizate(fig.points, circle.center, circle.radius)


if __name__ == "__main__":
    main()
