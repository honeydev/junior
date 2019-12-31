

def flat_user_test_case(relations: list) -> tuple:
    relations = tuple(
        {**relation, **relation['test_question']}
        for relation in relations
    )

    return tuple(
        {
            question_key: question_value for question_key, question_value
            in relation.items() if question_key != 'test_question'
        }
        for relation in relations
    )
