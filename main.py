import funciones, const, utilidades

def main():
    while True:
        utilidades.limpiarConsola()
        crearUsuaOIniciarSesion = funciones.menuInicio()
        
        if crearUsuaOIniciarSesion == 1:
            utilidades.limpiarConsola()
            numeroUsuario = funciones.iniciarSesion(const.USUARIOSCONTRASENAS)
            break
        else:
            utilidades.limpiarConsola()
            funciones.crearUsuario(const.USUARIOSCONTRASENAS, const.MOVIMIENTOS)

    utilidades.limpiarConsola()

    opciones = [
        lambda: funciones.realizarTransaccion(const.MOVIMIENTOS, numeroUsuario), # Opcion 1
        lambda: funciones.verMovimientos(const.MOVIMIENTOS, numeroUsuario), # Opcion 2
        lambda: funciones.creditos(), # Opcion 3
        lambda: funciones.plazoFijo(), # Opcion 4
        lambda: funciones.compraVentaDolar(const.MOVIMIENTOS, numeroUsuario), # Opcion 5
        lambda: funciones.gastosClasificacion(), # Opcion 6
        lambda: funciones.salir(const.USUARIOSCONTRASENAS, numeroUsuario) # Opcion 7
        ]

    opcion = 0

    while opcion != 7:
        opcion = funciones.menuPrincipal(opciones, numeroUsuario, const.USUARIOSCONTRASENAS, const.MOVIMIENTOS)
        opciones[opcion - 1]()
        

main()