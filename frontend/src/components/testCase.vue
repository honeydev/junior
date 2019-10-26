<template>
    <section class="container">
        <div class="row">
            <div class="col">
                <div v-for="question in questions" v-bind:key="question.id">
                    <question 
                        :id="question.id"
                        :question_type=question.question_type
                        :text=question.text
                        :answers=question.answers
                        :active=question.active />
                </div>
            </div>
        </div>
    </section>
</template>

<script>

import TestCaseApi from '../api/testCaseApi';
import _ from 'lodash';

import { getQuestionIdByUrl } from '../helpers/commonHelpers.js';
import question from './question.vue';

export default {
    name: 'TestCase',
    data() {
        return {
            questions: []
        }
    },
    created: function () {
        TestCaseApi.getTestCase(this, getQuestionIdByUrl())
    },
    methods: {
        handleTestCaseResponse(apiResponse) {
            const questions = apiResponse['data']['test_questions'];
            const head = _.head(questions)
            head['active'] = true;
            const tail = _.tail(questions).map(question => {
                question['active'] = false;
                return question;
            })
            this.questions = [head].concat(tail);
        }
    },
    components: {
        'question': question
    }
};

</script>
