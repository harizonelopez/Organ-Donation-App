/* =========================================
   GLOBAL NOTIFICATION AUTO-DISMISS
========================================= */
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


