let tumOdalar = [];

document.addEventListener('DOMContentLoaded', () => {
    getRooms();
    setInterval(getRooms, 5000);
});

function getRooms() {
    fetch(`${API}/api/rooms`)
        .then(res => res.json())
        .then(data => {
            tumOdalar = data;
            renderOzet(data);
            renderRooms();
        })
        .catch(err => console.error('Bağlantı hatası:', err));
}

function renderOzet(data) {
    let tamDolu = 0;
    let tamBos = 0;
    let toplamKapasite = 0;
    let toplamOgrenci = 0;
    let kalanBos = 0;

    for (let i = 0; i < data.length; i++) {
        if (data[i].available === 0) tamDolu++;
        if (data[i].occupancy === 0) tamBos++;
        toplamKapasite += data[i].capacity;
        toplamOgrenci += data[i].occupancy;
        kalanBos += data[i].available;
    }

    const ozet = document.getElementById('ozet');
    ozet.innerHTML = '';

    ozet.innerHTML += `<div class="summary-card"><div>🚪</div><div class="summary-value">${data.length}</div><div class="summary-label">Toplam Oda</div></div>`;
    ozet.innerHTML += `<div class="summary-card"><div>🔴</div><div class="summary-value">${tamDolu}</div><div class="summary-label">Tam Dolu Oda</div></div>`;
    ozet.innerHTML += `<div class="summary-card"><div>🟢</div><div class="summary-value">${tamBos}</div><div class="summary-label">Tamamen Boş Oda</div></div>`;
    ozet.innerHTML += `<div class="summary-card"><div>👥</div><div class="summary-value">${toplamKapasite}</div><div class="summary-label">Toplam Kapasite</div></div>`;
    ozet.innerHTML += `<div class="summary-card"><div>🎓</div><div class="summary-value">${toplamOgrenci}</div><div class="summary-label">Kayıtlı Öğrenci</div></div>`;
    ozet.innerHTML += `<div class="summary-card"><div>🛏</div><div class="summary-value">${kalanBos}</div><div class="summary-label">Boş Yatak</div></div>`;
}

function renderRooms() {
    const siralama = document.getElementById('siralama').value;
    let liste = [...tumOdalar];

    if (siralama === 'dolu-azalan') {
        liste.sort((a, b) => (b.occupancy / b.capacity) - (a.occupancy / a.capacity));
    } else if (siralama === 'dolu-artan') {
        liste.sort((a, b) => (a.occupancy / a.capacity) - (b.occupancy / b.capacity));
    }

    const bloklar = {};
    liste.forEach(room => {
        if (!bloklar[room.block]) bloklar[room.block] = [];
        bloklar[room.block].push(room);
    });

    const container = document.getElementById('bloklar');
    container.innerHTML = ''

    for (const blok in bloklar) {
        const odalar = bloklar[blok];
        const div = document.createElement('div');
        div.style.marginBottom = '24px';
        div.innerHTML = `
            <div class = "blok-baslik">
                ${blok} Blok
            </div>
            <div class="card">
                <table>
                    <thead>
                        <tr>
                            <th>Oda No</th>
                            <th>Kapasite</th>
                            <th>Dolu</th>
                            <th>Boş</th>
                            <th>Doluluk</th>
                            <th>Durum</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${odalar.map(oda => {
            const yuzde = Math.round((oda.occupancy / oda.capacity) * 100);
            const dolu = oda.available === 0;
            return `
                                <tr>
                                    <td>${oda.roomno}</td>
                                    <td>${oda.capacity}</td>
                                    <td>${oda.occupancy}</td>
                                    <td>${oda.available}</td>
                                    <td>
                                        <div class="progress-wrapper">
                                            <div class="progress-track">
                                                <div class="${dolu ? 'progress-fill-dolu' : 'progress-fill-musait'}" style="width:${yuzde}%"></div>
                                            </div>
                                            <span style="font-size:11px; min-width:30px;">%${yuzde}</span>
                                        </div>
                                    </td>
                                    <td>
                                        <span class="badge ${dolu ? 'badge-rejected' : 'badge-active'}">
                                            ${dolu ? '● Dolu' : '● Müsait'}
                                        </span>
                                    </td>
                                </tr>
                            `;
        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.appendChild(div);
    }
}