from flask import Flask
from flask_login import LoginManager
from google.cloud import storage, bigquery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

storage_client = storage.Client()
bq_client = bigquery.Client()

from app import routes

