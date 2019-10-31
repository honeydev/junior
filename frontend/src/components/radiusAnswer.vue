<template>
    <div class="form-check">
        <input v-on:change="changeEvent" class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios1" value="option1">
        <label class="form-check-label" for="exampleRadios1" v-html=text></label>
    </div>
</template>

<script>

import { eventBus } from '../eventBus.js';

export default {
    'name': 'answer',
    props: ['text', 'id'],
    methods: {
        changeEvent (event) {
            console.log(event);
            eventBus.$emit('switch-radius-value', this);
        }
    }
};
</script>
