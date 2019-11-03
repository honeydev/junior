<template>
    <div class="custom-control custom-radio">
        <input v-on:change="switchChecked" class="custom-control-input" type="radio" name="answerRadio" :id="id" :value="id" :checked="checked">
        <label class="custom-control-label" :for="id" v-html=text></label>
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
