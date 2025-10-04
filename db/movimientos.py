INDICE_PESOS = 0
INDICE_DOLAR = 1
INDICE_PLAZO_FIJO = 2
INDICE_CREDITO = 3
INDICE_TIPO_OPERACION = 4

TIPOS_OPERACIONES = [
    "Deposito",
    "Gastos",
    "Servicio",
    "Deudas",
    "Ahorros",
    "Deudas",
    "Otros"
]

# Cada usuario tendrá [movimientos, tenencia dólar, plazo fijo, crédito, tipo de gasto]
MOVIMIENTOS = [
    [[1000, -200, -500], [100], [], [], ["Deposito", "Gastos", "Servicio"]],  # Usuario 0
    [[2000, -300], [50], [], [], ["Deposito", "Gastos"]],  # Usuario 1
    [[500, -100, -250], [0], [], [], ["Deposito", "Gastos", "Deudas"]],  # Usuario 2
    [[3000, -1500], [300], [], [], ["Deposito", "Gastos"]],  # Usuario 3
    [[1500, -200, -100], [150], [], [], ["Deposito", "Deudas", "Servicio"]],  # Usuario 4
]

def crearMovimientos():
    MOVIMIENTOS.append([[], [], [], [], []])

def operacionMonto(indiceUsuario, monto, tipoOperacion):
    MOVIMIENTOS[indiceUsuario][INDICE_PESOS].append(monto)
    MOVIMIENTOS[indiceUsuario][INDICE_TIPO_OPERACION].append(tipoOperacion)
