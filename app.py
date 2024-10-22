from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from Usuario import Usuario
from pymongo import MongoClient
from bson.objectid import ObjectId

import datetime
status = {'secionIniciada' : False,
    'nombre' : "",
    "correo" : "",
    "rol" : "",
    'fotoPerfil' : "",
    'idUsuario' : 0,
    }
publicaciones = ""
PubliPersonales = ""

app = Flask(__name__)

cliente = MongoClient("mongodb+srv://kevincj2415:e2BhakVv76vBMD7f@cluster0.hb2dv.mongodb.net/")
app.db = cliente.redsocialuniversidadlibre

publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]

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
    if status['secionIniciada']:
        return render_template('sitio/inicio.html', publicaciones=publicaciones, status=status, PubliPersonales=PubliPersonales)
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
        global status
        global PubliPersonales
        status['secionIniciada'] = True
        status['nombre'] = usuario.nombre
        status["correo"] = usuario.correo
        status['rol'] = usuario.rol
        status['fotoPerfil'] = usuario.foto
        status['idUsuario'] = usuario.pid
        PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
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
    global status
    status['secionIniciada'] = False
    return redirect('/')

@app.route('/perfil')
def perfil():
    return render_template('sitio/perfil.html', status=status, publiPersonales=PubliPersonales)

@app.route('/publicacion')
def publicarcion():
    return render_template('sitio/publicacion.html')

@app.route('/publicar', methods=['POST'])
def publicar():
    global PubliPersonales
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    imagen = request.form['imagen']
    categoria = request.form['categoria']
    autor = {"id":status['idUsuario'], "nombre":status['nombre'], "foto":status['fotoPerfil']}
    reacciones = {'likes':0, 'comentarios':0, 'compartidos':0, 'idLikes':[]}
    comentarios = []
    publicacion = {'titulo':titulo, 'contenido':contenido, 'imagen':imagen, 'categoria':categoria, 'fecha_publicacion':datetime.datetime.now(), 'reacciones':reacciones, 'autor':autor, 'comentarios':comentarios}
    app.db.publicaciones.insert_one(publicacion)
    publicaciones.append(publicacion)
    PubliPersonales = []
    PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
    return redirect('/inicio')


@app.route('/cambiarFoto')
def cambiarFoto():
    return render_template('sitio/cambiarFotoPerfil.html', status=status)

@app.route('/cambiarFotoPerfil', methods=['POST'])
def cambiarFotoPerfil():
    global publicaciones
    global PubliPersonales
    foto = request.form['foto']
    sql = "UPDATE usuario SET foto_perfil = %s WHERE id = %s"
    datos = (foto, status['idUsuario'])
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    for publicacion in app.db.publicaciones.find({'autor.id': status['idUsuario']}):
        id = publicacion['_id']
        ayuda = {'autor.foto': foto}
        app.db.publicaciones.update_one({'_id': ObjectId(id)}, {'$set': ayuda})
    status['fotoPerfil'] = foto
    publicaciones = []
    publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
    PubliPersonales = []
    PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
    return redirect('/perfil')

@app.route('/actualizar_usuario', methods=['POST'])
def actualizarUsuario():
    global publicaciones
    global PubliPersonales
    nombre = request.form['nombre']
    correo = request.form['correo']
    rol = request.form['rol']
    foto = request.form['foto_perfil']
    sql = "UPDATE usuario SET nombre = %s, correo = %s, rol = %s, foto_perfil = %s WHERE id = %s"
    datos = (nombre, correo, rol, foto, status['idUsuario'])
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    for publicacion in app.db.publicaciones.find({'autor.id': status['idUsuario']}):
        id = publicacion['_id']
        ayuda = {'autor.nombre': nombre, 'autor.foto': foto}
        app.db.publicaciones.update_one({'_id': ObjectId(id)}, {'$set': ayuda})
    status['nombre'] = nombre
    status['correo'] = correo
    status['rol'] = rol
    status['fotoPerfil'] = foto
    publicaciones = []
    publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
    PubliPersonales = []
    PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
    return redirect('/perfil')

@app.route('/editarPerfil')
def editarPerfil():
    return render_template('sitio/editraPerfil.html', status=status)

@app.route('/eliminarpublicacion/<id>', methods=['POST'])
def eliminarPublicacion(id):
    global PubliPersonales
    try:
        
        object_id = ObjectId(id)
        app.db.publicaciones.delete_one({'_id': object_id})

        publicaciones = []
        publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
        PubliPersonales = []
        PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]

    except Exception as e:
        print(f"Error al eliminar la publicación: {e}")
        return redirect('/error') 

    return render_template('sitio/inicio.html', publicaciones=publicaciones, status=status)

@app.route('/editarpublicacion', methods=['POST'])
def editarpublicacion():
    id = request.form['_id']
    publicacion = app.db.publicaciones.find_one({'_id': ObjectId(id)})
    return render_template('sitio/editarPublicacion.html', status=status, publicacion=publicacion)


@app.route('/editarPublicacion/<id>', methods=['POST'])
def editarPublicacion(id):
    global PubliPersonales
    global publicaciones
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    imagen = request.form['imagen']
    publicacion = {'titulo':titulo, 'contenido':contenido, 'imagen':imagen}
    app.db.publicaciones.update_one({'_id': ObjectId(id)}, {'$set': publicacion})
    publicaciones = []
    publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
    PubliPersonales = []
    PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
    return redirect('/inicio')


@app.route('/like', methods=['POST'])
def like():
    global publicaciones
    global PubliPersonales
    id = request.form['_id']
    idUsuario = request.form['idUsuario']
    likes = int(request.form['likes'])
    idlike = app.db.publicaciones.find_one({'_id': ObjectId(id)})
    likeslist = [likes for likes in idlike['reacciones']['idLikes']]
    for usuario in idlike['reacciones']['idLikes']:
        if  idUsuario == usuario:
            likes = likes - 1
            likeslist.remove(idUsuario)
            app.db.publicaciones.update_one({'_id': ObjectId(id)}, {'$set': {'reacciones.likes': likes, 'reacciones.idLikes': likeslist}})
            publicaciones = []
            publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
            PubliPersonales = []    
            PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
            return render_template('sitio/inicio.html', publicaciones=publicaciones, status=status, PubliPersonales=PubliPersonales)
    else:
        likes = likes + 1
        likeslist.append(idUsuario)
        app.db.publicaciones.update_one({'_id': ObjectId(id)}, {'$set': {'reacciones.likes': likes, 'reacciones.idLikes': likeslist}})
        publicaciones = []
        publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
        PubliPersonales = []    
        PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
        return render_template('sitio/inicio.html', publicaciones=publicaciones, status=status, PubliPersonales=PubliPersonales)    
    
@app.route('/verComentarios', methods=['POST'])
def verComentarios():
    id = request.form['_id']
    comentarios = []
    publicacion = app.db.publicaciones.find_one({'_id': ObjectId(id)})
    comentarios = [comentario for comentario in publicacion['comentarios']]
    return render_template('sitio/comentarios.html', comentarios=comentarios, publicacion = publicacion, status=status)

@app.route('/comentar', methods=['POST'])
def comentar():
    global publicaciones
    global PubliPersonales
    global status
    nombreAutor = request.form['nombreAutor']
    fotoAutor = request.form['fotoAutor']
    contenido= request.form['contenido']
    id = request.form['_id']
    publicacion = app.db.publicaciones.find_one({'_id': ObjectId(id)})
    comentarios = [comentario for comentario in publicacion['comentarios']]
    comentario = {'autor': {'nombre':nombreAutor, 'foto':fotoAutor}, 'contenido':contenido}
    comentarios.append(comentario)
    app.db.publicaciones.update_one({'_id': ObjectId(id)}, {'$set': {'comentarios': comentarios, 'reacciones.comentarios': len(comentarios)}})
    publicacion = app.db.publicaciones.find_one({'_id': ObjectId(id)})
    comentarios = [comentario for comentario in publicacion['comentarios']]
    publicaciones = []
    publicaciones = [publicacion for publicacion in app.db.publicaciones.find({})]
    PubliPersonales = []
    PubliPersonales = [publiPersonale for publiPersonale in app.db.publicaciones.find({ "autor.id": status['idUsuario'] })]
    return render_template('sitio/comentarios.html', comentarios=comentarios, publicacion = publicacion, status=status)

if __name__ == '__main__':
    app.run(debug=True)
    