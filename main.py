from database import usuarios
import menu
import funciones, utilidades

def main():
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