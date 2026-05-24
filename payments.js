let tumOdemeler = [];

document.addEventListener('DOMContentLoaded', () => {
    getPayments();
    setInterval(getPayments, 5000);
});

function getPayments() {
    fetch(`${API}/api/date`)
        .then(r => r.json())
        .then(currentdate => {
            const day = new Date(currentdate.date).getDate();
            document.getElementById('bildirim-banner').style.display = day >= 25 ? 'block' : 'none';

            fetch(`${API}/api/payments`)
                .then(r => r.json())
                .then(data => {
                    tumOdemeler = data;
                    renderTable();
                });
        });
}

function renderTable() {
    const filtre = document.getElementById('odeme-filtre').value;
    const count = document.getElementById('count');
    const tablo = document.getElementById('tablo');

    let liste = [...tumOdemeler];

    if (filtre === 'paid') liste = liste.filter(d => d.paid);
    else if (filtre === 'unpaid') liste = liste.filter(d => !d.paid);

    liste.sort((a, b) => a.paid - b.paid);

    const odeyenler = tumOdemeler.filter(d => d.paid).length;
    count.textContent = `${odeyenler} / ${tumOdemeler.length} ödedi`;

    if (liste.length === 0) {
        tablo.innerHTML = `
            <tr><td colspan="6">
                <div class="empty-state">
                    <div class="empty-icon">💳</div>
                    <p>Gösterilecek kayıt yok</p>
                </div>
            </td></tr>
        `;
        return;
    }


    tablo.innerHTML = liste.map(item => `
        <tr>
            <td>${item.tcno}</td>
            <td>${item.fullname}</td>
            <td>${item.room}</td>
            <td>
                <span class="badge ${item.paid ? 'badge-active' : 'badge-rejected'}">
                    ${item.paid ? 'Ödedi' : 'Ödemedi'}
                </span>
            </td>
            <td>${item.paydate ?? '—'}</td>
            <td>${item.fee ? item.fee + ' ₺' : '—'}</td>
        </tr>
    `).join('');
}