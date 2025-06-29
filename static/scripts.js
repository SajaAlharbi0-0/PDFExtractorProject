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
    body: JSON.stringify({ fileType, department, subjectCode, chartType, viewType })
  })
    .then(res => res.json())
    .then(res => {
      if (res.status !== 'success') {
        chartError.textContent = res.message || 'Failed to load chart data.';
        chartError.style.display = 'block';
        return;
      }

      const chartArea = document.getElementById("queryList");
      chartArea.innerHTML = '';

      if (viewType === 'chart') {
        const labels = res.data.labels;
        const values = res.data.values;
        const title = res.data.chartTitle || 'Chart';
        const isSingle = res.isSingleCourse;

        const canvas = isSingle ? chartSubjectCanvas : chartAllCanvas;
        canvas.style.display = 'block';
        chartArea.appendChild(canvas);

        if (chartType === 'stakeholders') {
          canvas.width = 1000;
          canvas.height = 500;
        } else if (chartType === 'evaluation') {
          canvas.width = 500;
          canvas.height = 500;
        } else {
          canvas.width = 600;
          canvas.height = 400;
        }

        const ctx = canvas.getContext('2d');

        let chartKind = 'bar';
        if (chartType === 'evaluation') chartKind = 'pie';
        else if (chartType === 'stakeholders') chartKind = 'scatter';

        const scatterData = chartKind === 'scatter'
          ? values.map(item => ({ x: item.x, y: item.y }))
          : [];

        const data = chartKind === 'scatter'
          ? {
              datasets: [{
                label: title,
                data: scatterData,
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

        let options = {
          responsive: true,
          plugins: {
            legend: { display: true }
          }
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
          const xLabels = res.data.xLabels || [];
          const yLabels = res.data.yLabels || [];

          options.scales = {
            x: {
              type: 'category',
              labels: xLabels,
              title: { display: true, text: 'Stakeholders' },
              ticks: {
                autoSkip: false,
                maxRotation: 45,
                minRotation: 45,
                font: { size: 12 }
              }
            },
            y: {
              type: 'category',
              labels: yLabels,
              title: { display: true, text: 'Activities' },
              ticks: {
                autoSkip: false,
                font: { size: 12 }
              }
            }
          };
        } else if (chartKind === 'pie') {
          options.plugins.tooltip = {
            callbacks: {
              label: function (context) {
                const dataset = context.dataset;
                const total = dataset.data.reduce((a, b) => a + b, 0);
                const value = context.raw;
                const percentage = ((value / total) * 100).toFixed(1);
                return `${context.label}: ${value} (${percentage}%)`;
              }
            }
          };

          options.plugins.datalabels = {
            color: '#fff',
            font: {
              weight: 'bold',
              size: 16
            },
            anchor: 'center',
            align: 'center',
            formatter: function (value, context) {
              const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
              const percentage = ((value / total) * 100).toFixed(1) + '%';
              return percentage;
            }
          };
        }

        const chart = new Chart(ctx, {
          type: chartKind,
          data: data,
          options: options,
          plugins: chartKind === 'pie' ? [ChartDataLabels] : []
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


loadBtn.addEventListener('click', () => {
  const fileType = document.getElementById('fileType').value;
  const department = document.getElementById('department').value;
  let subjectCode = document.getElementById('subjectCode').value.trim().replace(/\s+/g, '');
  const chartType = document.getElementById('chartType').value;

  const chartArea = document.getElementById("queryList");
  chartArea.innerHTML = '';

  chartSubjectCanvas.style.display = 'none';
  chartAllCanvas.style.display = 'none';

  if (chartAllInstance) chartAllInstance.destroy();
  if (chartSubInstance) chartSubInstance.destroy();

  if (!fileType || !department || !chartType) {
    chartArea.innerHTML = '<p class="text-danger">⚠ Please select file type, department, and chart type.</p>';
    return;
  }

  const isCourse = fileType === "Course";
  const body = { fileType, department };
  if (subjectCode) {
    body[isCourse ? "subjectCode" : "code"] = subjectCode;
  }

  // ===== Chart Type 1: Assessment Distribution =====
  if (chartType === 'assessment') {
    body.chartType = chartType;

    fetch('/get_course_charts_data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(res => {
      if (res.status !== 'success') {
        chartArea.innerHTML = `<p class="text-danger">⚠ ${res.message || 'Failed to load chart data.'}</p>`;
        return;
      }

      const labels = res.data.labels;
      const values = res.data.values;
      const title = res.data.chartTitle || 'Chart';
      const isSingle = res.isSingleCourse;

      const canvas = isSingle ? chartSubjectCanvas : chartAllCanvas;
      canvas.style.display = 'block';
      chartArea.appendChild(canvas);

      const ctx = canvas.getContext('2d');

      const chart = new Chart(ctx, {
        type: isSingle ? 'pie' : 'bar',
        data: {
          labels,
          datasets: [{
            label: title,
            data: values,
            backgroundColor: isSingle
              ? ['#4f4a8b', '#d25629', '#058646', '#999']
              : '#4f4a8b'
          }]
        },
        options: { responsive: true }
      });

      if (isSingle) chartSubInstance = chart;
      else chartAllInstance = chart;
    })
    .catch(() => {
      chartArea.innerHTML = `<p class="text-danger">⚠ Error connecting to server.</p>`;
    });

  // ===== Chart Type 2: Learning Outcomes =====
  } else if (chartType === 'outcomes') {
    fetch('/get_learning_outcomes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(res => {
      if (res.status !== 'success') {
        chartArea.innerHTML = `<p class="text-danger">⚠ ${res.message || 'Failed to load outcomes data.'}</p>`;
        return;
      }

      const outcomesHtml = res.data.map(course => {
        const details = course.data.map(item =>
          `<li><strong>Outcome:</strong> ${item.outcome}<br><strong>Assessed by:</strong> ${item.assessment}</li>`
        ).join('');
        return `<h3>${course.course}</h3><ul>${details}</ul>`;
      }).join('');

      chartArea.innerHTML = outcomesHtml;
    })
    .catch(() => {
      chartArea.innerHTML = `<p class="text-danger">⚠ Error connecting to server.</p>`;
    });

  // ===== Chart Type 3: Required vs Elective =====
  } else if (chartType === 'elective') {
    fetch('/get_required_vs_elective', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileType, department })
    })
    .then(res => res.json())
    .then(res => {
      if (res.status !== 'success') {
        chartArea.innerHTML = `<p class="text-danger">⚠ ${res.message || 'Failed to load data.'}</p>`;
        return;
      }

      const required = res.data.required;
      const elective = res.data.elective;
      const deptName = res.data.department;

      chartAllCanvas.style.display = 'block';
      chartArea.appendChild(chartAllCanvas);

      const ctx = chartAllCanvas.getContext('2d');
      chartAllInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Required', 'Elective'],
          datasets: [{
            label: `Required vs Elective in ${deptName}`,
            data: [required, elective],
            backgroundColor: ['steelblue', 'darkorange']
          }]
        },
        options: { responsive: true }
      });
    })
    .catch(() => {
      chartArea.innerHTML = `<p class="text-danger">⚠ Error connecting to server.</p>`;
    });

  // ===== Chart Type 4: Learning Resources =====
  } else if (chartType === 'resources') {
    fetch('/get_learning_resources', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(res => {
      if (res.status !== 'success') {
        chartArea.innerHTML = `<p class="text-danger">⚠ ${res.message || 'Failed to load learning resources.'}</p>`;
        return;
      }

      const resourcesHtml = res.data.map(course => {
        const resList = Object.entries(course.resources).map(([category, items]) => {
          const itemsHtml = items.length ? items.map(r => `<li>${r}</li>`).join('') : "<li>None listed</li>";
          return `<strong>${category}:</strong><ul>${itemsHtml}</ul>`;
        }).join('');
        return `<h3>${course.course}</h3>${resList}<hr>`;
      }).join('');

      chartArea.innerHTML = resourcesHtml;
    })
    .catch(() => {
      chartArea.innerHTML = `<p class="text-danger">⚠ Error connecting to server.</p>`;
    });

  } else {
    chartArea.innerHTML = `<p class="text-danger">⚠ This chart type is not implemented yet.</p>`;
  }
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
