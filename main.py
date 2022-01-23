from flask import Flask, render_template ,request, redirect, url_for, flash, make_response, jsonify
from flask_login import LoginManager, login_user, login_required
from panel import *


app = Flask(__name__)
app.secret_key = 'dev'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
login_manager = LoginManager(app)


controller = UsersController()


@login_manager.user_loader
def load_user(user_id):
    return controller.get_user(user_id)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
@login_required
def index():
    return render_template('index.html.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html.jinja')
    else:
        remember = False
        user = {
            "login":None,
            "password":None,
        }
        if request.content_type == "application/json":
            user["login"] = request.json.get("user")
            user["password"] = request.json.get("pass")
            remember = request.json.get("remember")
        else:
            user["login"] = request.form.get("user")
            user["password"] = request.form.get("pass")
            remember = request.form["remember"]
        user = controller.login_user(user["login"], user['password'])
        if not user:
            if request.content_type == "application/json":
                return make_response(jsonify({"error": "Invalid username or password"}),400)
            else:
                flash("You type don't correct password")
                return redirect(url_for('login'))
        login_user(user,remember=remember)
        if request.content_type == "application/json":
            return make_response(jsonify({"status":"ok"}),200)
        return redirect(url_for('index'))

@app.errorhandler(404)
def on_404(e):
    return render_template('404.html.jinja')

@app.errorhandler(401)
def on_401(e):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
