import color, utilidades, funciones
from database import movimientos, usuarios

def menuBasico(idUser, opciones, obtenerTexto: lambda: "Bienvenido a VVBA !"):
    opcion = 0
    while True:
        opcion = utilidades.elegirOpcion(
            "Elegí una opción: ", 
            list(map(lambda elemento: elemento["opcion"], opciones)), #tomamos los valores de los prompts
            obtenerTexto()
        )

        utilidades.limpiarConsola()
        opciones[opcion]["funcion"]()
        utilidades.limpiarConsola()
        if opcion == 6:
            break
        elif opcion == 7:
            return -1

def usuario(idUser):
    funciones.verificarVencimientosPlazoFijo(idUser)
    
    opciones = [
        { "opcion": "Realizar operación", "funcion": lambda: funciones.realizarOperacion(idUser) }, # 1
        { "opcion": "Ver movimientos", "funcion": lambda: funciones.verMovimientos(idUser) }, # 2
        { "opcion": "Créditos", "funcion": lambda: funciones.creditosF(idUser) }, # 3
        { "opcion": "Plazo fijo", "funcion": lambda: funciones.plazoFijo(idUser) }, # 4
        { "opcion": "Compra/Venta Dolar", "funcion": lambda: funciones.compraVentaDolar(idUser) }, # 5
        { "opcion": "Gastos por clasificacion", "funcion": lambda: funciones.gastosClasificacion(idUser) }, # 6
        { "opcion": "Cerrar Sesión", "funcion": lambda: funciones.saludoFin(idUser) }, # 7
        { "opcion": "Salir", "funcion": lambda: funciones.saludoFin(idUser) } # 8
    ]

    return menuBasico(
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
        { "opcion": "Ver logs", "funcion": lambda: menuLogs(idUser) }, # 3
        { "opcion": "Cerrar Sesión", "funcion": lambda: None } # 4
        # 4
    ]

    return menuBasico(
        idUser, 
        opciones, 
        lambda: f"Bienvenido/a {color.azul(usuarios.obtenerPorId(idUser)['username'])} al Banco VVBA (Vanguardia Virtual del Banco Argentino)\n"
    )

def menuLogs(idUser):
    opciones = [
        { "opcion": "Ver Movimientos", "funcion": lambda: funciones.verMovimientosAdmin()}, # 1
        { "opcion": "Buscar por id", "funcion": lambda: funciones.buscarMovimientosPorId() }, # 2
        { "opcion": "Cerrar Sesión", "funcion": lambda: None } # 3
    ]

    return menuBasico( idUser, 
        opciones, 
        lambda: f"Seleccione una de las siguientes opciones\n"
    )
