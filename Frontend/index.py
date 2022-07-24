from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL, MySQLdb

# pip install Flask Flask-MySQLdb Flask_wtf Flask_login


# Conexion BD
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Prueba'
# db = MySQL(app)


# rutas aplicacion
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login_admin')
def login_admin():
    return render_template('login_admin.html')


@app.route('/login_operador', methods=['GET', 'POST'])
def login_operador():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return render_template('login_operador.html')
    else:
        return render_template('login_operador.html')


@app.route('/operador/inicio')
def inicio_operador():
    return render_template('inicio_operador.html')


@app.route('/admin/inicio')
def inicio_admin():
    return render_template('inicio_admin.html')


@app.route('/registro_operador', methods=['GET', 'POST'])
def registro_operador():
    return render_template('registro_operador.html')


@app.route('/registro_estudiante')
def registro_estudiante():
    return render_template('registro_estudiante.html')


@app.route('/actualizar_estudiante')
def actualizar_estudiante():
    return render_template('actualizar_estudiante.html')


@app.route('/recarga')
def recarga():
    return render_template('recarga.html')

@app.route('/dashboard/operador')
def dashboard_operador():
    return render_template('inicioOperador.html')

@app.route('/dashboard/admin')
def dashboard_admin():
    return render_template('inicioAdmin.html')

@app.route('/operador/reporte')
def interfaz_reporte():
    return render_template('reporteFallos.html')

@app.route('/operador/recarga')
def interfaz_recarga():
    return render_template('recarga.html')


if __name__ == '__main__':
    app.run(debug=True)
