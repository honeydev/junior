import Axios from 'axios';

class TestCaseApi {
  static getTestCase (component, questionId) {
    Axios.get(`/api/testcase/${questionId}`)
      .then(response => {
        component.handleTestCaseResponse(response);
      });
  }

  static finalizeTestQuestion (component, testCaseQuestionId) {
    Axios.put(`/api/testcase/finalize-question/${testCaseQuestionId}`, {
      'test_case_question_id': testCaseQuestionId
    })
      .then(response => {
        component.handleFinalizeResponse(response);
      });
  }
}

export default TestCaseApi;
