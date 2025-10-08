INDICE_PESOS = 0
INDICE_DOLAR = 1
INDICE_PLAZO_FIJO = 2
INDICE_CREDITO = 3
INDICE_TIPO_OPERACION = 4

# Tipos de operación posibles (categorías de gasto/ingreso)
TIPOS_OPERACIONES = [
    "Deposito",
    "Gastos",
    "Servicio",
    "Deudas",
    "Ahorros",
    "Deudas",
    "Otros"
]

# Estructura principal: MOVIMIENTOS es una lista por usuario.
# Cada usuario es una lista con 5 elementos:
# 0: lista de movimientos en pesos (positivo=ingreso, negativo=gasto)
# 1: lista de tenencia en dólares
# 2: lista de plazos fijos
# 3: lista de créditos
# 4: lista de tipos (categoría) correspondientes a cada movimiento en pesos
MOVIMIENTOS = [
    [[1000, -200, -500], [100], [], [], ["Deposito", "Gastos", "Servicio"]],  # Usuario 0
    [[2000, -300], [50], [], [], ["Deposito", "Gastos"]],  # Usuario 1
    [[500, -100, -250], [0], [], [], ["Deposito", "Gastos", "Deudas"]],  # Usuario 2
    [[3000, -1500], [300], [], [], ["Deposito", "Gastos"]],  # Usuario 3
    [[1500, -200, -100], [150], [], [], ["Deposito", "Deudas", "Servicio"]],  # Usuario 4
]

def crearMovimientos():
<<<<<<< HEAD
    # Agrega la entrada de movimientos para un nuevo usuario (estructura vacía).
    MOVIMIENTOS.append([[], [], [], [], []])
=======
MOVIMIENTOS.append([[], [], [], [], []])
>>>>>>> caf92cef6e62f7d890e9869bf733a4f85b222f48

# Conexiones: este módulo es usado por `funciones.py` para:
# - calcular saldos (`calcularSaldo`) -> lee `MOVIMIENTOS`
# - registrar operaciones (`realizarOperacion`) -> usa `operacionMonto`
# - ver movimientos (`verMovimientos`) -> lee `MOVIMIENTOS` para listar historiales

def operacionMonto(indiceUsuario, monto, tipoOperacion):
    # Registra un monto en pesos y guarda su tipo/categoría
    MOVIMIENTOS[indiceUsuario][INDICE_PESOS].append(monto)
    MOVIMIENTOS[indiceUsuario][INDICE_TIPO_OPERACION].append(tipoOperacion)
