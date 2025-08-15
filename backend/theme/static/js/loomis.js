document.addEventListener("DOMContentLoaded", function () {
    const imgElement = document.getElementById("loomis-image");
    const intervalInput = document.getElementById("interval-input");
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const nextBtn = document.getElementById("next-btn");
    const timerOverlay = document.getElementById("timer-overlay");

    let loomisImages = [];
    let currentIndex = 0;
    let timerId = null;
    let countdownId = null;
    let timeLeft = 0; // en secondes

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    fetch("/loomis/count/")
        .then(response => response.json())
        .then(data => {
            const count = data.count;
            loomisImages = Array.from({ length: count }, (_, i) => `/static/loomis/face${i + 1}.jpg`);
            loomisImages = shuffleArray(loomisImages);
            showImage(0);
        })
        .catch(err => console.error("Erreur lors de la récupération du nombre d'images Loomis :", err));

    function showImage(index) {
        imgElement.style.opacity = 0;
        setTimeout(() => {
            imgElement.src = loomisImages[index];
            imgElement.style.opacity = 1;
            startCountdown();
        }, 300);
    }

    function nextImage() {
        currentIndex++;
        if (currentIndex >= loomisImages.length) {
            loomisImages = shuffleArray(loomisImages);
            currentIndex = 0;
        }
        showImage(currentIndex);
    }

    function startSlideshow() {
        stopSlideshow();
        const intervalMinutes = Math.max(0.1, parseFloat(intervalInput.value));
        const interval = intervalMinutes * 60 * 1000; // convert to ms
        timerId = setInterval(nextImage, interval);
        showImage(currentIndex);
    }

    function stopSlideshow() {
        if (timerId) {
            clearInterval(timerId);
            timerId = null;
        }
        if (countdownId) {
            clearInterval(countdownId);
            countdownId = null;
        }
    }

    function startCountdown() {
        if (countdownId) clearInterval(countdownId);

        const intervalMinutes = Math.max(0.1, parseFloat(intervalInput.value));
        timeLeft = Math.round(intervalMinutes * 60); // en secondes

        timerOverlay.classList.remove("hidden");
        updateTimerDisplay();

        countdownId = setInterval(() => {
            timeLeft--;
            if (timeLeft <= 0) {
                clearInterval(countdownId);
            }
            updateTimerDisplay();
        }, 1000);
    }

    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = String(timeLeft % 60).padStart(2, "0");
        timerOverlay.textContent = `${minutes}:${seconds}`;
    }

    // Plein écran au clic
    imgElement.addEventListener("click", () => {
        const imageContainer = imgElement.parentElement; // récupérer le parent
        if (imageContainer.requestFullscreen) {
            imageContainer.requestFullscreen();
        } else if (imageContainer.webkitRequestFullscreen) { // Safari
            imageContainer.webkitRequestFullscreen();
        } else if (imageContainer.msRequestFullscreen) { // IE/Edge
            imageContainer.msRequestFullscreen();
        }
    });


    startBtn.addEventListener("click", startSlideshow);
    stopBtn.addEventListener("click", stopSlideshow);
    nextBtn.addEventListener("click", nextImage);
});
