//modal, AUld Lang Syne
const auldBtn = document.querySelector('#auld-button');
const modalBg = document.querySelector('#auld-bg');
const modalAuld = document.querySelector('#auld');

auldBtn.addEventListener('click', ()=>{
    modalAuld.classList.add('is-active');
});
modalBg.addEventListener('click', ()=>{
    modalAuld.classList.remove('is-active')
})