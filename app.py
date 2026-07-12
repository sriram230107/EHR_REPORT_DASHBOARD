from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app=Flask(__name__)
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
            return redirect(url_for("doctor_dashboard"))
        else:
            return "Incorrect Credentials"
    else:
        return render_template("doctor_login.html")
@app.route("/doctor_dashboard")
def doctor_dashboard():
    return render_template("doctor_dashboard.html")
# @app.route("/login")
# def login():
#     return "LET'S LOGIN..!"
if __name__ =="__main__":
    app.run(debug=True)