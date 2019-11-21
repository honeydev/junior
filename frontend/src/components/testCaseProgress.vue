<template>
    <div class="progress testCaseProgress">
        <div
            class="progress-bar"
            role="progressbar"
            :style="'width: ' + progress + '%'"
            ></div>
    </div>
</template>

<script>

import stateStorage from '../stateSorage';

export default {
    'name': 'TestCaseProgress',
    data () {
        return stateStorage.state;
    },
    computed: {
        progress () {
            const progressPart = 100 / stateStorage.state['questions'].length;
            return String(this.successQuestions.length * progressPart);
        }
    }
};
</script>
