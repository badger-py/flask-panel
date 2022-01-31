from unittest.mock import seal
from flask import Flask, render_template ,request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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
                    0:lambda x: True if type(x) is int or str.isnumeric(x) else False,
                    2:lambda x: True if type(x) is int or str.isnumeric(x) else False
                }
            ),
            Table(
                name = "photos",
                columns = ['id', 'url', 'positions_id'],
                validators = {
                    0:lambda x: True if type(x) is int or str.isnumeric(x) else False
                }
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

@app.before_request
def before_request():
    if request.endpoint == '' or request.endpoint == 'login':
        return
    user = current_user
    if type(user.is_anonymous) is not bool:
        user.is_anonymous = user.is_anonymous()
    if user.is_anonymous:
        abort(401)
    
    if user.role != 4:
        if request.endpoint.split('/')[0] == 'add' and user.role < 2:
            abort(403)
        if (request.endpoint.split('/')[0] == 'edit' or request.endpoint.split('/')[0] == 'delete') and user.role < 3:
            abort(403)
        if request.endpoint.split('/')[0] == 'execute' and user.role < 4:
            abort(403)


@app.route('/')
@login_required
def index():
    return render_template('index.html.jinga', tables=database.get_tables())

@app.route('/table/<name>', methods=['POST'])
@login_required
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
@login_required
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

@app.route('/delete/<table_name>/<id>', methods=['POST'])
@login_required
def delete(table_name, id):
    database.check_query(table_name)
    database.connector.execute_sql(
        query = f'DELETE FROM {table_name} WHERE id=?',
        params = (id,),
        commit = True
    )
    return 'OK', 200

@app.route('/add/<table_name>', methods=['POST'])
@login_required
def add(table_name):
    json = request.json

    table = database.get_tables()
    table = [i for i in table if i.name == table_name]

    if not table:
        abort(404, description = 'Table not found')
    
    table = table[0]
    table_columns = table.columns


    # validate JSON
    if len(json) != len(table_columns) - 1:
        abort(400)
    
    for key, validator in list(table.validators.items())[1:]:
        try:
            key -= 1
            if not validator(json[key]):
                abort(400, description = "Validation not comleted")
        except IndexError:
            abort(400, description = 'Index Error')
    

    database.connector.execute_sql(
        query = f'INSERT INTO {table_name}({", ".join([str(column) for column in table_columns[1:]])}) VALUES({",".join(list("?" * (len(table_columns) - 1)))})',
        params = json,
        commit = True
    )
    return 'OK', 201

@app.route('/execute', methods = ['POST'])
def execute():
    json = request.json

    try:
        database.connector.execute_sql(
            query = json["query"]
            commit = json["commit"]
        )
        return "OK", 200
    except KeyError or TypeError:
        abort(401)

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def on_404(e):
    return render_template('404.html.jinja')

@app.errorhandler(401)
def on_401(e):
    return redirect(url_for('login'))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(host=sys.argv[1].split(":")[0], port=sys.argv[1].split(":")[1])
    else:
        app.run()
