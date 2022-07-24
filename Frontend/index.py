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

# ///////////////////////////////////////rutas admin/////////////////////////////


@app.route('/admin/login')
def login_admin():
    return render_template('/admin/login_admin.html')


@app.route('/admin/inicio')
def inicio_admin():
    return render_template('/admin/inicioAdmin.html')


@app.route('/admin/registro_operador', methods=['GET', 'POST'])
def registro_operador():
    return render_template('registro_operador.html')


@app.route('/admin/reporte')
def reporte_admin():
    return render_template('/admin/reporte_ventas.html')

# ///////////////////////////////////////rutas admin/////////////////////////////


# ///////////////////////////////////////rutas operador/////////////////////////////
@app.route('/operador/login', methods=['GET', 'POST'])
def login_operador():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return redirect('/operador/inicio')
    else:
        return render_template('/op/login_operador.html')


@app.route('/operador/inicio')
def inicio_operador():
    return render_template('/op/inicioOperador.html')


@app.route('/admin/inicio')
def inicio_admin():
    return render_template('/admin/inicioAdmin.html')


# ///////////////////////////////////////rutas comunes/////////////////////////////
@app.route('/recarga')
def interfaz_recarga():
    return render_template('recarga.html')


@app.route('/registro_estudiante')
def registro_estudiante():
    return render_template('registro_estudiante.html')


@app.route('/actualizar_estudiante')
def actualizar_estudiante():
    return render_template('actualizar_estudiante.html')
# ///////////////////////////////////////rutas comunes/////////////////////////////


@app.route('/operador/reporte')
def interfaz_reporte():
    return render_template('reporteFallos.html')


if __name__ == '__main__':
    app.run(debug=True)
