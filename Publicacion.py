class Publicacion:
    def __init__(self, publicacion):
        self.id = publicacion['id']
        self.titulo = publicacion['titulo']
        self.descripcion = publicacion['descripcion']
        self.fecha = publicacion['fecha']
        self.autor = publicacion['autor']
        self.foto = publicacion['foto']
        self.url = publicacion['url']
        self.categoria = publicacion['categoria']
        self.comentarios = publicacion['comentarios']
        self.likes = publicacion['likes']
        self.shares = publicacion['shares']

    def __repr__(self):
        return '<Publicacion %r>' % self.titulo 