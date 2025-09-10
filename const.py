USUARIOSCONTRASENAS = [[0, 1, 2, 3, 4], # ID
                       ["Ana", "Luis", "María", "Carlos", "Sofía"], # Nombre de usuario
                       ["Pass123!", "Qwerty2025", "Segura#45", "Clave*89", "MiPass_77"]] # Contraseñas

# Cada usuario tendrá [movimientos, tenencia dólar, plazo fijo, crédito, tipo de gasto]
MOVIMIENTOS = [
    [[1000, -200, -500], [100], [], [], ["Deposito", "Gastos", "Servicio"]],  # Usuario 0
    [[2000, -300], [50], [], [], ["Deposito", "Gastos"]],  # Usuario 1
    [[500, -100, -250], [0], [], [], ["Deposito", "Gastos", "Deudas"]],  # Usuario 2
    [[3000, -1500], [300], [], [], ["Deposito", "Gastos"]],  # Usuario 3
    [[1500, -200, -100], [150], [], [], ["Deposito", "Deudas", "Servicio"]],  # Usuario 4
    ]

TIPOCATEGORIA = ["Sueldo", "Deposito", "Otros", "Servicio", "Gastos", "Deudas", "Ahorros"]