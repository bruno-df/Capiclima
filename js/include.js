$(function() {
  $("#navbar").load("navbar.html");
});

$(function() {
  // Carrega a navbar e só depois executa o destaque
  $("#navbar").load("navbar.html", function() {
    var path = window.location.pathname.split("/").pop();
    if (path === "" || path === "/") path = "index.html"; // padrão para home

    // Para links normais
    $('.navbar-nav .nav-link').each(function() {
      if ($(this).attr('href') === path) {
        $(this).addClass('active');
      }
    });

    // Para o botão Apoie, se for um <a> fora do ul
    $('.btn[href]').each(function() {
      if ($(this).attr('href') === path) {
        $(this).addClass('active');
      }
    });
  });
});