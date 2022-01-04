import matplotlib.pyplot as plt


def vizualizate(points, center, radius):
    x = [x for x, y in points]
    y = [y for x, y in points]
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='deeppink')
    circle_patch = plt.Circle(center, radius, fill=False)
    ax.add_patch(circle_patch)
    plt.show()
