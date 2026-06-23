/**
 * CapiClima — Contadores animados e atualização em tempo real
 *
 * Lê a URL da API a partir do atributo data-stats-url na .stats-section.
 */
(function () {

    /* ---- Animated count-up ---- */
    function animateCounter(el) {
        if (el.dataset.animated) return;
        var target = parseInt(el.dataset.target, 10);
        if (isNaN(target)) return;
        el.dataset.animated = '1';
        var suffix = el.dataset.suffix || '';
        var duration = 1600;
        var start = performance.now();

        function step(now) {
            var elapsed = now - start;
            var progress = Math.min(elapsed / duration, 1);
            /* easeOutExpo */
            var ease = 1 - Math.pow(2, -10 * progress);
            var current = Math.round(ease * target);
            el.textContent = current + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    /* ---- Trigger on scroll (IntersectionObserver) ---- */
    var statsSection = document.querySelector('.stats-section');
    if (!statsSection) return;

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var counters = entry.target.querySelectorAll('.stat-number[data-target]');
                counters.forEach(animateCounter);
            }
        });
    }, { threshold: 0.3 });

    observer.observe(statsSection);

    /* ---- Real-time polling every 30 s ---- */
    var apiUrl = statsSection.dataset.statsUrl;
    if (!apiUrl) return;

    function refreshStats() {
        fetch(apiUrl)
            .then(function (r) { return r.json(); })
            .then(function (data) {
                var elAtiv = document.getElementById('stat-atividades');
                var elEquipe = document.getElementById('stat-equipe');
                if (elAtiv && data.total_atividades !== undefined) {
                    var prev = parseInt(elAtiv.textContent, 10) || 0;
                    if (data.total_atividades !== prev) {
                        elAtiv.dataset.target = data.total_atividades;
                        elAtiv.dataset.animated = '';
                        animateCounter(elAtiv);
                    }
                }
                if (elEquipe && data.total_equipe !== undefined) {
                    var prev2 = parseInt(elEquipe.textContent, 10) || 0;
                    if (data.total_equipe !== prev2) {
                        elEquipe.dataset.target = data.total_equipe;
                        elEquipe.dataset.animated = '';
                        animateCounter(elEquipe);
                    }
                }
            })
            .catch(function () { /* silently retry next interval */ });
    }

    setInterval(refreshStats, 30000);

})();
