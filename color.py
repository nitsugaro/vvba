COLORES = {
    "negro": "\033[30m",
    "rojo": "\033[31m",
    "verde": "\033[32m",
    "amarillo": "\033[33m",
    "azul": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "blanco": "\033[37m",
    "gris": "\033[37m",
    "rosa": "\033[35m",
    "naranja": "\033[33m",
    "marron": "\033[31m",
    "verde_lima": "\033[32m",
    "violeta": "\033[35m",
    "celeste": "\033[36m",
    "reset": "\033[0m",
    "negrita": "\033[1m"
}

# ===== FUNCIONES PARA SETEAR COLOR DE TEXTO =====

def color(texto, nombre_color):
    codigo = COLORES.get(nombre_color.lower())
    if codigo:
        return f"{codigo}{texto}{COLORES['reset']}"
    return texto

def negro(texto): return color(texto, "negro")
def rojo(texto): return color(texto, "rojo")
def verde(texto): return color(texto, "verde")
def amarillo(texto): return color(texto, "amarillo")
def azul(texto): return color(texto, "azul")
def magenta(texto): return color(texto, "magenta")
def cyan(texto): return color(texto, "cyan")
def blanco(texto): return color(texto, "blanco")
def gris(texto): return color(texto, "gris")
def rosa(texto): return color(texto, "rosa")
def naranja(texto): return color(texto, "naranja")
def marron(texto): return color(texto, "marron")
def verde_lima(texto): return color(texto, "verde_lima")
def violeta(texto): return color(texto, "violeta")
def celeste(texto): return color(texto, "celeste")
def negrita(texto): return f"{COLORES['negrita']}{texto}{COLORES['reset']}"