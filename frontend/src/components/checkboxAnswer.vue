<template>
    <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="defaultCheck1">
        <label class="form-check-label" for="defaultCheck1">
            Default checkbox
        </label>
    </div>
</template>

<script>

import { eventBus } from '../eventBus.js';

export default {
    'name': 'Answer',
    props: ['text', 'id'],
    methods: {
        changeEvent (event) {
            eventBus.$emit('switch-radius-value', this);
        }
    }
};
</script>
