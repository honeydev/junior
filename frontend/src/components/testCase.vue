<template>
    <section class="container">
        <div class="row">
            <div class="col">
                <div v-for="question in questions" v-bind:key="question.id">
                    <radiusQuestion v-if="question.question_type == 'radius'"
                        :id="question.id"
                        :question_type=question.question_type
                        :text=question.text
                        :answers=question.answers
                        :active=question.active
                    />
                    <checkboxQuestion v-else-if="question.question_type == 'check_box'"
                        :id="question.id"
                        :question_type=question.question_type
                        :text=question.text
                        :answers=question.answers
                        :active=question.active
                    />
                </div>
            </div>
        </div>
    </section>
</template>

<script>

import TestCaseApi from '../api/testCaseApi';
import _ from 'lodash';

import { getQuestionIdByUrl } from '../helpers/commonHelpers';
import radiusQuestion from './radiusQuestion';
import checkboxQuestion from './checkboxQuestion';
import { eventBus } from '../eventBus';

export default {
    name: 'TestCase',
    data () {
        return {
            questions: []
        };
    },
    created: function () {
        TestCaseApi.getTestCase(this, getQuestionIdByUrl());
        eventBus.$on('click-next', questionComponent => {
            const currentIndex = _.findIndex(this.questions, question => {
                return Number(question.id) === Number(questionComponent.id);
            });
            const nextIndex = (currentIndex + 1 < this.$children.length) ? currentIndex + 1 : 0;
            const nextQuestion = this.$children[nextIndex];

            nextQuestion.active = true;
        });
    },
    methods: {
        handleTestCaseResponse (apiResponse) {
            const questions = apiResponse['data']['test_questions'];
            const head = _.head(questions);
            head['active'] = true;
            const tail = _.tail(questions).map(question => {
                question['active'] = false;
                return question;
            });
            this.questions = [head].concat(tail);
        }
    },
    components: {
        'radiusQuestion': radiusQuestion,
        'checkboxQuestion': checkboxQuestion
    }
};

</script>
