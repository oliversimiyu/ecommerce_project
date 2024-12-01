document.addEventListener('DOMContentLoaded', function() {
    // Initialize all carousels
    var carousels = document.querySelectorAll('.carousel');
    carousels.forEach(function(carousel) {
        new bootstrap.Carousel(carousel, {
            interval: 5000,  // Change slides every 5 seconds
            wrap: true,      // Continuous loop
            keyboard: true,  // Keyboard controls
            pause: 'hover'   // Pause on mouse hover
        });
    });

    // Add smooth transition effects
    document.querySelectorAll('.carousel-item').forEach(function(item) {
        item.addEventListener('transitionend', function() {
            if (this.classList.contains('active')) {
                this.querySelector('.carousel-caption').classList.add('animate__animated', 'animate__fadeInUp');
            }
        });
        
        item.addEventListener('transitionstart', function() {
            if (!this.classList.contains('active')) {
                this.querySelector('.carousel-caption').classList.remove('animate__animated', 'animate__fadeInUp');
            }
        });
    });
});
