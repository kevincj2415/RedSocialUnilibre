from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from Usuario import Usuario
import pymongo
import datetime
secionIniciada = False

app = Flask(__name__)
app.secret_key = 'secret'

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'redsocialuniversidadlibre'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

@app.route('/')
def index():
    return render_template('sitio/index.html')

@app.route('/registro')
def registro():
    return render_template('sitio/registro.html')

@app.route('/inicioSesion')
def inicioSesion():
    return render_template('sitio/inicioSesion.html')

@app.route('/inicio')
def inicio():
    return render_template('sitio/inicio.html')

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['email']
    password = request.form['password']
    sql = "SELECT * FROM usuario WHERE correo = %s"
    datos = (correo,)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    user = cursor.fetchone()
    conexion.commit()
    usuario = Usuario(user)
    if not usuario.check_password(password):
        return redirect('/inicioSesion')
    else:
        global secionIniciada
        secionIniciada = True
        return redirect('/inicio')
    
@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    correo = request.form['email']
    password = request.form['password']
    rol = request.form['role']
    foto = 'https://via.placeholder.com/150'
    fechaRegistro = datetime.datetime.now()
    usuario = {'nombre':nombre, 'correo':correo, 'contraseña':password, 'rol':rol, 'foto':'https://via.placeholder.com/150', 'fecha_registro':datetime.datetime.now()}
    usuario = Usuario(usuario)
    contraseña = usuario.set_password(password)
    sql = "INSERT INTO usuario (nombre, correo, contraseña, rol, foto_perfil, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (nombre, correo, contraseña, rol, foto, fechaRegistro)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/inicioSesion')

@app.route('/logout')
def logout():
    global secionIniciada
    secionIniciada = False
    return redirect('/')

@app.route('/perfil')
def perfil():
    return render_template('sitio/perfil.html')

if __name__ == '__main__':
    app.run(debug=True)
    