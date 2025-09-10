import validaciones, utilidades

def iniciarSesion(matriz):
    while True: 
        usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")
        for i in range(len(matriz[0])):
            if matriz[1][i] == usuario and matriz[2][i] == contraseña:
                return i
        print("Usuario o Contraseña incorrecta")

def crearUsuario(matrizUsuarios, matrizMovimientos):
    nuevoId = len(matrizUsuarios[0])
    matrizUsuarios[0].append(nuevoId)

    nombreUsuario = input("Cree un nombre de usuario: ")
    validaciones.validarNombreUsuario(nombreUsuario, matrizUsuarios)

    contraseñaUsuario = input("Cree una contraseña (Mayor a 5 caracteres y con almenos un digito): ")
    validaciones.validarContraseña(contraseñaUsuario, matrizUsuarios)

    matrizMovimientos.append([[0], [0], [], [], []])
    # print(matrizUsuarios)
    # print(matrizMovimientos)
    input("Usuario creado con éxito. Presione enter para continuar ... ")
    
def menuInicio():
    while True:
        try: 
            print("1. Iniciar Sesion \n2. Crear Usuario")
            opcionSeleccionada = int(input("Elegi una opcion: "))
            opcionSeleccionada = validaciones.validarOpcionMenuInicio(opcionSeleccionada)
        except ValueError: 
            print("Error. Ingrese un numero")
        else:
            return opcionSeleccionada

def menuPrincipal(lstOpciones, intId, matrizUsuarios, matrizMovimientos):
    while True:
        try:
            saldoPesos = calcularSaldo(matrizMovimientos, intId, 0)
            saldoDolares = calcularSaldo(matrizMovimientos, intId, 1)

            utilidades.limpiarConsola()
            print(f"Bienvenido/a {matrizUsuarios[1][intId]} al banco\nSaldo pesos: {saldoPesos} y Saldo dolares: {saldoDolares}\n" \
            "1. Realizar transaccion \n2. Ver movimientos \n3. Creditos \n4. Plazo fijo \n5. Compra/Venta Dolar \n6. Gastos por clasificacion \n7. Salir")

            opcion = int(input("Elija una opción: "))
            opcion = validaciones.validarOpcionMenuPrincipal(opcion, lstOpciones)
        except ValueError: 
            print("Error. Ingrese un numero")
        else:
            utilidades.limpiarConsola()
            return opcion
        
def calcularSaldo(matrizMovimientos, intId, intPesosODolares):
    saldo = 0

    for i in matrizMovimientos[intId][intPesosODolares]:
        saldo += i

    return saldo

def realizarTransaccion(matrizMovimientos, intId):
    try: 
        transaccion = float(input("Ingrese la cantidad de dinero: "))
        tipoGasto = input("Ingrese el tipo de gasto: ")

        matrizMovimientos[intId][0].append(transaccion)
        matrizMovimientos[intId][4].append(tipoGasto)
    except ValueError:
        print("Error. Ingrese un numero")

def verMovimientos(matrizMovimientos, intId):
    inicio = len(matrizMovimientos[intId][0]) - 5

    if inicio < 0:
        inicio = 0

    for i in range(inicio, len(matrizMovimientos[intId][0])):
        print(f"Gasto: {matrizMovimientos[intId][0][i]} corresponde al tipo de gasto: {matrizMovimientos[intId][4][i]}")

    input("Presione enter para continuar ... ")

def creditos():
    print("...")

def plazoFijo():
    print("...")

def compraVentaDolar(matrizMovimientos, intId):
    compraDolar = 1400
    ventaDolar = 1350

    saldo = calcularSaldo(matrizMovimientos, intId, 0)
    saldoDolar = calcularSaldo(matrizMovimientos, intId, 1)

    print(f"La cotizacion del dolar para comprar es {compraDolar} y para vender es {ventaDolar}.")

    compraOVenta = input("Que desea hacer? (Escriba compra, venta o cualquier letra para salir): ").lower().strip()

    if compraOVenta == "compra":
        montoDolar = float(input("Cuantos dolares quiere comprar: "))
        montoDolar = validaciones.validarNumeroPositivo(montoDolar)

        montoPesos = montoDolar * compraDolar
        
        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()

        if siONo == "S":
            validaciones.validarTransaccion(matrizMovimientos, intId, montoPesos, montoDolar, saldo, 1, 0)
    elif compraOVenta == "venta":
        montoDolar = float(input("Cuantos dolares quiere vender: "))
        montoDolar = validaciones.validarNumeroPositivo(montoDolar)

        montoPesos = montoDolar * ventaDolar

        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()

        if siONo == "S":
            validaciones.validarTransaccion(matrizMovimientos, intId, montoDolar, montoPesos, saldoDolar, 0, 1)

def gastosClasificacion():
    print("...")

def salir(matrizUsuario, intNum):
    print(f"Muchas Gracias {matrizUsuario[1][intNum]} por usar nuestro programa.")
