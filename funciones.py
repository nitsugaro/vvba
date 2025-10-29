from database import creditos, usuarios, movimientos
import color, validaciones, utilidades, random

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

#def credito():
    #pass

def plazoFijo():
    pass

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

def creditosF(idUsuario):
    while True:
        utilidades.limpiarConsola()
        op = utilidades.elegirOpcion("Elegí una opción: ", [
            "Crear préstamo",
            "Mis préstamos",
            "Ver préstamo por ID",
            "Pagar",
            "Volver"
        ])

        if op == 0:
            capital = utilidades.validarInputs(float, "Capital: ", lambda v: None if v>0 else "Debe ser > 0")
            tasa    = utilidades.validarInputs(float, "Tasa mensual (0.04=4%): ", lambda v: None if v>=0 else "No puede ser negativa")
            meses   = utilidades.validarInputs(int,   "Plazo en meses: ", lambda v: None if v>0 else "Debe ser > 0")
            pid = creditos.crearCredito(idUsuario, capital, tasa, meses, acreditarEnCuenta=False)
            input(f"Credito creado ID {pid}. Enter...")

        elif op == 1:
            creditosL = creditos.listarPorUsuario(idUsuario)
            if not creditosL:
                print("No tenes creditos registrados...")
            else:
                utilidades.limpiarConsola()
                for r in creditosL:
                    print(f'ID del Prestamo {r["idPrestamos"]}\nCapital: {r["capital"]}\nCuota: {r["cuotaFija"]}\nSaldo: {r["saldoPendiente"]}\nEstado: {r["estado"]}')
                input("Enter para volver al menu de creditos...")

        elif op == 2:
            pid = utilidades.validarInputs(int, "ID de credito: ")
            print(creditos.obtenerPorId(pid) or "No encontrado")
            input("Enter...")

        elif op == 3:
            pid = utilidades.validarInputs(int,   "ID de credito: ")
            monto = utilidades.validarInputs(float,"Monto a pagar: ", lambda v: None if v>0 else "Debe ser > 0")
            print(creditos.pagar(pid, monto, debitarDeCuenta=False))
            input("Enter...")

        else:
            break