import validaciones, utilidades

def iniciarSesion(matriz):
    utilidades.limpiarConsola()
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")
        for i in range(len(matriz[0])):
            if matriz[1][i] == usuario and matriz[2][i] == contraseña:
                return i
        print("Usuario o Contraseña incorrecta")

def crearUsuario(matrizUsuarios, matrizMovimientos):
    utilidades.limpiarConsola()
    while True:
        nuevoId = len(matrizUsuarios[0])
        matrizUsuarios[0].append(nuevoId)

        nombreUsuario = input("Cree un nombre de usuario: ")
        validaciones.validarNombreUsuario(nombreUsuario, matrizUsuarios)

        contraseñaUsuario = input("Cree una contraseña (Mayor a 5 caracteres y con almenos un digito): ")
        validaciones.validarContraseña(contraseñaUsuario, matrizUsuarios)

        matrizMovimientos.append([[0], [], [], [0], []])
        # print(matrizUsuarios)
        # print(matrizMovimientos)

        break

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

def menuPrincipal(lstOpciones, intNum, matriz):
    while True:
        try:
            utilidades.limpiarConsola()
            print(f"Bienvenido/a {matriz[1][intNum]} al banco\n" \
            "1. Consultar saldo \n2. Depositar dinero \n3. Movimientos \n4. Creditos \n5. Plazo fijo \n6. Compra/Venta Dolar \n7. Gastos por clasificacion \n8. Salir")

            opcion = int(input("Elija una opción: "))
            validaciones.validarOpcionMenuPrincipal(opcion, lstOpciones)
        except ValueError: 
            print("Error. Ingrese un numero")
        else:
            utilidades.limpiarConsola()
            return opcion
        
def consultarSaldo(matrizMovimientos, intNum):
    saldo = 0

    for i in matrizMovimientos[intNum][0]:
        saldo += i

    print(f"Tu saldo es de {saldo}$.")

    input("Presione enter para continuar ...")

def depositarDinero():
    print("...")

def movimientos():
    print("...")

def creditos():
    print("...")

def plazoFijo():
    print("...")

def compraVentaDolar():
    print("...")

def gastosClasificacion():
    print("...")

def salir(matrizUsuario, intNum):
    print(f"Muchas Gracias {matrizUsuario[1][intNum]} por usar nuestro programa.")
