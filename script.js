// ========== Upload Section ========== //
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

// ========== Chart Section ========== //
const chartType = document.getElementById('chartType');
const chartCanvas = document.getElementById('chartCanvas');
let chartInstance = null;

chartType.addEventListener('change', () => {
  const type = chartType.value;

  if (chartInstance) chartInstance.destroy();

  let chartData = {};
  let chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      }
    }
  };

  if (type === 'distribution') {
    chartData = {
      labels: ['Lecturer', 'Coordinator', 'QA', 'Students'],
      datasets: [{
        label: 'Activity Distribution',
        data: [30, 25, 20, 25],
        backgroundColor: ['#4dc9f6', '#f67019', '#f53794', '#537bc4']
      }]
    };
  } else if (type === 'evaluation') {
    chartData = {
      labels: ['Direct', 'Indirect'],
      datasets: [{
        label: 'Evaluation Type',
        data: [70, 30],
        backgroundColor: ['#36a2eb', '#ff6384']
      }]
    };
  } else if (type === 'assessment') {
    chartData = {
      labels: ['Quizzes', 'Midterms', 'Projects', 'Final'],
      datasets: [{
        label: 'Assessment Distribution',
        data: [15, 30, 25, 30],
        backgroundColor: ['#9966ff', '#ff9f40', '#4bc0c0', '#ffcd56']
      }]
    };
  }

  chartInstance = new Chart(chartCanvas, {
    type: 'bar',
    data: chartData,
    options: chartOptions
  });
});
