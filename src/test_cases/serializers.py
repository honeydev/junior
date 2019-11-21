from marshmallow import Schema, fields

from src.test_cases.constants import AnswerTypes


class TestCaseSchema(Schema):
    """TestCase model serializer."""

    id = fields.Int(dump_only=True)  # noqa: A003
    question_id = fields.Int()
    test_questions = fields.Nested('TestQuestionSchema', many=True)


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
