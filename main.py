from unittest.mock import seal
from flask import Flask, render_template ,request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required
from panel import *
from sqlite_db_connector import Connector, Table


app = Flask(__name__)
app.secret_key = 'dev'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


login_manager = LoginManager(app)


controller = UsersController()
database = SQLTables(
    Connector(
        file_name = r"/home/yan/Desktop/test_database.db",
        tables = [
            Table(
                name = "positions",
                columns = ['id', 'name', 'price'],
                validators = {
                    0:lambda x: True if type(x) is int or str.isnumeric else False,
                    2:str.isnumeric
                }
            ),
            Table(
                name = "photos",
                columns = ['id', 'url', 'positions_id']
            )
        ]
    )
)


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
    return render_template('index.html', tables=database.get_tables())

@app.route('/table/<name>', methods=['POST'])
def get_data_from_table(name):
    json = request.json

    if (not json['limit']) or (not json['offset']):
        abort(400) # BadRequest

    data = database.get_data_from_table(
        name = name,
        limit = json['limit'],
        offset = json['offset']
    )
    return data # is a list like [(1, 'Yan', 'admin'), (2, 'MrNektom', 'admin')]

@app.route('/edit/<table_name>/<id>', methods=['POST'])
def edit(table_name, id):
    json = request.json

    table = database.get_tables()
    table = [i for i in table if i.name == table_name]

    if not table:
        abort(404, description = 'Table not found')
    
    table = table[0]
    table_columns = table.columns


    # validate JSON
    if len(json) != len(table_columns):
        abort(400)
    
    for key, validator in table.validators.items():
        try:
            if not validator(json[key]):
                abort(400, description = "Validation not comleted")
        except KeyError:
            abort(400)
                

    database.connector.execute_sql(
        query = f'UPDATE {table_name} SET {", ".join([f"{column}=?" for column in table_columns])} WHERE id=?',
        params = json + [id],
        commit = True
    )
    return 'OK', 200


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
    import sys
    if len(sys.argv) > 1:
        app.run(host=sys.argv[1].split(":")[0], port=sys.argv[1].split(":")[1])
    else:
        app.run()