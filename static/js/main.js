// Obtenez des références vers les éléments du menu burger
const iconeBurger = document.querySelector('.menu-burger');
const menuDeroulant = document.querySelector('.dropdown-menu');

// Ajoutez un écouteur d'événements de clic à l'icône du menu burger
iconeBurger.addEventListener('click', () => {
    // Basculez la visibilité du menu déroulant
    menuDeroulant.classList.toggle('afficher');
});

// Ajoutez un écouteur d'événements de clic au document pour masquer le menu déroulant lors du clic en dehors de celui-ci
document.addEventListener('click', (e) => {
    if (!iconeBurger.contains(e.target) && !menuDeroulant.contains(e.target)) {
        menuDeroulant.classList.remove('afficher');
    }
});

function openSidebar() {
    document.querySelector('.sidebar').style.width = '250px';
    document.querySelector('.open-button').style.display = 'none';
    document.querySelector('.close-button').style.display = 'block';
}

function closeSidebar() {
    document.querySelector('.sidebar').style.width = '0';
    document.querySelector('.open-button').style.display = 'block';
    document.querySelector('.close-button').style.display = 'none';
}


