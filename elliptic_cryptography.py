import random

import numpy as np
import sympy
import random
from elliptic_curve import EllipticCurve, Point
import matplotlib.pyplot as plt
from alphabet import get_char, LENGTH


class Cryptographer:
    def __init__(self, e, max_prime_index=100):
        self.e = e
        self.closed_key = random.randint(1, prime - 1)
        # self.closed_key = 5

        # while len(self.e.points) < LENGTH:
        #     prime = sympy.prime(random.randint(sympy.nextprime(LENGTH), max_prime_index))
        #     a = random.randint(0, prime - 1)
        #     b = random.randint(0, prime - 1)
        #     self.e = EllipticCurve(a, b, prime)
        self.dictionary = {}

    def generate_path(self,ind= None):
        i = 1
        # выбираем случайно генеральную точку из всех точек эллиптической кривой
        plt.close()

        if ind is None:
            index = random.randint(0, len(self.e.points) - 1)
        else:
            index = ind
        print('general point', index)
        self.e.set_general_point(index)
        point = self.e.general_point
        self.dictionary.update({get_char(i): point.get_tuple()})
        self.g = [point]
        print(get_char(i), point)
        point = point + point

        # если 2G = G выбираем другую генеральную точку из всех точек эллиптической кривой
        while point.get_tuple() == (0, 0):
            # while not point == self.e.general_point:
            if ind is None:
                index = random.randint(0, len(self.e.points) - 1)
            else:
                index = ind
            # index = 0
            print('general point', index)
            self.e.set_general_point(index)
            self.dictionary = {}
            point = self.e.general_point
            self.dictionary.update({get_char(i): point.get_tuple()})
            self.g = [point]
            point = point + point

        i += 1
        self.dictionary.update({get_char(i): point.get_tuple()})
        self.g.append(point)

        # region plot
        plt.rcParams['figure.figsize'] = [20, 10]
        line = plt.plot((self.e.general_point.x, point.x), (self.e.general_point.y, point.y), color=(0.1, 0.1, 0.1))[0]
        add_arrow(line)

        plt.scatter(self.e.general_point.x, self.e.general_point.y)
        plt.annotate(
            str(0),
            xy=(self.e.general_point.x, self.e.general_point.y), xytext=(-5, 5),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.1', fc='blue', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )

        plt.annotate(
            str(1),
            xy=(point.x, point.y), xytext=(-5, 5),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.1', fc='blue', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )
        plt.scatter(point.x, point.y)
        # endregion
        print(get_char(i), point)
        color_val = 0.1

        while not point.get_tuple() == (0, 0):
            # while not point == self.e.general_point:
            i += 1
            color_val += 0.01
            p_last = point

            # рассчитываем новую точку
            point = point + self.e.general_point
            self.g.append(point)
            # if not point == self.e.general_point:
            self.dictionary.update({get_char(i): point.get_tuple()})
            print(get_char(i), point)
            # region plot
            line = plt.plot((p_last.x, point.x), (p_last.y, point.y),
                            color=((0.7 - color_val) % 1, (0.1 - color_val) % 1, color_val % 1))[0]
            add_arrow(line)

            plt.scatter(point.x, point.y)
            plt.annotate(
                str(i),
                xy=(point.x, point.y), xytext=(-5, 5),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.1', fc='blue', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                color='white'
            )
            endregion
        print('closed key',self.closed_key)
        print('g len',len(self.g))
        self.open_key = self.g[self.closed_key % len(self.g) - 1]
        # составляем словарь точка - номер
        self.point_to_num = dict(zip([i.get_tuple() for i in self.g], np.arange(1, len(self.g) + 1)))
        # составляем словарь точка - буква
        self.reverse_dict = {}
        for k, v in self.dictionary.items():
            self.reverse_dict.update({v: k})
        print('reversed dict', end=' ')
        for k, v in self.reverse_dict.items():
            print(f'{k}: {v}', end=' ')

        # если точек меньше чем в алфавите то начинаем генерацию заново
        # while len(self.dictionary) < LENGTH:
        #     print(len(self.dictionary))
        #     print(self.dictionary)
        #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     plt.figure().clear()
        #     self.generate_path()
        print('dictionary', self.dictionary)
        return index

    def encode(self, message: str, open_key: Point):
        print('point_to_num', self.point_to_num)
        print('g_list', self.g)
        cipher = ''
        open_key_num = self.point_to_num[open_key.get_tuple()]
        # n * P
        k = self.closed_key * open_key_num

        g_len = len(self.g)
        for sym in message:
            # номер точки для символа сообщения + n * P = номер новой точки
            num = self.point_to_num[self.dictionary[sym]] + k
            # ищем точку соответствующую номеру

            p_c = self.g[num % g_len - 1]
            # пишем в шифр букву соответствующую точке вычисленной выше
            cipher += self.reverse_dict[p_c.get_tuple()]
        print(cipher)

        return cipher

    def decode(self, cipher, open_key: Point):
        message = ''
        # self.closed_key = 9
        open_key_num = self.point_to_num[open_key.get_tuple()]
        k = self.closed_key * open_key_num
        # print('k', k)
        g_len = len(self.g)
        for sym in cipher:
            num = self.point_to_num[self.dictionary[sym]] - k
            # print('num', self.point_to_num[self.dictionary[sym]])
            # print('index', num % g_len)
            p_m = self.g[num % g_len - 1]

            message += self.reverse_dict[p_m.get_tuple()]
        print(message)
        return message


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


