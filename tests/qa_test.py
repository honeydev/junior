from faker import Faker
from faker.generator import Generator
from flask import url_for

from src.qa.models import Answer, Chapter, Question
from src.user.models import User
from tests.base import BaseTest


class TestQuestionAndChapter(BaseTest):
    def test(self):  # noqa: WPS210
        factory: Generator = Faker()

        chapter_name: str = factory.paragraph()
        chapter_order_number: int = 1

        chapter = Chapter(
            name=chapter_name,
            order_number=chapter_order_number,
        )
        Chapter.save(chapter)
        exist_chapter = Chapter.query.get(1)
        self.assertEqual(exist_chapter.name, chapter_name)
        self.assertEqual(exist_chapter.order_number, chapter_order_number)

        question_text: str = factory.paragraph()
        question_order_number: int = 1
        question_user_id: int = 1
        question_chapter_id: int = 1
        question = Question(
            order_number=question_order_number,
            user=question_user_id,
            chapter_id=question_chapter_id,
            text=question_text,
        )
        Question.save(question)
        exist_question = Question.query.get(1)
        self.assertEqual(exist_question.order_number, question_order_number)
        self.assertEqual(exist_question.user, question_user_id)
        self.assertEqual(exist_question.chapter_id, question_chapter_id)
        self.assertEqual(exist_question.text, question_text)


class TestAnswerView(BaseTest):

    def test(self):  # noqa: WPS210
        factory: Generator = Faker()

        chapter_name: str = factory.paragraph()
        chapter_order_number: int = 1

        chapter = Chapter(
            name=chapter_name,
            order_number=chapter_order_number,
        )
        Chapter.save(chapter)
        chapter = Chapter.query.get(1)

        question_text: str = factory.paragraph()
        question_order_number: int = 1
        question_user_id: int = 1
        question = Question(
            order_number=question_order_number,
            user=question_user_id,
            chapter_id=chapter.id,
            text=question_text,
        )
        Question.save(question)
        question = Question.query.get(1)

        user_username: str = factory.md5()[:8]
        user_password: str = factory.password(8)
        user_email: str = factory.email()
        user_firstname: str = factory.first_name()
        user = User(
            login=user_username,
            email=user_email,
            password=user_password,
            firstname=user_firstname,
            is_aproved=True,
        )
        User.save(user)

        answer_text: str = factory.paragraph()
        answer_is_approve: bool = True
        answer_question_id: int = 1
        answer_owner_id: int = 1

        answer = Answer(
            text=answer_text,
            is_approve=answer_is_approve,
            question_id=answer_question_id,
            owner_id=answer_owner_id,
        )
        Answer.save(answer)
        answer = Answer.query.get(1)
        self.assertEqual(answer.text, answer_text)
        self.assertEqual(answer.is_approve, answer_is_approve)
        self.assertEqual(answer.question_id, answer_question_id)

        response = self.client.get(
            url_for('answers.answer', question_id=question.id),
        )
        self.assert_200(
            response, url_for('answers.answer', question_id=question.id),
        )
