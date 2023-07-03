function animateCounter(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current;
        if (current === endValue) {
            clearInterval(timer);
        }
    }, stepTime);
}
