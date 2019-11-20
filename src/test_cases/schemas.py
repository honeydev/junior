from marshmallow import Schema, fields

from src.test_cases.constants import AnswerTypes


class UserSchema(Schema):

    id = fields.Int(dump_only=True)  # noqa: A003
    question_relation = fields.Nested('TestQuestionUserRelation', many=True)


class TestQuestionUserRelation(Schema):
    id = fields.Int(dump_only=True)  # noqa: A003
    completed = fields.Boolean()
    test_question = fields.Nested('TestQuestionSchema')


class TestQuestionSchema(Schema):
    """TestQuestion Serializer."""

    id = fields.Int(dump_only=True)  # noqa: A003
    text = fields.String()
    question_type = fields.Method('format_question_type')
    test_case_id = fields.Int()
    answers = fields.Nested('TestCaseAnswerSchema', many=True)

    def format_question_type(self, instance):
        return AnswerTypes.get_name(instance.question_type).name.lower()


class TestCaseAnswerSchema(Schema):
    """TestAnswer schema."""

    id = fields.Int(dump_only=True)  # noqa: A003
    text = fields.String()
    right = fields.Boolean()
