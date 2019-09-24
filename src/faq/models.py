from src.base.base_models import BaseDateTimeModel
from src.extensions import db


class Question(BaseDateTimeModel):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}

    def __init__(self, text, answers):
        self.text = text
        self.answers = answers

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship(
        'Answer', backref='questions', lazy='dynamic'
    )

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Answer(BaseDateTimeModel):
    __tablename__ = 'answers'
    __table_args__ = {'extend_existing': True}

    def __init__(self, question):
        self.question = question

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    question = db.Column(db.Integer, db.ForeignKey('questions.id'))
