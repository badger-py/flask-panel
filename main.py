from flask import Flask, render_template ,request


app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        return 'login'

if __name__ == '__main__':
    app.run()
