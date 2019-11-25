import _ from 'lodash';

export const answerIsRight = (rightAnswers, choicedId) => {
  return rightAnswers.size === choicedId.length &&
    _.every(choicedId, id => rightAnswers.has(id));
};
