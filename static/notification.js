document.addEventListener("DOMContentLoaded", function () {
    const notification = document.getElementById("notification");
    const closeBtn = document.querySelector(".close-btn");

    // Show the notification
    setTimeout(() => {
        notification.classList.add("show");
    }, 100); // Small delay to trigger the animation

    // Automatically hide the notification after 4 seconds
    setTimeout(() => {
        notification.classList.remove("show");
    }, 4000);

    // Close notification on button click
    closeBtn.addEventListener("click", () => {
        notification.classList.remove("show");
    });
});
