from marshmallow import Schema, fields


class TestCaseSchema(Schema):
    """TestCase model serializer."""

    id = fields.Int(dump_only=True)  # noqa: A003
    question_id = fields.Int()
    test_questions = fields.Nested('TestQuestionSchema', many=True)


class TestQuestionSchema(Schema):
    """TestQuestion Serializer."""

    id = fields.Int(dump_only=True)  # noqa: A003
    text = fields.String()
    question_type = fields.Int()
    test_case_id = fields.Int()
