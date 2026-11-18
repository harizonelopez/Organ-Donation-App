// Hospital dashboard Structure
document.addEventListener("DOMContentLoaded", function () {
    const readData = (id) => {
        const element = document.getElementById(id);
        return element ? JSON.parse(element.textContent) : [];
    };

    const trendLabels = readData("reviewTrendLabels");
    const trendValues = readData("reviewTrendValues");
    const statusLabels = readData("reviewStatusLabels");
    const statusValues = readData("reviewStatusValues");
    const appointmentLabels = readData("appointmentChartLabels");
    const appointmentValues = readData("appointmentChartValues");

    if (typeof Chart === "undefined") return;

    Chart.defaults.font.family = "'DM Sans', sans-serif";
    Chart.defaults.color = "#8293a1";

    const trendCanvas = document.getElementById("reviewTrendChart");
    if (trendCanvas) {
        new Chart(trendCanvas, {
            type: "line",
            data: {
                labels: trendLabels,
                datasets: [{
                    label: "Review actions",
                    data: trendValues,
                    borderColor: "#0c9f91",
                    backgroundColor: "rgba(12,159,145,.12)",
                    borderWidth: 3,
                    fill: true,
                    tension: 0.38,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: "#ffffff",
                    pointBorderColor: "#0c9f91",
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: "#071b2c",
                        padding: 12,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 },
                        grid: { color: "#edf2f5" },
                        border: { display: false }
                    }
                }
            }
        });
    }

    const statusCanvas = document.getElementById("reviewStatusChart");
    if (statusCanvas) {
        new Chart(statusCanvas, {
            type: "doughnut",
            data: {
                labels: statusLabels,
                datasets: [{
                    data: statusValues,
                    backgroundColor: ["#e9a23b", "#0c9f91", "#e16b72"],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "74%",
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: "#071b2c",
                        padding: 12
                    }
                }
            }
        });
    }

    const appointmentCanvas = document.getElementById("appointmentChart");
    if (appointmentCanvas) {
        new Chart(appointmentCanvas, {
            type: "bar",
            data: {
                labels: appointmentLabels,
                datasets: [{
                    label: "Appointments",
                    data: appointmentValues,
                    backgroundColor: "#4388c7",
                    borderRadius: 6,
                    maxBarThickness: 38
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: "#071b2c",
                        padding: 12
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 },
                        grid: { color: "#edf2f5" },
                        border: { display: false }
                    }
                }
            }
        });
    }

    // Active navigation link
    document.querySelectorAll(".ops-nav-link").forEach(link => {
        link.addEventListener("click", function () {
            document.querySelectorAll(".ops-nav-link").forEach(item => {
                item.classList.remove("active");
            });

            this.classList.add("active");
        });
    });
});

