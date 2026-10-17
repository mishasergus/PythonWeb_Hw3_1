const tourInfos = document.querySelectorAll('.tour-card');

tourInfos.forEach(info => {
    info.addEventListener('click', () => {
        const imageUrl = info.getAttribute('data-img');
        if (imageUrl) {
            window.location.href = imageUrl;

        }
    });
});
const burgerBtn = document.getElementById('burgerBtn');
const mainNav = document.getElementById('mainNav');

if (burgerBtn && mainNav) {
    burgerBtn.addEventListener('click', () => {
        mainNav.classList.toggle('open');
        burgerBtn.classList.toggle('active');
    });
}