
document.addEventListener("DOMContentLoaded", function (){
    const toggles = document.querySelectorAll(".toggle-password");
    toggles.forEach(function (toggle) {
        toggle.addEventListener("click", function (){
            const targetID = this.getAttribute("data-target");
            const passwordField = document.getElementById(targetID);

            if (passwordField.type === "password") {
                passwordField.type = "text";

                this.classList.remove("fa-eye-slash");
                this.classList.add("fa-eye");
            } else {
                passwordField.type = "password";

                this.classList.remove("fa-eye");

                this.classList.add("fa-eye-slash");
            }
        });
    });
});