import sqlite3 as sq

conn = sq.connect("ehr.db")

cursor = conn.cursor()

record_id = int(input("Enter record ID to delete: "))

cursor.execute(
    "DELETE FROM medical_records WHERE record_id=?",
    (record_id,)
)

conn.commit()

conn.close()

print("Medical record deleted")