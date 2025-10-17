import validaciones


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
        nombresCampos = arch.readline().strip().split(';')
        arch.seek(-2, 2)  # ir casi al final ej: 'hol<ACA>a\n'
        while arch.read(1) != b'\n':  # buscar el salto de línea anterior
            arch.seek(-2, 1)  # retroceder para leer el byte anterior
        linea = arch.readline().decode().strip()  # leer y decodificar la última línea

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
