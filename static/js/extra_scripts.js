// Auto-dismiss alerts after 4 seconds
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    const alerts = document.querySelectorAll(".auto-dismiss-alert");
    alerts.forEach(alert => {
      // Bootstrap way to close alerts
      let bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    });
  }, 4000);
});
