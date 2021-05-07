let textClickPower = 'Your click power: ';
let textCoins = 'You have: ';
let textPrice = ' coins';


async function callbackClick() {
    let sound = new Audio();
    sound.src = 'static/hentai_information/audio/nya.mp3'
    sound.volume = 0.1;
    await sound.play();
    let coins = await (await fetch('/clicker/click/', {method: 'GET'})).json();
    document.querySelector('.coins').innerHTML = textCoins + coins
}

async function buyBoost(id) {
    let data = await (await fetch('/clicker/buyBoost/' + id + '/', {method: 'GET'})).json();
    document.querySelector('.clickPower').innerHTML = textClickPower + data['clickPower'];
    document.querySelector('.coins').innerHTML = textCoins + data['coins'];
    document.querySelector('.price-' + id).innerHTML = data['price'] + textPrice;
}