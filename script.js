// ==== Upload Button Logic ====
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const specType = document.getElementById('specType');
const message = document.getElementById('resultMessage');

document.addEventListener("DOMContentLoaded", () => {
  if (message && message.textContent.trim() !== "") {
    setTimeout(() => {
      message.style.opacity = "0";
      setTimeout(() => {
        message.style.display = "none";
      }, 500);
    }, 3000);
  }
});

uploadBtn.addEventListener('click', (e) => {
  const file = fileInput.files[0];
  const selectedType = specType.value;

  if (!selectedType || !file) {
    e.preventDefault(); // stop form submission
    message.textContent = '⚠️ Please select a type and upload a Word file.';
    message.className = 'result-message error';
    return;
  }

  if (!file.name.endsWith('.doc') && !file.name.endsWith('.docx')) {
    e.preventDefault();
    message.textContent = '⚠️ Invalid format. Upload a .doc or .docx file.';
    message.className = 'result-message error';
    return;
  }

  message.textContent = '⏳ Uploading... please wait.';
  message.className = 'result-message';
});

// ==== Validate subject code input ====
function validateSubjectCode(input) {
  input.value = input.value.replace(/[^0-9]/g, '').slice(0, 3);
}

// ==== Chart logic (same core) ====
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
    chartError.textContent = '⚠️ Please select a department.';
    chartError.style.display = 'block';
    return;
  }

  const validCodeFormat = /^[A-Z]{3,4}\d{3}$/;
  if (code && !validCodeFormat.test(code)) {
    chartError.textContent = '⚠️ Code must end in 3 digits (e.g., BIO390).';
    chartError.style.display = 'block';
    return;
  }

  chartAllInstance = new Chart(chartAllCanvas, {
    type: 'bar',
    data: {
      labels: departmentData[dept],
      datasets: [{
        label: `Average Score for ${dept}`,
        data: departmentData[dept].map(() => Math.floor(Math.random() * 50 + 50)),
        backgroundColor: '#4f4a8b'
      }]
    },
    options: { responsive: true }
  });

  if (code && departmentData[dept].includes(code)) {
    chartSubjectCanvas.style.display = 'block';

    let labels = ['Quiz', 'Midterm', 'Project', 'Final'];
    let subjectData = [10, 30, 25, 35];
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
  } else if (code) {
    chartError.textContent = '⚠️ Invalid subject code.';
    chartError.style.display = 'block';
  }

  showQueryList(dept, code);
});

// ==== Show processed queries ====
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
      content += `<br><br><strong style=\"color:#d25629\">Invalid subject code provided: ${code}</strong>`;
    }
  }

  queryList.innerHTML = content;
}
