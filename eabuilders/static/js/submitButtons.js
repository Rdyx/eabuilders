// Simple script to help user patienting after form submit to avoid unnecessary queries
const form = document.querySelector("form");
if (form) {
    form.addEventListener("submit", () => {
        document.getElementById('spinner-div').classList.remove('hidden');
        document.getElementById('spinner').classList.add('spin');
    });
}