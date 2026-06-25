from flask import Flask, render_template, redirect
from flask_login import LoginManager
from config import Config

from models.user import db, User
from models.resume import Resume
from models.interview import Interview

import os

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/logout")
def logout():
    return redirect("/")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        debug=True
    )
