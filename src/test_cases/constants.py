from enum import Enum


class AnswerTypes(Enum):

    RADIUS = 0
    CHECK_BOX = 1

    @classmethod
    def get_name(cls, answer_type):
        return list(cls)[answer_type]
