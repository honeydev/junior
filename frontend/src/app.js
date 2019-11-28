import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/style.css';

import Vue from 'vue';
import TestCase from './components/testCase';
import TestCaseProgress from './components/testCaseProgress';
import { newImage, btnRandom } from './avatar_randomizer';

window.onload = () => {
  new Vue().$mount('#app');

  if (document.getElementById('testCase')) {
    new Vue({
      render: h => h(TestCase)
    }).$mount('#testCase');

    new Vue({
      render: h => h(TestCaseProgress)
    }).$mount('#testCaseProgress');
  }
};
newImage();
btnRandom();
