import color
from database import movimientos, usuarios
import funciones
import utilidades

def menuBasico(idUser, opciones, obtenerTexto: lambda: "Bienvenido a VVBA !"):
    largoOpciones = len(opciones)
    opcion = 0
    while opcion != largoOpciones - 1:
        opcion = utilidades.elegirOpcion(
            "Elegí una opción: ", 
            list(map(lambda elemento: elemento["opcion"], opciones)), #tomamos los valores de los prompts
            obtenerTexto()
        )

        utilidades.limpiarConsola()
        opciones[opcion]["funcion"]()
        utilidades.limpiarConsola()
    else:
        utilidades.printPausa(f"Muchas gracias {color.azul(usuarios.obtenerPorId(idUser)["nombre"])} por usar nuestro programa!",pausa=0.01)
        input(color.negrita(color.gris("Presione enter para continuar...")))

def usuario(idUser):
    opciones = [
        { "opcion": "Realizar operación", "funcion": lambda: funciones.realizarOperacion(idUser) }, # 1
        { "opcion": "Ver movimientos", "funcion": lambda: funciones.verMovimientos(idUser) }, # 2
        { "opcion": "Créditos", "funcion": lambda: funciones.creditos() }, # 3
        { "opcion": "Plazo fijo", "funcion": lambda: funciones.plazoFijo() }, # 4
        { "opcion": "Compra/Venta Dolar", "funcion": lambda: funciones.compraVentaDolar(idUser) }, # 5
        { "opcion": "Gastos por clasificacion", "funcion": lambda: funciones.gastosClasificacion(idUser) }, # 6
        { "opcion": "Cerrar Sesión", "funcion": lambda: None } # 7
    ]

    menuBasico(
        idUser,
        opciones, 
        lambda: f"Bienvenido/a {color.azul(usuarios.obtenerPorId(idUser)['username'])} al Banco VVBA "
                f"(Vanguardia Virtual del Banco Argentino)\n"
                f"Saldo pesos: {movimientos.obtenerSaldoPesos(idUser)}$ y "
                f"Saldo dolares: ${movimientos.obtenerSaldoDolar(idUser)}"
    )

def admin(idUser):
    opciones = [
        { "opcion": "Listar Usuarios", "funcion": lambda: funciones.listarUsuario() }, # 1
        { "opcion": "Crear Nuevo Usuario", "funcion": lambda: funciones.crearUsuario() }, # 2
        { "opcion": "Cerrar Sesión", "funcion": lambda: None } # 3
    ]

    menuBasico(
        idUser, 
        opciones, 
        lambda: f"Bienvenido/a {color.azul(usuarios.obtenerPorId(idUser)['username'])} al Banco VVBA (Vanguardia Virtual del Banco Argentino)\n"
    )