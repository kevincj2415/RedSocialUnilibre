from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from Usuario import Usuario
from pymongo import MongoClient
import datetime
secionIniciada = False
nombre = ""
fotoPerfil = ""
idUsuario = 0
app = Flask(__name__)


cliente = MongoClient("mongodb+srv://kevincj2415:e2BhakVv76vBMD7f@cluster0.hb2dv.mongodb.net/")
app.db = cliente.redsocialuniversidadlibre
publicaciones = ''
publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]


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
    if secionIniciada:
        return render_template('sitio/inicio.html', publicaciones=publicaciones)
    else:
        return render_template('sitio/inicioSesion.html')


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
        global nombre
        global fotoPerfil
        global idUsuario
        idUsuario = usuario.id
        fotoPerfil = usuario.foto
        nombre = usuario.nombre
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

@app.route('/publicacion')
def publicarcion():
    return render_template('sitio/publicacion.html')

@app.route('/publicar', methods=['POST'])
def publicar():
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    imagen = request.form['imagen']
    categoria = request.form['categoria']
    autor = {"id":globals()['idUsuario'], "nombre":globals()['nombre'], "foto":globals()['fotoPerfil']}
    reacciones = {'likes':0, 'comentarios':0, 'compartidos':0}
    comentarios = []
    publicacion = {'titulo':titulo, 'contenido':contenido, 'imagen':imagen, 'categoria':categoria, 'fecha_publicacion':datetime.datetime.now(), 'reacciones':reacciones, 'autor':autor, 'comentarios':comentarios}
    app.db.publicaciones.insert_one(publicacion)
    return redirect('/inicio')

if __name__ == '__main__':
    app.run(debug=True)
    