import sqlite3 as sq


conn = sq.connect("ehr.db")

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS medical_records(

    record_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER,

    symptoms TEXT,

    diagnosis TEXT,

    prescription TEXT,

    notes TEXT,

    icd_code TEXT,

    date TIMESTAMP DEFAULT (datetime('now','+5 hours','+30 minutes')),

    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)

)
""")


conn.commit()

conn.close()


print("Medical records table created")