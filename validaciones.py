from database import movimientos

def validarContraseña(strContraseña):
    while True:
        if len(strContraseña) < 5 or not any(i.isdigit() for i in strContraseña):
            print("La contraseña tiene que estar formada por almenos 5 caracteres y tener un numero.")
            strContraseña = input("Cree otra contraseña: ")
        else:
            break

    return strContraseña

def validarConversion(idUser, montoOrigen, montoDestino, saldoOrigen, tipoMonedaDestino, tipoMonedaOrigen):
    '''
        Utiliza la matriz de movimientos y los siguientes parámetros para hacer una venta o compra de la divisa designada y guardarlo de manera correspondiente en base a sus indices.
    '''

    if montoOrigen > saldoOrigen:
        input("Error. No tiene el saldo suficiente para realizar la operacion. Presione enter para continuar... ")
    else:
        movimientos.realizarMovimiento(idUser, -montoOrigen, tipoMonedaOrigen, movimientos.VENTA_MONEDA)
        movimientos.realizarMovimiento(idUser, montoDestino, tipoMonedaDestino, movimientos.COMPRA_MONEDA)

        input("Operacion realizada con exito. Presione enter para continuar ... ")

def esNumero(cadena):
    #eliminamos todos los '-' y '.' para preguntar si es un digito.
    return cadena.replace("-", "", 1).replace(".", "", 1).isdigit()