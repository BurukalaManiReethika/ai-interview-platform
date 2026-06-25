from models.user import db

class Interview(db.Model):

    __tablename__ = "interviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    score = db.Column(
        db.Integer,
        default=0
    )

    feedback = db.Column(
        db.Text
    )

    questions = db.Column(
        db.Text
    )

    answers = db.Column(
        db.Text
    )

    interview_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Interview {self.id}>"
