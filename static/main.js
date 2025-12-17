// main.js - IPS Dashboard enhancements

document.addEventListener('DOMContentLoaded', function () {
    // 1. Chart.js auto-init (if canvas with #attackChart exists)
    const chartCanvas = document.getElementById('attackChart');
    if (chartCanvas && window.attackData) {
        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: attackData.labels,
                datasets: [{
                    label: 'Attack Count',
                    data: attackData.counts,
                    backgroundColor: [
                        '#ffb86c', '#ff7e5f', '#8be9fd', '#50fa7b', '#bd93f9', '#ff5555', '#f1fa8c'
                    ],
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: "#35395a" },
                        ticks: { color: "#e0e3eb" }
                    },
                    x: {
                        grid: { color: "#35395a" },
                        ticks: { color: "#e0e3eb" }
                    }
                }
            }
        });
    }

    // 2. Table row highlight on click
    document.querySelectorAll('table').forEach(table => {
        table.addEventListener('click', function (e) {
            if (e.target.tagName === 'TD') {
                table.querySelectorAll('tr').forEach(row => row.classList.remove('selected-row'));
                e.target.parentNode.classList.add('selected-row');
            }
        });
    });

    // 3. Toast notification system
    window.showToast = function (message, type = "info") {
        let toast = document.createElement('div');
        toast.className = 'toast ' + type;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 500);
        }, 3000);
    };

    // 4. Optional: Table filtering by search (add <input id="tableSearch"> above your table in HTML)
    const tableSearch = document.getElementById('tableSearch');
    if (tableSearch) {
        tableSearch.addEventListener('input', function () {
            let filter = tableSearch.value.toLowerCase();
            document.querySelectorAll('table tbody tr').forEach(row => {
                row.style.display = Array.from(row.cells).some(td =>
                    td.textContent.toLowerCase().includes(filter)
                ) ? '' : 'none';
            });
        });
    }
});
