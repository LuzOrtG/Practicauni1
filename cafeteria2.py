#Codigo toatalmente funcional 🌟

class Persona: 
    def __init__(self, nombre, identificacion):
        self.nombre = nombre
        self.identificacion = identificacion

class Cliente(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)
        self.historial_pedidos = []
        self.pedidos_realizados = 0  # Contador de pedidos

    def realizar_pedido(self, pedido):
        print(f"\n🛒 Pedido en curso: {pedido}")  # Mostrará "EN PREPARACIÓN"

        # Simular el cambio de estado hasta "ENTREGADO"
        while pedido.estado != "ENTREGADO":
            pedido.cambiar_estado()

        self.historial_pedidos.append(pedido)
        self.pedidos_realizados += 1  # Incrementar contador de pedidos

        print(f"\n✅ El pedido ha sido entregado y agregado al historial.")

    def consultar_historial(self):
        if not self.historial_pedidos:
            print(f"⚠️ El cliente {self.nombre} no tiene pedidos entregados.")
            return

        print(f"\n📜 Historial de pedidos de {self.nombre}:")
        for idx, pedido in enumerate(self.historial_pedidos, 1):
            print(f"\n📦 Pedido {idx}:")
            print(f"    🏷️ Estado: ✅ ENTREGADO")  # Forzamos "ENTREGADO" en el historial
            print(f"    🥤 Productos:")

            if not pedido.productos:
                print("    🚫 Este pedido no tiene productos.")
                continue

            for producto in pedido.productos:
                if isinstance(producto, Bebida):
                    personalizaciones = ", ".join(producto.personalizables) if producto.personalizables else "Sin personalización"
                    print(f"    - ☕ {producto.nombre} ({producto.tamaño}) - 💲{producto.precio}")
                    print(f"      ✨ Personalización: {personalizaciones}")
                else:
                    print(f"    - 🍰 {producto.nombre} - 💲{producto.precio}")

            print(f"\n    💵 Subtotal: ${pedido.subtotal:.2f}")
            print(f"    🎁 Descuento aplicado: ${pedido.descuento_aplicado:.2f}")
            print(f"    Total final: ${pedido.total:.2f}")

    def aplicar_descuento_fidelidad(self, pedido):
        if self.pedidos_realizados >= 1:  # Umbral para clientes frecuentes
            print(f"\n🌟¡Cliente frecuente detectado! Aplicando 10% de descuento.")
            pedido.descuento_aplicado += pedido.subtotal * 0.10
            pedido.calcular_total()

class Empleado(Persona):
    def __init__(self, nombre, identificacion, rol):
        super().__init__(nombre, identificacion)
        self.rol = rol

    def actualizar_inventario(self, inventario, ingrediente, cantidad):
        inventario.actualizar_stock(ingrediente, cantidad)
        print(f"Inventario actualizado por {self.nombre} ({self.rol}). {ingrediente}: {cantidad}")

class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Bebida(ProductoBase):
    PERSONALIZACIONES_VALIDAS = {"extra leche", "sin azúcar", "descafeinado"}

    def __init__(self, nombre, precio, tamaño, tipo, ingredientes_requeridos=None, personalizables=None):
        super().__init__(nombre, precio)
        self.tamaño = tamaño
        self.tipo = tipo
        self.ingredientes_requeridos = ingredientes_requeridos if ingredientes_requeridos else {}
        self.personalizables = personalizables if personalizables else []

    def agregar_personalizaciones(self, personalizacion):
        if personalizacion in self.PERSONALIZACIONES_VALIDAS:
            self.personalizables.append(personalizacion)
            print(f"La personalización ha sido añadida: {personalizacion}")
        else:
            print(f"Error: '{personalizacion}' no es una personalización válida.")

class Postre(ProductoBase):
    def __init__(self, nombre, precio, vegano, sin_gluten):
        super().__init__(nombre, precio)
        self.vegano = vegano
        self.sin_gluten = sin_gluten

class Inventario:
    def __init__(self):
        self.stock = {}

    def agregar_ingrediente(self, ingrediente, cantidad):
        self.stock[ingrediente] = self.stock.get(ingrediente, 0) + cantidad

    def verificar_stock(self, ingrediente, cantidad):
        return self.stock.get(ingrediente, 0) >= cantidad

    def actualizar_stock(self, ingrediente, cantidad):
        self.stock[ingrediente] = self.stock.get(ingrediente, 0) + cantidad

    def consumir_ingredientes(self, ingredientes_requeridos):
        for ingrediente, cantidad in ingredientes_requeridos.items():
            if not self.verificar_stock(ingrediente, cantidad):
                return False
        for ingrediente, cantidad in ingredientes_requeridos.items():
            self.stock[ingrediente] -= cantidad
        return True

class Pedido:
    ESTADOS = ["PENDIENTE", "EN PREPARACIÓN", "ENTREGADO"]

    def __init__(self, cliente, inventario):
        self.cliente = cliente
        self.inventario = inventario
        self.productos = []
        self.subtotal = 0
        self.total = 0
        self.descuento_aplicado = 0
        self.estado = self.ESTADOS[0]

    def __str__(self):
        return f"\n🛍️ Pedido de {self.cliente.nombre} \n📌 Estado: {self.estado} \n🥤 Productos: {', '.join([p.nombre for p in self.productos])} \n💰 Total: ${self.total:.2f}"

    def agregar_producto_con_inventario(self, producto):
        if isinstance(producto, Bebida) and not self.inventario.consumir_ingredientes(producto.ingredientes_requeridos):
            print(f"\n❌ Pedido rechazado: No hay suficientes ingredientes para {producto.nombre}.")
            return
        
        self.productos.append(producto)
        self.subtotal += producto.precio
        self.calcular_total()

    def calcular_total(self):
        self.total = self.subtotal - self.descuento_aplicado

    def cambiar_estado(self):
        estado_actual = self.ESTADOS.index(self.estado)
        if estado_actual < len(self.ESTADOS) - 1:
            self.estado = self.ESTADOS[estado_actual + 1]
            print(f"🔄 El estado del pedido ha cambiado a: {self.estado}")

class Promocion:
    def __init__(self, nombre, descuento):
        self.nombre = nombre
        self.descuento = descuento

    def aplicar_descuento(self, pedido):
        descuento_aplicado = pedido.subtotal * (self.descuento / 100)
        pedido.descuento_aplicado += descuento_aplicado
        pedido.calcular_total()
        print(f"\nPromoción '{self.nombre}' aplicada. Descuento: ${descuento_aplicado:.2f}.")


# --- Crear clientes y empleados ---
cliente1 = Cliente("Carlos Pérez", "12345678")
empleado1 = Empleado("María López", "97654321", "Barista")

# --- Crear inventario y agregar ingredientes ---
inventario = Inventario()
inventario.agregar_ingrediente("Café", 10)
inventario.agregar_ingrediente("Leche", 5)
inventario.agregar_ingrediente("Azúcar", 5)
inventario.agregar_ingrediente("Chocolate", 3)

# --- Crear productos ---
# Bebidas con ingredientes requeridos
cafe = Bebida("Café Americano", 3.50, "Grande", "Caliente", {"Café": 1})
capuchino = Bebida("Capuchino", 4.00, "Mediano", "Caliente", {"Café": 1, "Leche": 1})
chocolate_caliente = Bebida("Chocolate Caliente", 3.80, "Grande", "Caliente", {"Leche": 1, "Chocolate": 1})

# Postres
brownie = Postre("Brownie de Chocolate", 2.50, vegano=False, sin_gluten=False)
galleta = Postre("Galleta de Avena", 1.80, vegano=True, sin_gluten=True)

# --- Personalizar bebidas ---
capuchino.agregar_personalizaciones("extra leche")
capuchino.agregar_personalizaciones("sin azúcar")
cafe.agregar_personalizaciones("descafeinado")

# --- Crear pedido ---
pedido1 = Pedido(cliente1, inventario)

# --- Agregar productos al pedido con verificación de inventario ---
pedido1.agregar_producto_con_inventario(capuchino)  # Capuchino con extra leche y sin azúcar
pedido1.agregar_producto_con_inventario(cafe)  # Café descafeinado
pedido1.agregar_producto_con_inventario(brownie)  # Brownie

# --- Aplicar descuento de promoción ---
promo = Promocion("Descuento Bienvenida", 10)  # 10% de descuento
promo.aplicar_descuento(pedido1)

# --- Cliente realiza el pedido ---
cliente1.realizar_pedido(pedido1)

# --- Crear otro pedido para probar clientes frecuentes ---
pedido2 = Pedido(cliente1, inventario)
pedido2.agregar_producto_con_inventario(chocolate_caliente)
pedido2.agregar_producto_con_inventario(galleta)

# Aplicar descuento de cliente frecuente si aplica
cliente1.aplicar_descuento_fidelidad(pedido2)

# Cliente realiza otro pedido
cliente1.realizar_pedido(pedido2)

# --- Consultar historial de pedidos ---
cliente1.consultar_historial()

# --- Empleado actualiza inventario ---
empleado1.actualizar_inventario(inventario, "Café", 5)  # Agregar más café al stock
empleado1.actualizar_inventario(inventario, "Leche", 5)  # Agregar más leche al stock

# --- Crear cliente ---
cliente2 = Cliente("Luz Marisol", "55544433")

# --- Crear inventario con pocos ingredientes ---
inventario2 = Inventario()
inventario2.agregar_ingrediente("Café", 2)  # Solo hay 2 porciones de café
inventario2.agregar_ingrediente("Leche", 1)  # Solo hay 1 porción de leche

# --- Crear bebidas con ingredientes requeridos ---
capuchino2 = Bebida("Capuchino", 4.00, "Mediano", "Caliente", {"Café": 1, "Leche": 1})
latte = Bebida("Latte", 3.50, "Grande", "Caliente", {"Café": 1, "Leche": 2})  # Requiere más leche

# --- Crear pedido ---
pedido3 = Pedido(cliente2, inventario2)

# --- Intentar agregar productos al pedido ---
print("\nIntentando agregar Capuchino al pedido...")
pedido3.agregar_producto_con_inventario(capuchino2)  # Debería agregarse correctamente

print("\nIntentando agregar Latte al pedido...")
pedido3.agregar_producto_con_inventario(latte)  # Debería ser rechazado por falta de leche

# --- Cliente intenta realizar el pedido ---
cliente2.realizar_pedido(pedido3)

# --- Consultar historial de pedidos ---
cliente2.consultar_historial()