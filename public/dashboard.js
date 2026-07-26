document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch real data from the Phase 3 endpoints!
        const overviewRes = await fetch('/api/v1/analytics/overview');
        if (!overviewRes.ok) throw new Error('Failed to fetch overview');
        const overviewData = await overviewRes.json();
        const data = overviewData.data;

        document.getElementById('kpi-total').textContent = data.total_firs || 0;
        document.getElementById('kpi-pending').textContent = data.pending_cases || 0;
        document.getElementById('kpi-unassigned').textContent = data.unassigned_count || 0;

        document.getElementById('timestamp').textContent = `Last Refreshed: ${new Date().toLocaleString()}`;

        // Fetch Statuses
        const statusRes = await fetch('/api/v1/analytics/statuses');
        const statusJson = await statusRes.json();
        const statusLabels = statusJson.data.map(d => d.status);
        const statusCounts = statusJson.data.map(d => d.count);
        
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: statusLabels,
                datasets: [{
                    data: statusCounts,
                    backgroundColor: ['#3498db', '#2ecc71', '#f1c40f', '#e74c3c']
                }]
            },
            options: {
                responsive: true,
                plugins: { title: { display: true, text: 'FIR Status Distribution' } }
            }
        });

        // Fetch Categories
        const catRes = await fetch('/api/v1/analytics/categories');
        const catJson = await catRes.json();
        const catLabels = catJson.data.map(d => d.category);
        const catCounts = catJson.data.map(d => d.count);

        const catCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(catCtx, {
            type: 'bar',
            data: {
                labels: catLabels,
                datasets: [{
                    label: 'FIRs',
                    data: catCounts,
                    backgroundColor: '#3498db'
                }]
            },
            options: {
                responsive: true,
                plugins: { title: { display: true, text: 'Crime Categories' } }
            }
        });

        // Fetch Aging
        const agingRes = await fetch('/api/v1/analytics/aging');
        const agingJson = await agingRes.json();
        const agingLabels = agingJson.data.map(d => d.bucket);
        const agingCounts = agingJson.data.map(d => d.count);

        const agingCtx = document.getElementById('agingChart').getContext('2d');
        new Chart(agingCtx, {
            type: 'bar',
            data: {
                labels: agingLabels,
                datasets: [{
                    label: 'Cases',
                    data: agingCounts,
                    backgroundColor: '#e67e22'
                }]
            },
            options: {
                responsive: true,
                plugins: { title: { display: true, text: 'Pending Case Aging' } }
            }
        });

        // Mock trend data since the backend doesn't explicitly return timeline yet
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'FIRs Registered',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: '#3498db',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: { title: { display: true, text: '6-Month Registration Trend' } }
            }
        });

        // Show dashboard
        document.getElementById('loading').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';

    } catch (err) {
        console.error(err);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
    }
});
