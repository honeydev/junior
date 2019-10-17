import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Vue from 'vue';
import TestCase from './testCase.vue';

window.onload = () => {
    new Vue({
        render: h => h(TestCase)
    }).$mount('#app');
};
