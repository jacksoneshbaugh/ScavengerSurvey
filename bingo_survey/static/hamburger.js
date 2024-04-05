let hamburger = document.getElementById('hamburger');
let sideNav = document.getElementById('side-nav');
let body = document.body;
hamburger.addEventListener('click', function() {
    if (sideNav.classList.contains('active')) {
        sideNav.classList.remove('active');
        hamburger.classList.remove('active');
        body.classList.remove('lock-scroll')
    } else {
        sideNav.classList.add('active');
        hamburger.classList.add('active');
        body.classList.add('lock-scroll')
    }
});

// any tap outside the side nav will close it
document.addEventListener('click', function(event) {
    if (sideNav.classList.contains('active')) {
        if (event.target.id !== 'hamburger' && event.target.id !== 'side-nav') {
            sideNav.classList.remove('active');
            hamburger.classList.remove('active');
            body.classList.remove('lock-scroll')
        }
    }
});