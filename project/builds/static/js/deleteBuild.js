// Ugly, too lazy for today
// TODO: refactor this
function deleteBuild(link) {
    const ask = window.confirm("Do you really want to delete this version of your build? You won't be able to get it back.");

    if (ask) {
        window.location.href = link;
    }
}

function deleteAllBuilds(link) {
    const ask = window.confirm("Do you really want to delete all versions of your build? You won't be able to get it back.");

    if (ask) {
        window.location.href = link;
    }
}

function deleteTeam(link) {
    const ask = window.confirm("Do you really want to delete your team? You won't be able to get it back.");

    if (ask) {
        window.location.href = link;
    }
}
