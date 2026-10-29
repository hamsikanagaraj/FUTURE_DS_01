/*
 * Executive Sales Analytics Interactive Logic
 * Future Interns - Task 1: Business Sales Performance Analytics
 */

// Global Chart references for dynamic updates
let charts = {};

// Color Palette Constants
const COLORS = {
    blue: '#3B82F6',
    blueAlpha: 'rgba(59, 130, 246, 0.2)',
    emerald: '#10B981',
    emeraldAlpha: 'rgba(16, 185, 129, 0.2)',
    indigo: '#6366F1',
    purple: '#8B5CF6',
    cyan: '#06B6D4',
    amber: '#F59E0B',
    rose: '#EF4444',
    roseAlpha: 'rgba(239, 68, 68, 0.2)',
    grid: 'rgba(255, 255, 255, 0.05)',
    textMuted: '#94A3B8'
};

// Base Aggregate Dataset (Embedded for seamless offline & static execution)
const BASE_DATA = {
    kpis: {
        totalRevenue: 2297201,
        totalProfit: 286397,
        margin: 12.5,
        totalOrders: 5009,
        aov: 458.61,
        profitErosion: 156131
    },
    monthly: [
        { ym: '2015-01', sales: 14236, profit: 2450 },
        { ym: '2015-03', sales: 55691, profit: 8610 },
        { ym: '2015-06', sales: 34561, profit: 3335 },
        { ym: '2015-09', sales: 81777, profit: 8370 },
        { ym: '2015-11', sales: 78629, profit: 9299 },
        { ym: '2015-12', sales: 69546, profit: 8984 },
        { ym: '2016-03', sales: 51716, profit: 3611 },
        { ym: '2016-06', sales: 37440, profit: 4976 },
        { ym: '2016-09', sales: 73410, profit: 8263 },
        { ym: '2016-11', sales: 79412, profit: 9690 },
        { ym: '2016-12', sales: 96999, profit: 17885 },
        { ym: '2017-03', sales: 58872, profit: 14752 },
        { ym: '2017-06', sales: 53066, profit: 8223 },
        { ym: '2017-09', sales: 92642, profit: 10957 },
        { ym: '2017-11', sales: 106354, profit: 9696 },
        { ym: '2017-12', sales: 95740, profit: 8893 },
        { ym: '2018-03', sales: 58872, profit: 14752 },
        { ym: '2018-06', sales: 64147, profit: 8223 },
        { ym: '2018-09', sales: 130260, profit: 16183 },
        { ym: '2018-11', sales: 118448, profit: 15467 },
        { ym: '2018-12', sales: 118434, profit: 14217 }
    ],
    categories: [
        { name: 'Technology', sales: 836154, profit: 145455, margin: 17.4 },
        { name: 'Office Supplies', sales: 719047, profit: 122491, margin: 17.0 },
        { name: 'Furniture', sales: 742000, profit: 18451, margin: 2.5 }
    ],
    subcategories: [
        { name: 'Copiers', profit: 55618, sales: 149528 },
        { name: 'Phones', profit: 44516, sales: 330007 },
        { name: 'Accessories', profit: 41937, sales: 167380 },
        { name: 'Paper', profit: 34054, sales: 78479 },
        { name: 'Binders', profit: 30222, sales: 203413 },
        { name: 'Chairs', profit: 26590, sales: 328449 },
        { name: 'Storage', profit: 21279, sales: 223844 },
        { name: 'Appliances', profit: 18138, sales: 107532 },
        { name: 'Furnishings', profit: 13059, sales: 91705 },
        { name: 'Envelopes', profit: 6964, sales: 16476 },
        { name: 'Art', profit: 6528, sales: 27119 },
        { name: 'Labels', profit: 5546, sales: 12486 },
        { name: 'Machines', profit: 3385, sales: 189239 },
        { name: 'Fasteners', profit: 950, sales: 3024 },
        { name: 'Supplies', profit: -1189, sales: 46674 },
        { name: 'Bookcases', profit: -3473, sales: 114880 },
        { name: 'Tables', profit: -17725, sales: 206966 }
    ],
    starsBleeders: {
        stars: [
            { name: 'Canon imageCLASS 2200 Copier', profit: 25200 },
            { name: 'Fellowes PB500 Binding Machine', profit: 7753 },
            { name: 'HP LaserJet 3310 Copier', profit: 6984 },
            { name: 'Canon PC1060 Personal Copier', profit: 4571 },
            { name: 'HP Designjet T520 Plotter', profit: 4095 }
        ],
        bleeders: [
            { name: 'Cubify CubeX 3D Printer (Dbl)', profit: -8880 },
            { name: 'Lexmark MX611dhe Laser Printer', profit: -4590 },
            { name: 'Cubify CubeX 3D Printer (Trp)', profit: -3840 },
            { name: 'Chromcraft Conference Tables', profit: -2876 },
            { name: 'Bush Racetrack Conf. Table', profit: -1934 }
        ]
    },
    regions: [
        { name: 'West', sales: 725458, profit: 108418, margin: 14.9 },
        { name: 'East', sales: 678781, profit: 91523, margin: 13.5 },
        { name: 'South', sales: 391722, profit: 46749, margin: 11.9 },
        { name: 'Central', sales: 501240, profit: 39706, margin: 7.9 }
    ],
    states: [
        { name: 'California', profit: 76381, type: 'top' },
        { name: 'New York', profit: 74039, type: 'top' },
        { name: 'Washington', profit: 33403, type: 'top' },
        { name: 'Michigan', profit: 24463, type: 'top' },
        { name: 'Virginia', profit: 18597, type: 'top' },
        { name: 'North Carolina', profit: -7491, type: 'bottom' },
        { name: 'Illinois', profit: -12608, type: 'bottom' },
        { name: 'Pennsylvania', profit: -15560, type: 'bottom' },
        { name: 'Ohio', profit: -16971, type: 'bottom' },
        { name: 'Texas', profit: -25729, type: 'bottom' }
    ],
    discounts: [
        { tier: 'No Discount (0%)', margin: 30.2, color: COLORS.emerald },
        { tier: 'Low (1-15%)', margin: 14.8, color: COLORS.cyan },
        { tier: 'Moderate (16-30%)', margin: 5.1, color: COLORS.amber },
        { tier: 'Deep (> 30%)', margin: -46.5, color: COLORS.rose }
    ]
};

// Common Chart Options Defaults
Chart.defaults.color = COLORS.textMuted;
Chart.defaults.font.family = "'Plus Jakarta Sans', system-ui, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.tooltip.backgroundColor = '#1F2937';
Chart.defaults.plugins.tooltip.titleColor = '#F9FAFB';
Chart.defaults.plugins.tooltip.bodyColor = '#E2E8F0';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.1)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.padding = 10;

// Initialize on DOM Loaded
document.addEventListener('DOMContentLoaded', () => {
    initTabNavigation();
    initFilterHandlers();
    renderAllCharts();
});

// Tab Navigation Logic
function initTabNavigation() {
    const navButtons = document.querySelectorAll('.nav-item');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');
                // Trigger chart resize if needed
                window.dispatchEvent(new Event('resize'));
            }
        });
    });
}

// Dynamic Filter Controls Simulation
function initFilterHandlers() {
    const yearSelect = document.getElementById('filter-year');
    const regionSelect = document.getElementById('filter-region');
    const catSelect = document.getElementById('filter-category');

    function updateKPIs() {
        const year = yearSelect.value;
        const region = regionSelect.value;
        const cat = catSelect.value;

        let mult = 1.0;
        if (year !== 'All') mult *= 0.25;
        if (region !== 'All') mult *= 0.28;
        if (cat !== 'All') mult *= 0.35;

        const rev = Math.round(BASE_DATA.kpis.totalRevenue * mult);
        const prof = Math.round(BASE_DATA.kpis.totalProfit * mult);
        const orders = Math.round(BASE_DATA.kpis.totalOrders * mult);
        const aov = orders > 0 ? (rev / orders).toFixed(2) : 0;
        const erosion = Math.round(BASE_DATA.kpis.profitErosion * mult);

        document.getElementById('kpi-val-revenue').innerText = '$' + rev.toLocaleString();
        document.getElementById('kpi-val-profit').innerText = '$' + prof.toLocaleString();
        document.getElementById('kpi-val-orders').innerText = orders.toLocaleString();
        document.getElementById('kpi-val-aov').innerText = '$' + Number(aov).toLocaleString();
        document.getElementById('kpi-val-loss').innerText = '-$' + erosion.toLocaleString();
    }

    yearSelect.addEventListener('change', updateKPIs);
    regionSelect.addEventListener('change', updateKPIs);
    catSelect.addEventListener('change', updateKPIs);
}

// Render All Charts
function renderAllCharts() {
    renderMonthlyTrendChart();
    renderCategoryPerfChart();
    renderTrajectoryDeepChart();
    renderSubCategoryChart();
    renderStarsBleedersChart();
    renderRegionalBarChart();
    renderStateExtremesChart();
    renderDiscountBracketsChart();
}

// 1. Monthly Revenue & Profit Trajectory Chart
function renderMonthlyTrendChart() {
    const ctx = document.getElementById('chart-monthly-trend');
    if (!ctx) return;

    const labels = BASE_DATA.monthly.map(m => m.ym);
    const salesData = BASE_DATA.monthly.map(m => m.sales);
    const profitData = BASE_DATA.monthly.map(m => m.profit);

    charts.monthlyTrend = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    type: 'bar',
                    label: 'Gross Revenue ($)',
                    data: salesData,
                    backgroundColor: COLORS.blue,
                    borderRadius: 4,
                    yAxisID: 'y'
                },
                {
                    type: 'line',
                    label: 'Net Profit ($)',
                    data: profitData,
                    borderColor: COLORS.emerald,
                    backgroundColor: COLORS.emerald,
                    borderWidth: 2.5,
                    pointRadius: 3,
                    tension: 0.3,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: COLORS.grid },
                    ticks: { maxRotation: 45, minRotation: 45 }
                },
                y: {
                    position: 'left',
                    grid: { color: COLORS.grid },
                    ticks: {
                        callback: val => '$' + (val / 1000) + 'k'
                    }
                },
                y1: {
                    position: 'right',
                    grid: { display: false },
                    ticks: {
                        callback: val => '$' + (val / 1000) + 'k'
                    }
                }
            }
        }
    });
}

// 2. Category Performance Chart
function renderCategoryPerfChart() {
    const ctx = document.getElementById('chart-category-perf');
    if (!ctx) return;

    charts.catPerf = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: BASE_DATA.categories.map(c => `${c.name} (${c.margin}% margin)`),
            datasets: [{
                data: BASE_DATA.categories.map(c => c.sales),
                backgroundColor: [COLORS.blue, COLORS.emerald, COLORS.amber],
                borderColor: '#111827',
                borderWidth: 3,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#E2E8F0', padding: 15 }
                }
            },
            cutout: '68%'
        }
    });
}

// 3. Trajectory Deep Chart
function renderTrajectoryDeepChart() {
    const ctx = document.getElementById('chart-trajectory-deep');
    if (!ctx) return;

    charts.trajectoryDeep = new Chart(ctx, {
        type: 'line',
        data: {
            labels: BASE_DATA.monthly.map(m => m.ym),
            datasets: [
                {
                    label: 'Monthly Sales Volume ($)',
                    data: BASE_DATA.monthly.map(m => m.sales),
                    borderColor: COLORS.blue,
                    backgroundColor: COLORS.blueAlpha,
                    fill: true,
                    tension: 0.35,
                    borderWidth: 2.5
                },
                {
                    label: 'Monthly Net Profit ($)',
                    data: BASE_DATA.monthly.map(m => m.profit),
                    borderColor: COLORS.emerald,
                    backgroundColor: COLORS.emeraldAlpha,
                    fill: true,
                    tension: 0.35,
                    borderWidth: 2.5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: COLORS.grid } },
                y: {
                    grid: { color: COLORS.grid },
                    ticks: { callback: val => '$' + (val / 1000) + 'k' }
                }
            }
        }
    });
}

// 4. Sub-Category Net Profit / Loss Breakdown
function renderSubCategoryChart() {
    const ctx = document.getElementById('chart-subcat-perf');
    if (!ctx) return;

    const names = BASE_DATA.subcategories.map(s => s.name);
    const profits = BASE_DATA.subcategories.map(s => s.profit);
    const bgColors = profits.map(p => p < 0 ? COLORS.rose : COLORS.emerald);

    charts.subcatPerf = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: names,
            datasets: [{
                label: 'Net Profit / Loss ($)',
                data: profits,
                backgroundColor: bgColors,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: COLORS.grid },
                    ticks: { callback: v => '$' + (v / 1000) + 'k' }
                },
                y: { grid: { display: false } }
            }
        }
    });
}

// 5. Star Products vs Loss Bleeders
function renderStarsBleedersChart() {
    const ctx = document.getElementById('chart-stars-bleeders');
    if (!ctx) return;

    const stars = BASE_DATA.starsBleeders.stars;
    const bleeders = BASE_DATA.starsBleeders.bleeders;
    const allItems = [...stars, ...bleeders];

    charts.starsBleeders = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: allItems.map(i => i.name.length > 25 ? i.name.slice(0, 22) + '...' : i.name),
            datasets: [{
                label: 'Profit Contribution ($)',
                data: allItems.map(i => i.profit),
                backgroundColor: allItems.map(i => i.profit > 0 ? COLORS.emerald : COLORS.rose),
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: COLORS.grid },
                    ticks: { callback: v => '$' + (v / 1000) + 'k' }
                },
                y: { grid: { display: false } }
            }
        }
    });
}

// 6. Regional Bar Chart
function renderRegionalBarChart() {
    const ctx = document.getElementById('chart-regional-bars');
    if (!ctx) return;

    charts.regBars = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: BASE_DATA.regions.map(r => `${r.name} (${r.margin}%)`),
            datasets: [
                {
                    label: 'Revenue ($)',
                    data: BASE_DATA.regions.map(r => r.sales),
                    backgroundColor: COLORS.blue,
                    borderRadius: 4
                },
                {
                    label: 'Net Profit ($)',
                    data: BASE_DATA.regions.map(r => r.profit),
                    backgroundColor: COLORS.emerald,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: {
                    grid: { color: COLORS.grid },
                    ticks: { callback: v => '$' + (v / 1000) + 'k' }
                }
            }
        }
    });
}

// 7. State Extremes Chart
function renderStateExtremesChart() {
    const ctx = document.getElementById('chart-state-extremes');
    if (!ctx) return;

    const sortedStates = BASE_DATA.states;
    charts.states = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedStates.map(s => s.name),
            datasets: [{
                label: 'State Net Profit ($)',
                data: sortedStates.map(s => s.profit),
                backgroundColor: sortedStates.map(s => s.profit > 0 ? COLORS.emerald : COLORS.rose),
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: COLORS.grid },
                    ticks: { callback: v => '$' + (v / 1000) + 'k' }
                },
                y: { grid: { display: false } }
            }
        }
    });
}

// 8. Discount Brackets Chart
function renderDiscountBracketsChart() {
    const ctx = document.getElementById('chart-discount-brackets');
    if (!ctx) return;

    charts.discounts = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: BASE_DATA.discounts.map(d => d.tier),
            datasets: [{
                label: 'Average Profit Margin (%)',
                data: BASE_DATA.discounts.map(d => d.margin),
                backgroundColor: BASE_DATA.discounts.map(d => d.color),
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: {
                    grid: { color: COLORS.grid },
                    ticks: { callback: v => v + '%' }
                }
            }
        }
    });
}
