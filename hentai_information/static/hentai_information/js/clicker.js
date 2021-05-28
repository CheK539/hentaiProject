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

    let data = await (await fetch('/clicker/click/', {method: 'GET'})).json();

    document.querySelector('.coins').innerHTML = textCoins + data['coins']

    let boost = data['boost']

    if (boost)
        renderBoost(boost)
}

function buyBoost(id, count) {
    let token = getCookie('csrftoken')

    boostSounds[count].pause();
    boostSounds[count].currentTime = 0;
    boostSounds[count].play();

    fetch('/clicker/buyBoost/', {
        method: 'POST',
        headers: {"X-CSRFToken": token, 'Content-Type': 'application/json'},
        body: JSON.stringify({boost_id: id})
    }).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return Promise.reject(response)
        }
    }).then(data => {
        document.querySelector('.clickPower').innerHTML = textClickPower + data['clickPower'];
        document.querySelector('.coins').innerHTML = textCoins + data['coins'];
        document.querySelector('.price-' + id).innerHTML = data['price'] + textPrice;
    })
}

function getCookie(name) {
    let resultCookie = null

    if (document.cookie !== '') {
        document.cookie.split(';').some(function (cookie) {
            let clearCookie = cookie.trim()

            if (clearCookie.substring(0, name.length) === name) {
                resultCookie = decodeURIComponent(clearCookie.substring(name.length + 1))
                return true
            }
        })
    }

    return resultCookie
}

function renderBoost(boost) {
    let boostList = document.querySelector('.boosts')
    let boostTemplate = document.querySelector('#boost-template').content;
    let newBoost = boostTemplate.querySelector('.boost')

    let boostItem = newBoost.cloneNode(true)
    let text = boostItem.querySelector('.text-simp')
    text.textContent = boost.name + " (+" + boost.power + " power)"

    let price = boostItem.querySelector('.simp-price')
    price.textContent = boost.price + " coins"
    price.classList.add('price-' + boost.id)

    let image = boostItem.querySelector('.image-simp')
    image.src = '/static/hentai_information/images/simp-1.png'

    boostItem.addEventListener('click', function () {
        buyBoost(boost.id, 1)
    })

    boostList.appendChild(boostItem)
}