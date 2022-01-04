from src.figure import Figure
from visualization import vizualizate


def main():
    fig = Figure(3)
    points, max_dist = fig.search_point()
    mid = ((points[0][0] + points[1][0]) / 2,
           (points[0][1] + points[1][1]) / 2)
    vizualizate(fig.points, mid, max_dist / 2)


if __name__ == "__main__":
    main()
