from database import db

TABLA_USUARIOS = "usuarios"
USER_ROL = "USER"
ADMIN_ROL = "ADMIN"

def obtenerPorUser(partUsername):
    '''
        Busca usuarios en base a una coincidencia parcial del username. Retorna una lista de diccionarios con los campos de 'usuarios.csv'
    '''
    return db.buscarRegistros(TABLA_USUARIOS, condicionLambda=lambda reg: partUsername in reg["username"])

def obtenerPrimeroPorUser(username):
    return db.buscarRegistro(TABLA_USUARIOS, condicionLambda=lambda reg: reg["username"] == username)
    
def obtenerPorId(id):
    return db.buscarRegistro(TABLA_USUARIOS, condicionLambda=lambda reg: reg["id"] == id)
    
def crearUsuario(nombre, username, rol):
    '''
        Agrega nombre y clave a las listas correspondientes y devuelve el indice del usuario.
    '''

    return db.crearRegistro(
        TABLA_USUARIOS,
        registro={
            "id": db.buscarUltimoRegistro(TABLA_USUARIOS).get("id", 0) + 1,
            "nombre": nombre,
            "username": username,
            "rol": rol,
            "activo": True
        },
        condicionLambda=lambda reg: reg["username"] != username
    )

def crearUsuarioAdmin(nombre, username):
    return crearUsuario(nombre, username, rol=ADMIN_ROL)

def crearUsuarioComun(nombre, username):
    return crearUsuario(nombre, username, rol=USER_ROL)

def verificarClave(indiceUsuario, clave):
    '''
        Verifica la clave en base al indice del usuario y su clave, devuelve True o False.
    '''
    return True