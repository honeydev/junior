<template>
    <div class="col-8 offset-2">
    <div v-if="active" class="card">
        <div class="card-body">
            <div class="card-title"><h3 v-html="text"/></div>
            <ul class="list-unstyled">
                <li v-for="answer in answers" v-bind:key="answer.id">
                    <answer :text="answer.text" :type="question_type" :id="answer.id"/>
                </li>
            </ul>
            <button v-on:click="checkAnswer" class="btn btn-primary" type="submit">Дальше</button>
        </div>
    </div>
    </div>
</template>

<script>

import answer from './answer';

import { eventBus } from '../eventBus.js';

export default {
    name: 'Question',
    props: ['text', 'active', 'question_type', 'answers', 'id'],

    components: {
        'answer': answer
    },
    created () {
    },
    methods: {
        checkAnswer (clickEvent) {
            this.$set(this, 'active', false);
            eventBus.$emit('click-next', this);
        }
    }
};
</script>
