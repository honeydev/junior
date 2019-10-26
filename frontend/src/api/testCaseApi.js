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
}

export default TestCaseApi;
