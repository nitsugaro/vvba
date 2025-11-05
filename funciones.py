import color, validaciones, utilidades, random
from database import usuarios, movimientos, db, creditos
from datetime import datetime

def iniciarSesion():
    banner = """
            ██╗   ██╗██╗   ██╗██████╗  █████╗ 
            ██║   ██║██║   ██║██╔══██╗██╔══██╗
            ██║   ██║██║   ██║██████╔╝███████║
            ╚██╗ ██╔╝╚██╗ ██╔╝██╔══██╗██╔══██║
             ╚████╔╝  ╚████╔╝ ██████╔╝██║  ██║
              ╚═══╝    ╚═══╝  ╚═════╝ ╚═╝  ╚═╝

          Vanguardia Virtual del Banco Argentino
    """

    print(color.azul(banner))
    while True: 
        usuario = input("Ingrese su nombre de usuario: ")
        clave = input("Ingrese su contraseña: ")
            
        usuarioEncontrado = usuarios.obtenerPrimeroPorUser(usuario)
        #usuarios.verificarClave(indiceUsuario, clave)
        if usuarioEncontrado:
            return usuarioEncontrado

        print("Usuario o Contraseña incorrecta. Intentelo nuevamente...")

def crearUsuario():
    '''
        Pide los inputs necesarios para crear un usuario y clave, inicializando a su vez la matriz de movimientos.
    '''
    username = utilidades.validarInputs(
        str, 
        "Ingrese un nombre de usuario: ", 
        validador=lambda username: 
            "El usuario no debe estar vacio y no debe tener espacios ni caracteres especiales: " 
            if not username.isalnum() 
            else f"El nombre de usuario {username} ya existe. Ingrese otro nombre de usuario: " 
            if usuarios.obtenerPrimeroPorUser(username) 
            else None
        )

    contraseñaUsuario = input("Cree una contraseña (Mayor a 5 caracteres y con almenos un digito): ")
    contraseñaUsuario = validaciones.validarContraseña(contraseñaUsuario)

    usuarios.crearUsuario(username, contraseñaUsuario)
    input("Usuario creado con éxito. Presione enter para continuar ... ")

def menuAdmin(idUser):
    return utilidades.elegirOpcion(
        "Elegí una opción: ", 
        ["Realizar operación", "Ver movimientos", "Creditos", "Plazo fijo", "Compra/Venta Dolar", "Gastos por clasificacion", "Salir", "Cerrar Sesion"],
        f"Bienvenido/a {usuarios.obtenerPorId(idUser)["username"]} al Banco VVBA (Vanguardia Virtual del Banco Argentino)\n: "
    )


def generarToken():
    #Genera el token apenas se inicia sesion y lo guarda en el archivo token.txt
    token = str(random.randint(1000, 9999))
    try:
        with open("token.txt", "w", encoding="utf-8") as tk:#W para que se actualice cada vez que se inicie sesion
            tk.write(token)
        print(f"Token generado y guardado en token.txt: {token}")
    except Exception as e:
        print(f"Error al guardar el token: {e}")

def tokenSeguridad(crear_token):
  #Valida si el token que se ingresa para compararlo con el guardado en token.txt
    try:
        with open("token.txt", "r", encoding="utf-8") as tk:
            token_guardado = tk.read().strip()
        return crear_token == token_guardado
    except Exception as e:
        print(f"Error al leer el token: {e}")
        return False

def realizarOperacion(idUsuario):
    crear_token=input("Ingrese el token de seguridad generado en el archivo token.txt: ")
    
    if not tokenSeguridad(crear_token):
        print("Token inválido. Operación cancelada.")
        return

    monto = utilidades.validarInputs(float, "Ingrese la cantidad de dinero: ", 
            validador=lambda monto: None if monto > 0 else "Ingrese un monto válido: "
    )
    tipoOpIndice = utilidades.elegirOpcion("Elegí el tipo de operacion: ", movimientos.TIPOS_OPERACIONES)

    if movimientos.TIPOS_OPERACIONES[tipoOpIndice] != movimientos.DEPOSITO:
        monto *= -1

    movimientos.realizarMovimiento(idUsuario, monto, movimientos.PESOS, movimientos.TIPOS_OPERACIONES[tipoOpIndice])

def verMovimientos(intId):
    movimientosPrev = 5
    movs = movimientos.obtenerMovimientos(intId)
    inicio = len(movs) - movimientosPrev

    if inicio < 0:
        inicio = 0

    for i in range(inicio, len(movs)):
        movimiento = movs[i]
        print(f"Monto {movimiento["monto"]} corresponde al tipo de gasto: {movimiento["tipoOperacion"]}")

    input("Presione enter para continuar ... ")

def creditosF(idUsuario):
    while True:
        utilidades.limpiarConsola()
        op = utilidades.elegirOpcion("Elegí una opción: ", [
            "Pedir un credito",
            "Mis creditos",
            #"Ver préstamo por ID",
            "Pagar",
            "Volver"
        ])

        if op == 0:
            utilidades.limpiarConsola()
            capital = utilidades.validarInputs(float, "Capital: ", lambda v: None if v>0 else "Debe ser > 0")
            tasa    = utilidades.validarInputs(float, "Tasa mensual (0.04=4%): ", lambda v: None if v>=0 else "No puede ser negativa")
            meses   = utilidades.validarInputs(int,   "Plazo en meses: ", lambda v: None if v>0 else "Debe ser > 0")
            pid = creditos.crearCredito(idUsuario, capital, tasa, meses, acreditarEnCuenta=True)
            input(f"Credito creado ID {pid}. Enter...")

        elif op == 1:
            creditosL = creditos.listarPorUsuario(idUsuario)
            if not creditosL:
                utilidades.limpiarConsola()
                print("No tenes creditos registrados...")
                print("Enter para volver al menu de creditos...")
            else:
                utilidades.limpiarConsola()
                for r in creditosL:
                    print(f'ID del Credito: {r["idUsuario"]}\nCapital: {r["capital"]}\nCuota: {r["cuotaFija"]}\nSaldo: {r["saldoPendiente"]}\nEstado: {r["estado"]}')
                input("Enter para volver al menu de creditos...")

        #elif op == 2:
            #pid = utilidades.validarInputs(int, "ID de credito: ")
            #print(creditos.obtenerPorId(pid) or "No encontrado")
            #input("Enter...")

        elif op == 2:
            utilidades.limpiarConsola()
            pid = utilidades.validarInputs(int,   "ID de credito: ")
            monto = utilidades.validarInputs(float,"Monto a pagar: ", lambda v: None if v>0 else "Debe ser > 0")

            # Verificar que el crédito existe y pertenece al usuario
            creditoSel = creditos.obtenerPorId(pid)
            if creditoSel is None:
                print("Crédito no encontrado. Verifique el ID e intente nuevamente.")
                input("Presione Enter para volver al menú de créditos...")
                continue

            # Asegurar que el crédito corresponde al usuario logueado
            if int(creditoSel["idUsuario"]) != int(idUsuario):
                print("El ID ingresado no corresponde a un crédito suyo.")
                input("Presione Enter para volver al menú de créditos...")
                continue

            # Verificar estado del préstamo
            if creditoSel.get("estado") != "ACTIVO":
                print(f'El crédito está en estado "{creditoSel.get("estado")}". No es posible pagarlo.')
                input("Presione Enter para volver al menú de créditos...")
                continue

            # Verificación de saldo antes de intentar debitar de la cuenta del usuario
            saldoPesos = movimientos.obtenerSaldoPesos(idUsuario)
            if saldoPesos < monto:
                print(f"Saldo insuficiente. Saldo actual: ${round(saldoPesos,2)}")
                input("Presione Enter para volver al menú de créditos...")
            else:
                # Confirmación antes de debitar de la cuenta (forzar respuesta S o N)
                while True:
                    confirmar = input(f"Confirma débito de ${round(monto,2)} de su cuenta? (S/N): ").upper().strip()
                    if confirmar in ('S', 'N'):
                        break
                    print("Respuesta inválida. Ingrese 'S' para confirmar o 'N' para cancelar.")

                if confirmar == 'S':
                    # Llama a pagar indicando que debe debitar de la cuenta
                    utilidades.limpiarConsola()
                    resultadoPago = creditos.pagar(pid, monto, debitarDeCuenta=True)
                    print("\nResultado del pago:")
                    print(f"Monto aplicado: ${round(resultadoPago['aplicado'], 2)}")
                    print(f"Cuotas completadas: {resultadoPago['cuotasCompletadas']}")
                    if resultadoPago['resto'] > 0:
                        print(f"Monto sobrante: ${round(resultadoPago['resto'], 2)}")
                    print(f"Saldo pendiente: ${round(resultadoPago['saldoPendiente'], 2)}")
                    print(f"Próxima cuota: {resultadoPago['cuotaActual']}")
                    print(f"Estado del crédito: {resultadoPago['estado']}")
                    input("\nPresione Enter para volver al menú de créditos...")
                else:
                    print("Operación cancelada. No se efectuó el débito.")
                    input("Presione Enter para volver al menú de créditos...")

        else:
            break

def plazoFijo(idUser):
    if db.buscarUltimoPF(idUser):
        return None

    saldoPesos = movimientos.obtenerSaldoPesos(idUser)

    indice = utilidades.elegirOpcion(
        "Elija una opcion: ", 
        [op[0] for op in movimientos.TIPOS_PF], 
        "Seleccione el plazo fijo que desea realizar: "
        )
    
    if indice == 3:
        return None
    else:
        texto, porcentaje, plazoDias = movimientos.TIPOS_PF[indice]

    montoInvertido = utilidades.validarInputs(
        int, 
        f"Ingrese el monto a invertir (máximo ${saldoPesos}): ",
        validador=lambda monto: None if monto > 0 and monto < saldoPesos else f"Ingrese un monto mayor a 0 y menor a {saldoPesos}: " 
        )
        
    movimientos.realizarMovimiento(idUser, -montoInvertido, "PESOS", "PLAZOFIJOACTIVO")

    db.crearPlazoFijo(idUser, montoInvertido, porcentaje, plazoDias, "ACTIVO")

def verificarVencimientosPlazoFijo(idUser):
    plazosUsuario = db.buscarRegistros("plazoFijo", lambda r: int(r["idUsuario"]) == idUser)
    
    if not plazosUsuario or plazosUsuario[-1]["estado"] != "ACTIVO":
        return None

    ultimoPf = plazosUsuario[-1]

    fechaVencimiento = utilidades.obtenerFechasPlazo(ultimoPf)

    if datetime.now() >= fechaVencimiento:
        monto = float(ultimoPf["montoInvertido"])
        tasa = float(ultimoPf["tasa"])
        total = utilidades.calcularInteres(monto, tasa, 100)

        movimientos.realizarMovimiento(idUser, total, "PESOS", "PLAZOFIJOFINALIZADO")
        
        db.crearPlazoFijo(idUser, monto, tasa, ultimoPf["plazoDias"], "FINALIZADO")

        input(f"Plazo fijo vencido: se acreditaron ${total:.2f} ... ")

def compraVentaDolar(idUser):
    compraDolar = round(random.uniform(1300, 2000), 2)
    ventaDolar = round(compraDolar + random.uniform(25, 50), 2)

    saldoPesos = movimientos.obtenerSaldoPesos(idUser)
    saldoDolares = movimientos.obtenerSaldoDolar(idUser)

    compraOVenta = utilidades.elegirOpcion(
        "¿Qué desea hacer? ", 
        ["Comprar", "Vender", "Salir"], 
        f"La cotizacion del dolar para comprar es ${compraDolar} y para vender es ${ventaDolar}."
    )

    if compraOVenta == 0:
        montoDolar = utilidades.validarInputs(
            float, 
            "Cuántos dolares desea comprar: ", 
            validador=lambda monto: None if monto > 0 else "Ingrese un monto mayor a 0: "
        )

        montoPesos = montoDolar * compraDolar
        
        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()
        if siONo == "S":
            validaciones.validarConversion(
                idUser, 
                montoOrigen=montoPesos, 
                montoDestino=montoDolar, 
                saldoOrigen=saldoPesos, 
                tipoMonedaOrigen=movimientos.PESOS,
                tipoMonedaDestino=movimientos.DOLARES,
            )
    elif compraOVenta == 1:
        montoDolar = utilidades.validarInputs(
            float, "Cuántos dolares desea vender: ", 
            validador=lambda monto: None if monto > 0 else "Ingrese un monto mayor a 0: "
        )

        montoPesos = montoDolar * ventaDolar

        siONo = input(f"{montoDolar} dolares equivalen a {montoPesos} pesos. Desea continuar con la operacion? (Escriba S o N): ").upper().strip()
        if siONo == "S":
            validaciones.validarConversion(
                idUser, 
                montoOrigen=montoDolar, 
                montoDestino=montoPesos, 
                saldoOrigen=saldoDolares, 
                tipoMonedaOrigen=movimientos.DOLARES,
                tipoMonedaDestino=movimientos.PESOS,
            )

def gastosClasificacion(idUser):
    for tipoOperacion in movimientos.TIPOS_OPERACIONES:
        saldo = movimientos.obtenerMovimientosClasificados(idUser, tipoOperacion)
        print(f"{tipoOperacion}: {movimientos.calcularSaldo(saldo)} $")
    input("Presione enter para continuar ... ")

def listarUsuario():
    partUsername = input("Buscar: ")
    usuariosEncontrados = usuarios.obtenerPorUser(partUsername)

    if len(usuariosEncontrados) != 0:
        print("Usuarios encontrados")
        for usuario in usuariosEncontrados:
            print(usuario["username"])
        input("Presione enter para continuar...")
    else:
        print("No se encontraron usuarios")
        input("Presione enter para continuar...")

def saludoFin(idUser):
    utilidades.limpiarConsola()
    utilidades.printPausa(f"Muchas gracias {color.azul(usuarios.obtenerPorId(idUser)["nombre"])} por usar nuestro programa!",pausa=0.01)
    input(color.negrita(color.gris("Presione enter para continuar...")))
