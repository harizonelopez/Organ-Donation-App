// LIFELINK welcome screen entrance transition
document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll(
        ".welcome-heading, .portal-card, .benefit"
    );

    elements.forEach((element, index) => {
        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";

        setTimeout(() => {
            element.style.transition = "opacity 0.7s ease, transform 0.7s ease";
            element.style.opacity = "1";
            element.style.transform = "translateY(0)";
        }, 120 * index);
    });
});


