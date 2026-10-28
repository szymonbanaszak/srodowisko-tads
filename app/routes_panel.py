from flask import Blueprint, abort, current_app, redirect, request, url_for

from .services import dostepne_regiony, policz_wskazniki, raporty_roku, zapisz_raport

panel_bp = Blueprint("panel", __name__)

ROK_DOMYSLNY = 2026


@panel_bp.get("/")
def index():
    return "Panel wskaźników"


@panel_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    if region is not None and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")
    w = policz_wskazniki(sciezka, region)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    return f"<h1>Wskaźniki: {w['region'] or 'wszystkie'}</h1><p>Marża: {w['marza']:.2%}</p>"


@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if kod not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {kod}")
    liczba = policz_wskazniki(sciezka, kod)["liczba_zamowien"]
    return f"<h1>Region {kod}</h1><p>Zamówień: {liczba}</p>"


@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"


@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "Wyślij formularz metodą POST z polami rok i region."
    rok = request.form.get("rok", type=int)
    region = request.form.get("region")
    if rok is None or region not in dostepne_regiony(current_app.config["SCIEZKA_DANYCH"]):
        abort(400, description="Niepoprawne dane formularza")
    if not 2020 <= rok <= 2030:
        abort(422, description="Rok poza zakresem 2020-2030")
    zapisz_raport(rok, region)
    return redirect(url_for("panel.raport", rok=rok), 303)


@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)