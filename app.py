from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
import sqlite3 as sq


app=Flask(__name__)
app.secret_key="abc123"
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/doctor_login", methods=['GET' , 'POST'])
def doctor_login():
    if request.method=="POST" :
        username=request.form["doctor_username"]
        did=request.form["doctor_id"]
        password=request.form["doctor_password"]
        if username=="admin" and did=="d123" and password=="admin@@":
            session["doctor"]=username
            return redirect(url_for("doctor_dashboard"))
        else:
            flash("INCORRECT CREDENTIALS")
            return redirect(url_for("doctor_login"))
    else:
        return render_template("doctor_login.html")
@app.route("/doctor_dashboard")
def doctor_dashboard():
    conn=sq.connect("ehr.db")
    cursor=conn.cursor()
    cursor.execute("SELECT*FROM patients")
    patients=cursor.fetchall()
    conn.close()
    if "doctor" in session:
        return render_template("doctor_dashboard.html",username=session["doctor"],patients=patients)
    else:
        return redirect(url_for("doctor_login"))
@app.route("/logout")
def logout():
    session.pop("doctor")
    return redirect(url_for("doctor_login"))
@app.route("/add_patient",methods=['GET','POST'])
def add_patient():
    if request.method=="GET":
        return render_template("add_patient.html")
    else:
        conn=sq.connect("ehr.db")
        cursor=conn.cursor()

        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        dob=request.form["dob"]
        blood_group=request.form["blood_group"]
        phone=request.form["phone"]
        gender=request.form["gender"]
        address=request.form["address"]
        email=request.form["email"]

        cursor.execute("""
        INSERT INTO patients(
        firstname,
        lastname,
        gender,
        dob,
        phone,
        email,
        address,
        blood_group
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
        firstname,
        lastname,
        gender,
        dob,
        phone,
        email,
        address,
        blood_group
        ))
        conn.commit()

        conn.close()

        return redirect(url_for("doctor_dashboard"))
    

@app.route("/search_patient", methods=["GET", "POST"])
def search_patient():

    if request.method == "GET":
        return render_template("search_patient.html")

    else:
        patient_id = request.form["patient_id"]

        conn = sq.connect("ehr.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        conn.close()

        if patient is None:
            return "Patient not found"

        return render_template(
            "search_result.html",
            patient=patient
        )
    
@app.route("/edit_patient/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):

    conn = sq.connect("ehr.db")
    cursor = conn.cursor()

    if request.method == "GET":

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id=?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        conn.close()

        if patient is None:
            return "Patient not found"

        return render_template(
            "edit_patient.html",
            patient=patient
        )


    if request.method == "POST":

        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        blood_group = request.form["blood_group"]

        cursor.execute(
            """
            UPDATE patients
            SET firstname=?,
                lastname=?,
                gender=?,
                dob=?,
                phone=?,
                email=?,
                address=?,
                blood_group=?
            WHERE patient_id=?
            """,
            (
                firstname,
                lastname,
                gender,
                dob,
                phone,
                email,
                address,
                blood_group,
                patient_id
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("doctor_dashboard"))

@app.route("/delete_patient/<int:patient_id>")
def delete_patient(patient_id):

    conn = sq.connect("ehr.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE patient_id=?",
        (patient_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("doctor_dashboard"))

@app.route("/medical_history/<int:patient_id>")
def medical_history(patient_id):

    conn = sq.connect("ehr.db")
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT * FROM medical_records
        WHERE patient_id=?
        """,
        (patient_id,)
    )


    records = cursor.fetchall()


    cursor.execute(
        """
        SELECT * FROM patients
        WHERE patient_id=?
        """,
        (patient_id,)
    )


    patient = cursor.fetchone()


    conn.close()


    return render_template(
        "medical_history.html",
        patient=patient,
        records=records
    )

@app.route("/add_record/<int:patient_id>", methods=["GET", "POST"])
def add_record(patient_id):

    conn = sq.connect("ehr.db")
    cursor = conn.cursor()


    if request.method == "POST":

        doctor_name = session["doctor"]
        symptoms = request.form["symptoms"]
        diagnosis = request.form["diagnosis"]
        prescription = request.form["prescription"]
        notes = request.form["notes"]


        cursor.execute(
            """
            INSERT INTO medical_records
            (patient_id, doctor_name, symptoms, diagnosis, prescription, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                doctor_name,
                symptoms,
                diagnosis,
                prescription,
                notes
            )
        )


        conn.commit()

        conn.close()


        return redirect(
            url_for(
                "medical_history",
                patient_id=patient_id
            )
        )


    conn.close()


    return render_template(
        "add_record.html",
        patient_id=patient_id
    )

if __name__ =="__main__":
    app.run(debug=True)