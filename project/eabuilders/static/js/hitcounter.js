/**
 * Replace target element inner html
 * @param string elementId
 * @param string text
 */
function replaceTextInElementById(elementId, text) {
    document.getElementById(elementId).innerHTML = text;
}

/**
 * Make ajax request and update hits counter
 * @param string url
 * @param string elementId
 */
function updateHitCounterText(url, elementId, count = false) {
    const hitCountDomain = 'rdyx';
    const countUrl = count ? 'count' : 'nocount';

    return $.ajax('https://' + hitCountDomain + '.pythonanywhere.com/' + countUrl, {
        data: { url: url },
        xhrFields: { withCredentials: true },
    }).then(
        (hitCount) => {
            replaceTextInElementById(elementId, hitCount);
        }
    );
}
