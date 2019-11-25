<template>
  <div class="col-8 offset-2">
    <div v-if="isActive" class="card" :class="{ 'bg-danger': isShowError, 'bg-success': isShowSuccess }">
      <div class="card-body">
        <div class="card-title"><h3 v-html="text"/></div>
        <ul class="list-unstyled">
          <li v-for="answer in answers" v-bind:key="answer.id">
              <answer :text="answer.text" :type="question_type" :id="answer.id"/>
          </li>
        </ul>
        <button v-on:click="checkAnswer" class="btn btn-primary" type="submit" :disabled="afterClick">Дальше</button>
      </div>
      <errorAlert v-if="isShowError"/>
      <successAlert v-if="isShowSuccess"/>
    </div>
  </div>
</template>

<script>

import { eventBus } from '../eventBus.js';
import ErrorAlert from './errorAlert';
import SuccessAlert from './successAlert';
import { answerIsRight } from '../helpers/questionHelpers';
import stateStorage from '../stateSorage';
import testCaseApi from '../api/testCaseApi';

export default {
  name: 'Question',
  props: ['text', 'question_type', 'answers', 'id'],
  components: {
    'errorAlert': ErrorAlert,
    'successAlert': SuccessAlert
  },
  data: () => stateStorage.state,
  created () {
    this.rightAnswers = this.answers.reduce((acc, el) => {
      if (el.right) {
        return acc.add(el.id);
      }
      return acc;
    }, new Set());
  },
  methods: {
    checkAnswer (clickEvent) {
      const choicedId = this.$children
        .filter(answerCmp => answerCmp.checked)
        .map(answerCmp => answerCmp.id);

      this.rightAnswer = answerIsRight(this.rightAnswers, choicedId);
      this.afterClick = true;

      if (this.rightAnswer) {
        testCaseApi.finalizeTestQuestion(this, this.id);
      } else {
        this.nextAsyncAction();
      }
    },
    handleFinalizeResponse (response) {
      this.nextAsyncAction();
    },
    nextAsyncAction () {
      const asyncAction = (additionalAction) => setTimeout(() => {
        this.afterClick = false;
        additionalAction();
      }, 1000);
      eventBus.$emit('click-next', this, asyncAction);
    }
  },
  watch: {
    activeComponentId (newComponentId) {
      this.active = Number(this.id) === Number(newComponentId);
    }
  },
  computed: {
    isShowError () {
      return this.afterClick && !this.rightAnswer;
    },
    isShowSuccess () {
      return this.afterClick && this.rightAnswer;
    },
    isActive () {
      return this.activeComponentId === this.id;
    }
  }
};
</script>
