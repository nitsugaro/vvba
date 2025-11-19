import validaciones
from datetime import datetime

def convertirLineaDict(linea, nombresCampos):
    '''
        Recibe una 'linea' como string y los 'nombresCampos' en una lista. Devuelve un dict referenciando key y value.
        Parsea campos que sean int, float o bool a su tipo en python.
    '''
    registro = {}
    valores = linea.strip().split(';')
    for campoIndex in range(len(nombresCampos)):
        campo = nombresCampos[campoIndex]
        valor: str = valores[campoIndex]
        if valor.lower() == "true":
            valor = True
        elif valor.lower() == "false":
            valor = False
        elif validaciones.esNumero(valor):
            try:
                valor = int(valor)
            except:
                #no debería explotar si es un numero
                valor = float(valor)

        registro[campo] = valor
        
    return registro

def buscarUltimoRegistro(nombreTabla):
    """
    - seek(offset, whence):
        offset: cuántos bytes moverse
        whence: desde dónde (0=inicio, 1=actual, 2=final)
    - Retrocedemos desde el final (-2, 2) para saltarnos el posible '\n' final.
    - Leemos byte a byte hacia atrás hasta encontrar '\n'.
    - Cuando lo encontramos, readline() nos da la última línea completa.
    """

    with open(nombreTabla + ".csv", "rb") as arch:
        lineas = arch.readlines()
        if len(lineas) == 0 or len(lineas) == 1:
            return None 

        nombresCampos = arch.readline().decode().strip().split(';')
        arch.seek(-2, 2)  # ir casi al final ej: 'hol<ACA>a\n'
        while arch.read(1) != b'\n':  # buscar el salto de línea anterior
            arch.seek(-2, 1)  # retroceder para leer el byte anterior
        linea = arch.readline().decode().strip()  # leer y decodificar la última línea

        if linea == "":
            return None

        return convertirLineaDict(linea, nombresCampos)

def buscarRegistros(nombreTabla, condicionLambda):
    try:
        registros = []
        with open(nombreTabla + ".csv", mode='r') as arch:
            nombresCampos = arch.readline().strip().split(';')

            for linea in arch:
                registroDict = convertirLineaDict(linea, nombresCampos)
                if condicionLambda(registroDict):
                    registros.append(registroDict)
        return registros
    except OSError as msg:
        print(f"ERROR abriendo el archivo: {msg}")

def buscarRegistro(nombreTabla, condicionLambda):
    '''
        Busca registro en el archivo usando 'idKey' como la columna que debe buscar e 'idValor' como el valor que debe encontrar.
        Devuelve un diccionario del registro encontrado o None
    '''
    try:
        with open(nombreTabla + ".csv", mode='r', encoding='utf-8') as arch:
            nombresCampos = arch.readline().strip().split(';')

            for linea in arch:
                registroDict = convertirLineaDict(linea, nombresCampos)
                if condicionLambda(registroDict):
                    return registroDict
    except OSError as msg:
        print(f"ERROR abriendo el archivo: {msg}")

def crearRegistro(nombreTabla, registro, condicionLambda):
    '''
        Crea un nuevo registro en el archivo, verificando el base al 'id' si se encuentra un registro almacenado. De no estarlo lo crea.
    '''

    if buscarRegistro(nombreTabla, lambda registro: not condicionLambda(registro)):
        print("ERROR el usuario ya se encuentra encontrado")
        return None
    try:
        with open(nombreTabla + ".csv", mode='a', encoding='utf-8') as arch:
            valores = ';'.join(map(str, dict.values(registro)))
            arch.write(f"{valores}\n")
    except OSError as msg:
        print(f"ERROR abriendo el archivo: {msg}")

def crearPlazoFijo(idUser, montoInvertido, porcentaje, plazoDias, estado):
    registro = {
        "idUser": idUser,
        "monto": montoInvertido,
        "porcentaje": porcentaje,
        "plazoDias": plazoDias,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "estado": estado
        }

    crearRegistro("plazoFijo", registro, condicionLambda=lambda r: True)

def buscarUltimoPF(idUser):
    plazosUsuario = buscarRegistros("plazoFijo", lambda r: int(r["idUsuario"]) == idUser)

    if plazosUsuario:
        ultimoPf = plazosUsuario[-1]
    else:
        ultimoPf = None

    if ultimoPf and int(ultimoPf["idUsuario"]) == idUser and ultimoPf["estado"] == "ACTIVO": 
        input("Ya tiene un plazo fijo activo. Debe esperar a que venza para crear uno nuevo ... ") 
        return ultimoPf
