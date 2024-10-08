from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime

class Usuario(UserMixin):
    def __init__(self,usuario:dict):
        self.nombre = usuario['nombre']
        self.correo = usuario['correo']
        self.contraseña = usuario['contraseña']
        self.rol = usuario['rol']
        self.foto = 'https://via.placeholder.com/150'
        self.fechaRegistro = datetime.datetime.now()
        
    def set_password(self, password):
        self.contraseña = generate_password_hash(password)
        return self.contraseña

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.correo)
    
    

        