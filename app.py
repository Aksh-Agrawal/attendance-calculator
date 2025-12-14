from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import sqlite3
import json

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Create students table
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  roll_number TEXT UNIQUE NOT NULL)''')
    
    # Create attendance table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  date TEXT NOT NULL,
                  lecture_number INTEGER NOT NULL,
                  status TEXT NOT NULL,
                  FOREIGN KEY (student_id) REFERENCES students(id),
                  UNIQUE(student_id, date, lecture_number))''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students ORDER BY name')
    students = c.fetchall()
    conn.close()
    
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', students=students, today=today)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    roll_number = request.form.get('roll_number')
    
    if name and roll_number:
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            c.execute('INSERT INTO students (name, roll_number) VALUES (?, ?)', 
                     (name, roll_number))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            return "Roll number already exists!", 400
    
    return redirect(url_for('index'))

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form.get('student_id')
    date = request.form.get('date')
    attendance_data = request.form.get('attendance_data')
    
    if not all([student_id, date, attendance_data]):
        return "Missing data", 400
    
    # Parse attendance data (JSON format)
    lectures = json.loads(attendance_data)
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    for lecture_num, status in lectures.items():
        c.execute('''INSERT OR REPLACE INTO attendance 
                     (student_id, date, lecture_number, status)
                     VALUES (?, ?, ?, ?)''',
                 (student_id, date, int(lecture_num), status))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/get_attendance/<int:student_id>/<date>')
def get_attendance(student_id, date):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT lecture_number, status FROM attendance 
                 WHERE student_id = ? AND date = ?''',
             (student_id, date))
    
    attendance = {}
    for row in c.fetchall():
        attendance[row[0]] = row[1]
    
    conn.close()
    return jsonify(attendance)

@app.route('/statistics/<int:student_id>')
def statistics(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Get student info
    c.execute('SELECT name, roll_number FROM students WHERE id = ?', (student_id,))
    student = c.fetchone()
    
    if not student:
        return "Student not found", 404
    
    # Calculate weekly attendance (last 7 days)
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    c.execute('''SELECT COUNT(*) FROM attendance 
                 WHERE student_id = ? AND date >= ? AND status = 'present' ''',
             (student_id, week_ago))
    weekly_present = c.fetchone()[0]
    
    c.execute('''SELECT COUNT(*) FROM attendance 
                 WHERE student_id = ? AND date >= ?''',
             (student_id, week_ago))
    weekly_total = c.fetchone()[0]
    
    # Calculate monthly attendance (last 30 days)
    month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    c.execute('''SELECT COUNT(*) FROM attendance 
                 WHERE student_id = ? AND date >= ? AND status = 'present' ''',
             (student_id, month_ago))
    monthly_present = c.fetchone()[0]
    
    c.execute('''SELECT COUNT(*) FROM attendance 
                 WHERE student_id = ? AND date >= ?''',
             (student_id, month_ago))
    monthly_total = c.fetchone()[0]
    
    # Calculate overall attendance
    c.execute('''SELECT COUNT(*) FROM attendance 
                 WHERE student_id = ? AND status = 'present' ''',
             (student_id,))
    overall_present = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM attendance WHERE student_id = ?', (student_id,))
    overall_total = c.fetchone()[0]
    
    # Get daily attendance records for the last 30 days
    c.execute('''SELECT date, lecture_number, status FROM attendance 
                 WHERE student_id = ? AND date >= ?
                 ORDER BY date DESC, lecture_number''',
             (student_id, month_ago))
    records = c.fetchall()
    
    conn.close()
    
    weekly_percentage = (weekly_present / weekly_total * 100) if weekly_total > 0 else 0
    monthly_percentage = (monthly_present / monthly_total * 100) if monthly_total > 0 else 0
    overall_percentage = (overall_present / overall_total * 100) if overall_total > 0 else 0
    
    return render_template('statistics.html',
                          student=student,
                          weekly_present=weekly_present,
                          weekly_total=weekly_total,
                          weekly_percentage=weekly_percentage,
                          monthly_present=monthly_present,
                          monthly_total=monthly_total,
                          monthly_percentage=monthly_percentage,
                          overall_present=overall_present,
                          overall_total=overall_total,
                          overall_percentage=overall_percentage,
                          records=records)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
    c.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
