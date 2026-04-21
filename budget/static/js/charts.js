// ═══════════════════════════════════════════════════════
//  RÉCUPÉRATION DES DONNÉES DJANGO (json_script)
// ═══════════════════════════════════════════════════════
const labelsCamembert  = JSON.parse(document.getElementById('data-labels-camembert').textContent);
const valeursCamembert = JSON.parse(document.getElementById('data-valeurs-camembert').textContent);
const couleursCamembert= JSON.parse(document.getElementById('data-couleurs-camembert').textContent);

const labelsBarres    = JSON.parse(document.getElementById('data-labels-barres').textContent);
const revenusBarres   = JSON.parse(document.getElementById('data-revenus-barres').textContent);
const depensesBarres  = JSON.parse(document.getElementById('data-depenses-barres').textContent);


// ═══════════════════════════════════════════════════════
//  OPTIONS COMMUNES
// ═══════════════════════════════════════════════════════
Chart.defaults.font.family = "'Segoe UI', sans-serif";
Chart.defaults.font.size   = 13;
Chart.defaults.color       = '#6c757d';


// ═══════════════════════════════════════════════════════
//  GRAPHIQUE CAMEMBERT — dépenses par catégorie
// ═══════════════════════════════════════════════════════
const canvasCamembert = document.getElementById('chartCamembert');

if (canvasCamembert) {
  new Chart(canvasCamembert, {
    type: 'doughnut',
    data: {
      labels: labelsCamembert,
      datasets: [{
        data: valeursCamembert,
        backgroundColor: couleursCamembert,
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      cutout: '60%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 16,
            usePointStyle: true,
            pointStyle: 'circle',
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const valeur = context.parsed;
              const pct = ((valeur / total) * 100).toFixed(1);
              return ` ${context.label} : ${valeur} DH (${pct}%)`;
            }
          }
        }
      }
    }
  });
}


// ═══════════════════════════════════════════════════════
//  GRAPHIQUE BARRES — revenus vs dépenses 6 mois
// ═══════════════════════════════════════════════════════
const canvasBarres = document.getElementById('chartBarres');

if (canvasBarres) {
  new Chart(canvasBarres, {
    type: 'bar',
    data: {
      labels: labelsBarres,
      datasets: [
        {
          label: 'Revenus',
          data: revenusBarres,
          backgroundColor: 'rgba(25, 135, 84, 0.75)',
          borderColor:      'rgba(25, 135, 84, 1)',
          borderWidth: 1.5,
          borderRadius: 6,
          borderSkipped: false,
        },
        {
          label: 'Dépenses',
          data: depensesBarres,
          backgroundColor: 'rgba(220, 53, 69, 0.75)',
          borderColor:      'rgba(220, 53, 69, 1)',
          borderWidth: 1.5,
          borderRadius: 6,
          borderSkipped: false,
        }
      ]
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            pointStyle: 'rectRounded',
            padding: 20,
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return ` ${context.dataset.label} : ${context.parsed.y} DH`;
            },
            footer: function(items) {
              const rev = items.find(i => i.dataset.label === 'Revenus')?.parsed.y || 0;
              const dep = items.find(i => i.dataset.label === 'Dépenses')?.parsed.y || 0;
              const solde = rev - dep;
              return `Solde : ${solde >= 0 ? '+' : ''}${solde} DH`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 12 } }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0,0,0,0.05)',
          },
          ticks: {
            callback: function(value) {
              return value + ' DH';
            }
          }
        }
      }
    }
  });
}