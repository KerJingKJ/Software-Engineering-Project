import sqlite3

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# First, backup any existing data
print("=== Backing up existing data ===")
try:
    cursor.execute("SELECT * FROM student_scholarship_application")
    existing_data = cursor.fetchall()
    print(f"Found {len(existing_data)} rows in student_scholarship_application")
except:
    existing_data = []
    print("No existing data or table doesn't exist")

try:
    cursor.execute("SELECT * FROM student_guardian")
    guardian_data = cursor.fetchall()
    print(f"Found {len(guardian_data)} rows in student_guardian")
except:
    guardian_data = []
    print("No guardian data")

# Drop the old tables
print("\n=== Dropping old tables ===")
try:
    cursor.execute("DROP TABLE IF EXISTS student_guardian")
    print("Dropped student_guardian")
except Exception as e:
    print(f"Error dropping student_guardian: {e}")

try:
    cursor.execute("DROP TABLE IF EXISTS student_scholarship_application")
    print("Dropped student_scholarship_application")
except Exception as e:
    print(f"Error dropping student_scholarship_application: {e}")

# Create the new tables with correct schema
print("\n=== Creating new tables ===")

cursor.execute('''
CREATE TABLE student_scholarship_application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    scholarship_id INTEGER NOT NULL REFERENCES committee_scholarship(id),
    name VARCHAR(200) NOT NULL,
    home_address TEXT NOT NULL,
    correspondence_address TEXT NOT NULL,
    ic_no VARCHAR(20) NOT NULL,
    age INTEGER NOT NULL,
    date_of_birth DATE NOT NULL,
    intake DATE NOT NULL,
    programme VARCHAR(200) NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    race VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email_address VARCHAR(254) NOT NULL,
    highest_qualification VARCHAR(200) NOT NULL,
    passport_photo VARCHAR(100) NOT NULL,
    academic_result VARCHAR(100) NOT NULL,
    supporting_document VARCHAR(100) NOT NULL,
    personal_achievement TEXT NOT NULL,
    reason_deserve TEXT NOT NULL,
    ea_form VARCHAR(100) NOT NULL,
    payslip VARCHAR(100) NOT NULL
)
''')
print("Created student_scholarship_application")

cursor.execute('''
CREATE TABLE student_guardian (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL REFERENCES student_scholarship_application(id),
    relationship VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    ic_no VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    age INTEGER NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    address TEXT NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email_address VARCHAR(254) NOT NULL,
    monthly_income DECIMAL(12, 2) NOT NULL
)
''')
print("Created student_guardian")

conn.commit()
print("\n=== Done! ===")

# Verify the new schema
print("\n=== Verifying new schema ===")
cursor.execute("PRAGMA table_info(student_scholarship_application)")
columns = cursor.fetchall()
print("student_scholarship_application columns:")
for col in columns:
    print(f"  {col[1]}: {col[2]}")

column_names = [col[1] for col in columns]
print(f"\nHas scholarship_id: {'scholarship_id' in column_names}")

conn.close()
