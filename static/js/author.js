particlesJS.load('particles-js', '/static/js/particle_config.json', function() {
    // console.log('callback - particles.js config loaded');
});

$( document ).ready(function() {
    $('.ui.accordion').accordion();
    $('.ui.search').search({
        apiSettings: {
            url: '/search/?term={query}'
        },
      type: 'category'
    });

    // ===== Scroll to Top ==== 
    $(window).scroll(function() {
        if ($(this).scrollTop() >= 50) {        // If page is scrolled more than 50px
            $('#return-to-top').fadeIn(200);    // Fade in the arrow
        } else {
            $('#return-to-top').fadeOut(200);   // Else fade out the arrow
        }
    });
    $('#return-to-top').click(function() {      // When arrow is clicked
        $('body,html').animate({
            scrollTop : 0                       // Scroll to top of body
        }, 500);
    });
});


