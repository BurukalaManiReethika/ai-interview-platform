from models.user import db

class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    ats_score = db.Column(
        db.Integer,
        default=0
    )

    extracted_skills = db.Column(
        db.Text
    )

    suggestions = db.Column(
        db.Text
    )

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Resume {self.filename}>"
