document.addEventListener('DOMContentLoaded', () => {
    // Example: Toggle a class for theme switching
    const toggleButton = document.querySelector('#theme-toggle');
    toggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
    });
});
