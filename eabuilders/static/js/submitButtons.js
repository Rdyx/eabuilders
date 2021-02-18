// Simple script to help user patienting after form submit to avoid unnecessary queries

document.querySelector("form").addEventListener("submit", () => {
    document.getElementById('spinner-div').classList.remove('hidden');
    document.getElementById('spinner').classList.add('spin');
});