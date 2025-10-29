import os
from database import db
try:
    from database import movimientos  # opcional: para acreditar/descontar en cuenta
    _MOVS_OK = True
except Exception:
    _MOVS_OK = False

TABLA = "creditos"

# Orden y nombres de columnas del CSV (deben coincidir con el header)
CAMPOS = [
    "id",             # int
    "idUsuario",      # int
    "capital",        # float
    "tasaMensual",    # float (0.04 = 4% mensual)
    "plazoMeses",     # int
    "cuotaFija",      # float (sistema francés)
    "cuotaActual",    # int (>1)
    "pagadoCuota",    # float (acumulado pagado de la cuota actual)
    "saldoPendiente", # float (capital remanente)
    "estado"          # str: 'ACTIVO' | 'CANCELADO'
]

# ---------- utilidades internas ----------

def initTablaSiNoExiste():
    """Crea 'creditos.csv' con header si no existe."""
    path = TABLA + ".csv"
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(";".join(CAMPOS) + "\n")


def leerTodos():
    """Lista de creditos como dicts ya tipados (gracias a db.convertirLineaDict)."""
    initTablaSiNoExiste()
    return db.buscarRegistros(TABLA, lambda r: True)  # lee con header y castea tipos fileciteturn2file0

def guardarTodos(regs):
    """Sobreescribe el CSV completo en el orden de CAMPOS."""
    with open(TABLA + ".csv", "w", encoding="utf-8") as f:
        f.write(";".join(CAMPOS) + "\n")
        for r in regs:
            fila = [str(r[c]) for c in CAMPOS]
            f.write(";".join(fila) + "\n")

def proxId():
    regs = leerTodos()
    return (max(r["id"] for r in regs) + 1) if regs else 1

def r2(x):
    return round(float(x), 2)

def cuotaFrancesa(capital, tasaMensual, plazoMeses):
    P = float(capital); i = float(tasaMensual); n = int(plazoMeses)
    if i == 0: return r2(P / n)
    return r2(P * i / (1.0 - (1.0 + i) ** (-n)))

# ---------- API pública ----------

def crearCredito(idUsuario, capital, tasaMensual, plazoMeses, acreditarEnCuenta=False):
    """Crea credito (cuota francesa mensual). Devuelve id (int).
    Si acreditar_en_cuenta=True y existe 'movimientos', acredita el capital como DEPÓSITO en PESOS.
    """
    initTablaSiNoExiste()
    pid   = proxId()
    P     = r2(capital)
    i     = float(tasaMensual)
    n     = int(plazoMeses)
    cuota = cuotaFrancesa(P, i, n)

    # registro en el orden del header
    reg = {
        "id": pid,
        "idUsuario": int(idUsuario),
        "capital": P,
        "tasaMensual": round(i, 6),
        "plazoMeses": n,
        "cuotaFija": cuota,
        "cuotaActual": 1,
        "pagadoCuota": 0.0,
        "saldoPendiente": P,
        "estado": "ACTIVO",
    }

    # usa el helper común para agregar la fila (escribe una línea; requiere que exista header)
    db.crearRegistro(TABLA, reg, condicionLambda=lambda r: r["id"] != pid)  # fileciteturn2file0

    # (opcional) impactar en cuenta
    if acreditarEnCuenta and _MOVS_OK:
        try:
            movimientos.realizarMovimiento(idUsuario, P, movimientos.PESOS, movimientos.DEPOSITO)  # fileciteturn2file1
        except Exception:
            pass

    return pid

def listarPorUsuario(idUsuario):
    return [r for r in leerTodos() if r["idUsuario"] == int(idUsuario)]

def obtenerPorId(idCredito):
    regs = leerTodos()
    for r in regs:
        if r["id"] == int(idCredito):
            return r
    return None

def pagar(idCredito, monto, debitarDeCuenta=False):
    """Paga cuotas en cascada con estado agregado (sin cronograma).
    - Calcula interés del período como saldo * tasaMensual y amortización = cuotaFija - interés.
    - Ajusta la última cuota si amortización > saldo.
    - Completa cuota si alcanza; si no, queda como pago parcial.
    Devuelve dict resumen.
    """
    pago = r2(monto)
    if pago <= 0:
        return {"aplicado": 0.0, "cuotasCompletadas": 0, "resto": pago, "msg": "monto <= 0"}

    regs = leerTodos()
    idx = next((i for i, r in enumerate(regs) if r["id"] == int(idCredito)), None)
    if idx is None:
        return {"aplicado": 0.0, "cuotasCompletadas": 0, "resto": pago, "msg": "no encontrado"}

    row = regs[idx]
    if row["estado"] != "ACTIVO":
        return {"aplicado": 0.0, "cuotasCompletadas": 0, "resto": pago, "msg": "prestamo cancelado"}

    cuota = r2(row["cuotaFija"])
    i     = float(row["tasaMensual"])
    n     = int(row["plazoMeses"])
    k     = int(row["cuotaActual"])  # en curso
    saldo = r2(row["saldoPendiente"])
    pag   = r2(row["pagadoCuota"])  # acumulado cuota actual

    aplicado = 0.0
    cuotasOk = 0
    EPS = 0.01

    # (opcional) debitar primero de la cuenta del usuario
    if debitarDeCuenta and _MOVS_OK and pago > 0:
        try:
            # movimiento negativo (egreso)
            movimientos.realizarMovimiento(row["idUsuario"], -pago, movimientos.PESOS, "Pago credito")  # fileciteturn2file1
        except Exception:
            pass

    while pago > 0 and row["estado"] == "ACTIVO":
        interes = r2(saldo * i)
        amort   = r2(cuota - interes)
        if amort > saldo:
            amort = saldo
        cuota_teo = r2(interes + amort)

        faltante = r2(cuota_teo - pag)
        if pago + EPS >= faltante:
            # completa la cuota k
            pago      = r2(pago - faltante)
            aplicado  = r2(aplicado + faltante)
            cuotasOk += 1

            saldo = r2(saldo - amort)  # reduce capital
            k    += 1
            pag   = 0.0

            if saldo <= EPS or k > n:
                saldo = 0.0
                row["estado"] = "CANCELADO"
                break
        else:
            # pago parcial de la cuota
            pag   = r2(pag + pago)
            aplicado = r2(aplicado + pago)
            pago  = 0.0
            break

    # persistir en CSV
    row.update({
        "saldoPendiente": saldo,
        "cuotaActual": k,
        "pagadoCuota": pag,
    })
    regs[idx] = row
    guardarTodos(regs)

    return {
        "aplicado": aplicado,
        "cuotasCompletadas": cuotasOk,
        "resto": pago,
        "saldoPendiente": saldo,
        "cuotaActual": k,
        "estado": row["estado"],
    }