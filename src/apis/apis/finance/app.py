from flask import Flask

from .api import finance_api_bp
from .authorizer import Authorizer
from .db_model.user_db_manager import DBUserManager


def create_app():
    app = Flask(__name__)

    app.user_db_manager = DBUserManager()
    app.authorizer = Authorizer(db_manager=app.user_db_manager)

    app.register_blueprint(finance_api_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)