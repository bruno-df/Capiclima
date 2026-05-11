/**
 * CapiClima — JavaScript (Vanilla, sem jQuery)
 */
document.addEventListener('DOMContentLoaded', () => {

    // Fechar navbar mobile ao clicar em link
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navCollapse = document.getElementById('navbarNav');
    if (navCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                if (bsCollapse) bsCollapse.hide();
            });
        });
    }

});