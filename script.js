document.addEventListener('DOMContentLoaded', () => {
    getApplications();
    setInterval(getApplications, 2000);
});

function getApplications() {
    fetch(`${API}/api/applications`)
        .then(res => res.json())
        .then(data => {
            const tablo = document.getElementById('tablo');
            const count = document.getElementById('count');

            count.textContent = `${data.length} başvuru`;

            if (data.length === 0) {
                tablo.innerHTML = `
                    <tr><td colspan="5">
                        <div class="empty-state">
                            <div class="empty-icon">📭</div>
                            <p>Bekleyen başvuru yok</p>
                        </div>
                    </td></tr>
                `;
                return;
            }

            tablo.innerHTML = data.map(item => `
                <tr>
                    <td>${item.tcno}</td>
                    <td>${item.fullname}</td>
                    <td>${item.appdate}</td>
                    <td><span class="badge badge-pending">⏳ Beklemede</span></td>
                    <td style="text-align:center;">
                        <button class="btn btn-approve" onclick="onayla('${item.tcno}')">Onayla</button>
                        <button class="btn btn-reject" onclick="reddet('${item.tcno}')">Reddet</button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(err => console.error('Bağlantı hatası:', err));
}

function onayla(tc) {
    fetch(`${API}/api/applications/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tcno: tc })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) alert('Hata: ' + data.error);
            getApplications();
        });
}

function reddet(tc) {
    fetch(`${API}/api/applications/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tcno: tc })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) alert('Hata: ' + data.error);
            getApplications();
        });
}