from flask import Flask, request, jsonify
from .authorizer import Authorizer
from .functions.price import get_random_price


app = Flask(__name__)

AUTHORIZER = Authorizer()

@app.route("/auth/status", methods=["GET"])
def check_auth():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer"):
        return jsonify({"message": "Missing or malformed Authorization header"}), 401

    bearer_token = auth_header.split(" ")[1]
    is_auth = AUTHORIZER.check_auth(bearer_token)

    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"status": "ok"}), 200


@app.route("/prices/<symbol>", methods=["GET"])
def get_price(symbol: str):
    price = get_random_price(symbol=symbol)

    if not price:
        return jsonify({"error": "Unknown symbol"}), 404

    return jsonify({**price}), 200


@app.route("/ingest", methods=["POST"])
def ingest_data():
    pass


