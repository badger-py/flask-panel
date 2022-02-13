from flask import Flask, render_template, request, redirect, url_for, flash, abort, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from pydantic import ValidationError
from users_controller import UsersController
from data_views.sql import SQLTables
from sqlite_db_connector import Connector


app = Flask(__name__)
app.secret_key = 'dev'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


login_manager = LoginManager(app)


controller = UsersController()
database = SQLTables(
    Connector(
        file_name=r"/home/yan/Desktop/test_database.db",
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
    if request.path == None:
        abort(404, description="Invalid path")
    if request.path[1:] == '' or request.path[1:] == 'login' or request.path[1:].split('/')[0] == 'static':
        return
    user = current_user
    if type(user.is_anonymous) is not bool:
        user.is_anonymous = user.is_anonymous()
    if user.is_anonymous:
        abort(401)

    if user.role != 4:
        if request.path[1:].split('/')[0] == 'add' and user.role < 2:
            abort(403)
        if (request.path[1:].split('/')[0] == 'edit' or request.path[1:].split('/')[0] == 'delete') and user.role < 3:
            abort(403)
        if request.path[1:].split('/')[0] == 'execute' and user.role < 4:
            abort(403)


@app.route('/')
@login_required
def index():
    return render_template(
        'index.html.jinja',
        tables=database.get_tables()
    )


@app.route('/table/<string:table_name>', methods=['POST'])
@login_required
def get_data_from_table(table_name):
    json = request.json

    # validate JSON on fileds limit and offset
    if (json.get('limit') == None) or (json.get('offset') == None):
        # BadRequest
        abort(400, description='JSON needs to have limit and offset fields')

    table = database.get_tables()
    table = [i for i in table if i.get_name() == table_name]

    if not table:
        abort(404, description='Table not found')
    table = table[0]

    data = database.get_data_from_table(
        table_name=table_name,
        limit=json['limit'],
        offset=json['offset']
    )

    table_columns = list(dict(table.__dict__)['__annotations__'].keys())
    out_data = []
    for string in data:
        # append dict to out_data
        out_data.append(dict(zip(table_columns, string)))

    return jsonify(out_data)


@app.route('/edit/<string:table_name>/<int:id>', methods=['POST'])
@login_required
def edit(table_name, id):
    json = request.json

    table = database.get_tables()
    table = [i for i in table if i.get_name() == table_name]

    if not table:
        abort(404, description='Table not found')
    table = table[0]

    try:
        # validate data
        data = table.parse_obj(json)
    except ValidationError as v_error:
        error = v_error.errors()[0]
        abort(400, description=f"Error in {error['loc'][0]}: {error['msg']}")

    out_json = data.dict(exclude={'id'})

    database.connector.execute_sql(
        query=f'UPDATE {table_name} SET {", ".join([f"{column}=?" for column in out_json.keys()])} WHERE id=?',
        params=list(out_json.values()) + [id],
        commit=True
    )
    return 'OK', 200


@app.route('/delete/<string:table_name>/<int:id>', methods=['DELETE'])
@login_required
def delete(table_name, id):
    database.check_query(table_name)
    database.connector.execute_sql(
        query=f'DELETE FROM {table_name} WHERE id=?',
        params=(id,),
        commit=True
    )
    return 'OK', 200


@app.route('/add/<string:table_name>', methods=['POST'])
@login_required
def add(table_name):
    # check table_name
    database.check_query(table_name)

    json = request.json

    table = database.get_tables()
    table = [i for i in table if i.get_name() == table_name]

    if not table:
        abort(404, description='Table not found')

    table = table[0]

    try:
        # validate data
        data = table.parse_obj(json)
    except ValidationError as v_error:
        error = v_error.errors()[0]
        abort(400, description=f"Error in {error['loc'][0]}: {error['msg']}")

    out_json = data.dict(exclude={'id'})

    q = f'INSERT INTO {table_name}({", ".join([str(column) for column in out_json.keys()])}) VALUES({",".join(list("?" * len(out_json.keys())))})'

    database.connector.execute_sql(
        query=q,
        params=list(out_json.values()),
        commit=True
    )
    return 'OK', 201


@app.route('/execute', methods=['POST'])
@login_required
def execute():
    json = request.json

    try:
        res = database.connector.execute_sql(
            query=json["query"],
            commit=json["commit"]
        )
        if not json["commit"]:
            return jsonify(res)

        return "OK", 200
    except KeyError or TypeError:
        abort(401)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html.jinja')
    else:
        user = {}
        if request.content_type == "application/json":
            user["login"] = request.json.get("user")
            user["password"] = request.json.get("pass")
            remember = request.json.get("remember")
        else:
            user["login"] = request.form.get("user")
            user["password"] = request.form.get("pass")
            remember = request.get("remember")

        user = controller.login_user(
            user["login"],
            user['password']
        )

        if not user:
            # if json in get json out
            if request.content_type == "application/json":
                return make_response(jsonify({"error": "Invalid username or password"}), 400)
            else:
                flash("You type don't correct password")
                return redirect(url_for('login'))

        login_user(user, remember=remember)

        # if json in get json out
        if request.content_type == "application/json":
            return make_response(jsonify({"status": "ok"}), 200)
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def on_404(e):
    return render_template('404.html.jinja')


@app.errorhandler(401)
def on_401(e):
    return redirect(url_for('login'))


@app.errorhandler(400)
def on_400(e):
    return {"error": e.description}, 400


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(host=sys.argv[1].split(":")[0],
                port=sys.argv[1].split(":")[1],
                debug=True
                )
    else:
        app.run(debug=True)
