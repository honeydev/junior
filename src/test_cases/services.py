from src.extensions import db
from src.test_cases.models import TestQuestionUserRelation
from src.test_cases.schemas import UserSchema


class TestCaseService:
    """Uset test case logic layer."""

    def __init__(self, user, test_case):
        self.user = user
        self.test_case = test_case

    def load_user_case(self):
        """Return user test case relations."""
        self.create_missing_relations()
        schema = UserSchema()

        return schema.dump(self.user)

    def create_missing_relations(self):

        questions_id = {
            test_question.id
            for test_question in self.test_case.test_questions
        }

        user_question_relations = TestQuestionUserRelation.query.filter(
            TestQuestionUserRelation.user == self.user,
            TestQuestionUserRelation.test_question_id.in_(questions_id),
        ).all()

        existed_relations_ids = {
            relation.test_question.id
            for relation in user_question_relations
        }

        questions_without_relations = questions_id - existed_relations_ids

        new_relations = tuple(
            TestQuestionUserRelation(
                test_question_id=question_id,
                user_id=self.user.id,
            )
            for question_id in questions_without_relations
        )

        db.session.bulk_save_objects(new_relations)
        db.session.commit()
