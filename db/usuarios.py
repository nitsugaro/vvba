INDICE_USUARIO = 0
INDICE_CLAVES = 1

USUARIOSCLAVES = [
    ["Ana", "Luis", "María", "Carlos", "Castro"], # Nombre de usuario
    ["Pass123!", "Qwerty2025", "Segura#45", "Clave*89", "MiPass_77"] # Claves
]

def obtenerUsuarios():
    return USUARIOSCLAVES[INDICE_USUARIO]

def obtenerIndexUsuario(nombre):
    '''
        Obtiene el indice del usuario en base al nombre, si no lo encuentra devuelve -1.
    '''

    try:
        return USUARIOSCLAVES[INDICE_USUARIO].index(nombre)
    except ValueError:
        return -1
    
def obtenerNombreUsuario(indiceUsuario):
    return USUARIOSCLAVES[INDICE_USUARIO][indiceUsuario]
    
def crearUsuarioClave(nombre, clave):
    '''
        Agrega nombre y clave a las listas correspondientes y devuelve el indice del usuario.
    '''

    USUARIOSCLAVES[INDICE_USUARIO].append(nombre)
    USUARIOSCLAVES[INDICE_CLAVES].append(clave)
    return len(USUARIOSCLAVES[INDICE_USUARIO]) - 1

def verificarClave(indiceUsuario, clave):
    '''
        Verifica la clave en base al indice del usuario y su clave, devuelve True o False.
    '''
    return USUARIOSCLAVES[INDICE_CLAVES][indiceUsuario] == clave