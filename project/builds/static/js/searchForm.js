function removeEmptyInputs(querySelector) {
  Array.from(document.querySelectorAll(querySelector)).forEach((elem) => {
    if (!elem.value) {
      elem.disabled = true;
    }
  });
}

document.getElementById('search-form-submit').onclick = () => {
  removeEmptyInputs('input[type=text]');
  removeEmptyInputs('select');
};
