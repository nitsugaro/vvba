from database import usuarios
import menu, funciones, utilidades

def main():
    # Generar el token al iniciar sesion
    funciones.generarToken()
    
    while True:
        utilidades.limpiarConsola()
        usuario = funciones.iniciarSesion()

        utilidades.limpiarConsola()
        if usuario["rol"] == usuarios.USER_ROL:
            menu.usuario(usuario["id"])
        else:
            menu.admin(usuario["id"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utilidades.limpiarConsola()
        print("Saliendo, cerrando el programa...")
