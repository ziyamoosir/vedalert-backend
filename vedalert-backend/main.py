from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
