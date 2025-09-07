import funciones, const, utilidades

def main():
    crearUsuaOIniciarSesion = funciones.menuInicio()
    
    if crearUsuaOIniciarSesion == 1:
        numeroUsuario = funciones.iniciarSesion(const.USUARIOSCONTRASENAS)
    else:
        funciones.crearUsuario(const.USUARIOSCONTRASENAS, const.MOVIMIENTOS)
        input("Usuario creado con éxito. Ahora debe iniciar sesion. Presione enter para continuar ...")
        numeroUsuario = funciones.iniciarSesion(const.USUARIOSCONTRASENAS)

    utilidades.limpiarConsola()

    opciones = [
        lambda: funciones.consultarSaldo(const.MOVIMIENTOS, numeroUsuario), # Opcion 1
        lambda: funciones.depositarDinero(), # Opcion 2
        lambda: funciones.movimientos(), # Opcion 3
        lambda: funciones.creditos(), # Opcion 4
        lambda: funciones.plazoFijo(), # Opcion 5
        lambda: funciones.compraVentaDolar(), # Opcion 6
        lambda: funciones.gastosClasificacion(), # Opcion 7
        lambda: funciones.salir(const.USUARIOSCONTRASENAS, numeroUsuario) # Opcion 8
        ]

    opcion = 0

    while opcion != 8:
        opcion = funciones.menuPrincipal(opciones, numeroUsuario, const.USUARIOSCONTRASENAS)
        opciones[opcion - 1]()
        

main()