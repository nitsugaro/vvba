import db.movimientos
import funciones, utilidades

def main():
    while True:
        utilidades.limpiarConsola()
        opcionPrincipal = funciones.menuInicio()
        
        utilidades.limpiarConsola()
        if opcionPrincipal == 0:
            numeroUsuario = funciones.iniciarSesion()
            break
        elif opcionPrincipal == 1:
            funciones.crearUsuario()
        else:
            funciones.listarUsuario()

    utilidades.limpiarConsola()
    opciones = [
        lambda: funciones.realizarOperacion(numeroUsuario), # Opcion 1
        lambda: funciones.verMovimientos(numeroUsuario), # Opcion 2
        lambda: funciones.creditos(), # Opcion 3
        lambda: funciones.plazoFijo(), # Opcion 4
        lambda: funciones.compraVentaDolar(numeroUsuario), # Opcion 5
        lambda: funciones.gastosClasificacion(numeroUsuario, db.movimientos.TIPOS_OPERACIONES), # Opcion 6
        lambda: funciones.salir() # Opcion 7
        ]

    opcion = 0

    largoOpciones = len(opciones) - 1

    while opcion != largoOpciones:
        opcion = funciones.menuPrincipal(numeroUsuario)
        utilidades.limpiarConsola()
        opciones[opcion]()
        utilidades.limpiarConsola()
    else:
        utilidades.limpiarConsola()
        print(f"Muchas gracias {funciones.usuario} por usar nuestro programa!")
        print("Saliendo, cerrando el programa...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utilidades.limpiarConsola()
        print("Saliendo, cerrando el programa...")