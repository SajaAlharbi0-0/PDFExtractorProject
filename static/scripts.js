// ===== Upload logic =====
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const specType = document.getElementById('specType');
const message = document.getElementById('message');

document.addEventListener("DOMContentLoaded", () => {
  const messageDiv = document.getElementById("resultMessage");
  if (messageDiv && messageDiv.textContent.trim() !== "") {
    setTimeout(() => {
      messageDiv.style.opacity = "0";
      setTimeout(() => {
        messageDiv.style.display = "none";
      }, 500);
    }, 3000);
  }
});

uploadBtn?.addEventListener('click', () => {
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


// ===== Load Departments =====
function loadDepartments() {
  const fileType = document.getElementById("fileType").value;
  const departmentDropdown = document.getElementById("department");

  departmentDropdown.innerHTML = '<option value="" disabled selected>Loading...</option>';

  fetch("/get_departments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fileType: fileType })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      departmentDropdown.innerHTML = '<option value="" disabled selected>Select Department</option>';
      data.departments.forEach(dep => {
        const option = document.createElement("option");
        option.value = dep;
        option.textContent = dep;
        departmentDropdown.appendChild(option);
      });
    } else {
      departmentDropdown.innerHTML = '<option value="" disabled selected>No departments found</option>';
    }
  })
  .catch(() => {
    departmentDropdown.innerHTML = '<option value="" disabled selected>Error loading departments</option>';
  });
}


// ===== Chart logic =====
const loadBtn = document.getElementById('loadCharts');
const chartAllCanvas = document.getElementById('chartAll');
const chartSubjectCanvas = document.getElementById('chartSubject');
const chartError = document.getElementById('chartError');

let chartAllInstance = null;
let chartSubInstance = null;

loadBtn.addEventListener('click', () => {
  const fileType = document.getElementById('fileType').value;
  const department = document.getElementById('department').value;
  const subjectCode = document.getElementById('subjectCode').value.trim();
  const chartType = document.getElementById('chartType').value;

  chartError.style.display = 'none';
  chartSubjectCanvas.style.display = 'none';

  if (chartAllInstance) chartAllInstance.destroy();
  if (chartSubInstance) chartSubInstance.destroy();

  if (!fileType || !department || !chartType) {
    chartError.textContent = 'Please select file type, department, and chart type.';
    chartError.style.display = 'block';
    return;
  }

  fetch('/get_charts_data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      fileType,
      department,
      subjectCode,
      chartType
    })
  })
  .then(res => res.json())
  .then(res => {
    if (res.status !== 'success') {
      chartError.textContent = res.message || 'Failed to load chart data.';
      chartError.style.display = 'block';
      return;
    }

    const labels = res.data.labels;
    const values = res.data.values;
    const title = res.data.chartTitle || 'Chart';
    const isSingle = res.isSingleCourse;

    if (isSingle) {
      chartSubjectCanvas.style.display = 'block';
      chartSubInstance = new Chart(chartSubjectCanvas, {
        type: chartType === 'evaluation' ? 'pie' : 'bar',
        data: {
          labels,
          datasets: [{
            label: title,
            data: values,
            backgroundColor: ['#4f4a8b', '#d25629', '#058646', '#999']
          }]
        },
        options: { responsive: true }
      });
    } else {
      chartAllInstance = new Chart(chartAllCanvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: title,
            data: values,
            backgroundColor: '#4f4a8b'
          }]
        },
        options: { responsive: true }
      });
    }
  })
  .catch(() => {
    chartError.textContent = '⚠️ Error connecting to server.';
    chartError.style.display = 'block';
  });
});


// ===== Update Chart Type Options Based on File Type =====
function updateChartTypeOptions() {
  const fileType = document.getElementById("fileType").value;
  const chartTypeDropdown = document.getElementById("chartType");

  chartTypeDropdown.innerHTML = '<option value="" disabled selected>Select Chart Type</option>';

  if (fileType === "Course") {
    chartTypeDropdown.innerHTML += `
      <option value="assessment">Assessment Distribution</option>
      <option value="outcomes">Learning Outcomes & Assessment</option>
      <option value="elective">Required vs Elective Courses per Department</option>
      <option value="resources">Learning Resources and References</option>
    `;
  } else if (fileType === "Experience") {
    chartTypeDropdown.innerHTML += `
      <option value="location">Field Experience Location</option>
      <option value="clo_group">CLO Count By Group</option>
      <option value="stakeholders">Stakeholder Activities</option>
      <option value="evaluation">Evaluation Methods (Direct or Indirect)</option>
    `;
  }
}