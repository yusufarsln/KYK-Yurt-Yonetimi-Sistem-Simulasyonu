let tumOgrenciler = [];

document.addEventListener('DOMContentLoaded', () => {
    getStudents();
});

document.getElementById('ara').addEventListener('input', () => renderTable());
document.getElementById('blok-filtre').addEventListener('change', () => renderTable());
document.getElementById('siralama').addEventListener('change', () => renderTable());

function getStudents() {
    fetch(`${API}/api/students`)
        .then(res => res.json())
        .then(data => {
            tumOgrenciler = data;

            const bloklar = [];
            for (let i = 0; i < data.length; i++) {
                const blok = data[i].room.split(' ')[0];
                if (!bloklar.includes(blok)) {
                    bloklar.push(blok);
                }
            }
            bloklar.sort();
            const filtre = document.getElementById('blok-filtre');
            const mevcutDeger = filtre.value;
            filtre.innerHTML = '<option value="">Tüm Bloklar</option>';
            bloklar.forEach(b => {
                filtre.innerHTML += `<option value="${b}" ${mevcutDeger === b ? 'selected' : ''}>${b} Blok</option>`;
            });

            renderTable();
        })
        .catch(err => console.error('Bağlantı hatası:', err));
}

function renderTable() {
    const q = document.getElementById('ara').value.toLowerCase();
    const blok = document.getElementById('blok-filtre').value;
    const durum = document.getElementById('durum-filtre').value;
    const siralama = document.getElementById('siralama').value;
    const count = document.getElementById('count');

    let liste = [...tumOgrenciler];
    let info = ''

    if (q) {
        liste = liste.filter(item =>
            item.tcno.toLowerCase().includes(q) ||
            item.fullname.toLowerCase().includes(q)
        );
    }

    if (blok) {
        liste = liste.filter(item => item.room.startsWith(blok));
    }

    if (durum !== "") {
        liste = liste.filter(item => item.is_active == durum);
        info = (durum == "1") ? 'aktif' : 'deaktif'
    }

    if (siralama === 'dogum-eski') {
        liste.sort((a, b) => new Date(a.birthdate) - new Date(b.birthdate));
    } else if (siralama === 'dogum-yeni') {
        liste.sort((a, b) => new Date(b.birthdate) - new Date(a.birthdate));
    } else if (siralama === 'izin-az') {
        liste.sort((a, b) => a.allowance - b.allowance);
    } else if (siralama === 'izin-cok') {
        liste.sort((a, b) => b.allowance - a.allowance);
    }

    const tablo = document.getElementById('tablo');

    count.textContent = `${liste.length} ${info} öğrenci`;

    if (liste.length === 0) {
        tablo.innerHTML = `
            <tr><td colspan="7">
                <div class="empty-state">
                    <div class="empty-icon">👤</div>
                    <p>Öğrenci bulunamadı</p>
                </div>
            </td></tr>
        `;
        return;
    }


    tablo.innerHTML = liste.map((item, i) => {
        let butonlar = '';

        if (item.is_active === 1) {
            butonlar = `
                <button class="btn btn-approve" onclick="window.location.href='student_detail.html?tc=${item.tcno}'">Detay</button>
                <button class="btn btn-reject" onclick="expel('${item.tcno}')">At</button>
            `;
        } else {
            butonlar = `
                <button class="btn btn-warning" onclick="reactivate('${item.tcno}')">Aktifleştir</button>
            `;
        }

        return `
        <tr>
            <td style="color:var(--text-muted)">${i + 1}</td>
            <td>${item.tcno}</td>
            <td>${item.fullname}</td>
            <td>${item.birthdate ?? '—'}</td>
            <td>${item.allowance} gün</td>
            <td>${item.room}</td>
            <td><span class="badge ${item.is_active ? 'badge-active' : 'badge-rejected'}">
            ${item.is_active ? 'Aktif' : 'Aktif Degil'}</span></td>
            <td style="text-align:center;">
                ${butonlar}
            </td>
        </tr>
    `;
    }).join('');
}

function expel(tc) {
    fetch(`${API}/api/expel`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tcno: tc })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) alert('Hata: ' + data.error);
            getStudents();
        });
}

function reactivate(tc) {
    fetch(`${API}/api/activate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tcno: tc })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) alert('Hata: ' + data.error);
            getStudents();
        });
}