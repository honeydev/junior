import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/style.css';

import Vue from 'vue';
import TestCase from './components/testCase.vue';

window.onload = () => {
    new Vue().$mount('#app');

    if (document.getElementById('testCase')) {
        new Vue({
            render: h => h(TestCase)
        }).$mount('#testCase');
    }
};
