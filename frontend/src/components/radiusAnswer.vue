<template>
    <div class="form-check">
        <input v-model="picked" v-on:change="changeEvent" class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios1" value=":id">
        <label class="form-check-label" for="exampleRadios1" v-html=text></label>
    </div>
</template>

<script>

import { eventBus } from '../eventBus.js';

export default {
    'name': 'Answer',
    props: ['text', 'picked', 'id'],
    methods: {
        changeEvent (event) {
            eventBus.$emit('switch-radius-value', this);
        }
    }
};
</script>
