const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const specType = document.getElementById('specType');
const message = document.getElementById('message');

uploadBtn.addEventListener('click', () => {
  const file = fileInput.files[0];
  const selectedType = specType.value;

  if (!selectedType) {
    message.textContent = 'Please select a specification type.';
    message.className = 'message error';
    return;
  }

  if (!file) {
    message.textContent = 'Please upload a Word file (.doc or .docx).';
    message.className = 'message error';
    return;
  }

  if (!file.name.endsWith('.doc') && !file.name.endsWith('.docx')) {
    message.textContent = 'Invalid file format. Please upload a .doc or .docx file.';
    message.className = 'message error';
    return;
  }

  message.textContent = 'File uploaded successfully as ' + selectedType + '.';
  message.className = 'message success';
});
