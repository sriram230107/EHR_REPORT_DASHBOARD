import sqlite3

# Connect to the database
conn = sqlite3.connect("ehr.db")

# Create a cursor
cursor = conn.cursor()

# Execute SELECT query
cursor.execute("SELECT * FROM patients")

# Fetch all records
patients = cursor.fetchall()

# Print each patient
for patient in patients:
    print(patient)


# Close the connection
conn.close()