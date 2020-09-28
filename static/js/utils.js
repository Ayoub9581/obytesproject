const ENTER_KEYCODE = 13;
const TAB_KEYCODE = 9;
const BACKSPACE_KEYCODE = 8;
const UP_ARROW_KEYCODE = 38;
const DOWN_ARROW_KEYCODE = 40;
const SPACE_KEYCODE = 32;
const hashtagList = [];
let meesageVlaue;

const regexp = RegExp(/#(\w+)/g);

const id_message = document.querySelector('#id_message');
let hashtags = document.querySelectorAll('.message-text');

// get Last Item in table
function getLastItem(table) {
  const len = table.length - 1;
  return table[len];
}


function hashtag(text) {
  var repl = text.replace(/#(\w+)/g, '<a href="#" class="hashtag">#$1</a>');
  return repl;
}

function counterText(text) {
  return text.length;
}

function changeCounter(e) {
  const counter = counterText(e.target.value);
  counter === 200 ? e.preventDefault() : counter;
  document.getElementById('counter-text').textContent = `${counter}/200`;
}

async function detectHashtagWord(e) {
  let content = String(e.target.value);
  const regexp = RegExp(/#(\w+)/g);
  let match;

  while ((match = regexp.exec(content)) !== null) {
    const query = match[0].split('#').join('');
    let endpoint = `/hashtag/all/?q=${query}`;
    let res = await fetch(`${endpoint}`);
    let data = await res.text();
    hashtagList.push(match[0]);
    document.getElementById('hashtag-add').innerHTML = data;
  }
}

function get_last_hashtag(text) {
  const t = [];
  let content = String(text);
  const regexp = RegExp(/#(\w+)/g);
  let match;

  while ((match = regexp.exec(content)) !== null) {
    // const query = match[0].split('#').join('');
    t.push(match[0]);
  }

  return t[t.length - 1];
}
function findHashtags(searchText) {
  var regexp = /\B\#\w\w+\b/g;
  result = searchText.match(regexp);
  if (result) {
    console.log(result);
    return result;
  }
}

function click_on_hashtage(e, value) {
  e.preventDefault();
  const g = findHashtags(meesageVlaue);
  console.log(`last hashtag ${g}`);

  meesageVlaue = meesageVlaue.replace(g, value);
  id_message.value = meesageVlaue + ' ';
}



function onClickHashtag(e, value) {
  e.preventDefault();
  let text = id_message.value;
  const found = text.match(regexp);
  const last = getLastItem(found);
  text = text.split(' ');
  for (let i = 0; i < text.length; i++) {
    if (text[i] === last) {
      text[i] = value;
    }
  }
  text = text.join(' ' || '#');
  id_message.value = text;
  hashtags.innerHTML = '';
}



if (hashtags) {
  hashtags = Array.from(hashtags);
  hashtags.forEach((element) => {
    element.innerHTML = hashtag(element.textContent);
  });
}

let hashtagLinks = document.querySelectorAll('.hashtag');
if (hashtagLinks) {
  hashtagLinks = Array.from(hashtagLinks);
  hashtagLinks.forEach((element) => {
    tag = element.textContent.replace('#', '');
    element.href = `/hashtag/status/${tag}/`;
  });
}

// Event Listener
if (id_message) {
  id_message.addEventListener('input', async (e) => {
    changeCounter(e);
    meesageVlaue = myTrimHashtag(e.target.value);
    await detectHashtagWord(e);
    id_message.value = myTrimHashtag(String(meesageVlaue));

  });
}

function myTrimHashtag(text) {
  console.log('trim fucntion');
  text = text.replace('#', ' #');
  text = text.replace(/\s+/g, ' ');
  return text;
}
