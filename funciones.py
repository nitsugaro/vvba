import db.usuarios
import db.movimientos
import validaciones, utilidades, random

def iniciarSesion():
    while True: 
        usuario = input("Ingrese su nombre de usuario: ")
        clave = input("Ingrese su contraseña: ")
                
        indiceUsuario = db.usuarios.obtenerIndexUsuario(usuario)

        if indiceUsuario != -1 and db.usuarios.verificarClave(indiceUsuario, clave):
            return indiceUsuario

        print("Usuario o Contraseña incorrecta")

def crearUsuario():
    '''
        Pide los inputs necesarios para crear un usuario y clave, inicializando a su vez la matriz de movimientos.
    '''

    nombreUsuario = input("Cree un nombre de usuario: ")

    #Todo se puede hacer que valide el valor del nombre y que no exista previamente en una sola función
    nombreUsuario = validaciones.validarNombreExiste(nombreUsuario)
    nombreUsuario = validaciones.validarNuevoUsuario(nombreUsuario)

    contraseñaUsuario = input("Cree una contraseña (Mayor a 5 caracteres y con almenos un digito): ")
    contraseñaUsuario = validaciones.validarContraseña(contraseñaUsuario)

    db.usuarios.crearUsuarioClave(nombreUsuario, contraseñaUsuario)
    db.movimientos.crearMovimientos()

    input("Usuario creado con éxito. Presione enter para continuar ... ")
    
def menuInicio():    
    return utilidades.elegirOpcion("Elegi una opcion: ", ["Iniciar Sesión", "Crear Usuario", "Listar Usuarios"])

def menuPrincipal(intId):
    while True:
        saldoPesos = calcularSaldo(db.movimientos.MOVIMIENTOS, intId, 0)
        saldoDolares = calcularSaldo(db.movimientos.MOVIMIENTOS, intId, 1)

        return utilidades.elegirOpcion(
            "Elegí una opción: ", 
            ["Realizar operación", "Ver movimientos", "Creditos", "Plazo fijo", "Compra/Venta Dolar", "Gastos por clasificacion", "Salir"],
            f"Bienvenido/a {db.usuarios.obtenerNombreUsuario(intId)} al Banco VVBA (Vanguardia Virtual del Banco Argentino)\nSaldo pesos: {saldoPesos}$ y Saldo dolares: ${saldoDolares}: "
        )
        
def calcularSaldo(matrizMovimientos, intId, intPesosODolares):
    saldo = 0

    for i in matrizMovimientos[intId][intPesosODolares]:
        saldo += i

    return round(saldo, 2)

def realizarOperacion(intId):
    try: 
        monto = float(input("Ingrese la cantidad de dinero: "))
        tipoOpIndice = utilidades.elegirOpcion("Elegí el tipo de operacion: ", db.movimientos.TIPOS_OPERACIONES)

        if db.movimientos.TIPOS_OPERACIONES[tipoOpIndice] != "Deposito":
            monto *= -1

        db.movimientos.operacionMonto(intId, monto, db.movimientos.TIPOS_OPERACIONES[tipoOpIndice])
    except ValueError:
        print("Error. Ingrese un numero")

def verMovimientos(intId):
    movimientosPrev = 5
    inicio = len(db.movimientos.MOVIMIENTOS[intId][0]) - movimientosPrev

    if inicio < 0:
        inicio = 0

    for i in range(inicio, len(db.movimientos.MOVIMIENTOS[intId][0])):
        print(f"Monto {db.movimientos.MOVIMIENTOS[intId][0][i]} corresponde al tipo de gasto: {db.movimientos.MOVIMIENTOS[intId][4][i]}")

    input("Presione enter para continuar ... ")

def creditos():
    pass

def plazoFijo():
    pass

def compraVentaDolar(indiceUsuario):
    compraDolar = round(random.uniform(1300, 2000), 2)
    ventaDolar = round(compraDolar + random.uniform(25, 50), 2)

    saldo = calcularSaldo(db.movimientos.MOVIMIENTOS, indiceUsuario, 0)
    saldoDolar = calcularSaldo(db.movimientos.MOVIMIENTOS, indiceUsuario, 1)

    compraOVenta = utilidades.elegirOpcion(
        "¿Qué desea hacer? ", 
        ["Comprar", "Vender", "Salir"], 
        f"La cotizacion del dolar para comprar es ${compraDolar} y para vender es ${ventaDolar}."
    )

    if compraOVenta == 0:
        montoDolar = float(input("Cuantos dolares quiere comprar: "))
        montoDolar = validaciones.validarMontoPositivo(montoDolar)

        montoPesos = montoDolar * compraDolar
        
        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()
        if siONo == "S":
            validaciones.validarTransaccion(
                db.movimientos.MOVIMIENTOS, 
                indiceUsuario, 
                montoOrigen=montoPesos, 
                montoDestino=montoDolar, 
                saldoOrigen=saldo, 
                indiceDestino=db.movimientos.INDICE_DOLAR, 
                indiceOrigen=db.movimientos.INDICE_PESOS
            )
    elif compraOVenta == 1:
        montoDolar = float(input("Cuantos dolares quiere vender: "))
        montoDolar = validaciones.validarMontoPositivo(montoDolar)

        montoPesos = montoDolar * ventaDolar

        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()
        if siONo == "S":
            validaciones.validarTransaccion(
                db.movimientos.MOVIMIENTOS, 
                indiceUsuario, 
                montoOrigen=montoDolar, 
                montoDestino=montoPesos, 
                saldoOrigen=saldoDolar, 
                indiceDestino=db.movimientos.INDICE_PESOS, 
                indiceOrigen=db.movimientos.INDICE_DOLAR
            )

def gastosClasificacion(intId, lstCategoria):
    saldo = 0
    movimientos = db.movimientos.MOVIMIENTOS[intId][0]  
    categorias = db.movimientos.MOVIMIENTOS[intId][4]

    for i in range(len(categorias)):
        for j in range(len(lstCategoria)):
            if categorias[i] == lstCategoria[j]:
                saldo += movimientos[i]
        print(f"{categorias[i]}: {saldo}")
        saldo = 0
    input("Presione enter para continuar ... ")

def listarUsuario():
    partNombre = input("Buscar: ")
    usuarios = db.usuarios.obtenerUsuarios()
    usuariosFiltro = [nombre for nombre in usuarios if nombre.lower().startswith(partNombre.lower()) ]

    if usuariosFiltro:
        print("Usuarios encontrados")
        for nombre in usuariosFiltro:
            print(nombre)
        input("Presione enter para continuar...")
    else:
        print("No se encontraron usuarios")
        input("Presione enter para continuar...")

def salir():
    pass