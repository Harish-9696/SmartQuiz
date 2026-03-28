/**
 * form-validation.js – Generic Bootstrap 5 form validation helper.
 * Attach class "needs-validation" to any form to enable.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".needs-validation");
    Array.from(forms).forEach(function (form) {
      form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      }, false);
    });
  });
})();
