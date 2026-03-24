document.addEventListener('DOMContentLoaded', () => {
    // --- Configuración ---
    // Aquí puedes cambiar el título de la clase y la duración en segundos.
    const config = {
        "mainTitle": "Webinar 22-Sprint 7- Análisis estadístico para detectar patrones y outliers",
        "subtitle": "Comenzamos en Breve ⏳",
        "countdownDuration": 600
    };
    // ---------------------

    const mainTitleElement = document.getElementById('main-title');
    const subtitleElement = document.getElementById('subtitle');
    const countdownTimerElement = document.getElementById('countdown-timer');

    let countdownInterval;

    // Iniciar la aplicación
    try {
        mainTitleElement.textContent = config.mainTitle;
        subtitleElement.textContent = config.subtitle;
        startCountdown(config.countdownDuration);
    } catch (error) {
        console.error('Error al iniciar la aplicación:', error);
        mainTitleElement.textContent = "Error al Cargar";
        countdownTimerElement.textContent = "---";
    }

    function startCountdown(durationInSeconds) {
        let timer = durationInSeconds;

        countdownInterval = setInterval(() => {
            if (timer < 0) {
                clearInterval(countdownInterval);
                countdownTimerElement.textContent = "¡Comenzamos!";
                countdownTimerElement.style.animation = 'none';
                countdownTimerElement.style.transform = 'scale(1.1)';
                return;
            }
            
            const minutes = Math.floor(timer / 60);
            let seconds = timer % 60;

            // Formatear para que siempre tenga dos dígitos
            seconds = seconds < 10 ? '0' + seconds : seconds;
            const minutesStr = minutes < 10 ? '0' + minutes : minutes;

            countdownTimerElement.textContent = `${minutesStr}:${seconds}`;
            timer--;

        }, 1000);
    }
});