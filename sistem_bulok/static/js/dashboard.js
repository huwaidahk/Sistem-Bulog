console.log('Sistem Bulok: dashboard.js loaded');

document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.auto-hide');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";

            // Hapus elemen setelah animasi hilang
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});
