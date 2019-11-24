

def flat_user_test_case(user_test_case: dict) -> tuple:
    return tuple(
        {
            **{
                'completed': question_relation['completed'],
                'id': question_relation['id'],
            },
            **question_relation['test_question'],
        }
        for question_relation in user_test_case['question_relation']
    )
