function showSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'flex';
}

function hideSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'none';
}

function showMenu(menuClass) {
    const menus = document.querySelectorAll('ul.users, ul.productos, ul.proveedores, ul.bodega');
    menus.forEach(menu => {
        if (menu.classList.contains(menuClass)) {
            menu.classList.toggle('hidden');
        } else {
            menu.classList.add('hidden');
        }
    });
}
