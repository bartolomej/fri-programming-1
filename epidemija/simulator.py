# Tu dodajte svoje razrede

from random import uniform
from math import *
from risar import *

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

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError('Hopsa fantic tole pa nebo uredu!')

    def __sub__(self, other):
        return self + (-other)

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
        self.okuzena = False
        self.radius = 5
        self.hitrost = Vector(angle=uniform(0, 2 * pi), mag=uniform(0, 5))
        self.pozicija = Vector(uniform(0, w), uniform(0, h))
        self.krog = krog(self.pozicija.x, self.pozicija.y, self.radius)
        self.st_korakov_do_ozdravljenja = 150
        self.korak_zdravljenja = self.st_korakov_do_ozdravljenja
        self.st_korakov_v_izolaciji = 101
        self.korak_izolacije = self.st_korakov_v_izolaciji

    def premik(self, osebe):
        if self.je_izolirana():
            for o in osebe:
                if abs(o.pozicija - self.pozicija) <= 20:
                    o.hitrost.angle += radians(180)
        if self.korak_izolacije == 0:
            self.korak_izolacije = self.st_korakov_v_izolaciji
            zapolni(self.krog, risar.crna)
        elif self.korak_izolacije < self.st_korakov_v_izolaciji:
            self.korak_izolacije -= 1
            risar.zapolni(self.krog, risar.rumena)
            return
        self.preveri_zadetke()
        self.hitrost.angle += radians(uniform(-20, 20))
        self.pozicija += self.hitrost
        self.narisi()

    def narisi(self):
        spremeni_barvo(self.krog,
                       risar.zelena if 0 == self.korak_zdravljenja else risar.rdeca if self.okuzena else risar.bela)
        premakni_na(self.krog, self.pozicija.x, self.pozicija.y)

    def preveri_zadetke(self):
        w, h = w_size
        x, y = self.pozicija
        # preveri zadetke za obe dimenziji
        # ce je oseba zadela ob rob samo obrnemo primerno komponento vektorja hitrosti
        if x <= self.radius or x + self.radius >= w:
            self.hitrost.x *= -1
        if y <= self.radius or y + self.radius >= h:
            self.hitrost.y *= -1

    def okuzi_se(self):
        # ozdravljene so tiste osebe, ki jim je ostalo 0 korakov zdravljenja
        # zdravijo se tiste osebe, ki imajo stevilo korakov zdravljenja med 0 in 150
        if not self.korak_zdravljenja == 0 or self.korak_zdravljenja == self.st_korakov_do_ozdravljenja:
            self.okuzena = True
            nijz.sporoci_okuzbo()

    def se_dotikata(self, oseba):
        return abs(self.pozicija - oseba.pozicija) <= self.radius + oseba.radius

    def okuzi_bliznje(self, osebe):
        for o in osebe:
            if self.okuzena and self.se_dotikata(o) and o is not self:
                o.okuzi_se()

    def zdravi_se(self):
        if self.okuzena and self.korak_zdravljenja > 0:
            self.korak_zdravljenja -= 1
        elif self.korak_zdravljenja == 0:
            self.okuzena = False
            nijz.sporoci_ozdravitev()

    def vrni_krog(self):
        return self.krog

    def v_izolacijo(self):
        self.korak_izolacije -= 1

    def je_izolirana(self):
        return self.korak_izolacije < self.st_korakov_v_izolaciji


class NIJZ:
    def __init__(self):
        self.okuzbe = [0, 0]
        self.ozdravitve = [0, 0]
        self.graf_okuzb = []
        self.graf_ozdravitev = []

    def sporoci_okuzbo(self):
        self.okuzbe[-1] += 1

    def sporoci_ozdravitev(self):
        self.ozdravitve[-1] += 1

    def porocaj(self):
        w, h = w_size
        x_scale = 8
        y_scale = lambda y: y if y == 0 else log(y) * 20
        oky0, oky1 = list(map(y_scale, self.okuzbe[-2:]))
        ozy0, ozy1 = list(map(y_scale, self.ozdravitve[-2:]))
        x0, x1 = ((len(self.okuzbe) - 1) * x_scale, len(self.okuzbe) * x_scale)
        # narisi graf okuzb in ozdravitev
        self.graf_okuzb.append(risar.crta(x0, h - oky0, x1, h - oky1, barva=risar.rdeca))
        self.graf_ozdravitev.append(risar.crta(x0, h - ozy0, x1, h - ozy1, barva=risar.zelena))
        self.okuzbe.append(0)
        self.ozdravitve.append(0)


nijz = NIJZ()
stevilo_oseb = 150

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

    osebe = [Oseba() for _ in range(stevilo_oseb)]
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


if __name__ == '__main__':
    main()
