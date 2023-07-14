function animateCounter(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    const element = document.getElementsByClassName(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current;
        if (current === endValue) {
            clearInterval(timer);
        }
    }, stepTime);
}


function animateCounter2(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 0.1 : -0.1;
    const stepTime = Math.abs(Math.floor(duration / Math.abs(range)));
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current.toFixed(decimalPlaces);
        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue)) {
            clearInterval(timer);
        }
    }, stepTime);
}

function animateCounter3(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 0.1 : -0.1;
    const stepTime = Math.abs(Math.floor(duration / Math.abs(range)));
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent =current.toFixed(decimalPlaces)+ ' €';
        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue)) {
            clearInterval(timer);
        }
    }, stepTime);
}