from elliptic_cryptography import Cryptographer
from elliptic_curve import EllipticCurve, Point
import random
import sympy
from alphabet import LENGTH
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # prime = 11
    # a = 1
    # b = 6
    max_prime_index = 200
    prime = sympy.prime(random.randint(sympy.nextprime(LENGTH), max_prime_index))
    a = random.randint(0, prime - 1)
    b = random.randint(0, prime - 1)
    elliptic_curve = EllipticCurve(a, b, prime)
    sender = Cryptographer(elliptic_curve)
    receiver = Cryptographer(elliptic_curve)
    index = sender.generate_path()
    receiver.generate_path(ind=index)
    print('sender', sender.e.points)
    print('receiver', receiver.e.points)
    c = sender.encode('бедалже', receiver.open_key)
    receiver.decode(c, sender.open_key)
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.grid()
    plt.show()
