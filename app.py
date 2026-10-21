from pathlib import Path

from flask import Flask, abort, jsonify, request

from services import dostepne_regiony, policz_wskazniki

app = Flask(__name__)
SCIEZKA_DANYCH = str(Path(__file__).resolve().parent / "dane" / "zamowienia.csv")


@app.get("/")
def index():
    return "Panel wskaźników"


@app.get("/kpi")
def kpi():
    region = request.args.get("region")
    if region is not None and region not in dostepne_regiony(SCIEZKA_DANYCH):
        abort(404, description=f"Nieznany region: {region}")
    w = policz_wskazniki(SCIEZKA_DANYCH, region)
    return f"<h1>Wskaźniki: {w['region'] or 'wszystkie'}</h1><p>Marża: {w['marza']:.2%}</p>"


@app.get("/api/kpi")
def api_kpi():
    region = request.args.get("region")
    if region is not None and region not in dostepne_regiony(SCIEZKA_DANYCH):
        abort(404, description=f"Nieznany region: {region}")
    w = policz_wskazniki(SCIEZKA_DANYCH, region)
    return jsonify(w)