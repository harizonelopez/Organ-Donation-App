// Global notification auto-dismiss
document.addEventListener("DOMContentLoaded", () => {
    const notifications = document.querySelectorAll(".ll-toast");

    notifications.forEach((notification) => {
        setTimeout(() => {
            notification.classList.add("ll-toast-exit");

            setTimeout(() => {
                notification.remove();
            }, 350);

        }, 4000);
    });
});

// Active navigation link when clicked
document.querySelectorAll(".ops-nav-link").forEach(link => { d
    link.addEventListener("click", function () {
        document.querySelectorAll(".ops-nav-link").forEach(item => {
            item.classList.remove("active");
        });

        this.classList.add("active");
    });
});


