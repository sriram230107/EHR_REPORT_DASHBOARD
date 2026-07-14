from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash

app=Flask(__name__)
app.secret_key="abc123"
patients=[{"doctor_name":"Ram","patient_name":"arjun","age":17},{"doctor_name":"Ragul","patient_name":"gokul","age":19}]
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
    if "doctor" in session:
        return render_template("doctor_dashboard.html",username=session["doctor"],patients=patients)
    else:
        return redirect(url_for("doctor_login"))
@app.route("/logout")
def logout():
    session.pop("doctor")
    return redirect(url_for("doctor_login"))
if __name__ =="__main__":
    app.run(debug=True)