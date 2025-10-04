import db
import db.movimientos
import db.usuarios

def validarNombreExiste(strUsuario):
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

def validarMontoPositivo(floatNum):
    while floatNum <= 0:
        print("Error. Ingrese un monto mayor a 1.")

        floatNum = float(input("Ingrese la cantidad que desea depositar: "))
    
    return floatNum

def validarTransaccion(matrizMovimientos, indiceUsuario, montoOrigen, montoDestino, saldoOrigen, indiceDestino, indiceOrigen):
    '''
        Utiliza la matriz de movimientos y los siguientes parámetros para hacer una venta o compra de la divisa designada y guardarlo de manera correspondiente en base a sus indices.
    '''

    if montoOrigen > saldoOrigen:
        input("Error. No tiene el saldo suficiente para realizar la operacion. Presione enter para continuar ... ")
    else:
        matrizMovimientos[indiceUsuario][indiceDestino].append(montoDestino)
        matrizMovimientos[indiceUsuario][indiceOrigen].append(-montoOrigen)
        matrizMovimientos[indiceUsuario][db.movimientos.INDICE_TIPO_OPERACION].append("Deposito")

        input("Operacion realizada con exito. Presione enter para continuar ... ")

def validarNuevoUsuario(strUsuario):
    '''
        Verifica que el nombre proporcionado no esté vacío o tenga caracteres especiales.
    '''

    while True:
        if not strUsuario.isalnum():
            print("Error, el usuario no debe estar vacio y no debe tener espacios ni caracteres especiales")
            strUsuario = input("Ingrese otro usuario: ")
        else:
            break
    return strUsuario