import db
import db.usuarios

def validarNombreUsuario(strUsuario):
    while True: 
        if db.usuarios.obtenerIndexUsuario(strUsuario) != -1:
            strUsuario = input(f"El nombre de usuario {strUsuario} ya existe. Cree otro nombre de usuario: ")
        else: 
            break

    return strUsuario

def validarContraseña(strContraseña):
    while True:
        if len(strContraseña) < 5 or not any(i.isdigit() for i in strContraseña):
            print("La contraseña tiene que estar formada por almenos 5 caracteres y tener un numero.")
            strContraseña = input("Cree otra contraseña: ")
        else:
            break

    return strContraseña

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
