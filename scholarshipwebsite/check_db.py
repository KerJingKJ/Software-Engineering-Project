import sqlite3

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== student_scholarship_application columns ===")
cursor.execute("PRAGMA table_info(student_scholarship_application)")
columns = cursor.fetchall()
if columns:
    for col in columns:
        print(f"  {col[1]}: {col[2]}")
else:
    print("Table does not exist or has no columns")

# Check if scholarship_id column exists
column_names = [col[1] for col in columns]
print(f"\nColumn names: {column_names}")
print(f"Has scholarship_id: {'scholarship_id' in column_names}")

# Check data in the table
print("\n=== Sample data ===")
try:
    cursor.execute("SELECT * FROM student_scholarship_application LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"Row: {row}")
    else:
        print("No data in table")
except Exception as e:
    print(f"Error: {e}")

conn.close()
