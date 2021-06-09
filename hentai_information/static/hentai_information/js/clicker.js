let sound = new Audio();
sound.src = 'static/hentai_information/audio/nya.mp3'
sound.volume = 0.08;
let boostSounds = []
boostsCount = 2;
let userId = JSON.parse(document.getElementById('user_id').textContent);
let cache = getCache()

activateBoosts()
setAutoClickInterval()
saveCoinsInterval()

for (let i = 1; i < boostsCount + 1; i++) {
    let newSound = new Audio();
    newSound.src = 'static/hentai_information/audio/sound-' + i + '.mp3';
    boostSounds.push(newSound);
    boostSounds[i - 1].volume = 0.4;
}

async function getCache() {
    return (await (await fetch('/json/' + userId, {method: 'GET'})).json())[0]
}

async function callbackClick() {

    if (sound.currentTime > 0.3 || sound.currentTime === 0) {
        await sound.pause();
        sound.currentTime = 0;
        await sound.play();
    }

    cache.then(data => {
        data['coins'] += data['clickPower']

        document.querySelector('.coins .data').innerText = data['coins']
        activateBoosts()
    })
}

function buyBoost(id, count) {
    boostSounds[count].pause();
    boostSounds[count].currentTime = 0;
    boostSounds[count].play();

    cache.then(cacheData => {
        let token = getCookie('csrftoken')
        let coins = cacheData['coins']

        saveCoins(coins).then(_ => {
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
                cacheData['clickPower'] = data['clickPower']
                cacheData['autoClickPower'] = data['autoClickPower']
                cacheData['coins'] = data['coins']

                document.querySelector('.clickPower .data').innerText = data['clickPower'];
                document.querySelector('.autoClick .data').innerText = data['autoClickPower'];
                document.querySelector('.coins .data').innerText = data['coins'];
                document.querySelector('.price-' + id).innerHTML = data['price'];

                activateBoosts()
            })
        })
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

    if (boost['type'] === 1)
        boostList = document.querySelector('.autoClickBoosts')

    let boostTemplate = document.querySelector('#boost-template').content;
    let newBoost = boostTemplate.querySelector('.boost')
    let boostItem = newBoost.cloneNode(true)
    let text = boostItem.querySelector('.text-simp')
    text.textContent = boost.name + " (+" + boost['power'] + " power)"

    let price = boostItem.querySelector('.simp-price')
    price.textContent = boost['price']
    price.classList.add('price-' + boost.id)

    let image = boostItem.querySelector('.image-simp')

    if (boost['type'] === 0)
        image.src = '/static/hentai_information/images/simp-1.png'
    if (boost['type'] === 1)
        image.src = '/static/hentai_information/images/autoBoost-1.png'

    boostItem.addEventListener('click', function () {
        buyBoost(boost.id, 1)
    })

    boostList.appendChild(boostItem)
}

function setAutoClickInterval() {
    setInterval(function () {
        cache.then(data => {
            let coinsField = document.querySelector('.coins .data')
            let autoClickField = document.querySelector('.autoClick .data').innerText

            data['coins'] += parseInt(autoClickField)
            coinsField.innerText = data['coins'];

            activateBoosts()
        })
    }, 1000)
}

function saveCoinsInterval() {
    setInterval(async function () {
        cache.then(cacheData => {
            saveCoins(cacheData['coins'])
        })
    }, 10000)
}

function saveCoins(coins) {
    let token = getCookie('csrftoken')

    return fetch('/clicker/saveCoins/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            coins: coins,
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return Promise.reject(response)
        }
    }).then(data => {
        let boost = data['boost']

        if (boost)
            renderBoost(boost)
    }).catch(err => console.log(err))
}

function activateBoosts() {
    cache.then(data => {
        let coins = data['coins']
        const boosts = document.querySelectorAll('.boost')

        for (let boost of boosts) {
            activateBoost(coins, boost)
        }
    })
}

function activateBoost(coins, boost) {
    let price = parseInt(boost.querySelector(".simp-price").innerText)

    if (price > coins) {
        boost.setAttribute('disabled', 'true')
        boost.style.pointerEvents = 'none';
    } else {
        boost.removeAttribute('disabled')
        boost.style.pointerEvents = 'auto';
    }
}