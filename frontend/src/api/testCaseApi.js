import Axios from 'axios';

class TestCaseApi {
    static getTestCase (component, questionId) {
        Axios.get(`/api/testcase/${questionId}`)
            .then(response => {
                component.handleTestCaseResponse(response);
            })
            .catch(response => {
                component.handleTestCaseException(response);
            });
    }

    static finalizeTestQuestion (component, testCaseQuestionId) {
        Axios.put(
            `/api/testcase/finalize_question`, {
                'test_case_question_id': testCaseQuestionId
            })
            .then(response => component.handleFinalizeResponse(response))
            .catch(response => component.handleFinalizeException(response));
    }
}

export default TestCaseApi;
