from flask import Flask, render_template,request
import auth
auth.init()
app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        if auth.is_valid(request.form["user"],request.form["pass"]):
            return auth.log_user(request.form["user"])
    return render_template("login.html")

@app.route("/<p>")
def not_found(p):
    return render_template("404.html",path=p)

if __name__ == "__main__":
    app.run(debug=True)
