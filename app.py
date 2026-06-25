from flask import Flask, render_template, redirect
from flask_login import LoginManager
from config import Config

from models.user import db, User
from models.resume import Resume
from models.interview import Interview
from flask import request
from werkzeug.utils import secure_filename

from services.pdf_service import extract_text_from_pdf
from services.ats_service import (
    calculate_ats_score,
    extract_skills,
    missing_skills
)

from services.question_service import (
    generate_interview_questions
)

from services.report_service import (
    create_report
)
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

@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if request.method == "POST":

        file = request.files["resume"]

        if file:

            filename = secure_filename(
                file.filename
            )

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            resume_text = extract_text_from_pdf(
                filepath
            )

            ats_score = calculate_ats_score(
                resume_text
            )

            skills = extract_skills(
                resume_text
            )

            missing = missing_skills(
                skills
            )

            questions = generate_interview_questions(
                resume_text
            )

            return render_template(
                "report.html",
                ats_score=ats_score,
                skills=skills,
                missing=missing,
                questions=questions
            )

    return render_template(
        "upload_resume.html"
    )
if __name__ == "__main__":
    app.run(
        debug=True
    )
