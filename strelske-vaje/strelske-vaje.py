import math

# Napiši program za izračun dolžine strela s topom (ki brez trenja izstreljuje točkaste krogle v brezzračnem
# prostoru, a pustimo trivio). Program od uporabnika ali uporabnice zahteva, da mu ta vpiše hitrost izstrelka in kot,
# pod katerim je izstreljena (krogla, ne uporabnica). Program izračuna in izpiše, kako daleč bo letela krogla.
#
# Pomoč za fizično nebogljene: s=v2sin2ϕg, kjer je s razdalja, v hitrost izstrelka, ϕ je kot, g pa osma črka
# slovenske abecede.
#
# Preverite tole: krogla leti najdalj, če jo izstrelimo pod kotom 45 stopinj. Poskusite, kako daleč gre pod kotom 45
# in kako daleč pod 46 stopinj - po 45 mora leteti dlje. In če pod kotom 50 stopinj leti nazaj (razdalja je
# negativna), ste ga gotovo nekje polomili. Kaj, točno, je narobe, vam lahko hitro sčveka kolega, ki je že rešil
# problem, vendar vam priporočam, da ga poskusite odkriti sami - za vajo v sledenju programu. Za namig lahko
# poškilite na del Wikipedijine strani o kotih.
#
# Ali program deluje pravilno, lahko preverite tudi tako, da na roko izračunate, kako daleč leti krogla,
# ki jo izstrelite pod kotom 45 stopinj s hitrostjo 10 m/s in primerjate rezultat s tem, kar vrne program.

g = 9.82


def distance(v, phi):
    return (v ** 2 * math.sin(2 * phi)) / g


velocity = 10
print("razdalja pri kotu 90 stopinj: %d" % distance(velocity, math.pi / 2))
print("razdalja pri kotu 45 stopinj: %d" % distance(velocity, math.pi / 4))
print("razdalja pri kotu >45 stopinj: %d" % distance(velocity, math.pi / 3))
print("razdalja pri kotu <45 stopinj: %d" % distance(velocity, math.pi / 8))
