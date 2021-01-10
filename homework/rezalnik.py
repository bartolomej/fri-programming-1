from math import ceil


class Rezalnik:
    def __init__(self):
        self.dolzina = 4

    def nastavi_dolzino(self, n):
        self.dolzina = n

    def razrezi(self, a):
        res = []
        for i in range(0, ceil(len(a) / self.dolzina)):
            res.append(a[i*self.dolzina:(i+1)*self.dolzina])
        return res
