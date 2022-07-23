from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/db_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# -------------------------------------------------


#Todo lo del modelo Persona -------------------------------------------------

#Creacion tabla Persona
class Persona(db.Model):

    Id = db.Column(db.Integer,primary_key=True)
    N_Documento = db.Column(db.Integer, unique=True)
    Tipo_Documento = db.Column(db.String(10))
    Primer_Nombre = db.Column(db.String(20))
    Segundo_Nombre = db.Column(db.String(20))
    Primer_Apellido = db.Column(db.String(20))
    Segundo_Apellido = db.Column(db.String(20))
    Correo = db.Column(db.String(250))
    Celular = db.Column(db.Integer)

    # OperadorAs = db.relationship("Operador", back_populates="persona", uselist=False)

    def __init__(self,N_Documento,Tipo_Documento,Primer_Nombre,Segundo_Nombre,Primer_Apellido,Segundo_Apellido,Correo,Celular):

        self.N_Documento = N_Documento
        self.Tipo_Documento = Tipo_Documento
        self.Primer_Nombre = Primer_Nombre
        self.Segundo_Nombre = Segundo_Nombre
        self.Primer_Apellido = Primer_Apellido
        self.Segundo_Apellido = Segundo_Apellido
        self.Correo = Correo
        self.Celular = Celular

db.create_all()

#Esquema Persona
class PersonaSchema(ma.Schema):
     class Meta:
        fields = ('Id','N_Documento','Tipo_Documento','Primer_Nombre','Segundo_Nombre','Primer_Apellido','Segundo_Apellido','Correo','Celular')
 
#Una respuesta
persona_schema = PersonaSchema()

#Varias respuestas
personas_schema = PersonaSchema(many=True)

#(Get) todas las personas
@app.route('/personas', methods=['GET'])
def get_personas():
    all_personas = Persona.query.all()
    result = personas_schema.dump(all_personas)
    return jsonify(result)

#(Get) una persona
@app.route('/persona/<id>', methods=['GET'])
def get_persona(id):
    persona = Persona.query.get(id)
    # print(persona.Correo)
    return persona_schema.jsonify(persona)

#(Post) persona
@app.route('/addpersona', methods=['POST'])
def add_persona():

    info = request.get_json(force=True)

    N_Documento = info['N_Documento']
    Tipo_Documento = info['Tipo_Documento']
    Primer_Nombre = info['Primer_Nombre']
    Segundo_Nombre = info['Segundo_Nombre']
    Primer_Apellido = info['Primer_Apellido']
    Segundo_Apellido = info['Segundo_Apellido']
    Correo = info['Correo']
    Celular = info['Celular']

    add_r = Persona(N_Documento,Tipo_Documento,Primer_Nombre,Segundo_Nombre,Primer_Apellido,Segundo_Apellido,Correo,Celular)

    db.session.add(add_r)
    db.session.commit()

    return persona_schema.jsonify(add_r)

#(Put) persona
@app.route('/updatepersona/<id>', methods=['PUT'])
def update_persona(id):

    persona = Persona.query.get(id)

    info = request.get_json(force=True)

    N_Documento = info['N_Documento']
    Tipo_Documento = info['Tipo_Documento']
    Primer_Nombre = info['Primer_Nombre']
    Segundo_Nombre = info['Segundo_Nombre']
    Primer_Apellido = info['Primer_Apellido']
    Segundo_Apellido = info['Segundo_Apellido']
    Correo = info['Correo']
    Celular = info['Celular']

    persona.N_Documento = N_Documento
    persona.Tipo_Documento = Tipo_Documento
    persona.Primer_Nombre= Primer_Nombre
    persona.Segundo_Nombre = Segundo_Nombre
    persona.Primer_Apellido = Primer_Apellido
    persona.Segundo_Apellido = Segundo_Apellido
    persona.Correo = Correo
    persona.Celular = Celular

    # update_r = Persona(N_Documento,Tipo_Documento,Primer_Nombre,Segundo_Nombre,Primer_Apellido,Segundo_Apellido,Correo,Celular)

    db.session.commit()

    return persona_schema.jsonify(persona)

#(Delete) una persona
@app.route('/deletepersona/<id>', methods=['DELETE'])
def delete_persona(id):

    persona = Persona.query.get(id)

    db.session.delete(persona)
    db.session.commit()

    return jsonify({ 'Result' : 'Usuario eliminado'})

#Tests ---

# #Get una persona 
# @app.route('/persona/<email>', methods=['GET'])
# def get_personaemail(email):
#     # print(email)
#     persona = dbsession.query(Persona).filter(Persona.Correo == email)
#     # print(persona.Id)
#     return persona_schema.jsonify(persona)

# -------------------------------------------------


#Todo lo del modelo Operador -------------------------------------------------

#Creacion tabla Operador
class Operador(db.Model):

    idOperador = db.Column(db.Integer,primary_key=True)
    Persona_Id = db.Column(db.Integer, db.ForeignKey('persona.Id'), nullable=False)
    Usuario = db.Column(db.String(50), nullable=False)
    Contrasena = db.Column(db.String(50))

    # persona = db.relationship("Persona", back_populates="OperadorAs")

    def __init__(self,Persona_Id,Usuario,Contrasena):

        self.Persona_Id = Persona_Id
        self.Usuario = Usuario
        self.Contrasena = Contrasena

db.create_all()

#Esquema Operador
class OperadorSchema(ma.Schema):
     class Meta:
        fields = ('idOperador','Persona_Id','Usuario','Contrasena')

#Una respuesta
operador_schema = OperadorSchema()

#Varias respuestas
operadores_schema = OperadorSchema(many=True)

# #Get info completa operador
# @app.route('/infoop/<id>', methods=['GET'])
# def get_operador(id):
#     operador = Operador.query.get(id)

#     relacion = Persona.query.get(operador.Persona_Id)

#     return persona_schema.jsonify(relacion)

#(Get) todos los operadores
@app.route('/operadores', methods=['GET'])
def get_operadores():
    all_op = Operador.query.all()
    result = operadores_schema.dump(all_op)
    return jsonify(result)

#(Get) un operador
@app.route('/operador/<id>', methods=['GET'])
def get_operador(id):
    operador = Operador.query.get(id)
    
    return operador_schema.jsonify(operador)

#(Get) un operador Email
@app.route('/operadoremail/<usuario>', methods=['GET'])
def get_operadoremail(usuario):
    operador = db.session.query(Operador).filter(Operador.Usuario == usuario).first()
    
    val = "";
                   #None = null
    if operador != None:
        print("funcionando")
        val = True;
        print(val)
    else:
        print("no joda")
        val = False;
        print(val)
    

    return operador_schema.jsonify(operador)
    # return jsonify(val)

#(Post) operador
@app.route('/addoperador', methods=['POST'])
def add_operador():

    info = request.get_json(force=True)

    Persona_Id = info['Persona_Id']
    Usuario = info['Usuario']
    Contrasena = info['Contrasena']
    
    add_o = Operador(Persona_Id,Usuario,Contrasena)

    db.session.add(add_o)
    db.session.commit()

    return operador_schema.jsonify(add_o)

#(Put) operador
@app.route('/updateoperador/<id>', methods=['PUT'])
def update_operador(id):

    operador = Operador.query.get(id)

    info = request.get_json(force=True)

    Usuario = info['Usuario']
    Contrasena = info['Contrasena']

    operador.Usuario = Usuario
    operador.Contrasena = Contrasena

    db.session.commit()
    
    return operador_schema.jsonify(operador)
    

#(Delete) operador
@app.route('/deleteoperador/<id>', methods=['DELETE'])
def delete_operador(id):

    operador = Operador.query.get(id)

    db.session.delete(operador)
    db.session.commit()

    return jsonify({ 'Result' : 'Operador eliminado'})

# -------------------------------------------------


#Todo lo del modelo Administrador -------------------------------------------------

#Creacion tabla Administrador
class Administrador(db.Model):

    idAdministrador = db.Column(db.Integer,primary_key=True)
    Persona_Id = db.Column(db.Integer, db.ForeignKey('persona.Id'))
    Usuario = db.Column(db.String(50))
    Contrasena = db.Column(db.String(50))

    def __init__(self,Persona_Id,Usuario,Contrasena):

        # self.idAdministrador = idAdministrador
        self.Persona_Id = Persona_Id
        self.Usuario = Usuario
        self.Contrasena = Contrasena

db.create_all()

#Esquema Administrador
class AdministradorSchema(ma.Schema):
     class Meta:
        fields = ('idAdministrador','Persona_Id','Usuario','Contrasena')

#Una respuesta
administrador_schema = AdministradorSchema()

#Varias respuestas
administradores_schema = AdministradorSchema(many=True)


#(Get) todos los administradores
@app.route('/admins', methods=['GET'])
def get_admins():
    all_adm = Administrador.query.all()
    result = administradores_schema.dump(all_adm)
    return jsonify(result)

#(Get) un administrador
@app.route('/admin/<id>', methods=['GET'])
def get_admin(id):
    administrador = Administrador.query.get(id)
    
    return administrador_schema.jsonify(administrador)

#(Post) administrador
@app.route('/addadmin', methods=['POST'])
def add_admin():

    info = request.get_json(force=True)

    Persona_Id = info['Persona_Id']
    Usuario = info['Usuario']
    Contrasena = info['Contrasena']
    
    add_a = Administrador(Persona_Id,Usuario,Contrasena)

    db.session.add(add_a)
    db.session.commit()

    return administrador_schema.jsonify(add_a)

#(Put) administrador
@app.route('/updateadmin/<id>', methods=['PUT'])
def update_admin(id):

    administrador = Administrador.query.get(id)

    info = request.get_json(force=True)

    Usuario = info['Usuario']
    Contrasena = info['Contrasena']

    administrador.Usuario = Usuario
    administrador.Contrasena = Contrasena

    db.session.commit()
    
    return administrador_schema.jsonify(administrador)
    

#(Delete) administrador
@app.route('/deleteadmin/<id>', methods=['DELETE'])
def delete_administrador(id):

    administrador = Administrador.query.get(id)

    db.session.delete(administrador)
    db.session.commit()

    return jsonify({ 'Result' : 'Administrador eliminado'})

# -------------------


#Todo lo del modelo Estudiante -------------------------------------------------

#Creacion tabla Estudiante
class Estudiante(db.Model):

    idEstudiante = db.Column(db.Integer,primary_key=True)
    Persona_Id = db.Column(db.Integer, db.ForeignKey('persona.Id'))

    def __init__(self,Persona_Id):

        self.Persona_Id = Persona_Id

db.create_all()

#Esquema Estudiante
class EstudianteSchema(ma.Schema):
     class Meta:
        fields = ('idEstudiante','Persona_Id')

#Una respuesta
estudiante_schema = EstudianteSchema()

#Varias respuestas
estudiantes_schema = EstudianteSchema(many=True)


#(Get) todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    all_est = Estudiante.query.all()
    result = estudiantes_schema.dump(all_est)
    return jsonify(result)

#(Get) un estudiante
@app.route('/est/<id>', methods=['GET'])
def get_estudiante(id):
    estudiante = Estudiante.query.get(id)
    
    return estudiante_schema.jsonify(estudiante)

#(Post) estudiante
@app.route('/addestudiante', methods=['POST'])
def add_estudiante():

    info = request.get_json(force=True)

    Persona_Id = info['Persona_Id']
    
    add_est = Estudiante(Persona_Id)

    db.session.add(add_est)
    db.session.commit()

    return estudiante_schema.jsonify(add_est)

#(Put) estudiante
@app.route('/updateestudiante/<id>', methods=['PUT'])
def update_estudiante(id):

    estudiante = Estudiante.query.get(id)

    info = request.get_json(force=True)

    Persona_Id = info['Persona_Id']

    estudiante.Persona_Id = Persona_Id
    
    db.session.commit()
    
    return estudiante_schema.jsonify(estudiante)
    

#(Delete) estudiante
@app.route('/deleteestudiante/<id>', methods=['DELETE'])
def delete_estudiante(id):

    estudiante = Estudiante.query.get(id)

    db.session.delete(estudiante)
    db.session.commit()

    return jsonify({ 'Result' : 'Estudiante eliminado'})

# -------------------


#Todo lo del modelo Cuenta -------------------------------------------------

#Creacion tabla Cuenta
class Cuenta(db.Model):

    Serial = db.Column(db.Integer,primary_key=True)
    Estudiante_idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante'))
    Saldo = db.Column(db.Float)
    

    def __init__(self,Estudiante_idEstudiante,Saldo):

        self.Estudiante_idEstudiante = Estudiante_idEstudiante
        self.Saldo = Saldo

db.create_all()

#Esquema Cuenta
class CuentaSchema(ma.Schema):
     class Meta:
        fields = ('Serial','Estudiante_idEstudiante','Saldo')

#Una respuesta
cuenta_schema = CuentaSchema()

#Varias respuestas
cuentas_schema = CuentaSchema(many=True)


#(Get) todas las cuentas
@app.route('/cuentas', methods=['GET'])
def get_cuentas():
    all_cut = Cuenta.query.all()
    result = cuentas_schema.dump(all_cut)
    return jsonify(result)

#(Get) una cuenta
@app.route('/cuenta/<id>', methods=['GET'])
def get_cuenta(id):
    cuenta = Cuenta.query.get(id)
    
    return cuenta_schema.jsonify(cuenta)

#(Post) cuenta
@app.route('/addcuenta', methods=['POST'])
def add_cuenta():

    info = request.get_json(force=True)

    Estudiante_idEstudiante = info['idEstudiante']
    Saldo = info['Saldo']
    
    add_cut = Cuenta(Estudiante_idEstudiante,Saldo)

    db.session.add(add_cut)
    db.session.commit()

    return cuenta_schema.jsonify(add_cut)

#(Put) cuenta
@app.route('/updatecuenta/<id>', methods=['PUT'])
def update_cuenta(id):

    cuenta = Cuenta.query.get(id)

    info = request.get_json(force=True)

    Estudiante_idEstudiante = info['idEstudiante']
    Saldo = info['Saldo']

    cuenta.Estudiante_idEstudiante = Estudiante_idEstudiante
    cuenta.Saldo = Saldo

    db.session.commit()
    
    return cuenta_schema.jsonify(cuenta)
    

#(Delete) cuenta
@app.route('/deletecuenta/<id>', methods=['DELETE'])
def delete_cuenta(id):

    cuenta = Cuenta.query.get(id)

    db.session.delete(cuenta)
    db.session.commit()

    return jsonify({ 'Result' : 'Cuenta eliminada'})

# -------------------


#Todo lo del modelo Transferencia -------------------------------------------------

#Creacion tabla Transferencia
class Transferencia(db.Model):

    idTransferencia = db.Column(db.Integer,primary_key=True)
    Cuenta_Serial = db.Column(db.Integer, db.ForeignKey('cuenta.Serial'))
    Fecha = db.Column(db.Date)
    Valor = db.Column(db.Float)

    def __init__(self,Cuenta_Serial,Fecha,Valor):

        self.Cuenta_Serial = Cuenta_Serial
        self.Fecha = Fecha
        self.Valor = Valor

db.create_all()

#Esquema Transferencia
class TransferenciaSchema(ma.Schema):
     class Meta:
        fields = ('idTransferencia','Cuenta_Serial','Fecha','Valor')

#Una respuesta
transferencia_schema = TransferenciaSchema()

#Varias respuestas
transferencias_schema = TransferenciaSchema(many=True)


#(Get) todas las transferencias
@app.route('/transferencias', methods=['GET'])
def get_transferencias():
    all_tfs = Transferencia.query.all()
    result = transferencias_schema.dump(all_tfs)
    return jsonify(result)

#(Get) una transferencia
@app.route('/tfs/<id>', methods=['GET'])
def get_transferencia(id):
    transferencia = Transferencia.query.get(id)
    
    return transferencia_schema.jsonify(transferencia)

#(Post) transferencia
@app.route('/addtfs', methods=['POST'])
def add_transferencia():

    info = request.get_json(force=True)

    Cuenta_Serial = info['Cuenta']
    Fecha = info['Fecha']
    Valor = info['Valor']

    add_tfs = Transferencia(Cuenta_Serial,Fecha,Valor)

    db.session.add(add_tfs)
    db.session.commit()

    return transferencia_schema.jsonify(add_tfs)

#(Put) transferencia
@app.route('/updatetfs/<id>', methods=['PUT'])
def update_transferencia(id):

    transferencia = Transferencia.query.get(id)

    info = request.get_json(force=True)

    Fecha = info['Fecha']
    Valor = info['Valor']

    transferencia.Fecha = Fecha
    transferencia.Valor = Valor

    db.session.commit()
    
    return transferencia_schema.jsonify(transferencia)
    

#(Delete) transferencia
@app.route('/deletetfs/<id>', methods=['DELETE'])
def delete_transferencia(id):

    transferencia = Transferencia.query.get(id)

    db.session.delete(transferencia)
    db.session.commit()

    return jsonify({ 'Result' : 'Transferencia eliminada'})

# -------------------


#Mensaje de bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'Mensaje' : 'Bienvenido :)'})

if __name__=="__main__":
    app.run(port = 7000, debug=True)
          # port = 6000,
  
