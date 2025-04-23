from flask import Flask
from .routes.ppg import ppg_bp
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(ppg_bp)

    # Database config
    app.config['DB'] = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return app
