# College Attendance Calculator

A simple web application to track college attendance for students with 7 daily lectures.

## Features

- ✅ Add and manage students
- ✅ Mark daily attendance for 7 lectures
- ✅ View attendance statistics (Weekly, Monthly, Overall)
- ✅ Automatic percentage calculation
- ✅ Visual attendance records with date-wise tracking
- ✅ Alerts for attendance below 75% and 60%
- ✅ Responsive design for mobile and desktop

## Installation

1. Install Python 3.7 or higher

2. Install required packages:

```bash
cd attendance
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory:

```bash
cd attendance
```

2. Run the Flask application:

```bash
python app.py
```

3. Open your browser and go to:

```
http://localhost:5000
```

## Usage

### Adding a Student

1. Enter student name and roll number
2. Click "Add Student"

### Marking Attendance

1. Click "Mark Attendance" on any student card
2. Select the date
3. Mark each lecture as Present or Absent
4. Click "Save Attendance"

### Viewing Statistics

1. Click "View Stats" on any student card
2. See weekly, monthly, and overall attendance percentages
3. View detailed attendance records for the last 30 days

## Features Overview

- **7 Lectures per Day**: Track all 7 daily lectures
- **Weekly Stats**: Attendance for last 7 days
- **Monthly Stats**: Attendance for last 30 days
- **Overall Stats**: All-time attendance record
- **Color-coded Alerts**:
  - Green: ≥75% (Good)
  - Yellow: 60-75% (Warning)
  - Red: <60% (Critical)

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with responsive design

## Database Schema

### Students Table

- id (Primary Key)
- name
- roll_number (Unique)

### Attendance Table

- id (Primary Key)
- student_id (Foreign Key)
- date
- lecture_number (1-7)
- status (present/absent)

## License

Free to use for educational purposes.
