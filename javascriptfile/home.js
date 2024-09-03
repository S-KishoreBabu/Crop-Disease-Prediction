


document.addEventListener("DOMContentLoaded", function () {
    var topbar = document.getElementById('topbar');

    window.addEventListener("scroll", function () {
        var scrollPosition = window.scrollY;

        if (350 < scrollPosition) { 
            topbar.style.background = "rgba(38, 182, 61, 0.7)";
            topbar.style.backdropFilter = "blur(4px)";
            topbar.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.5)";
        }
        else {
            topbar.style.backgroundColor = "rgba(255, 0, 0, 0)";
            topbar.style.backdropFilter = "blur(0px)";
            topbar.style.boxShadow = "0 0 0px rgba(0, 0, 0, 0.5)";
        }
        reveal();
    });
});




