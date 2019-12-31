from marshmallow import Schema, fields

from src.test_cases.constants import AnswerTypes


class TestQuestionUserRelationSchema(Schema):
    id = fields.Int(dump_only=True)  # noqa: A003
    completed = fields.Boolean()
    test_question = fields.Nested('TestQuestionSchema')


class TestQuestionSchema(Schema):

    id = fields.Int(dump_only=True)  # noqa: A003
    text = fields.String()
    question_type = fields.Method('format_question_type')
    test_case_id = fields.Int()
    answers = fields.Nested('TestCaseAnswerSchema', many=True)

    def format_question_type(self, instance):
        return AnswerTypes.get_name(instance.question_type).name.lower()


class TestCaseAnswerSchema(Schema):

    id = fields.Int(dump_only=True)  # noqa: A003
    text = fields.String()
    right = fields.Boolean()
