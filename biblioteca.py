#Codigo toatalmente funcional 🌟
from datetime import datetime, timedelta
class Material:
    def __init__(self, titulo, estado = "DISPONIBLE"):
        self.titulo = titulo
        self.estado = estado

class Libro(Material):
    def __init__(self, titulo, autor, genero, estado = "DISPONIBLE"):
        super().__init__(titulo, estado)
        self.autor = autor 
        self.genero = genero

class Revista(Material):
    def __init__(self, titulo, edicion, periodidad, estado = "DISPONIBLE"):
        super().__init__(titulo, estado)
        self.edicion = edicion 
        self.periodidad = periodidad

class MaterialDigital(Material):
    def __init__(self, titulo, tipo_archivo, enlace_descarga):
        super().__init__(titulo, estado = "DISPONIBLE")
        self.tipo_archivo = tipo_archivo 
        self.enlace_descarga = enlace_descarga

class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Usuario(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.materiales_prestados = []
        self.penalizaciones = 0

    def consultar_catalogo(self, catalogo):
        catalogo.mostrarCatalogo()

    def devolver_material(self, material):
        for prestamo in self.materiales_prestados:
            if prestamo.material == material:
                self.materiales_prestados.remove(prestamo)
                material.estado = "DISPONIBLE"

                #verificar si hay retraso en la devollucion 
                if datetime.now() > prestamo.fecha_devolucion:
                    Penalizacion.aplicar_penalizacion(self, prestamo)
                else:
                    print(f"{self.nombre} ha devuelto '{material.titulo}' a tiempo.\n")
                return
        print("Este material no fue prestado a este usuario.")
                #print(f"{material.titulo} ha sido devuelto por {self.nombre}")
                #return
        #print("Este material no fue prestado a este usuario.")

class Bibliotecario(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)

    def agregar_material(self, sucursal, material):
        sucursal.agregar_material(material)

    def gestion_prestamo(self, usuario, material, sucursal):#
        if material in sucursal.catalogo and material.estado == "DISPONIBLE":
            prestamo = Prestamo(usuario, material)
            usuario.materiales_prestados.append(prestamo)
            material.estado = "PRESTADO"
            print(f"\n'{material.titulo}' ha sido prestado a {usuario.nombre}\n")
            print(f"Fecha de préstamo: {prestamo.fecha_prestamo.strftime('%d-%m-%Y %H:%M:%S')}")
            print(f"Fecha de devolución esperada: {prestamo.fecha_devolucion.strftime('%d-%m-%Y %H:%M:%S')}\n")
        else:
            print("Lo sentimos, el material no esta disponible")


    def transferir_material(self, material, sucursal_origen, sucursal_final):#
        if material in sucursal_origen.catalogo:
            sucursal_origen.catalogo.remove(material)
            sucursal_final.agregar_material(material)
            print(f"{material.titulo} fue tranferiado a {sucursal_final.nombre}")

class Sucursal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []

    def agregar_material(self, material):
        self.catalogo.append(material)

    def mostrarCatalogo(self):
        print(f"\nCatalogo de la sucursal {self.nombre}:")
        for material in self.catalogo:
            print(f"📙 {material.titulo} ({material.estado})")

class Prestamo:
    def __init__(self, usuario, material):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = datetime.now()
        #se simula un retraso
        self.fecha_devolucion = self.fecha_prestamo - timedelta(days=2)

class Penalizacion:
    COSTO_POR_DIA = 10  # Costo de penalización por día de retraso

    @staticmethod
    def aplicar_penalizacion(usuario, prestamo):
        dias_retraso = (datetime.now() - prestamo.fecha_devolucion).days
        multa = dias_retraso * Penalizacion.COSTO_POR_DIA
        usuario.penalizaciones += 1
        print(f"{usuario.nombre} devolvió '{prestamo.material.titulo}' con retraso de {dias_retraso} días.")
        print(f"Fecha de devolución esperada: {prestamo.fecha_devolucion.strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"Fecha real de devolución: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"Se ha aplicado una multa de ${multa}. \nTotal de penalizaciones: {usuario.penalizaciones}\n")

class Catalogo:
    @staticmethod
    def buscar_material(sucursales, criterio, tipo_busqueda):
        print(f"Buscando material por {tipo_busqueda}: {criterio}")
        for sucursal in sucursales:
            for material in sucursal.catalogo:
                if tipo_busqueda == "titulo" and criterio.lower() in material.titulo.lower():
                    print(f"{material.titulo} disponible en {sucursal.nombre}")
                elif tipo_busqueda == "genero" and isinstance(material, Libro) and criterio.lower() in material.genero.lower():
                    print(f"{material.titulo} ({material.genero}) disponible en {sucursal.nombre}")


sucursal1 = Sucursal("Stuttgart Municipal Library")
sucursal2 = Sucursal("Biblioteca Joanina")
sucursal3 = Sucursal("Biblioteca Klementinum")

bibliotecario = Bibliotecario("Felipe")
usuario = Usuario("Luz Marisol Otiz Garcia")

libro = Libro("La materia de las sombras","Antonio Runa","Terror")
libro2 = Libro("Un legado de sangre","S.T. Gibson","Terror")
resvista = Revista("National Geographic","Edicion 2025","Mensual")
resvista2 = Revista("Vogue","Edicion 2025","Mensual")
digital = MaterialDigital("Alas de sangre","PDF","https://www.udocz.com/apuntes/665973/alas-de-sangre-rebecca-yarros")
digital2 = MaterialDigital("La grieta del silencio","PDF","https://es.scribd.com/document/745153770/La-Grieta-Del-Silencio-Javier-Castillo-Epub-Docer-ar")

bibliotecario.agregar_material(sucursal1, libro)
bibliotecario.agregar_material(sucursal1, resvista)
bibliotecario.agregar_material(sucursal2, libro2)
bibliotecario.agregar_material(sucursal2, digital)
bibliotecario.agregar_material(sucursal3, resvista2)
bibliotecario.agregar_material(sucursal3, digital2)

usuario.consultar_catalogo(sucursal1)
usuario.consultar_catalogo(sucursal2)
usuario.consultar_catalogo(sucursal2)

bibliotecario.gestion_prestamo(usuario, libro, sucursal1)
usuario.devolver_material(libro)
print(f"\n")
#La busqueda es por genero
Catalogo.buscar_material([sucursal1, sucursal2, sucursal3], "Terror", "genero")
print(f"\n")
bibliotecario.transferir_material(resvista, sucursal1, sucursal2)
print(f"\n")
#Catalogos actualizados
usuario.consultar_catalogo(sucursal1)

usuario.consultar_catalogo(sucursal2)

usuario.consultar_catalogo(sucursal3)