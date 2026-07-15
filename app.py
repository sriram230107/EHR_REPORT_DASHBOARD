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
    conn.row_factory = sq.Row
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



if __name__ =="__main__":
    app.run(debug=True)