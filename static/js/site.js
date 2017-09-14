particlesJS.load('particles-js', '/static/js/particle_config.json', function() {
    // console.log('callback - particles.js config loaded');
});

$( document ).ready(function() {
    $('.ui.search').search({
        apiSettings: {
            url: '/search/?term={query}'
        },
      type: 'category'
    });
});


