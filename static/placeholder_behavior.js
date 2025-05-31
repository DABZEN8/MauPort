document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("titleInput");
    const originalPlaceholder = input.placeholder;

    input.addEventListener("focus", function () {
        input.placeholder = "";
    });

    input.addEventListener("blur", function () {
        if (input.value === "") {
            input.placeholder = originalPlaceholder;
        }
    });
});
