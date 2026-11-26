const burgerBtnOpen = document.getElementById('burger-btn');
const burgerBtnHide = document.getElementById('burget-btn-hide'); // Se mantiene id original
const hiddenNav = document.getElementById('hidden-nav');

burgerBtnOpen.addEventListener('click', () => {
    hiddenNav.classList.remove('hiden');
});

burgerBtnHide.addEventListener('click', () => {
    hiddenNav.classList.add('hiden');
});
hiddenNav.addEventListener('click', (e) => {
    if (e.target === hiddenNav) {
        hiddenNav.classList.add('hiden');
    }
});

const navLinks = document.querySelectorAll('.link-menu-floating .nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hiddenNav.classList.add('hiden');
    });
});