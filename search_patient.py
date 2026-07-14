import sqlite3

conn=sqlite3.connect("ehr.db")

cursor=conn.cursor()
patient_id = int(input("Enter Patient ID: "))
cursor.execute("SELECT*FROM patients WHERE patient_id=?",(patient_id,))
patient=cursor.fetchone()
if patient:
    print("Patient Found!")
    print("ID:", patient[0])
    print("Name:", patient[1], patient[2])
    print("Gender:", patient[3])
    print("Phone:", patient[5])
else:
    print("patient not found    ")

conn.close()