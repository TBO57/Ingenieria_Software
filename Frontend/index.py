from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import requests
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
        cur.execute("SELECT * FROM administrador WHERE Usuario='{0}'".format(usuario))
        user = cur.fetchone()
        cur.close()


        if user != None:
            if password == user[3]:

                idb = user[1];

                query = db.connection.cursor()
                query.execute("SELECT * FROM persona WHERE Id='{0}'".format(idb))
                person = query.fetchone()
                query.close()

                session['name'] = person[3]
                session['email'] = person[7]
                
                return redirect('/admin/inicio')

            else:

                print("Usuario o contraseña inválido")
                return render_template("/admin/login_admin.html")

        else:

            print("Este Admin no está registrado")
            
            return render_template("/admin/login_admin.html")
    else:
        
        return render_template('/admin/login_admin.html')


@app.route('/admin/inicio')
def inicio_admin():
    return render_template('/admin/inicioAdmin.html')


@app.route('/admin/registro_operador', methods=['GET', 'POST'])
def registro_operador():
    return render_template('/admin/registro_operador.html')


@app.route('/admin/reporte')
def reporte_admin():
    return render_template('/admin/reporte_ventas.html')

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
        cur.execute("SELECT * FROM operador WHERE Usuario='{0}'".format(usuario))
        user = cur.fetchone()
        cur.close()


        if user != None:
            if password == user[3]:

                idb = user[1];

                query = db.connection.cursor()
                query.execute("SELECT * FROM persona WHERE Id='{0}'".format(idb))
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


@app.route('/operador/reporte')
def interfaz_reporte():
    return render_template('/op/reporteFallos.html')

# @app.route('/admin/inicio')
# def inicio_admin():
#     return render_template('/admin/inicioAdmin.html')
#

# ///////////////////////////////////////rutas comunes/////////////////////////////

@app.route('/recarga')
def interfaz_recarga():

    if request.method == 'POST':
        ndocumento = request.form['Cuenta']
        # password = request.form['password']

        print(ndocumento)
        # print(password)

        cur = db.connection.cursor()
        cur.execute("SELECT * FROM persona WHERE N_Documento='{0}'".format(ndocumento))
        user = cur.fetchone()
        cur.close()


        if user != None:
            # if password == user[3]:

                idb = user[1];
                print(idb)

                # query = db.connection.cursor()
                # query.execute("SELECT * FROM persona WHERE Id='{0}'".format(idb))
                # person = query.fetchone()
                # query.close()

                # session['name'] = person[3]
                # session['email'] = person[7]

                url = 'http://127.0.0.1:5000/recarga'

                datos= {
                    'Ndocumento' : user[1],
                    'Nombre' : user[3],
                    'Apellido' : user[5]
                }

                headers = {
                    'User-Agent' : 'Mozilla/5.0',
                    'Agent-Version' : '1.0.0'

                }

                requests.post(url, data=datos, headers=headers)

                return render_template('recarga.html')

            # else:

            #     print("Usuario o contraseña inválido")
            #     return render_template("/op/login_operador.html")

        else:

            print("Este Usuario no está registrado")
            
            return render_template("/op/login_operador.html")
    else:
        
        return render_template('recarga.html')



    return render_template('recarga.html')


@app.route('/registro_estudiante', methods=['GET','POST'])
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
        cur.execute("INSERT INTO persona (N_Documento, Tipo_Documento, Primer_Nombre, Segundo_Nombre, Primer_Apellido, Segundo_Apellido, Correo, Celular) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (numdoc, tipo, nom1, nom2, ape1, ape2, email, numtel))
        db.connection.commit()

        cur = db.connection.cursor()
        cur.execute("INSERT INTO estudiante (Persona_ID) VALUES ((SELECT MAX(Id) FROM persona))")
        db.connection.commit()
        print("Funcionando")
        
        return redirect('/operador/inicio')


@app.route('/actualizar_estudiante')
def actualizar_estudiante():
    return render_template('actualizar_estudiante.html')

# ///////////////////////////////////////rutas comunes/////////////////////////////




if __name__ == '__main__':
    app.secret_key = "thisappissafe"
    app.run(debug=True)
