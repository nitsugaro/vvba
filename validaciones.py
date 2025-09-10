
def validarOpcionMenuInicio(intNum):
    while intNum != 1 and intNum != 2:
        print("Error. Ingrese un 1 o un 2.")
        intNum = int(input("Ingrese 1 para iniciar sesion o 2 para crear un usuario: "))
    return intNum

def validarOpcionMenuPrincipal(intNum, lstOpciones):
    while 1 > intNum or intNum > len(lstOpciones):
        print("Error. Ingrese un numero correspondiente con las opciones.\n" \
        "1. Consultar saldo \n2. Depositar dinero \n3. Movimientos \n4. Creditos \n5. Plazo fijo \n6. Compra/Venta Dolar \n7. Gastos por clasificacion \n8. Salir")
        
        intNum = int(input("Elija una opción: "))
    return intNum

def validarNombreUsuario(strUsuario, matrizUsuario):
    while True: 
        if strUsuario in matrizUsuario[1]:
            strUsuario = input(f"El nombre de usuario {strUsuario} ya existe. Cree otro nombre de usuario: ")
        else:
            matrizUsuario[1].append(strUsuario)
            break

def validarContraseña(strContraseña, matrizUsuario):
    while True:
        if strContraseña in matrizUsuario[2]:
            strContraseña = input("Cree otra contraseña: ")
        elif len(strContraseña) < 5 or not any(i.isdigit() for i in strContraseña):
            print("La contraseña tiene que estar formada por almenos 5 caracteres y tener un numero.")
            strContraseña = input("Cree otra contraseña: ")
        else: 
            matrizUsuario[2].append(strContraseña)
            break

def validarNumeroPositivo(intNum):
    while intNum <= 0:
        print("Error. Ingrese un monto mayor a 1.")

        intNum = float(input("Ingrese la cantidad que desea depositar: "))
    
    return intNum

def validarTransaccion(matrizMovimientos, intId, floatMonto1, floatMonto2, floatSaldo, intNum1, intNum2):
    if floatMonto1 > floatSaldo:
        input("Error. No tiene el saldo suficiente para realizar la operacion. Presione enter para continuar ... ")
    else:
        matrizMovimientos[intId][intNum1].append(floatMonto2)
        matrizMovimientos[intId][intNum2].append(-floatMonto1)

        input("Operacion realizada con exito. Presione enter para continuar ... ")
