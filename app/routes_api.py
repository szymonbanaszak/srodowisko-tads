from flask import Blueprint, abort, current_app, jsonify, request

from .services import dostepne_regiony, policz_wskazniki, raporty_roku
from .decorators import wymagany_parametr
from .validators import parametr_int

api_bp = Blueprint("api", __name__)


@api_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    if region is not None and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")
    return jsonify(policz_wskazniki(sciezka, region))


@api_bp.get("/raporty")
@wymagany_parametr("rok")
def raporty():
    rok = parametr_int("rok", 2020, 2030)
    return jsonify(rok=rok, raporty=raporty_roku(rok))