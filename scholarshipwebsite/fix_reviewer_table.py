import sqlite3

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current columns
print("=== Current reviewer_eligibilitycheck columns ===")
cursor.execute("PRAGMA table_info(reviewer_eligibilitycheck)")
columns = cursor.fetchall()
current_cols = [col[1] for col in columns]
for col in columns:
    print(f"  {col[1]}: {col[2]}")

# Add missing columns
new_columns = [
    ('leadership_leader', 'BOOLEAN NOT NULL DEFAULT 0'),
    ('leadership_subleader', 'BOOLEAN NOT NULL DEFAULT 0'),
    ('leadership_secretary', 'BOOLEAN NOT NULL DEFAULT 0'),
    ('leadership_committee', 'BOOLEAN NOT NULL DEFAULT 0'),
    ('leadership_member', 'BOOLEAN NOT NULL DEFAULT 0'),
]

print("\n=== Adding missing columns ===")
for col_name, col_type in new_columns:
    if col_name not in current_cols:
        try:
            cursor.execute(f"ALTER TABLE reviewer_eligibilitycheck ADD COLUMN {col_name} {col_type}")
            print(f"  Added: {col_name}")
        except Exception as e:
            print(f"  Error adding {col_name}: {e}")
    else:
        print(f"  Already exists: {col_name}")

conn.commit()

# Verify
print("\n=== Verifying new columns ===")
cursor.execute("PRAGMA table_info(reviewer_eligibilitycheck)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]}: {col[2]}")

conn.close()
print("\nDone!")
