<template>
    <section class="container">

        <div class="row">
            <div class="col">
                <v-if="completed" completedDialog/>
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
import RadiusQuestion from './radiusQuestion';
import CheckboxQuestion from './checkboxQuestion';
import { eventBus } from '../eventBus';
import stateStorage from '../stateSorage';
import CompletedDialog from './completedDialog';

export default {
    name: 'TestCase',
    data: () => stateStorage.state,
    created: function () {
        TestCaseApi.getTestCase(this, getQuestionIdByUrl());
        eventBus.$on('click-next', questionComponent => {
            
            if (this.completed) {
                return;
            }

            const currentIndex = _.findIndex(this.questions, question => {
                return Number(question.id) === Number(questionComponent.id);
            });

            this.questions[currentIndex]['active'] = false;
            const nextIndex = (currentIndex + 1 < this.$children.length) ? currentIndex + 1 : 0;
            this.questions[nextIndex]['active'] = true;
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
    watch: {
        successQuestions(newQuestions) {
            if (newQuestions.length === this.questions.length) {
                this.questions.map(question => question.active = false)
                this.completed = true;
            }
        }
    },
    components: {
        'radiusQuestion': RadiusQuestion,
        'checkboxQuestion': CheckboxQuestion,
        'completedDialog': CompletedDialog
    }
};

</script>
