import sqlite3

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add missing columns for Personal Statement / Essay Quality
new_columns = [
    ('essay_compelling', 'BOOLEAN NOT NULL DEFAULT 0'),
    ('essay_generic', 'BOOLEAN NOT NULL DEFAULT 0'),
    ('essay_poor', 'BOOLEAN NOT NULL DEFAULT 0'),
]

print("=== Adding Personal Statement / Essay Quality columns ===")
cursor.execute("PRAGMA table_info(reviewer_eligibilitycheck)")
current_cols = [col[1] for col in cursor.fetchall()]

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
conn.close()
print("Done!")
