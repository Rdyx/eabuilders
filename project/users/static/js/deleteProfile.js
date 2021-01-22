function deleteProfile() {
    const ask = window.confirm("Are you sure you want to delete your profile? Every build related to you will be delete too.");

    if (ask) {
        window.location.href = deleteUserUrl;
    }
}