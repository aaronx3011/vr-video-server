let varCPU = [];
let varGPU = [];
let varRAM = [];
const ctx = document.getElementById('myChart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['30s','','','','','','','','','','','','','','','15s','','','','','','','','','','','','','','','0s'],
    datasets: [
      {
        label: 'CPU (%)',
        data: varCPU,
        borderWidth: 1,
        lineTension: 0.5,
        borderColor: "#ffffff",  // Cambiado a blanco
        backgroundColor: 'rgba(108, 119, 161, 0.2)',
        pointStyle: false
      }
    ]
  },
  options: {
    scales: {
      x: {
        ticks: {
          color: 'rgba(255, 255, 255, 0.8)'  // Un blanco suave para el texto en el eje X
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.3)',  // Un blanco más oscuro para las líneas de la cuadrícula en el eje X
          zeroLineColor: 'rgba(255, 255, 255, 0.5)'  // Un blanco intermedio para la línea base (cero)
        }
      },
      y: {
        ticks: {
          color: 'rgba(255, 255, 255, 0.8)',  // Un blanco suave para el texto en el eje Y
          beginAtZero: true
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.3)',  // Un blanco más oscuro para las líneas de la cuadrícula en el eje Y
          zeroLineColor: 'rgba(255, 255, 255, 0.5)'  // Un blanco intermedio para la línea base (cero)
        },
        suggestedMin: 0,
        suggestedMax: 100
      }
    },
    plugins: {
      legend: {
        labels: {
          color: 'rgba(255, 255, 255, 0.8)'  // Un blanco suave para el texto en la leyenda
        }
      }
    }
  }
});
