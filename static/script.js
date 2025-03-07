// Author: Garry Ivanovs
// Created: 07-03-2025
// Last modified: 07-03-2025

document.addEventListener("DOMContentLoaded", function () {
    const today = new Date().toISOString().split("T")[0];

    const dateOfRotation = document.getElementById("dateOfRotation");
    if (dateOfRotation) {
        dateOfRotation.value = today;
    }

    const newLastRotated = document.getElementById("newLastRotated");
    if (newLastRotated) {
        if (newLastRotated.value === "") {
            newLastRotated.value = today;
        }
    }
});
