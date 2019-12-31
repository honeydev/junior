from src.extensions import db
from src.test_cases.models import TestQuestionUserRelation
from src.test_cases.schemas import TestQuestionUserRelationSchema
from src.test_cases.uttils import flat_user_test_case


class TestCaseService:
    """Сервис отвечающий за формирование данных тест-кейса."""

    def __init__(self, user, test_case):
        self.user = user
        self.test_case = test_case

    def load_user_case(self) -> tuple:
        """Возвращает сформированные данные тест-кейса."""
        self.select_test_case_questions_id()
        self.create_missing_relations()
        schema = TestQuestionUserRelationSchema()

        relations = TestQuestionUserRelation.query.filter(
            TestQuestionUserRelation.id.in_(self.test_questions_id),
            TestQuestionUserRelation.user == self.user,
        )

        return flat_user_test_case(schema.dump(relations, many=True))

    def select_test_case_questions_id(self):
        """Делает выборку id вопросов относящихся к текущему тест-кейсу."""
        self.test_questions_id = {
            test_question.id
            for test_question in self.test_case.test_questions
        }

    def create_missing_relations(self):
        """
        Создает связи TestQuestionUserRelation.

        В том случае, если он отстутсвует для текущего пользователя.
        """
        user_question_relations = TestQuestionUserRelation.query.filter(
            TestQuestionUserRelation.user == self.user,
            TestQuestionUserRelation.test_question_id.in_(self.test_questions_id),
        )

        existed_relations_ids = {
            relation.test_question.id
            for relation in user_question_relations
        }

        questions_without_relations = self.test_questions_id - existed_relations_ids

        new_relations = tuple(
            TestQuestionUserRelation(
                test_question_id=question_id,
                user_id=self.user.id,
            )
            for question_id in questions_without_relations
        )

        db.session.bulk_save_objects(new_relations)
        db.session.commit()
