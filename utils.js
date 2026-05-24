const API = 'http://127.0.0.1:5000';

const AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];

function formatTarih(tarihStr) {
    if (!tarihStr) return '—';
    const t = new Date(tarihStr);
    return `${t.getDate()} ${AYLAR[t.getMonth()]} ${t.getFullYear()}`;
}

function formatAyYil(tarihStr) {
    if (!tarihStr) return '—';
    const t = new Date(tarihStr);
    return `${AYLAR[t.getMonth()]} ${t.getFullYear()}`;
}

function simTarihGoster() {
    fetch(`${API}/api/date`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('date').textContent = formatTarih(data.date);
        });
}

simTarihGoster();
setInterval(simTarihGoster, 30000);