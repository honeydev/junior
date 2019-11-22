from src.extensions import db


class TestCase(db.Model):
    """Question test cases set model."""

    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship('Question', back_populates='test_case')
    test_questions = db.relationship('TestQuestion', back_populates='test_case')


class TestQuestion(db.Model):
    """Question for test case."""

    __tablename__ = 'test_questions'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Integer, nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'))
    test_case = db.relationship('TestCase', back_populates='test_questions')
    user_relation = db.relationship(
        'TestQuestionUserRelation',
        back_populates='test_question',
    )
    answers = db.relationship('TestAnswer', back_populates='question')

    def __str__(self):
        return f'{self.text[:30]}'


class TestQuestionUserRelation(db.Model):
    """Relation with User and TestQuestion."""

    __tablename__ = 'test_questions_users_relations'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    completed = db.Column(db.Boolean, nullable=False, default=False)
    test_question_id = db.Column(
        db.Integer,
        db.ForeignKey('test_questions.id'),
    )
    test_question = db.relationship(
        'TestQuestion',
        back_populates='user_relation',
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(
        'User',
        back_populates='question_relation',
    )

    def __str__(self):
        return f'Связь пользователя {self.user} и вопроса {self.test_question}'


class TestAnswer(db.Model):

    __tablename__ = 'test_answers'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    text = db.Column(db.Text, nullable=False)
    right = db.Column(db.Boolean, nullable=False, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('test_questions.id'))
    question = db.relationship('TestQuestion', back_populates='answers')
