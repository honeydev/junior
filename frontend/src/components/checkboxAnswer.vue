<template>
    <div class="custom-control custom-checkbox">
        <input v-on:change="switchChecked" class="custom-control-input" type="checkbox" :id="id" :value="id" :checked="checked">
        <label class="custom-control-label" :for="id" v-html=text />
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
