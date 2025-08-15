document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.querySelectorAll('.alert, .django-message').forEach(function(el) {
            el.style.transition = "opacity 0.5s";
            el.style.opacity = 0;
            setTimeout(function() { el.style.display = "none"; }, 500);
        });
    }, 5000);
});
