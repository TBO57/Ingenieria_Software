from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/operador')
def operador():
    return render_template('operador.html')

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
