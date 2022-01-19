from flask import Flask


app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'

if __name__ == '__main__':
    app.run()