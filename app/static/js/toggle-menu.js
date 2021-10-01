//mobile menu
const burgerIcon = document.querySelector('#burger');
const navbarMenu = document.querySelector('#nav-links');

function toggleMenu(){
    navbarMenu.classList.toggle('is-active')
};
burgerIcon.addEventListener('click', toggleMenu);