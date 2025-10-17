import random
import time
from database import db
from datetime import datetime

TABLA_MOVIMIENTOS = "movimientos"

######### TIPOS MONEDAS ########
PESOS = "PESOS"
DOLARES = "DOLARES"

######### TIPOS OPERACIONES ########
DEPOSITO = "DEPOSITO"
GASTOS = "GASTOS"
SERVICIO = "SERVICIO"
DEUDAS = "DEUDAS"
AHORROS = "AHORROS"
OTROS = "OTROS"
COMPRA_MONEDA = "COMPRA_MONEDA"
VENTA_MONEDA = "VENTA_MONEDA"

####### OPERACIONES LISTADAS #######
TIPOS_OPERACIONES = [
    DEPOSITO,
    GASTOS,
    SERVICIO,
    DEUDAS,
    AHORROS,
    OTROS
]

def realizarMovimiento(idUsuario, monto, tipoMoneda, tipoOperacion):
    ahora = int(time.time() * 1000)        
    aleatorio = random.randint(0, 999)        
    comprobanteId = f"VVBA{ahora}{aleatorio:03d}"
    
    registro = {
        "comprobanteId": comprobanteId,
        "idUsuario": idUsuario,
        "monto": monto,
        "tipoMoneda": tipoMoneda,
        "tipoOperacion": tipoOperacion,
        "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }

    return db.crearRegistro(TABLA_MOVIMIENTOS, registro, condicionLambda=lambda reg: reg["comprobanteId"] != comprobanteId)

def obtenerMovimientos(idUsuario):
    return db.buscarRegistros(TABLA_MOVIMIENTOS, lambda reg: reg["idUsuario"] == idUsuario)

def obtenerMovimientosClasificados(idUsuario, tipoOperacion):
    return db.buscarRegistros(TABLA_MOVIMIENTOS, lambda reg: reg["idUsuario"] == idUsuario and reg["tipoOperacion"] == tipoOperacion)

def calcularSaldo(movimientos):
    #convertimos una nueva lista en base a los montos y los sumamos
    return round(sum(map(lambda mov: mov["monto"], movimientos)), 2)

def obtenerSaldoPesos(idUsuario):
    return calcularSaldo(db.buscarRegistros(TABLA_MOVIMIENTOS, lambda reg: reg["idUsuario"] == idUsuario and reg["tipoMoneda"] == PESOS))

def obtenerSaldoDolar(idUsuario):
    return calcularSaldo(db.buscarRegistros(TABLA_MOVIMIENTOS, lambda reg: reg["idUsuario"] == idUsuario and reg["tipoMoneda"] == DOLARES))