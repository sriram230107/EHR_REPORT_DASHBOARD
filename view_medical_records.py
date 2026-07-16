import sqlite3 as sq


conn = sq.connect("ehr.db")

cursor = conn.cursor()


cursor.execute(
    "SELECT * FROM medical_records"
)


records = cursor.fetchall()


for record in records:
    print(record)


conn.close()