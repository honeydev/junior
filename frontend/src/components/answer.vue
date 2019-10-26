<template>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios1" value="option1">
        <label class="form-check-label" for="exampleRadios1" v-html=text></label>
    </div>
</template>

<script>
export default {
    'name': 'answer',
    props: ['text', 'id']
}
</script>
