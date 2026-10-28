from flask import abort, request


def parametr_int(nazwa, minimum, maksimum):
    wartosc = request.args.get(nazwa)
    if wartosc is None:
        abort(400, description=f"Brak parametru {nazwa}")
    try:
        liczba = int(wartosc)
    except ValueError:
        abort(400, description=f"Parametr {nazwa} nie jest liczbą")
    if not minimum <= liczba <= maksimum:
        abort(422, description=f"Parametr {nazwa} poza zakresem {minimum}-{maksimum}")
    return liczba