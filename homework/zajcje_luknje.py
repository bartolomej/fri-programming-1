def obvezna_naloga(bobri, luknje):
    for x in luknje:
        bobri = (bobri[len(bobri) - x:len(bobri)])[::-1] + bobri[0:len(bobri) - x]
    return bobri


# Kakšne luknje bi morali dodati, da bi se bobri, ko gredo prek njih, spet preuredili v prvotni vrstni red?
# Nalogo lahko najprej rešiš za te konkretne bobre in luknje. Nato razmisli, kako to narediti v splošnem. Skratka, ideja je razmisliti, kako k nekemu podanemu seznamo dodati seznam lukenj, ki nevtralizira podani seznam (za podano število bobrov).
# Pri dodatni nalogi (najbrž) ne bo veliko programiranja, temveč predvsem razmislek.
def dodatna_naloga(bobri, luknje):
    neutral = []
    for x in luknje[::-1]:
        n = len(bobri) - x
        bobri = (bobri[len(bobri) - n:len(bobri)])[::-1] + bobri[0:x]
        neutral.append(n)
    return neutral, bobri


if __name__ == "__main__":
    bobri = "54321"
    luknje = [4, 2, 3]
    print("Zacetni seznam bobrov je: ", bobri)
    koncni_bobri = obvezna_naloga(bobri, luknje)
    print("Ko pridejo bobri cez lukne je vrstni red: ", koncni_bobri)
    neutral, nevtralni_bobri = dodatna_naloga(koncni_bobri, luknje)
    if nevtralni_bobri == bobri:
        print("Pravilen razultat")
    else:
        print("Napacen razultat: ", nevtralni_bobri)
    print("Seznam lukenj, ki nevtralizira dani seznam je: ", neutral)
