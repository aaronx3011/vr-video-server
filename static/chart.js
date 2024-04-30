
let varCPU = [];
let varGPU = [];
let varRAM = [];
const ctx = document.getElementById('myChart');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['30s','','','','','','','','','','','','','','','15s','','','','','','','','','','','','','','','0s'],
      datasets: [
        {
          label: 'GPU (%)',
          data: varCPU,
          borderWidth: 1,
          lineTension: 0.5,
          pointStyle: false,
          borderColor: "#6c77a1",
          fontColor: "FFFFFF"
        }
        // }, 
        // {
        //   label: 'GPU (%)',
        //   data: varGPU,
        //   borderWidth: 1
        // },
        // {
        //   label: 'RAM (%)',
        //   data: varRAM,
        //   borderWidth: 1
        // }
      ]
    },
    options: {
      scales: {
        xAxes: [{
          ticks: {
            reverse: true
          },
          gridLines: {
            zeroLineColor: '#ffcc33'
        }
          }]
        },
        y: {
            // ticks: {
            //   fontColor: 'white',
            // },
            suggestedMin: 0,
            suggestedMax: 100
          }
        
      }
    }
);