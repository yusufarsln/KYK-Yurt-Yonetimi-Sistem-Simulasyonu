document.addEventListener('DOMContentLoaded', () => {
    getLeaves();
    setInterval(getLeaves, 2000);
});

function getLeaves() {
    fetch(`${API}/api/leaves`)
        .then(res => res.json())
        .then(data => {
            const tablo = document.getElementById('tablo');
            const count = document.getElementById('count');

            count.textContent = `${data.length} talep`;

            if (data.length === 0) {
                tablo.innerHTML = `
                    <tr><td colspan="7">
                        <div class="empty-state">
                            <div class="empty-icon">🗓</div>
                            <p>Bekleyen izin talebi yok</p>
                        </div>
                    </td></tr>
                `;
                return;
            }

            tablo.innerHTML = data.map(item => {
                const yetersiz = item.allowance < item.duration;

                return `
                    <tr>
                        <td class="td-mono">${item.tcno}</td>
                        <td>${item.fullname}</td>
                        <td class="td-mono">${item.startdate}</td>
                        <td class="td-mono">${item.enddate}</td>
                        <td>${item.duration} gün</td>
                        <td>
                            <span class="${yetersiz ? 'badge badge-rejected' : 'badge badge-active'}">
                                ${item.allowance} gün
                            </span>
                        </td>
                        <td style="text-align:right;">
                            <button class="btn btn-approve" onclick="onayla(${item.id})" ${yetersiz ? 'disabled style="opacity:0.4;cursor:not-allowed"' : ''}>
                                ✓ Onayla
                            </button>
                            <button class="btn btn-reject" onclick="reddet(${item.id})" style="margin-left:6px;">
                                ✕ Reddet
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');
        })
        .catch(err => console.error('Bağlantı hatası:', err));
}

function onayla(id) {
    fetch(`${API}/api/leaves/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) alert('Hata: ' + data.error);
        getLeaves();
    });
}

function reddet(id) {
    fetch(`${API}/api/leaves/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) alert('Hata: ' + data.error);
        getLeaves();
    });
}