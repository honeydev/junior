<template>
  <section class="container">
    <div class="row">
      <div class="col">
        <completedDialog v-if="isCompleted"/>
        <div v-for="question in notCompletedQuestions" v-bind:key="question.id">
          <radiusQuestion
            v-if="question.question_type == 'radius'"
            :id="question.id"
            :question_type="question.question_type"
            :text="question.text"
            :answers="question.answers"
          />
          <checkboxQuestion
            v-else-if="question.question_type == 'check_box'"
            :id="question.id"
            :question_type="question.question_type"
            :text="question.text"
            :answers="question.answers"
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
    eventBus.$on('click-next', (questionComponent, asyncAction) => {
      if (questionComponent.rightAnswer) {
        this.completedQuestions.push(this.notCompletedQuestions.shift());
      } else {
        this.notCompletedQuestions.push(this.notCompletedQuestions.shift());
      }

      asyncAction(() => {
        this.activeComponentId = _.head(this.notCompletedQuestions).id;
      });
    });
  },
  methods: {
    handleTestCaseResponse (apiResponse) {
      this.completedQuestions = apiResponse['data'].filter(
        question => question.completed
      );
      this.notCompletedQuestions = apiResponse['data'].filter(
        question => !question.completed
      );

      if (!_.isEmpty(this.notCompletedQuestions)) {
        const head = _.head(this.notCompletedQuestions);
        head['active'] = true;
        this.activeComponentId = head.id;

        const tail = _.tail(this.notCompletedQuestions).map(question => {
          question['active'] = false;
          return question;
        });
        this.notCompletedQuestions = [head].concat(tail);
      }
    }
  },
  computed: {
    isCompleted () {
      return _.isEmpty(this.notCompletedQuestions) && !_.isEmpty(this.completedQuestions);
    }
  },
  components: {
    radiusQuestion: RadiusQuestion,
    checkboxQuestion: CheckboxQuestion,
    completedDialog: CompletedDialog
  }
};
</script>
