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

    matrizMovimientos.append([[0], [], [], [0], []])
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

def menuPrincipal(lstOpciones, intId, matriz):
    while True:
        try:
            utilidades.limpiarConsola()
            print(f"Bienvenido/a {matriz[1][intId]} al banco\n" \
            "1. Consultar saldo \n2. Realizar transaccion \n3. Ver movimientos \n4. Creditos \n5. Plazo fijo \n6. Compra/Venta Dolar \n7. Gastos por clasificacion \n8. Salir")

            opcion = int(input("Elija una opción: "))
            opcion = validaciones.validarOpcionMenuPrincipal(opcion, lstOpciones)
        except ValueError: 
            print("Error. Ingrese un numero")
        else:
            utilidades.limpiarConsola()
            return opcion
        
def consultarSaldo(matrizMovimientos, intId):
    saldo = 0

    for i in matrizMovimientos[intId][0]:
        saldo += i

    print(f"Tu saldo es de {saldo}$.")

    input("Presione enter para continuar ... ")

def realizarTransaccion(matrizMovimientos, intId):
    try: 
        transaccion = float(input("Ingrese la cantidad de dinero: "))
        tipoGasto = input("Ingrese el tipo de gasto: ")

        matrizMovimientos[intId][0].append(transaccion)
        matrizMovimientos[intId][4].append(tipoGasto)
    except ValueError:
        print("Error. Ingrese un numero")

def verMovimientos(matrizMovimientos, intId):
    largo = len(matrizMovimientos[intId][0]) - 5

    if largo < 0:
        largo = 0

    for i in range(largo, len(matrizMovimientos[intId][0])):
        print(f"Gasto: {matrizMovimientos[intId][0][i]} corresponde al tipo de gasto: {matrizMovimientos[intId][4][i]}")

    input("Presione enter para continuar ... ")

def creditos():
    print("...")

def plazoFijo():
    print("...")

def compraVentaDolar(matrizMovimientos, intId):
    compraDolar = 1400
    ventaDolar = 1350
    saldoDolar = 0
    saldo = 0

    for i in matrizMovimientos[intId][0]:
        saldo += i

    for i in matrizMovimientos[intId][3]:
        saldoDolar += i

    print(f"Actualmente tiene {saldoDolar} dolares.")

    print(f"La cotizacion del dolar para comprar es {compraDolar} y para vender es {ventaDolar}.")

    compraOVenta = input("Que desea hacer? (Escriba compra, venta o cualquier letra para salir): ").lower().strip()

    if compraOVenta == "compra":
        montoDolar = float(input("Cuantos dolares quiere comprar: "))
        montoDolar = validaciones.validarNumeroPositivo(montoDolar)

        montoPesos = montoDolar * compraDolar
        
        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()

        if siONo == "S":
            validaciones.validarTransaccion(matrizMovimientos, intId, montoPesos, montoDolar, saldo, 3, 0)
    elif compraOVenta == "venta":
        montoDolar = float(input("Cuantos dolares quiere vender: "))
        montoDolar = validaciones.validarNumeroPositivo(montoDolar)

        montoPesos = montoDolar * ventaDolar

        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()

        if siONo == "S":
            validaciones.validarTransaccion(matrizMovimientos, intId, montoDolar, montoPesos, saldoDolar, 0, 3)

def gastosClasificacion():
    print("...")

def salir(matrizUsuario, intNum):
    print(f"Muchas Gracias {matrizUsuario[1][intNum]} por usar nuestro programa.")
