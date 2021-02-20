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
	const hitCountUrl =
		'https://' +
		hitCountDomain +
		'.pythonanywhere.com/' +
		countUrl +
		'?url=' +
		url;

	const xhr = new XMLHttpRequest();
	xhr.withCredentials = true;
	xhr.open('GET', hitCountUrl);
	xhr.onload = function () {
		if (xhr.status === 200) {
			const hitCount = xhr.responseText;
			replaceTextInElementById(elementId, hitCount);
		}
	};
	xhr.send();
}
