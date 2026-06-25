from flask import Flask, render_template, redirect
from flask_login import LoginManager
from config import Config

from models.user import db, User
from models.resume import Resume
from models.interview import Interview
from flask import request
from werkzeug.utils import secure_filename
from services.gemini_service import generate_response

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
from flask import (
    render_template,
    request,
    redirect,
    flash,
    url_for
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
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
@app.route("/mock-interview", methods=["GET", "POST"])
@login_required
def mock_interview():

    if request.method == "POST":

        answer = request.form["answer"]

        question = request.form["question"]

        prompt = f"""
        Evaluate this interview answer.

        Question:
        {question}

        Answer:
        {answer}

        Give:

        1. Score out of 10
        2. Strengths
        3. Weaknesses
        4. Improvements
        """

        feedback = generate_response(prompt)

        return render_template(
            "evaluation.html",
            feedback=feedback
        )

    sample_question = (
        "Explain the difference between "
        "Abstraction and Encapsulation."
    )

    return render_template(
        "mock_interview.html",
        question=sample_question
    )
@app.route("/download-report")
@login_required
def download_report():

    path = create_report(
        "report.pdf",
        85,
        ["Python","Flask"],
        "Sample Questions"
    )

    return send_file(
        path,
        as_attachment=True
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/analytics")
@login_required
def analytics():

    resumes = Resume.query.filter_by(
        user_id=current_user.id
    ).all()

    scores = [
        r.ats_score
        for r in resumes
    ]

    return render_template(
        "analytics.html",
        scores=scores
    )
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

is_admin = db.Column(
    db.Boolean,
    default=False
)
@app.route("/admin")
@login_required
def admin():

    if not current_user.is_admin:

        return "Access Denied"

    users = User.query.count()

    resumes = Resume.query.count()

    interviews = Interview.query.count()

    return render_template(
        "admin.html",
        users=users,
        resumes=resumes,
        interviews=interviews
    )
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
    @app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = generate_password_hash(
            request.form["password"]
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already exists")

            return redirect("/register")

        user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(user)

        db.session.commit()

        flash("Registration Successful")

        return redirect("/login")

    return render_template("register.html")
    @app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )
    @app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")
    @app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")
    resume_record = Resume(

    filename=filename,

    ats_score=ats_score,

    extracted_skills=",".join(skills),

    suggestions=",".join(missing),

    user_id=current_user.id
)

db.session.add(resume_record)

db.session.commit()
if __name__ == "__main__":
    app.run(
        debug=True
    )
