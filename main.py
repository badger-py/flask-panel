from flask import Flask, render_template ,request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required
from panel import *


app = Flask(__name__)
app.secret_key = 'dev'
login_manager = LoginManager(app)


controller = UsersController()

@login_manager.user_loader
def load_user(user_id):
    return controller.get_user(user_id)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        user = controller.login_user(request.form.get('user'), request.form.get('pass'))
        if not user:
            flash("You type don't correct password")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

@app.errorhandler(404)
def on_404(e):
    return render_template('404.html')

@app.errorhandler(401)
def on_401(e):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
