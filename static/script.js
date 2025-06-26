// ===== Upload logic =====
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const specType = document.getElementById('specType');

document.addEventListener("DOMContentLoaded", () => {
  const messageDiv = document.getElementById("resultMessage");
  if (messageDiv && messageDiv.textContent.trim() !== "") {
    setTimeout(() => {
      messageDiv.style.opacity = "0";
      setTimeout(() => {
        messageDiv.style.display = "none";
      }, 500); // وقت الإخفاء بعد الانميشن
    }, 3000); // انتظر 3 ثواني قبل بدء الإخفاء
  }
});



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

  const formData = new FormData();
  formData.append('docx_files', file);
  formData.append('file_type', selectedType);

  message.textContent = '⏳ Uploading... please wait.';
  message.className = 'message';

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then(res => res.text())
    .then(data => {
      message.innerHTML = data.includes('✅')
        ? '✅ File processed and uploaded to Firebase.'
        : data;
      message.className = data.includes('✅') ? 'message success' : 'message error';
    })
    .catch(err => {
      console.error('Error:', err);
      message.textContent = '⚠️ Error uploading file.';
      message.className = 'message error';
    });
});


// ===== Chart logic =====
const departmentData = {
  BIO: ['BIO101', 'BIO210', 'BIO390'],
  CHEM: ['CHEM101', 'CHEM202'],
  PHYS: ['PHYS101']
};

const loadBtn = document.getElementById('loadCharts');
const chartAllCanvas = document.getElementById('chartAll');
const chartSubjectCanvas = document.getElementById('chartSubject');
const chartError = document.getElementById('chartError');

let chartAllInstance = null;
let chartSubInstance = null;

loadBtn.addEventListener('click', () => {
  const dept = document.getElementById('department').value;
  const code = document.getElementById('subjectCode').value.trim().toUpperCase();
  const chartType = document.getElementById('chartType').value;

  chartError.style.display = 'none';
  chartSubjectCanvas.style.display = 'none';

  if (chartAllInstance) chartAllInstance.destroy();
  if (chartSubInstance) chartSubInstance.destroy();

  if (!dept) {
    chartError.textContent = 'Please select a department.';
    chartError.style.display = 'block';
    return;
  }

  const validCodeFormat = /^[A-Z]{3,4}\d{3}$/;
  if (code && !validCodeFormat.test(code)) {
    chartError.textContent = 'Subject code format is invalid. Must end with exactly 3 digits (e.g., BIO390).';
    chartError.style.display = 'block';
    return;
  }

  // Chart for all subjects in department
  chartAllInstance = new Chart(chartAllCanvas, {
    type: 'bar',
    data: {
      labels: departmentData[dept],
      datasets: [{
        label: `Average Score for ${dept} Dept`,
        data: departmentData[dept].map(() => Math.floor(Math.random() * 50 + 50)),
        backgroundColor: '#4f4a8b'
      }]
    },
    options: { responsive: true }
  });

  // If subject code is provided
  if (code) {
    if (departmentData[dept].includes(code)) {
      chartSubjectCanvas.style.display = 'block';

      let subjectData = [10, 30, 25, 35];
      let labels = ['Quiz', 'Midterm', 'Project', 'Final'];
      let backgroundColors = ['#058646', '#d25629', '#4f4a8b', '#999'];

      if (chartType === "evaluation") {
        labels = ['Direct', 'Indirect'];
        subjectData = [70, 30];
      } else if (chartType === "stakeholders") {
        labels = ['Instructor', 'Coordinator', 'Institution'];
        subjectData = [40, 35, 25];
      }

      chartSubInstance = new Chart(chartSubjectCanvas, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: `Assessment Breakdown for ${code}`,
            data: subjectData,
            backgroundColor: backgroundColors
          }]
        }
      });
    } else {
      chartError.textContent = 'Invalid subject code.';
      chartError.style.display = 'block';
    }
  }

  showQueryList(dept, code);
});

// ===== Show list of queries used =====
function showQueryList(dept, code) {
  const queryList = document.getElementById('queryList');
  queryList.innerHTML = '';

  if (!dept || !departmentData[dept]) {
    queryList.innerHTML = `<strong>No department selected or invalid department.</strong>`;
    return;
  }

  const validSubjects = departmentData[dept].filter(c => /\d{3}$/.test(c));
  let content = `<strong>Processed Queries for Department ${dept}:</strong><br>`;
  content += validSubjects.map(c => `• ${c}`).join('<br>');

  if (code) {
    if (validSubjects.includes(code)) {
      content += `<br><br><strong>Detailed Subject Query:</strong><br>• ${code}`;
    } else {
      content += `<br><br><strong style="color:#d25629">Invalid subject code provided: ${code}</strong>`;
    }
  }

  queryList.innerHTML = content;
}
