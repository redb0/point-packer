import matplotlib.pyplot as plt


def vizualizate(points, center, radius):
    """ Визуализация точек и окружности """
    x = [x for x, _ in points]
    y = [y for _, y in points]
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='deeppink')
    circle_patch = plt.Circle(center, radius, fill=False)
    ax.add_patch(circle_patch)
    ax.set_xlim([min(x) - 5, max(x) + 5])
    ax.set_ylim([min(x) - 5, max(x) + 5])
    plt.axis('equal')
    plt.show()
