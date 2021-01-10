# Sem pišite svoje funkcije

# prejme koordinati dveh topov in vrne True, če se med seboj napadata (torej:
# če sta v isti vrstici ali stolpcu) in False, če se ne. Če gre za eno in isto trdnjavo, pa vedno vrne False.
def se_napadata(top1, top2):
    return (top1[0] == top2[0] or top1[1] == top2[1]) and top1 != top2


# prejme koordinato enega topa in seznam koordinat vseh topov na šahovnici.
# Vrniti mora seznam koordinat vseh topov, ki jih napada podani top.
def napadeni(top, topovi):
    napada = []
    for t in topovi:
        if se_napadata(top, t):
            napada.append(t)
    return napada


# prejme koordinato topa in koordinate vseh topov ter vrne število topov, ki napadajo podani top.
def napadenost(top, topovi):
    return len(napadeni(top, topovi))


# vrne True, če podani top ni napaden in False, če je.
def varen(top, topovi):
    return len(napadeni(top, topovi)) == 0


# prejme seznam topov in vrne koordinati topa, ki ga napada največ drugih topov.
# Če je enako napadenih več, vrne tistega, ki je prej na seznamu. Če ni napaden nihče, vrne None.
def najbolj_napaden(topovi):
    max_n = 0
    max_top = None
    for t in topovi:
        n = napadenost(t, topovi)
        if n > max_n:
            max_n = n
            max_top = t
    return max_top


# vrne True, če noben top ne napada nobenega drugega.
def vse_varno(topovi):
    return najbolj_napaden(topovi) is None


# DODATNA NALOGA
# Napiši funkcijo direkten_napad(top1, top2, topovi), ki prejme koordinati dveh topov in seznam vseh topov.
# Funkcija vrne True, če se top1 in top2 napadata - seveda tako, da med njima ni nobenega drugega topa.
def direkten_napad(top1, top2, topovi):
    # preveri ali sta topa sploh poravnana po vrsticah ali stolpah
    if not se_napadata(top1, top2):
        return False
    col_sort = [top1, top2]
    col_sort.sort(key=lambda x: x[0])
    row_sort = [top1, top2]
    row_sort.sort(key=lambda x: x[1])
    for t in topovi:
        if ((t[0] == top1[0] == top2[0] and row_sort[0][1] < t[1] < row_sort[1][1]) or
                (t[1] == top1[1] == top2[1] and col_sort[0][0] < t[0] < col_sort[1][0])):
            return False
    return True


import unittest


class TestObvezna(unittest.TestCase):
    def test_se_napadate(self):
        self.assertTrue(se_napadata("a4", "d4"))
        self.assertTrue(se_napadata("e8", "c8"))
        self.assertTrue(se_napadata("e8", "e5"))
        self.assertTrue(se_napadata("f4", "f6"))

        self.assertFalse(se_napadata("f4", "g8"))
        self.assertFalse(se_napadata("g8", "f4"))
        self.assertFalse(se_napadata("c3", "c3"))

    def test_napadeni(self):
        self.assertEqual(["c1", "c8", "c6", "a3", "h3"],
                         napadeni("c3", ["c1", "c3", "d6", "c8", "c6", "e5", "a3", "h3"]))
        self.assertEqual(["c1", "c8", "c6", "a3", "h3"],
                         napadeni("c3", ["c1", "c3", "c8", "c6", "a3", "h3"]))
        self.assertEqual(["c3", "c4", "c5", "a1"],
                         napadeni("c1", ["c1", "c3", "c4", "c5", "a1"]))
        self.assertEqual([], napadeni("a8", ["c1", "a8", "c6", "h3"]))
        self.assertEqual([], napadeni("a8", ["a8"]))

    def test_napadenost(self):
        self.assertEqual(5, napadenost("c3", ["c1", "c3", "d6", "c8", "c6", "e5", "a3", "h3"]))
        self.assertEqual(5, napadenost("c3", ["c1", "c3", "c8", "c6", "a3", "h3"]))
        self.assertEqual(0, napadenost("a8", ["c1", "a8", "c6", "h3"]))
        self.assertEqual(0, napadenost("a8", ["a8"]))

    def test_varen(self):
        self.assertFalse(varen("c3", ["c1", "d6", "c8", "c6", "e5", "a3", "h3"]))
        self.assertFalse(varen("c3", ["c1", "c8", "c6", "a3", "h3"]))
        self.assertTrue(varen("a8", ["c1", "c6", "h3"]))
        self.assertTrue(varen("a8", []))

    def test_najbolj_napaden(self):
        self.assertEqual("c5", najbolj_napaden(["a5", "c5", "f5", "c6", "c8", "d3", "f7"]))
        self.assertEqual("f5", najbolj_napaden(["a5", "e5", "f5", "c6", "c8", "d3", "f7"]))

        self.assertIsNone(najbolj_napaden(["a5", "c6", "e8", "d3"]))
        self.assertIsNone(najbolj_napaden([]))

        self.assertEqual("a5", najbolj_napaden(["a5", "a6"]))
        self.assertEqual("a6", najbolj_napaden(["a6", "a5"]))

    def test_vse_varno(self):
        self.assertFalse(vse_varno(["a5", "c5", "f5", "c6", "c8", "d3", "f7"]))
        self.assertTrue(vse_varno(["a5", "c6", "e8", "d3"]))
        self.assertTrue(vse_varno(["a5", "c6", "e8", "d3"]))


class TestDodatna(unittest.TestCase):
    def test_direkten_napad(self):
        pozicija = ["a5", "c5", "f5", "c6", "c8", "d3", "f7"]

        self.assertFalse(direkten_napad("a5", "a5", pozicija))

        self.assertFalse(direkten_napad("a5", "c8", pozicija))
        self.assertFalse(direkten_napad("c8", "a5", pozicija))
        self.assertTrue(direkten_napad("f5", "f7", pozicija))
        self.assertTrue(direkten_napad("f7", "f5", pozicija))

        self.assertTrue(direkten_napad("a5", "c5", pozicija))
        self.assertTrue(direkten_napad("c5", "a5", pozicija))
        self.assertTrue(direkten_napad("c5", "f5", pozicija))
        self.assertTrue(direkten_napad("f5", "c5", pozicija))
        self.assertFalse(direkten_napad("f5", "a5", pozicija))
        self.assertFalse(direkten_napad("a5", "f5", pozicija))

        self.assertTrue(direkten_napad("c5", "c6", pozicija))
        self.assertTrue(direkten_napad("c6", "c5", pozicija))
        self.assertTrue(direkten_napad("c6", "c8", pozicija))
        self.assertTrue(direkten_napad("c8", "c6", pozicija))
        self.assertFalse(direkten_napad("c8", "c5", pozicija))
        self.assertFalse(direkten_napad("c5", "c8", pozicija))
        self.assertFalse(direkten_napad("c5", "c8", pozicija))


if __name__ == "__main__":
    unittest.main()
