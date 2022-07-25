from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb

# pip install Flask Flask-MySQLdb Flask_wtf Flask_login


# Conexion BD
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_python'
db = MySQL(app)


# rutas aplicacion
@app.route('/')
def index():
    return render_template('index.html')

# ///////////////////////////////////////rutas admin/////////////////////////////


@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']

        # print(usuario)
        # print(password)f

        cur = db.connection.cursor()
        cur.execute(
            "SELECT * FROM administrador WHERE Usuario='{0}'".format(usuario))
        user = cur.fetchone()
        cur.close()

        if user != None:
            if password == user[3]:

                idb = user[1]

                query = db.connection.cursor()
                query.execute(
                    "SELECT * FROM persona WHERE Id='{0}'".format(idb))
                person = query.fetchone()
                query.close()

                session['name'] = person[3]
                session['email'] = person[7]

                return redirect('/admin/inicio')

            else:

                flash("Usuario o contraseña inválido")
                print("Usuario o contraseña inválido")
                return render_template("/admin/login_admin.html")

        else:

            print("Este Admin no está registrado")
            flash("Este Admin no está registrado")
            return render_template("/admin/login_admin.html")
    else:

        return render_template('/admin/login_admin.html')


@app.route('/admin/inicio')
def inicio_admin():
    return render_template('/admin/inicioAdmin.html')


@app.route('/admin/registro_operador', methods=['GET', 'POST'])
def registro_operador():

    if request.method == 'GET':
        return render_template('/admin/registro_operador.html')

    else:

        tipo = request.form['tipodocumento']
        numdoc = request.form['ndocumento']
        nom1 = request.form['primernombre']
        nom2 = request.form['segundonombre']
        ape1 = request.form['primerapellido']
        ape2 = request.form['segundoapellido']
        user = request.form['username']
        password = request.form['password']
        numtel = request.form['ntelefono']
        email = request.form['email']

        cur = db.connection.cursor()
        cur.execute("INSERT INTO persona (N_Documento, Tipo_Documento, Primer_Nombre, Segundo_Nombre, Primer_Apellido, Segundo_Apellido, Correo, Celular) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (numdoc, tipo, nom1, nom2, ape1, ape2, email, numtel))
        db.connection.commit()

        cur = db.connection.cursor()
        cur.execute(
            "INSERT INTO operador (Persona_Id, Usuario, Contrasena) VALUES ((SELECT MAX(Id) FROM persona), %s, %s)", (user, password))

        db.connection.commit()
        print("Funcionando")

        return redirect('/admin/inicio')


@app.route('/admin/reporte')
def reporte_admin():
    return render_template('/admin/reporte_ventas.html')


@app.route('/admin/reporte/informe')
def reporte1():
    return render_template('/admin/reporte1.html')

@app.route('/admin/reporte/informe2')
def reporte2():
    return render_template('/admin/reporte2.html')

@app.route('/admin/reporte/informe3')
def reporte3():
    return render_template('/admin/reporte3.html')

# ///////////////////////////////////////rutas admin/////////////////////////////


# ///////////////////////////////////////rutas operador/////////////////////////////
@app.route('/operador/login', methods=['GET', 'POST'])
def login_operador():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']

        # print(usuario)
        # print(password)

        cur = db.connection.cursor()
        cur.execute(
            "SELECT * FROM operador WHERE Usuario='{0}'".format(usuario))
        user = cur.fetchone()
        cur.close()

        if user != None:
            if password == user[3]:

                idb = user[1]

                query = db.connection.cursor()
                query.execute(
                    "SELECT * FROM persona WHERE Id='{0}'".format(idb))
                person = query.fetchone()
                query.close()

                session['name'] = person[3]
                session['email'] = person[7]

                return redirect('/operador/inicio')

            else:

                print("Usuario o contraseña inválido")
                return render_template("/op/login_operador.html")

        else:

            print("Este Usuario no está registrado")

            return render_template("/op/login_operador.html")
    else:

        return render_template('/op/login_operador.html')


@app.route('/operador/inicio')
def inicio_operador():
    return render_template('/op/inicioOperador.html')


@app.route('/operador/reporte', methods=['GET', 'POST'])
def interfaz_reporte():

    if request.method == 'POST':
        body = request.form['fallo']

        cur = db.connection.cursor()
        cur.execute(
            "INSERT INTO reporte (descripcion) VALUES ('{0}')".format(body))
        db.connection.commit()

        return redirect('/operador/inicio')

    else:

        return render_template('/op/reporteFallos.html')


# ///////////////////////////////////////rutas comunes/////////////////////////////

@app.route('/recarga', methods=['GET', 'POST'])
def interfaz_recarga():

    if request.method == 'POST':
        ndocumento = request.form['cuenta']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        valor = request.form['valor']

        cur = db.connection.cursor()
        cur.execute(
            "SELECT * FROM persona WHERE N_Documento='{0}'".format(ndocumento))
        user = cur.fetchone()
        cur.close()

        userdoc = str(user[1])

        if user != None:
            if userdoc == ndocumento and user[3] == nombre and user[5] == apellido:

                pid = user[0]
                ndoc = user[1]
                nom = user[3]
                ape = user[5]

                query1 = db.connection.cursor()
                query1.execute(
                    "SELECT * FROM estudiante WHERE Persona_Id='{0}'".format(pid))
                est = query1.fetchone()
                query1.close()

                idest = est[0]

                query2 = db.connection.cursor()
                query2.execute(
                    "SELECT * FROM cuenta WHERE Estudiante_idEstudiante='{0}'".format(idest))
                acc = query2.fetchone()
                query2.close()

                saldo = int(acc[2])

                valortotal = int(valor) + saldo

                if valortotal < 50:

                    insert = db.connection.cursor()
                    insert.execute(
                        "UPDATE cuenta SET Saldo=%s WHERE Estudiante_idEstudiante=%s", (valortotal, idest))
                    db.connection.commit()

                    return redirect('/recarga')

                else:

                    return redirect('/recarga')

            else:

                print("Los campos no coinciden")
                return redirect("/recarga")

        else:

            print("Este Usuario no está registrado")

            return render_template("recarga.html")
    else:

        return render_template('recarga.html')


@app.route('/registro_estudiante', methods=['GET', 'POST'])
def registro_estudiante():

    if request.method == 'GET':
        return render_template("registro_estudiante.html")

    else:

        tipo = request.form['tipodocumento']
        nom1 = request.form['primernombre']
        numdoc = request.form['ndocumento']
        nom2 = request.form['segundonombre']
        ape1 = request.form['primerapellido']
        ape2 = request.form['segundoapellido']
        numtel = request.form['ntelefono']
        email = request.form['email']

        cur = db.connection.cursor()
        cur.execute("INSERT INTO persona (N_Documento, Tipo_Documento, Primer_Nombre, Segundo_Nombre, Primer_Apellido, Segundo_Apellido, Correo, Celular) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (numdoc, tipo, nom1, nom2, ape1, ape2, email, numtel))
        db.connection.commit()

        cur = db.connection.cursor()
        cur.execute(
            "INSERT INTO estudiante (Persona_ID) VALUES ((SELECT MAX(Id) FROM persona))")
        db.connection.commit()

        return redirect('/operador/inicio')


@app.route('/actualizar_estudiante', methods=['GET','POST'])
def actualizar_estudiante():

        if request.method == 'GET':
            return render_template('actualizar_estudiante.html')

        else:

            tipo = request.form['tipodocumento']
            numdoc = request.form['ndocumento']
            nom1 = request.form['primernombre']
            nom2 = request.form['segundonombre']
            ape1 = request.form['primerapellido']
            ape2 = request.form['segundoapellido']
            numtel = request.form['ntelefono']
            email = request.form['email']

            cur = db.connection.cursor()
            cur.execute("UPDATE persona SET N_Documento = %s, Tipo_Documento = %s, Primer_Nombre = %s, Segundo_Nombre   = %s, Primer_Apellido = %s, Segundo_Apellido = %s, Correo = %s, Celular = %s WHERE N_Documento = %s",
                        (int(numdoc), tipo, nom1, nom2, ape1, ape2, email, int(numtel), int(numdoc)))
            db.connection.commit()

            print("funcionando")

            return redirect('/actualizar_estudiante')


@app.route('/buscar_estudiante', methods=['GET', 'POST'])
def buscar_estudiante():
    if request.method == 'POST':
        return redirect('/actualizar_estudiante')
    else:
        return render_template("buscar.html")


# ///////////////////////////////////////rutas comunes/////////////////////////////

if __name__ == '__main__':
    app.secret_key = "thisappissafe"
    app.run(debug=True)
