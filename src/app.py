from flask import Flask
from src.common.database import Database


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "1234"


@app.before_first_request
def init_db():
    Database.initialize()


from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")