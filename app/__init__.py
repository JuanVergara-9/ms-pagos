from flask import Flask
from .extension import db, migrate
from .routes import pagos

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(pagos)

    return app