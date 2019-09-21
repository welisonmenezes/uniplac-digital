from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# create a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# apply app configurations
app.config.from_pyfile('config.py')

# initialize app dependencies
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# routes all nonexistent route to / (UI)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return 'É o Sandroooo', 200

if __name__ == "__main__":
    app.run()