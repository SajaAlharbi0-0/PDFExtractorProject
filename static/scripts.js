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


// ===== Show Output Type after selecting department =====
document.getElementById("department").addEventListener("change", () => {
  const selectedDept = document.getElementById("department").value;
  if (selectedDept) {
    document.getElementById("viewType").style.display = "block";
  }
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
  document.getElementById("queryList").innerHTML = '';

  const fileType = document.getElementById('fileType').value;
  const department = document.getElementById('department').value;
  const subjectCode = document.getElementById('subjectCode').value.trim();
  const chartType = document.getElementById('chartType').value;
  const viewType = document.getElementById('viewType').value;

  chartError.style.display = 'none';
  chartSubjectCanvas.style.display = 'none';
  chartAllCanvas.style.display = 'none';

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
      chartType,
      viewType
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

      const chartArea = document.getElementById("queryList");

      if (viewType === 'chart') {
        const canvas = isSingle ? chartSubjectCanvas : chartAllCanvas;
        canvas.style.display = 'block';
        chartArea.innerHTML = '';
        chartArea.appendChild(canvas);
        canvas.width = 1000; // 🔁 عرض أوسع
        canvas.height = 500;


        const ctx = canvas.getContext('2d');

        let chartKind = 'bar';
        if (chartType === 'evaluation') chartKind = 'pie';
        else if (chartType === 'stakeholders') chartKind = 'scatter';

        const data = chartKind === 'scatter'
          ? {
              datasets: [{
                label: title,
                data: values,
                backgroundColor: 'blue'
              }]
            }
          : {
              labels,
              datasets: [{
                label: title,
                data: values,
                backgroundColor: ['#4f4a8b', '#d25629', '#058646', '#999']
              }]
            };

        const options = {
          responsive: true,
          plugins: { legend: { display: false } },
        };

        if (chartKind === 'bar') {
          options.scales = {
            x: {
              ticks: {
                autoSkip: false,
                maxRotation: 0,
                minRotation: 0,
                font: { size: 12 }
              }
            }
          };
        } else if (chartKind === 'scatter') {
          options.scales = {
            x: {
              type: 'category',
              title: { display: true, text: 'Stakeholders' },
              labels: [
                "Department/College",
                "Field Supervisor",
                "Student",
                "Teaching Staff",
                "Training Organization"
              ],
              ticks: {
                autoSkip: false,
                maxRotation: 45,
                minRotation: 45,
                font: { size: 12 }
              }
            },
            y: {
              type: 'category',
              title: { display: true, text: 'Activities' }
            }
          };
        }

        const chart = new Chart(ctx, {
          type: chartKind,
          data: data,
          options: options
        });

        if (isSingle) chartSubInstance = chart;
        else chartAllInstance = chart;

      } else if (viewType === 'table') {
        if (res.html) {
          chartArea.innerHTML = res.html;
        } else {
          chartArea.innerHTML = '<p>No data available for this query.</p>';
        }
      }

    })
    .catch(() => {
      chartError.textContent = '⚠️ Error connecting to server.';
      chartError.style.display = 'block';
    });
});


// ===== Update Chart Type Options Based on File Type & View =====
function updateChartTypeOptions() {
  const fileType = document.getElementById("fileType").value;
  const viewType = document.getElementById("viewType")?.value;
  const chartTypeDropdown = document.getElementById("chartType");

  chartTypeDropdown.innerHTML = '<option value="" disabled selected>Select Chart Type</option>';

  if (!viewType) return;

  if (viewType === "chart") {
    if (fileType === "Course") {
      chartTypeDropdown.innerHTML += `
        <option value="assessment">Assessment Distribution</option>
        <option value="elective">Required vs Elective Courses per Department</option>
      `;
    } else if (fileType === "Experience") {
      chartTypeDropdown.innerHTML += `
        <option value="clo_group">CLO Count By Group</option>
        <option value="stakeholders">Stakeholder Activities</option>
        <option value="evaluation">Evaluation Methods (Direct or Indirect)</option>
      `;
    }
  } else if (viewType === "table") {
    if (fileType === "Course") {
      chartTypeDropdown.innerHTML += `
        <option value="outcomes">Learning Outcomes & Assessment</option>
        <option value="resources">Learning Resources and References</option>
      `;
    } else if (fileType === "Experience") {
      chartTypeDropdown.innerHTML += `
        <option value="location">Field Experience Location</option>
      `;
    }
  }
}
