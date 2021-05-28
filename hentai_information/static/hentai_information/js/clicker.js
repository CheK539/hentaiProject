let textClickPower = 'Your click power: ';
let textCoins = 'You have: ';
let textPrice = ' coins';
let sound = new Audio();
sound.src = 'static/hentai_information/audio/nya.mp3'
sound.volume = 0.08;
let boostSounds = []
boostsCount = 2;
for (let i = 1; i < boostsCount + 1; i++) {
    let newSound = new Audio();
    newSound.src = 'static/hentai_information/audio/sound-' + i + '.mp3';
    boostSounds.push(newSound);
    boostSounds[i - 1].volume = 0.4;
}


async function callbackClick() {

    if (sound.currentTime > 0.3 || sound.currentTime === 0) {
        sound.pause();
        sound.currentTime = 0;
        await sound.play();
    }

    let coins = await (await fetch('/clicker/click/', {method: 'GET'})).json();
    document.querySelector('.coins').innerHTML = textCoins + coins
}

async function buyBoost(id, count) {
    boostSounds[count].pause();
    boostSounds[count].currentTime = 0;
    await boostSounds[count].play();
    let data = await (await fetch('/clicker/buyBoost/' + id + '/', {method: 'GET'})).json();
    document.querySelector('.clickPower').innerHTML = textClickPower + data['clickPower'];
    document.querySelector('.coins').innerHTML = textCoins + data['coins'];
    document.querySelector('.price-' + id).innerHTML = data['price'] + textPrice;
}