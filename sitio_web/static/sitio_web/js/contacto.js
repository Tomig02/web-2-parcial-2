
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("contact-form");

    if (!form) return;

    const nombre = form.querySelector("#id_nombre");
    const email = form.querySelector("#id_email_telefono");
    const motivo = form.querySelector("#id_motivo");
    const mensaje = form.querySelector("#id_mensaje");

    function showError(input, message) {
        clearError(input);

        const error = document.createElement("span");
        error.className = "form-error js-error";
        error.textContent = message;

        input.classList.add("input-invalid");
        input.insertAdjacentElement("afterend", error);
    }

    function clearError(input) {
        input.classList.remove("input-invalid");

        const next = input.nextElementSibling;

        if (next && next.classList.contains("js-error")) {
            next.remove();
        }
    }

    function validateField(input, validation, message) {
        clearError(input);

        if (!validation) {
            showError(input, message);
            return false;
        }

        return true;
    }

    function validateForm() {
        let valid = true;

        // Nombre
        const nombreValue = nombre.value.trim();

        const nombreRegex = /^[A-Za-zÁÉÍÓÚáéíóúÜüÑñ\s]+$/;
        valid &= validateField(
            nombre,
            nombreValue.length >= 3 &&
            nombreValue.length <= 100 &&
            nombreRegex.test(nombreValue),
            "Ingresá un nombre válido, sin números ni caracteres especiales."
        );

        // Email
        const emailValue = email.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        valid &= validateField(
            email,
            emailRegex.test(emailValue) && emailValue.length <= 150,
            "Ingresá un correo electrónico válido."
        );

        // Motivo
        valid &= validateField(
            motivo,
            motivo.value !== "",
            "Seleccioná un motivo de consulta."
        );

        // Mensaje
        const mensajeValue = mensaje.value.trim();

        valid &= validateField(
            mensaje,
            mensajeValue.length >= 10,
            "El mensaje debe tener al menos 10 caracteres."
        );

        return Boolean(valid);
    }

    // Validación al enviar
    form.addEventListener("submit", (event) => {
        if (!validateForm()) {
            event.preventDefault();
        }
    });

    // Limpiar errores mientras el usuario corrige
    [nombre, email, motivo, mensaje].forEach(input => {
        input.addEventListener("input", () => clearError(input));
        input.addEventListener("change", () => clearError(input));
    });

});
