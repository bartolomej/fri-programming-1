# Tu dodajte svoje razrede

from random import uniform
from math import *
from risar import krog, pobrisi

w_size = (800, 500)


class Vector:
    def __init__(self, x=1.0, y=1.0, angle=None, mag=1.0):
        # moznost inicializacije tudi z smerjo in magnitudo
        if type(angle) is float:
            self.x = mag * cos(angle)
            self.y = mag * sin(angle)
        else:
            self.x = x
            self.y = y

    @property
    def angle(self):
        return atan2(self.y, self.x)

    @angle.setter
    def angle(self, new_angle):
        mag = abs(self)
        self.x = mag * cos(new_angle)
        self.y = mag * sin(new_angle)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError('Hopsa fantic tole pa nebo uredu!')

    def __mul__(self, other):
        if type(other) is float:
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError('Hopsa fantic tole pa nebo uredu!')

    def __abs__(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def __str__(self):
        return f"<{self.x}, {self.y}>"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('Hopsa tole je pa samo 2d vektor')


class Oseba:

    def __init__(self):
        w, h = w_size
        self.radius = 5
        self.hitrost = Vector(angle=uniform(0, 2 * pi), mag=uniform(0, 5))
        self.pozicija = Vector(uniform(0, w), uniform(0, h))

    def premik(self):
        self.preveri_zadetke()
        self.hitrost.angle += radians(uniform(-20, 20))
        self.pozicija += self.hitrost
        pobrisi()
        krog(self.pozicija.x, self.pozicija.y, r=self.radius)

    def preveri_zadetke(self):
        w, h = w_size
        x, y = self.pozicija
        # preveri zadetke za obe dimenziji
        # ce je oseba zadela ob rob samo obrnemo primerno komponento vektorja hitrosti
        if x <= self.radius or x + self.radius >= w:
            self.hitrost.x *= -1
        if y <= self.radius or y + self.radius >= h:
            self.hitrost.y *= -1


# Vse od tod naprej pustite pri miru

import risar


def main():
    # Tole poskrbi, da razred navidez dobi metode, ki jih še nisi sprogramiral(a)
    # Tega ni potrebno razumeti. Ignoriraj.

    from unittest.mock import Mock
    from itertools import count

    if hasattr(Oseba, "premik") and Oseba.premik.__code__.co_argcount == 1:
        Oseba.premik = lambda self, osebe, f=Oseba.premik: f(self)

    for method in ("premik", "okuzi_se", "okuzi_bliznje", "zdravi_se"):
        if not hasattr(Oseba, method):
            setattr(Oseba, method, Mock())

    globals().setdefault("nijz", None)

    osebe = [Oseba() for _ in range(100)]
    for oseba in osebe[:5]:
        oseba.okuzi_se()
    for oseba in osebe:
        if hasattr(Oseba, "vrni_krog") and hasattr(Oseba, "v_izolacijo"):
            oseba.vrni_krog().setOnClick(oseba.v_izolacijo)

    for cas in count():
        for oseba in osebe:
            oseba.zdravi_se()
            oseba.okuzi_bliznje(osebe)
            oseba.premik(osebe)
        if nijz and cas % 10 == 0:
            nijz.porocaj()
        risar.cakaj(0.02)
        # TODO: popravit je treba flickering pri prisanju
        # pobrisi()

def custom_tests():
    from itertools import count
    osebe = [Oseba() for _ in range(100)]

    for cas in count():
        for oseba in osebe:
            oseba.premik()
        risar.cakaj(0.02)
        pobrisi()

if __name__ == '__main__':
    main()