// Ugly, too lazy for today
// TODO: refactor this
function deleteBuild(link) {
    const ask = window.confirm("Are you sure you want to delete this version of your build? You won't be able to retrieve it.");

    if (ask) {
        window.location.href = link;
    }
}

function deleteAllBuilds(link) {
    const ask = window.confirm("Are you sure you want to delete all versions of your build? You won't be able to retrieve it.");

    if (ask) {
        window.location.href = link;
    }
}
