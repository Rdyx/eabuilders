function removeEmptyInputs(querySelector) {
  Array.from(document.querySelectorAll(querySelector)).forEach((elem) => {
    if (!elem.value) {
      elem.disabled = true;
    }
  });
}

document.getElementById('search-build-form-submit').onclick = () => {
  removeEmptyInputs('input[type=text]');
  removeEmptyInputs('select');
};
