<template>
    <div class="form-check">
        <input v-on:change="switchChecked" class="form-check-input" type="radio" name="answerRadio" :value="id" :checked="checked">
        <label class="form-check-label" for="exampleRadios1" v-html=text></label>
    </div>
</template>

<script>

export default {
    'name': 'Answer',
    props: ['text', 'id'],
    data () {
        return {
            checked: false
        };
    },
    methods: {
        switchChecked () {
            this.$parent.$children.map(cmp => {
                cmp.checked = false;
            });
            this.checked = !this.checked;
        }
    }
};
</script>
