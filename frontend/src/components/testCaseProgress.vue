<template>
    <div v-if="existQuestions" class="progress testCaseProgress">
        <div
            class="progress-bar"
            role="progressbar"
            :style="'width: ' + progress + '%'"
            ></div>
    </div>
</template>

<script>

import _ from 'lodash';
import stateStorage from '../stateSorage';

export default {
  'name': 'TestCaseProgress',
  data () {
    return stateStorage.state;
  },
  computed: {
    progress () {
      const progressPart = 100 /
        (stateStorage.state['completedQuestions'].length + stateStorage.state['notCompletedQuestions'].length);
      return String(this.completedQuestions.length * progressPart);
    },
    existQuestions () {
      return !_.isEmpty(this.completedQuestions) || !_.isEmpty(this.notCompletedQuestions);
    }
  }
};
</script>
