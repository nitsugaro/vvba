from database import usuarios
import menu, funciones, utilidades, color

def main():
    while True:
        
        try:
            utilidades.limpiarConsola()
            usuario = funciones.iniciarSesion()

            utilidades.limpiarConsola()
            if usuario["rol"] == usuarios.USER_ROL:
                salir = menu.usuario(usuario["id"])
            else:
                menu.admin(usuario["id"])
            if salir == -1:
                break
        except KeyboardInterrupt:
            utilidades.limpiarConsola()
            exit = utilidades.validarInputs(
                tipo=str, 
                prompt="¿Esta seguro que desea interrumpir el programa? (S/N): ", 
                validador=lambda s: None if s.lower() == "s" or s.lower() == "n" else "Porfavor, ingrese un valor valido (S/N): "
            ).lower()
            if exit == "s":
                print(color.negrita(color.gris("Cerrando el programa...")))
                break

if __name__ == "__main__":
    main()