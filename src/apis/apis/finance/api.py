from flask import Flask, request, jsonify
from .authorizer import Authorizer
from .db_model.user_db_manager import DBUserManager
from .functions.price import get_random_price
from dataclasses import asdict


app = Flask(__name__)

USER_DB_MANAGER = DBUserManager()
AUTHORIZER = Authorizer(db_manager=USER_DB_MANAGER)

@app.route("/auth/status", methods=["GET"])
def check_auth():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer"):
        return jsonify({"message": "Missing or malformed Authorization header"}), 401

    bearer_token = auth_header.split(" ")[1]
    authorization = AUTHORIZER.check_auth(bearer_token)
    return jsonify(**asdict(authorization)), authorization.status_code


@app.route("/prices/<symbol>", methods=["GET"])
def get_price(symbol: str):
    price = get_random_price(symbol=symbol)

    if not price:
        return jsonify({"error": "Unknown symbol"}), 404

    return jsonify({**price}), 200


@app.route("/ingest", methods=["POST"])
def ingest_data():
    pass


