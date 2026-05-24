const params = new URLSearchParams(window.location.search);
const tc = params.get('tc');

document.addEventListener('DOMContentLoaded', () => {
    if (!tc) {
        window.location.href = 'students.html';
        return;
    }

    fetch(`${API}/api/student_detail/${tc}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) return alert(data.error);
            document.getElementById('detay-avatar').textContent = data.fullname.charAt(0).toUpperCase();
            document.getElementById('detay-isim').textContent = data.fullname;
            document.getElementById('detay-tc').textContent = data.tcno;
            document.getElementById('detay-dogum').textContent = data.birthdate;
            document.getElementById('detay-izin').textContent = data.allowance;
            document.getElementById('detay-oda').textContent = data.room;
        });

    fetch(`${API}/api/rooms`)
        .then(r => r.json())
        .then(rooms => {
            const select = document.getElementById('room-select');
            select.innerHTML = '<option value="">Yeni Oda Seçin</option>';
            rooms.filter(r => r.available > 0).forEach(r => {
                select.innerHTML += `<option value="${r.id}">${r.block} Blok - ${r.roomno} (Boş: ${r.available})</option>`;
            });
        });
});

function expelStudent() {
    fetch(`${API}/api/expel`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tcno: tc })
    })
        .then(r => r.json())
        .then(data => {
            if (data.error) alert('Hata: ' + data.error);
            else window.location.href = 'students.html';
        })
        .catch(err => console.error('Bağlantı hatası:', err));
}

function updateRoom() {
    const newRoomId = document.getElementById('room-select').value;
    if (!newRoomId) return alert('Lütfen bir oda seçin.');

    fetch(`${API}/api/students/update-room`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tcno: tc, roomid: newRoomId })
    })
        .then(r => r.json())
        .then(data => {
            if (data.error) alert('Hata: ' + data.error);
            else {
                window.location.reload();
            }
        });
}