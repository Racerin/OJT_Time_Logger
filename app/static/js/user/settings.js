// Settings Tabs
const tabs = document.querySelectorAll('.tabs li');
const tabContents = document.querySelectorAll('#tab-content > div');

function selectActive(){};
function selectDetail(){};

// tabs.addEventListener('down', selectActive);
tabs.forEach(tab => {
    tab.addEventListener('click', ()=> {
        // Select active tab
        tabs.forEach(item => item.classList.remove('is-active'));
        tab.classList.add('is-active')

        // Set the content
        const target = tab.dataset.target;
        tabContents.forEach(tabContent => {
            // if (tabContent.getAttribute('id') == target){
            if (tabContent.id == target){
                tabContent.classList.remove('is-hidden');
            }
            else {
                tabContent.classList.add('is-hidden');
            };
        });
    })
});