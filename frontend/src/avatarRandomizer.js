const newImage = () => {
  var MD5 = require('crypto-js/md5');
  const faceApi = 'https://api.adorable.io/avatars/';
  const gravatarApi = 'https://www.gravatar.com/avatar/';
  const size = 128;
  let ava = document.getElementById('img_avatar');
  let randomStr = Math.random().toString(36).slice(-8);
  let newUrl;
  document.getElementById('avatar_img_str').value = randomStr;
  if (document.getElementById('chosen_avatar').value === 'face') {
    newUrl = `${faceApi}${size}/${randomStr}.png`;
  }
  if (document.getElementById('chosen_avatar').value === 'gravatar') {
    newUrl = `${gravatarApi}${MD5(randomStr)}?d=identicon&s=${size}`;
  }
  ava.setAttribute('src', newUrl);
};
const btnRandom = () => {
  const el = document.getElementById('random_btn');
  el.addEventListener('click', newImage);
};

export { newImage };
export { btnRandom };
