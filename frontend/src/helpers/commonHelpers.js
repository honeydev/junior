import _ from 'lodash';

const getQuestionIdByUrl = () => Number(_.last(document.URL.split('/')));

export { getQuestionIdByUrl };
