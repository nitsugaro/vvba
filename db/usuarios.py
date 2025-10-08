INDICE_USUARIO = 0
INDICE_CLAVES = 1

# Estructura principal: lista con dos listas internas
# - índice 0: lista de nombres de usuario
# - índice 1: lista de contraseñas (alineadas por índice con los usuarios)
USUARIOSCLAVES = [
    ["Ana", "Luis", "María", "Carlos", "Castro"], # Nombres de usuario
    ["Pass123!", "Qwerty2025", "Segura#45", "Clave*89", "MiPass_77"] # Claves (texto plano en esta versión)
]

# Conexiones: este módulo es usado por `funciones.py` para:
# - iniciar sesión (`iniciarSesion`) -> usa `obtenerIndexUsuario` y `verificarClave`
# - mostrar nombre en `menuPrincipal` -> usa `obtenerNombreUsuario`
# - crear un usuario -> usa `crearUsuarioClave`

def obtenerUsuarios():
    # Devuelve la lista de usuarios (nombres)
    return USUARIOSCLAVES[INDICE_USUARIO]

def obtenerIndexUsuario(nombre):
    # Retorna el índice del usuario por nombre o -1 si no existe
    try:
        return USUARIOSCLAVES[INDICE_USUARIO].index(nombre)
    except ValueError:
        return -1
    
def obtenerNombreUsuario(indiceUsuario):
    # Devuelve el nombre de usuario en base al índice
    return USUARIOSCLAVES[INDICE_USUARIO][indiceUsuario]
    
def crearUsuarioClave(nombre, clave):
    # Agrega un nuevo usuario y su clave
    USUARIOSCLAVES[INDICE_USUARIO].append(nombre)
    USUARIOSCLAVES[INDICE_CLAVES].append(clave)
    # Devuelve el índice del usuario recién creado
    return len(USUARIOSCLAVES[INDICE_USUARIO]) - 1

def verificarClave(indiceUsuario, clave):
    # Comprueba si la clave coincide para el índice de usuario dado
    return USUARIOSCLAVES[INDICE_CLAVES][indiceUsuario] == clave