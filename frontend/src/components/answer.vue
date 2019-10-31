<template>
    <div>
        <div v-if="type == 'radius'">
            <radiusAnswer :text="text" :id="id"/>
        </div>
    </div>
</template>

<script>

import radiusAnswer from './radiusAnswer';

export default {
    'name': 'Answer',
    'props': ['text', 'type', 'id'],
    'components': {
        radiusAnswer
    }
};
</script>
