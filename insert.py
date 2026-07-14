import sqlite3

conn=sqlite3.connect("ehr.db")

cursor=conn.cursor()
cursor.execute("""
INSERT INTO patients(
    firstname,
    lastname,
    gender,
    dob,
    phone,
    email,
    address,
    blood_group)
    VALUES(?,?,?,?,?,?,?,?)""",
    ("John",
    "Doe",
    "Male",
    "2000-05-15",
    "9876543210",
    "john@example.com",
    "Chennai",
    "O+")
)

conn.commit()
print("inserted successfully")

conn.close()