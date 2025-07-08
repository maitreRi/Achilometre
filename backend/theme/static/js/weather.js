const uvDataScript = document.getElementById('uv-history-data');
if (uvDataScript) {
  const rawData = uvDataScript.textContent;
  const historyData = JSON.parse(rawData);

  const uvData = historyData.uv.map(item => ({ x: item.time, y: item.value }));
  const ctx = document.getElementById('historyChart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'UV',
          data: uvData,
          borderColor: 'orange',
          fill: false,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          type: 'time',
          time: {
            tooltipFormat: 'MMM d, HH:mm',
            unit: 'hour',
            displayFormats: {
              hour: 'HH:mm'
            }
          },
          title: {
            display: true,
            text: 'Heure'
          }
        },
        y1: {
          position: 'left',
          title: {
            display: true,
            text: 'Indice UV'
          },
          min: 0,
          max: 12
        }
      }
    }
  });
}
