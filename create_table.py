import sqlite3


conn=sqlite3.connect("ehr.db")

cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    gender TEXT NOT NULL,
    dob TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
 
conn.commit()

print("table created successfully")

conn.close()