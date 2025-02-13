#Codigo toatalmente funcional🌟
class Persona:
    lista = []

    def __init__(self, nombre, edad, correo):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo

    def registrar(self):
        Persona.lista.append(self)
        print(f"{self.nombre} ha sido registrada con el correo {self.correo}.")

    @classmethod
    def personas_registradas(cls):
        print("\n📋 Personas Registradas:")
        for persona in cls.lista:
            print(f"- {persona.nombre} - {persona.correo}")

class Usuario(Persona):
    def __init__(self, nombre, edad, correo):
        super().__init__(nombre, edad, correo)
        self.historial_reservas = []

    def hacer_reserva(self, funcion, asientos, promocion=None):
        if asientos > funcion.asientos_disponibles:
            print("❌ No hay suficientes asientos disponibles.")
            return

        descuento = promocion.descuento if promocion else 0
        precio_total = (asientos * 70) * ((100 - descuento) / 100)  

        funcion.asientos_disponibles -= asientos
        self.historial_reservas.append({"funcion": funcion, "asientos": asientos, "precio": precio_total})
        
        print(f"\n✅ Reserva exitosa: '{funcion.pelicula.titulo}' en sala {funcion.sala.nombre}.")
        print(f"Asientos: {asientos} | Precio Total: ${precio_total:.2f}")

    def cancelar_reserva(self, funcion):
        reserva = next((r for r in self.historial_reservas if r["funcion"] == funcion), None)
        if reserva:
            funcion.asientos_disponibles += reserva["asientos"]
            self.historial_reservas.remove(reserva)
            print(f"🔄 Reserva cancelada para '{funcion.pelicula.titulo}'.")
        else:
            print("❌ No tienes una reserva para esta función.")

class Empleado(Persona):
    def __init__(self, nombre, edad, correo, rol):
        super().__init__(nombre, edad, correo)
        self.rol = rol

    def agregar_funcion(self, funcion):
        print(f"\n🎬 Nueva función agregada: '{funcion.pelicula.titulo}' a las {funcion.hora} en la sala {funcion.sala.nombre}.")

    def modificar_promocion(self, promocion, nuevo_descuento, nuevas_condiciones):
        if self.rol in ["Taquillero", "Administrador"]:
            promocion.descuento = nuevo_descuento
            promocion.condiciones = nuevas_condiciones
            print(f"🔧 Promoción modificada: {promocion.descuento}% de descuento en {promocion.condiciones}.")
        else:
            print("❌ No tienes permisos para modificar promociones.")

class Espacio:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad

class Sala(Espacio):
    def __init__(self, nombre, capacidad, tipo_sala):
        super().__init__(nombre, capacidad)
        self.tipo_sala = tipo_sala  # 2D, 3D, IMAX
        self.asientos_disponibles = capacidad
    
    def mostrar_info(self):
        print(f"Sala {self.nombre} | Tipo: {self.tipo_sala} | Capacidad: {self.capacidad} asientos.")

class ZonaComida(Espacio):
    def __init__(self, nombre, capacidad, productos):
        super().__init__(nombre, capacidad)
        self.productos = productos 
    
    def mostrar_menu(self):
        print("\n🍿 Menú de la Zona de Comida:")
        for producto, precio in self.productos.items():
            print(f"{producto}: ${precio:.2f}")

    def vender_producto(self, producto, cantidad):
        if producto in self.productos:
            total = self.productos[producto] * cantidad
            print(f"🛒 Venta realizada: {cantidad}x {producto} | Total: ${total:.2f}")
        else:
            print("❌ Producto no disponible.")

class Pelicula:
    def __init__(self, titulo, genero, duracion, clasificacion):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion
        self.genero = genero

class Funcion:
    def __init__(self, pelicula, sala, hora):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora
        self.asientos_disponibles = sala.capacidad

    def mostrar_funcion(self):
        print(f"\n🎥 '{self.pelicula.titulo}' | Sala: {self.sala.nombre} | Hora: {self.hora} | Asientos disponibles: {self.asientos_disponibles}")

class Promocion:
    def __init__(self, descuento, condiciones):
        self.descuento = descuento
        self.condiciones = condiciones

    def mostrar(self):
        print(f"\n🎟️ Promoción: {self.descuento}% de descuento | Condiciones: {self.condiciones}")


#Crear usuarios y empleados
usuario1 = Usuario("Gabriel Gonzalez", 25, "GabrielG@gmail.com")
usuario2 = Usuario("Joshua Sanchez", 30, "JoshSan@gmail.com")
empleado1 = Empleado("Fernanda Ramírez", 40, "FerRamirez@cine.com", "Administrador")

usuario1.registrar()
usuario2.registrar()
empleado1.registrar()

#Películas
pelicula1 = Pelicula("Avatar 2", "Ciencia Ficción", 190, "PG-13")
pelicula2 = Pelicula("El conjuro", "Terror", 169, "R")

#Salas
sala1 = Sala("Sala IMAX", 50, "IMAX")
sala2 = Sala("Sala 3D", 30, "3D")

sala1.mostrar_info()
sala2.mostrar_info()

#Funciones
funcion1 = Funcion(pelicula1, sala1, "19:00")
funcion2 = Funcion(pelicula2, sala2, "21:00")

empleado1.agregar_funcion(funcion1)
empleado1.agregar_funcion(funcion2)

#Promociones
promo1 = Promocion(20, "Solo miercoles y sábado")
promo1.mostrar()

#Usuario hace una reserva con promoción
usuario1.hacer_reserva(funcion1, 3, promo1)


funcion1.mostrar_funcion()

#Intento de reservación de asientos ya ocupados
print("\n⚠️ Intento de reservar asientos ya ocupados:")
usuario2.hacer_reserva(funcion1, 48) 

#Cancelar reserva
usuario1.cancelar_reserva(funcion1)
funcion1.mostrar_funcion()

#Crear zona de comida y venta
zona_comida = ZonaComida("Snack Bar", 100, {"Palomitas": 5, "Refresco": 3})
zona_comida.mostrar_menu()
zona_comida.vender_producto("Palomitas", 2)

# Intento de comprar más productos de los disponibles
print("\n⚠️ Intento de comprar más productos de los disponibles:")
zona_comida.vender_producto("Palomitas", 10) 
