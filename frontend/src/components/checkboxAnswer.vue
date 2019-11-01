<template>
    <div class="form-check">
        <input v-on:change="switchChecked" class="form-check-input" type="checkbox" id="answerCheckbox" :value="id" :checked="checked">
        <label class="form-check-label" for="defaultCheck1">{{ text }}</label>
    </div>
</template>

<script>

export default {
    'name': 'Answer',
    props: ['text', 'id'],
    data () {
        return {
            'checked': false
        };
    },
    methods: {
        switchChecked () {
            this.checked = !this.checked;
        }
    }
};
</script>
