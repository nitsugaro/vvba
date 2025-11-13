import color, validaciones, utilidades, random
from database import usuarios, movimientos, db
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
    inicio = 0

    if inicio < 0:
        inicio = 0

    for i in range(inicio, len(movs)):
        movimiento = movs[i]
        print(f"Monto {movimiento["monto"]} corresponde al tipo de gasto: {movimiento["tipoOperacion"]}")

    input("Presione enter para continuar ... ")

def verMovimientosAdmin(intId=0):
    movimientosPrev = 5
    currentId = intId
    
    while True:
        movs = movimientos.obtenerMovimientos(currentId)
        inicio = len(movs) - movimientosPrev
        if inicio < 0:
            inicio = 0
        print(f"ID de usuario: {color.azul((currentId))}")
        for i in range(inicio, len(movs)):
            movimiento = movs[i]
           
            print(f"Comprobante {movimiento['comprobanteId']}")
            print(f"Tipo de moneda {movimiento['tipoMoneda']} Monto: {movimiento['monto']} corresponde al tipo de gasto: {movimiento['tipoOperacion']}")
            print(f"Fecha de movimiento: {color.amarillo(movimiento['fecha'])}")
            print(color.verde("-"*90))
            
       # "comprobanteId": comprobanteId,
        #    "idUsuario": idUsuario,
         #   "monto": monto,
          #  "tipoMoneda": tipoMoneda,
           # "tipoOperacion": tipoOperacion,
           # "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        
        # Permitir ingresar un número para saltar a un ID o negativo para volver al menú
        entrada = input("Ingrese un número para saltar a ese ID, número negativo para volver al menú, o Enter para siguiente usuario: ").strip()
        
        if entrada == "":
            # Enter vacío: continuar al siguiente usuario
            currentId += 1
        else:
            try:
                numeroId = int(entrada)
                if numeroId < 0:
                    # Número negativo: volver al menú
                    return
                else:
                    # Número positivo: saltar a ese ID
                    currentId = numeroId
            except ValueError:
                # Si no es un número válido, continuar al siguiente usuario
                print("Entrada inválida, continuando al siguiente usuario...")
                currentId += 1
        
        utilidades.limpiarConsola()

def buscarMovimientosPorId():
    '''
        Permite buscar y ver los movimientos de un usuario específico por su ID.
    '''
    idUsuario = utilidades.validarInputs(
        int,
        "Ingrese el ID del usuario para ver sus movimientos: ",
        validador=lambda id: None if id > 0 else "Ingrese un ID válido (mayor a 0): "
    )
    
    # Verificar que el usuario exista
    usuarioEncontrado = usuarios.obtenerPorId(idUsuario)
    if not usuarioEncontrado:
        print(f"No se encontró un usuario con ID {idUsuario}")
        input("Presione enter para continuar... ")
        return
    
    movimientosPrev = 5
    movs = movimientos.obtenerMovimientos(idUsuario)
    
    if not movs or len(movs) == 0:
        print(f"No se encontraron movimientos para el usuario con ID {color.azul(idUsuario)}")
        input("Presione enter para continuar... ")
        return
    
    inicio = len(movs) - movimientosPrev
    if inicio < 0:
        inicio = 0
    
    print(f"ID de usuario: {color.azul(idUsuario)}")
    print(f"Usuario: {color.azul(usuarioEncontrado['username'])}")
    print(f"Total de movimientos: {len(movs)}\n")
    
    for i in range(inicio, len(movs)):
        movimiento = movs[i]
        print(f"Comprobante {movimiento['comprobanteId']}")
        print(f"Tipo de moneda {movimiento['tipoMoneda']} Monto: {movimiento['monto']} corresponde al tipo de gasto: {movimiento['tipoOperacion']}")
        print(f"Fecha de movimiento: {color.amarillo(movimiento['fecha'])}")
        print(color.verde("-"*90))
    
    input("Presione enter para continuar... ")
def creditos():
    pass


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
