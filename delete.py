import sqlite3

conn=sqlite3.connect("ehr.db")

cursor=conn.cursor()
delid=input("Enter the id to be deleted : ")
cursor.execute("DELETE FROM patients WHERE patient_id=?",(delid))
conn.commit()
print("deleted successfully")
conn.close()