import sqlite3

conn=sqlite3.connect("ehr.db")

inp=int(input("Enter the patent id ."))
num=input("Enter the patent email id .")

cursor=conn.cursor()
cursor.execute("UPDATE patients SET email=? WHERE patient_id=?",(num,inp))


conn.commit()
print("updated successfully")
conn.close()