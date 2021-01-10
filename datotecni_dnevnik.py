import re


# vrne datum kot terko (leto, mesec, dan). Klic datum("5/15/1970 file with spaces.avi 42") vrne (1970, 5, 15).
def datum(line):
    d = list(map(int, re.compile("[/ ]").split(line)[0:3]))
    return d[2], d[0], d[1]


# vrne dolžino datoteke. Klic datum("5/15/1970 file with spaces.avi 42") vrne 42.
def dolzina(line):
    return int(re.compile('[ ]+').split(line)[-1:][0])


# vrne ime datoteke. Klic ime("5/15/1970 file with spaces.avi 42") vrne niz "file with spaces.avi".
def ime(line):
    # return " ".join(re.compile('[ ]+').split(line)[1:-1])
    s = re.compile('[ ]+').split(line)
    return (line.replace(s[0], "")).replace(s[-1], "").strip()


#  vrne terko z gornjimi podatki.
#  Klic podatki("5/15/1970 file with spaces.avi 42") vrne ((1970, 5, 15), file with spaces.avi", 42).
def podatki(line):
    return datum(line), ime(line), dolzina(line)


# prejme dve vrstici in vrne True, če ima s1 novejši (kasnejši) datum kot s2, in False, če ne.
# Klic je_novejsa("11/16/2020 ime.txt 316", "11/15/2015 foo.txt 314") vrne True.
def je_novejsa(s1, s2):
    return datum(s1) > datum(s2)


# prejme ime datoteke in seznam, kot je na začetku naloge.
# Vrniti mora podatke o datoteki v času zadnje spremembe.
# Klic najnovejsa("ime dat.avi", arhiv) (pri čemer je arhiv takšen,
# kot je definiran zgoraj) vrne ((2020, 10, 16), "ime_dat.avi", 314236),
# saj so to podatki o datoteki, kot je bila shranjena na zadnjega izmed štirih datumov, ko smo spreminjali to datoteko.
def najnovejsa(ime_datoteke, arhiv):
    max_data = None
    max_date = None
    for line in arhiv:
        if re.search(ime_datoteke, line):
            if max_date is None or datum(line) > max_date:
                max_date = datum(line)
                max_data = podatki(line)
    return max_data


# vrne datume sprememb podane datoteke.
# Datumi morajo biti urejeni od kasnejših proti starejšim.
# Klic datumi("ime dat.avi", arhiv) vrne [(2020, 10, 16), (2020, 10, 14), (2020, 5, 16), (2018, 12, 31)].
# Če datoteke s podanim imenom sploh ni, pač vrne prazen seznam.
def datumi(ime_datoteke, arhiv):
    dates = []
    for line in arhiv:
        if re.search(ime_datoteke, line):
            dates.append(datum(line))
    dates.sort(reverse=True)
    return dates


# iz podanega seznama arhiv odstrani vse vrstice, ki se nanašajo na datoteko s podanim imenom.
# Klic odstrani("ime dat.avi", arhiv) spremeni gornji seznam v
# arhiv = ["10/16/2020 some other.avi 314236",
#          "1/1/1970    file   with spaces.avi 42",
#          "10/18/2020 another file.avi 351352",
#          "10/18/2018 another file.avi 314236"]
def odstrani(ime_datoteke, arhiv):
    # https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python#answer-529427
    # reversed function reverses a list and allows you to access original indexes (in revesed order)
    for i, line in reversed(list(enumerate(arhiv))):
        if re.search(ime_datoteke, line):
            del arhiv[i]


# ------- DODATNA NALOGA -------

# Napiši funkcijo skupna_dolzina(arhiv), ki vrne skupno dolžino vseh datotek v arhivu. Klic
# skupna_dolzina([
#     "10/14/2020 ime dat.avi   1",
#     "5/16/2020   ime dat.avi 2",
#     "10/16/2020 ime dat.avi 4",
#     "12/31/2018   ime dat.avi 8",
#     "10/16/2020 some other.avi 16",
#     "10/18/2020 another file.avi 32",
#     "10/18/2018 another file.avi 64",
# ]
# vrne 52 (4 + 16 + 32). Upoštevati mora, očitno, le zadnje različice datotek.
def skupna_dolzina(arhiv):
    sum_dict = {}
    date_dict = {}
    for line in arhiv:
        d = datum(line)
        n = ime(line)
        c = date_dict.get(n)
        # ce je najden novejsa datoteka, povozi star zapis v date_dict
        # ter si zapomni velikost te datoteke v sum_dict
        if c is None or c < d:
            date_dict[n] = d
            sum_dict[n] = dolzina(line)
    # ko smo nasli vse najnovejse zapise lahko samo sestejemo vrednosti ki lezijo za vsakem kljucem
    s = 0
    for k in sum_dict:
        s = s + sum_dict[k]
    return s


import unittest
from random import shuffle


class TestObvezna(unittest.TestCase):
    def test_ime(self):
        self.assertEqual("ime_datoteke.md", ime("11/16/2020 ime_datoteke.md 314236"))
        self.assertEqual("ime datoteke s presledki.md", ime("11/6/2015 ime datoteke s presledki.md 123"))
        self.assertEqual("ime  s     presledki.md", ime("11/16/2020 ime  s     presledki.md 436"))
        self.assertEqual("ime  s     presledki.md", ime("1/6/2020     ime  s     presledki.md   0"))

    def test_dolzina(self):
        self.assertEqual(314236, dolzina("11/16/2020 ime_datoteke.md 314236"))
        self.assertEqual(123, dolzina("11/6/2015 ime datoteke s presledki.md 123"))
        self.assertEqual(436, dolzina("11/16/2020 ime  s     presledki.md 436"))
        self.assertEqual(0, dolzina("1/6/2020     ime  s     presledki.md   0"))

    def test_datum(self):
        self.assertEqual((2020, 11, 16), datum("11/16/2020 ime_datoteke.md 314236"))
        self.assertEqual((2015, 11, 6), datum("11/6/2015 ime datoteke s presledki.md 123"))
        self.assertEqual((2020, 11, 16), datum("11/16/2020 ime  s     presledki.md 436"))
        self.assertEqual((2020, 1, 6), datum("1/6/2020     ime  s     presledki.md   0"))

    def test_podatki(self):
        self.assertEqual(((2020, 11, 16), "ime_datoteke.md", 314236), podatki("11/16/2020 ime_datoteke.md 314236"))
        self.assertEqual(((2015, 11, 6), "ime datoteke s presledki.md", 123),
                         podatki("11/6/2015 ime datoteke s presledki.md 123"))
        self.assertEqual(((2020, 11, 16), "ime  s     presledki.md", 436),
                         podatki("11/16/2020 ime  s     presledki.md 436"))
        self.assertEqual(((2020, 1, 6), "ime  s     presledki.md", 0),
                         podatki("1/6/2020     ime  s     presledki.md   0"))

    def test_je_novejsa(self):
        self.assertIs(True, je_novejsa("11/16/2020   i   m e 314236", "10/16/2020   i  m e 314236"))
        self.assertIs(True, je_novejsa("11/16/2020   i   m e 314236", "11/5/2020   i  m e 314236"))
        self.assertIs(True, je_novejsa("11/16/2020   i   m e 314236", "11/15/2015   i  m e 314236"))
        self.assertIs(True, je_novejsa("11/16/2020   i   m e 314236", "5/16/2020   i  m e 314236"))
        self.assertIs(True, je_novejsa("5/16/2020   i   m e 314236", "4/16/2020   i  m e 314236"))

        self.assertIs(False, je_novejsa("10/16/2020   i   m e 314236", "11/16/2020   i  m e 314236"))
        self.assertIs(False, je_novejsa("11/5/2020   i   m e 314236", "11/16/2020   i  m e 314236"))
        self.assertIs(False, je_novejsa("11/5/2020   i   m e 314236", "11/5/2020   i  m e 314236"))
        self.assertIs(False, je_novejsa("11/15/2020   i   m e 314236", "11/16/2020   i  m e 314236"))
        self.assertIs(False, je_novejsa("5/16/2015   i   m e 314236", "11/16/2020   i  m e 314236"))
        self.assertIs(False, je_novejsa("4/16/2020   i   m e 314236", "5/16/2020   i  m e 314236"))

    def test_datumi(self):
        vrstice = [
            "10/16/2020 ime dat.avi 314236",
            "10/14/2020 ime dat.avi   312353",
            "5/16/2020   ime dat.avi 21532",
            "12/31/2018   ime dat.avi 21532",
            "10/16/2020 some other.avi 314236",
            "10/18/2020 another file.avi 351352",
            "10/18/2018 another file.avi 314236",
        ]
        for i in range(10):
            shuffle(vrstice)
            self.assertEqual([(2020, 10, 16), (2020, 10, 14), (2020, 5, 16), (2018, 12, 31)],
                             datumi("ime dat.avi", vrstice))
            self.assertEqual([(2020, 10, 16)], datumi("some other.avi", vrstice))
            self.assertEqual([], datumi("no such file.avi", vrstice))

    def test_najnovejsa(self):
        vrstice = [
            "10/16/2020 ime dat.avi 314236",
            "10/14/2020 ime dat.avi   312353",
            "5/16/2020   ime dat.avi 21532",
            "10/16/2020 some other.avi 314236",
            "10/18/2020 another file.avi 351352",
            "10/18/2018 another file.avi 314236",
        ]
        for i in range(10):
            shuffle(vrstice)
            self.assertEqual(((2020, 10, 16), "ime dat.avi", 314236), najnovejsa("ime dat.avi", vrstice))
            self.assertEqual(((2020, 10, 18), "another file.avi", 351352), najnovejsa("another file.avi", vrstice))
            self.assertEqual(((2020, 10, 16), "some other.avi", 314236), najnovejsa("some other.avi", vrstice))

    def test_odstrani(self):
        from random import shuffle

        f1 = ["10/18/2018 another file.avi 314236"]
        f2 = ["10/18/2020 ime dat.avi 314236"]
        f3 = ["10/18/2020 some other.avi 314236"]
        vrstice = 10 * f1 + 2 * f2 + f3

        self.assertIsNone(odstrani("another file.avi", vrstice[:]), "`odstrani` ne sme vračati ničesar")

        for i in range(10):
            kopija = vrstice[:]
            shuffle(kopija)
            odstrani("another file.avi", kopija)
            self.assertEqual(2 * f2 + f3, sorted(kopija))

        kopija = sorted(vrstice)
        odstrani("another file.avi", kopija)
        self.assertEqual(2 * f2 + f3, sorted(kopija))

        for i in range(10):
            kopija = vrstice[:]
            shuffle(kopija)
            odstrani("ime dat.avi", kopija)
            self.assertEqual(10 * f1 + f3, sorted(kopija))

        kopija = sorted(vrstice)
        odstrani("ime dat.avi", kopija)
        self.assertEqual(10 * f1 + f3, sorted(kopija))

        for i in range(10):
            kopija = vrstice[:]
            shuffle(kopija)
            odstrani("some other.avi", kopija)
            self.assertEqual(10 * f1 + 2 * f2, sorted(kopija))

        kopija = sorted(vrstice)
        odstrani("some other.avi", kopija)
        self.assertEqual(10 * f1 + 2 * f2, sorted(kopija))

        kopija = vrstice[:]
        odstrani("no such file.avi", kopija)
        self.assertEqual(10 * f1 + 2 * f2 + f3, sorted(kopija))


class TestDodatna(unittest.TestCase):
    def test_skupna_dolzina(self):
        vrstice = [
            "10/16/2020 ime dat.avi 1",
            "10/14/2020 ime dat.avi   2",
            "5/16/2020   ime dat.avi 4",
            "12/31/2018   ime dat.avi 8",
            "10/16/2020 some other.avi 16",
            "10/18/2020 another file.avi 32",
            "10/18/2018 another file.avi 64",
        ]
        for i in range(10):
            shuffle(vrstice)
            self.assertEqual(1 + 16 + 32, skupna_dolzina(vrstice))

        vrstice = [
            "10/14/2020 ime dat.avi   1",
            "5/16/2020   ime dat.avi 2",
            "10/16/2020 ime dat.avi 4",
            "12/31/2018   ime dat.avi 8",
            "10/16/2020 some other.avi 16",
            "10/18/2020 another file.avi 32",
            "10/18/2018 another file.avi 64",
        ]
        for i in range(10):
            shuffle(vrstice)
            self.assertEqual(4 + 16 + 32, skupna_dolzina(vrstice))


if __name__ == "__main__":
    unittest.main()
