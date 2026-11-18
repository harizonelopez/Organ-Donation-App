// Active navigation link
document.querySelectorAll(".sidebar-link").forEach(link => {
    link.addEventListener("click", function () {
        document.querySelectorAll(".sidebar-link").forEach(item => {
            item.classList.remove("active");
        });

        this.classList.add("active");
    });
});