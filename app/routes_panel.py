from flask import Blueprint, abort, current_app, request

from .services import dostepne_regiony, policz_wskazniki

panel_bp = Blueprint("panel", __name__)


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