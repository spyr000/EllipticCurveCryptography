import random
import numpy as np
from mod_utils import get_points
import matplotlib.pyplot as plt


class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.func = np.vectorize(lambda x: x ** 3 + self.a * x + self.b)
        x = np.arange(p)
        y_2 = self.func(x) % p
        self.points = get_points(y_2, p)
        self.general_point = Point(self.points[0], self)

    def set_general_point(self, index):
        point = self.points[index]
        self.general_point = Point((point[0], point[1]), self)


class Point:
    def __init__(self, xy, elliptic_curve: EllipticCurve):
        self.x = xy[0]
        self.y = xy[1]
        self.elliptic_curve = elliptic_curve

    def __mul__(self, other: int):
        if other % self.elliptic_curve.p:
            return Point((0, 0), self.elliptic_curve)
        point = Point((self.x, self.y), self.elliptic_curve)
        result = Point((self.x, self.y), self.elliptic_curve)
        for _ in range(other):
            result = result + point
            print(result)
        return result

    def __add__(self, other):
        if other.get_tuple() == (0, 0):
            return self
        if self == other:
            num = (3 * self.x * self.x + self.elliptic_curve.a) % self.elliptic_curve.p
            den = 2 * self.y % self.elliptic_curve.p
            s = 0
            for m in range(self.elliptic_curve.p):
                if num == 0:
                    break
                elif den == 0:
                    # return Point((other.x, other.y), other.elliptic_curve)
                    return Point((0, 0), other.elliptic_curve)
                elif num == ((den * m) // 1) % self.elliptic_curve.p:
                    s = m
            x_2g = (s ** 2 - 2 * self.x) % self.elliptic_curve.p
            y_2g = -self.y + s * (self.x - x_2g)
            y_2g = y_2g % self.elliptic_curve.p
            return Point((x_2g, y_2g), self.elliptic_curve)
        else:
            num = ((self.y - other.y) % self.elliptic_curve.p)
            den = ((self.x - other.x) % self.elliptic_curve.p)
            s = 0
            for m in range(self.elliptic_curve.p):
                if num == 0:
                    break
                elif den == 0:
                    # return Point((other.x, other.y), other.elliptic_curve)
                    return Point((0, 0), other.elliptic_curve)
                elif num == ((den * m) // 1) % self.elliptic_curve.p:
                    s = m
            x_3g = (s * s - self.x - other.x) % self.elliptic_curve.p
            y_2g = -self.y + s * (self.x - x_3g)
            y_2g = y_2g % self.elliptic_curve.p
            return Point((x_3g, y_2g), self.elliptic_curve)

    def get_tuple(self):
        return self.x, self.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.elliptic_curve)


def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate('',
                       xytext=(xdata[start_ind], ydata[start_ind]),
                       xy=(xdata[end_ind], ydata[end_ind]),
                       arrowprops=dict(arrowstyle="->", color=color),
                       size=size
                       )


if __name__ == '__main__':
    e = EllipticCurve(40, 50, 113)
    print(e.points)
    e.set_general_point(random.randint(0, len(e.points)))
    p = e.general_point
    p = p + p
    i = 0
    plott = plt.plot((e.general_point.x, p.x), (e.general_point.y, p.y), color=(0.1, 0.1, 0.1))[0]
    add_arrow(plott)
    plt.scatter(e.general_point.x, e.general_point.y)
    plt.annotate(
        str(0),
        xy=(e.general_point.x, e.general_point.y), xytext=(-5, 5),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.1', fc='blue', alpha=0.5),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
    )
    plt.annotate(
        str(1),
        xy=(p.x, p.y), xytext=(-5, 5),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.1', fc='blue', alpha=0.5),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
    )
    plt.scatter(p.x, p.y)

    print(p)
    c = 0.1

    while not p == e.general_point:
        i += 1
        c += 0.01
        p_last = p
        p = p + e.general_point
        print(p)
        print(e.general_point)
        plott = plt.plot((p_last.x, p.x), (p_last.y, p.y), color=((0.7 - c) % 1, (0.1 - c) % 1, c % 1))[0]
        add_arrow(plott)
        plt.scatter(p.x, p.y)
        plt.annotate(
            str(i),
            xy=(p.x, p.y), xytext=(-5, 5),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.1', fc='blue', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
            color='white'
        )

    ax = plt.gca()
    ax.set_facecolor('black')
    plt.grid()
    plt.show()
    # e.get_y(13)
