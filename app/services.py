import csv
_RAPORTY = []

def wczytaj_zamowienia(sciezka):
    with open(sciezka, encoding="utf-8", newline="") as plik:
        return list(csv.DictReader(plik))


def dostepne_regiony(sciezka):
    return sorted({z["region"] for z in wczytaj_zamowienia(sciezka)})


def policz_wskazniki(sciezka, region=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    if region is not None:
        zamowienia = [z for z in zamowienia if z["region"] == region]
    przychod = round(sum(float(z["przychod"]) for z in zamowienia), 2)
    koszt = round(sum(float(z["koszt"]) for z in zamowienia), 2)
    marza = round((przychod - koszt) / przychod, 4) if przychod else 0.0
    return {
        "region": region,
        "liczba_zamowien": len(zamowienia),
        "przychod": przychod,
        "koszt": koszt,
        "marza": marza,
    }


def zapisz_raport(rok, region):
    _RAPORTY.append({"rok": rok, "region": region})


def raporty_roku(rok):
    return [r for r in _RAPORTY if r["rok"] == rok]