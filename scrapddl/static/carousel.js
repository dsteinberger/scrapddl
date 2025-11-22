
// Carousel initialization for Bootstrap 5
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all carousels
    var carousels = document.querySelectorAll('.carousel');
    carousels.forEach(function(carouselElement) {
        // Bootstrap 5 uses bootstrap.Carousel class
        if (typeof bootstrap !== 'undefined') {
            new bootstrap.Carousel(carouselElement, {
                interval: false,
                wrap: false,
                touch: true,
                ride: false
            });
        }
    });
});