import flask
import time, random, threading
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_cors import CORS
import mysql.connector

date = datetime.now()

fee_amount = 1000
day_duration = 30
application_duration = 25
app = flask.Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kykyonetim"
    )

def generate_tc():
    while True:
        digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(9)]
        last_digit = sum(digits) % 10
        if last_digit % 2 == 0:
            digits.append(last_digit)
            return "".join(map(str, digits))

def generate_birth_date(min_age=18, max_age=24):
    today = datetime.now()
    start_date = datetime(today.year - max_age, 1, 1)
    end_date = datetime(today.year - min_age, 12, 31)
    day_range = (end_date - start_date).days
    random_day = random.randint(0, day_range)
    date = start_date + timedelta(days=random_day)
    return date.strftime('%Y-%m-%d')

def student_count():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM students WHERE is_active = 1")
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count

def date_timer():
    global date
    last_month = date.month
    sent_notification = False

    while True:
        time.sleep(day_duration)
        date += timedelta(days=1)

        if date.day == 25 and not sent_notification:
            sent_notification = True
            period = date.strftime('%Y-%m')
            threading.Thread(target=trigger_payments, args=(period,)).start()
        
        if date.month != last_month:
            expel_unpaid(last_month, date.year)
            sent_notification = False
            last_month = date.month

def trigger_payments(period):
    time.sleep(3)

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT tcno FROM students 
            WHERE is_active = 1
            AND tcno NOT IN (
                SELECT tcno FROM payments WHERE period = %s
            )
        """, (period,))
        unpaid_users = [row[0] for row in cursor.fetchall()]

        if not unpaid_users:
            return

        count = random.randint(1, len(unpaid_users))
        selected_users = random.sample(unpaid_users, count)

        pay_date = date.strftime('%Y-%m-%d')
        data = [(tc, pay_date, period, fee_amount) for tc in selected_users]

        cursor.executemany("""
            INSERT INTO payments (tcno, paydate, period, fee) VALUES (%s, %s, %s, %s)
        """, data)
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

def auto_application():
    while True:
        time.sleep(application_duration)
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT isim FROM havuz_isimler ORDER BY RAND() LIMIT 1")
            name = cursor.fetchone()[0]
            cursor.execute("SELECT soyisim FROM havuz_soyisimler ORDER BY RAND() LIMIT 1")
            surname = cursor.fetchone()[0]
            tc = generate_tc()
            cursor.execute(
                "INSERT INTO applications (tcno, name, surname) VALUES (%s, %s, %s)",
                (tc, name, surname)
            )
            db.commit()
        except Exception as e:
            print(f"Hata: {e}")
        finally:
            cursor.close()
            db.close()

def auto_payment():
    while True:
        count = student_count()
        if count == 0:
            time.sleep(30)
            continue

        duration = (30 * day_duration) / (count * 0.8)
        time.sleep(max(8, min(30, duration)) + random.uniform(-2, 2))

        db = get_db()
        cursor = db.cursor()
        try:
            period = date.strftime('%Y-%m')
            cursor.execute("""
                SELECT tcno FROM students 
                WHERE is_active = 1
                AND tcno NOT IN (
                    SELECT tcno FROM payments WHERE period = %s
                )
                ORDER BY RAND() LIMIT 1
            """, (period,))
            
            student = cursor.fetchone()
            if not student:
                continue
            
            tcno = student[0]
            cursor.execute(
                "INSERT INTO payments (tcno, period, paydate, fee) VALUES (%s, %s, %s, %s)",
                (tcno, period, date.strftime('%Y-%m-%d'), fee_amount)
            )
            db.commit()
        except Exception as e:
            print(f"Ödeme simülasyon hatası: {e}")
        finally:
            cursor.close()
            db.close()

def auto_leave():
    while True:
        count = student_count()
        if count == 0:
            time.sleep(30)
            continue

        duration = day_duration / (count * 0.045)
        time.sleep(max(8, min(30, duration)) + random.uniform(-2, 2))
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT tcno FROM students WHERE is_active = 1 ORDER BY RAND() LIMIT 1")
            student = cursor.fetchone()
            
            if not student:
                continue
            
            tcno = student[0]
            start_date = date + timedelta(days=random.randint(1, 30))
            l_duration = random.randint(1, 7)
            end_date = start_date + timedelta(days=l_duration)
            
            cursor.execute(
                "INSERT INTO leaves (tcno, startdate, enddate) VALUES (%s, %s, %s)",
                (tcno, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            )
            db.commit()
        except Exception as e:
            print(f"İzin simülasyon hatası: {e}")
        finally:
            cursor.close()
            db.close()

def expel_unpaid(month, year):
    period = f"{year}-{month:02d}"

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT tcno, roomid FROM students
            WHERE is_active = 1 
            AND tcno NOT IN (
                SELECT tcno FROM payments WHERE period = %s
            )
        """, (period,))
        unpaid_users = cursor.fetchall()

        for tcno, roomid in unpaid_users:
            cursor.execute("UPDATE students SET is_active = 0 WHERE tcno = %s", (tcno,))
            cursor.execute("UPDATE rooms SET occupancy = occupancy - 1 WHERE id = %s", (roomid,))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Öğrenciyi Yurttan Atma Hatası: {e}")
    finally:
        cursor.close()
        db.close()

@app.route('/api/notification', methods=["GET"])
def check_notification():
    day = date.day
    return jsonify({"sent": day >= 25})

@app.route('/api/applications', methods=["GET"])
def get_applications():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT tcno, name, surname, appdate FROM applications WHERE status = 'Pending'")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "tcno": row[0],
                "fullname": row[1] + " " + row[2],
                "appdate": row[3].strftime("%Y-%m-%d %H:%M:%S")
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/applications/reject', methods=["POST"])
def reject_application():
    db = get_db()
    cursor = db.cursor()
    try:
        tcno = request.get_json().get('tcno')
        if not tcno:
            return jsonify({"error": "TC numarası eksik"}), 400
        cursor.execute("UPDATE applications SET status = 'Rejected' WHERE tcno = %s", (tcno,))
        db.commit()
        return jsonify({"message": "Başvuru reddedildi"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/applications/approve', methods=["POST"])
def approve_application():
    db = get_db()
    cursor = db.cursor()
    try:
        tcno = request.get_json().get('tcno')
        if not tcno:
            return jsonify({"error": "TC numarası eksik"}), 400

        cursor.execute("SELECT id FROM rooms WHERE occupancy < capacity ORDER BY RAND() LIMIT 1")
        room = cursor.fetchone()
        if not room:
            return jsonify({"error": "Yurtta boş yer yok"}), 400
        room_id = room[0]

        cursor.execute("SELECT name, surname FROM applications WHERE tcno = %s", (tcno,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": "Başvuru bulunamadı"}), 404
        name, surname = student

        cursor.execute("UPDATE applications SET status = 'Approved' WHERE tcno = %s", (tcno,))

        birthdate = generate_birth_date()
        cursor.execute(
            "INSERT INTO students (tcno, name, surname, birthdate, roomid) VALUES (%s, %s, %s, %s, %s)",
            (tcno, name, surname, birthdate, room_id)
        )

        cursor.execute("UPDATE rooms SET occupancy = occupancy + 1 WHERE id = %s", (room_id,))

        db.commit()
        return jsonify({"message": "Başvuru onaylandı"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/students', methods=["GET"])
def get_students():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT s.tcno, s.name, s.surname, s.birthdate, s.allowance, s.is_active, r.block, r.roomno
            FROM students s
            JOIN rooms r ON s.roomid = r.id
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "tcno": row[0],
                "fullname": row[1] + " " + row[2],
                "birthdate": str(row[3]) if row[3] else None,
                "allowance": row[4],
                "is_active": row[5],
                "room": str(row[6]) + " Blok - " + str(row[7])
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/leaves', methods=["GET"])
def get_leaves():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT L.id, L.tcno, S.name, S.surname, 
                   L.startdate, L.enddate, S.allowance,
                   DATEDIFF(L.enddate, L.startdate) AS duration
            FROM leaves L
            JOIN students S ON L.tcno = S.tcno
            WHERE L.status = 'Pending'
            AND S.is_active = 1
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "tcno": row[1],
                "fullname": row[2] + " " + row[3],
                "startdate": str(row[4]),
                "enddate": str(row[5]),
                "allowance": row[6],
                "duration": row[7]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/leaves/reject', methods=["POST"])
def reject_leave():
    db = get_db()
    cursor = db.cursor()
    try:
        leave_id = request.get_json().get('id')
        if not leave_id:
            return jsonify({"error": "İzin ID eksik"}), 400
        cursor.execute("UPDATE leaves SET status = 'Rejected' WHERE id = %s", (leave_id,))
        db.commit()
        return jsonify({"message": "İzin talebi reddedildi"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/leaves/approve', methods=["POST"])
def approve_leave():
    db = get_db()
    cursor = db.cursor()
    try:
        leave_id = request.get_json().get('id')
        if not leave_id:
            return jsonify({"error": "İzin ID eksik"}), 400

        cursor.execute("""
            SELECT l.tcno, s.allowance,
                   DATEDIFF(l.enddate, l.startdate) AS duration
            FROM leaves l
            JOIN students s ON l.tcno = s.tcno
            WHERE l.id = %s
        """, (leave_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "İzin talebi bulunamadı"}), 404

        tcno, allowance, duration = row

        if allowance < duration:
            return jsonify({"error": "Yetersiz izin hakkı."}), 400

        cursor.execute("UPDATE leaves SET status = 'Approved' WHERE id = %s", (leave_id,))
        cursor.execute("UPDATE students SET allowance = allowance - %s WHERE tcno = %s", (duration, tcno))

        db.commit()
        return jsonify({"message": "İzin onaylandı"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/payments', methods=["GET"])
def get_payments():
    db = get_db()
    cursor = db.cursor()
    try:
        period = date.strftime('%Y-%m')
        
        cursor.execute("""
            SELECT s.tcno, s.name, s.surname, r.block, r.roomno,
                   p.paydate, p.fee
            FROM students s
            JOIN rooms r ON s.roomid = r.id
            LEFT JOIN payments p ON s.tcno = p.tcno AND p.period = %s
            WHERE s.is_active = 1
        """, (period,))
        
        rows = cursor.fetchall()
        result = []
        for row in rows:
            odedi = row[5] is not None
            result.append({
                "tcno": row[0],
                "fullname": row[1] + " " + row[2],
                "room": str(row[3]) + " Blok - " + str(row[4]),
                "paid": odedi,
                "paydate": str(row[5]) if odedi else None,
                "fee": str(row[6]) if odedi else None
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/date', methods=["GET"])
def get_simdate():
    return jsonify({
        "date": date.strftime('%Y-%m-%d'),
        "period": date.strftime('%Y-%m'),
        "display": date.strftime('%B %Y')
    })

@app.route('/api/rooms', methods=["GET"])
def get_rooms():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT id, block, roomno, capacity, occupancy
            FROM rooms
            ORDER BY block, roomno
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "block": str(row[1]),
                "roomno": str(row[2]),
                "capacity": row[3],
                "occupancy": row[4],
                "available": row[3] - row[4]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/expel', methods=["POST"])
def expel():
    db = get_db()
    cursor = db.cursor()
    try:
        tcno = request.get_json().get('tcno')
        if not tcno:
            return jsonify({"error": "TC numarası eksik"}), 400
        cursor.execute("SELECT roomid FROM students WHERE tcno = %s", (tcno,))
        room = cursor.fetchone()
        if not room:
            return jsonify({"error": "Öğrenci bulunamadı"}), 404
        
        roomid = room[0]
        cursor.execute("UPDATE students SET is_active = 0 WHERE tcno = %s", (tcno,))
        cursor.execute("UPDATE rooms SET occupancy = occupancy - 1 WHERE id = %s", (roomid,))
        cursor.execute("UPDATE leaves SET status = 'Rejected' WHERE tcno = %s AND status = 'Pending'", (tcno,))
        
        db.commit()
        return jsonify({"message": "Öğrenci yurttan atıldı"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/activate', methods=["POST"])
def activate():
    db = get_db()
    cursor = db.cursor()
    try:
        tcno = request.get_json().get('tcno')
        if not tcno:
            return jsonify({"error": "TC numarası eksik"}), 400
        cursor.execute("""
            SELECT R.id, R.occupancy, R.capacity
            FROM rooms R JOIN students S
            ON S.roomid = R.id
            WHERE tcno = %s
        """, (tcno,))
        row = cursor.fetchone()
        current_room_id, occupancy, capacity = row

        if occupancy < capacity:
            target_room_id = current_room_id
        else:
            cursor.execute("""
                SELECT id 
                FROM rooms 
                WHERE occupancy < capacity
                ORDER BY RAND()
                LIMIT 1
            """)
            new_room = cursor.fetchone()
            if not new_room:
                return jsonify({"error": "Hiç boş oda yok!"}), 400
            target_room_id = new_room[0]

        cursor.execute("UPDATE students SET is_active = 1, roomid = %s WHERE tcno = %s", (target_room_id, tcno))
        cursor.execute("UPDATE rooms SET occupancy = occupancy + 1 WHERE id = %s", (target_room_id,))
        db.commit()
        return jsonify({"message": "Öğrenci kaydı aktifleştirildi!"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/student_detail/<tc>', methods=["GET"])
def get_student_detail(tc):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT s.tcno, s.name, s.surname, s.birthdate, s.allowance, r.block, r.roomno
            FROM students S
            JOIN rooms R ON S.roomid = R.id
            WHERE S.tcno = %s
        """, (tc,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Öğrenci bulunamadı"}), 404
        
        return jsonify({
            "tcno": row[0],
            "fullname": row[1] + " " + row[2],
            "birthdate": str(row[3]) if row[3] else "—",
            "allowance": row[4],
            "room": str(row[5]) + " Blok - " + str(row[6])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/students/update-room', methods=["POST"])
def update_student_room():
    db = get_db()
    cursor = db.cursor()
    try:
        tcno = request.get_json().get('tcno')
        new_room_id = request.get_json().get('roomid')

        cursor.execute("SELECT roomid FROM students WHERE tcno = %s", (tcno,))
        old_room = cursor.fetchone()
        if not old_room:
            return jsonify({"error": "Öğrenci bulunamadı"}), 404
            
        old_room_id = old_room[0]
        cursor.execute("UPDATE rooms SET occupancy = occupancy - 1 WHERE id = %s", (old_room_id,))
        cursor.execute("UPDATE students SET roomid = %s WHERE tcno = %s", (new_room_id, tcno))
        cursor.execute("UPDATE rooms SET occupancy = occupancy + 1 WHERE id = %s", (new_room_id,))
        
        db.commit()
        return jsonify({"message": "Oda başarıyla güncellendi"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    threading.Thread(target=auto_application, daemon=True).start()
    threading.Thread(target=auto_leave, daemon=True).start()
    threading.Thread(target=auto_payment, daemon=True).start()
    threading.Thread(target=date_timer, daemon=True).start()
    app.run(debug=True, use_reloader=False)