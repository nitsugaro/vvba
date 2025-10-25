import time, os
from datetime import datetime, timedelta

import color

def limpiarConsola():
    os.system('cls' if os.name == 'nt' else 'clear')

def pedir(tipo=str, prompt="", validador=lambda x: None):
    while True:
        try:
            valor = tipo(input(prompt))
            error = validador(valor)
            if not error:
                return valor
            prompt = error + " "  # usa el mensaje de error como nuevo prompt
        except ValueError:
            prompt = f"Valor inválido. {prompt}"

def elegirOpcion(prompt, listOpciones, preText = ""):
    '''
        Presenta al usuario un prompt y una serie de opciones enumeradas del 1 a N. Devuelve el INDICE de la opción elegida.
    '''

    limpiarConsola()
    while True:
        if preText != "":
            printPausa(preText, pausa=0.01)

        #mostrar opciones
        for i in range(len(listOpciones)):
            printPausa(f"{color.amarillo(f"{i + 1}.")} {listOpciones[i]}", pausa=0.001)

        try:
            opcionIndice = int(input(prompt)) - 1
        except ValueError:
            #valor por defecto
            opcionIndice = -1
        
        if opcionIndice >= 0 and opcionIndice < len(listOpciones):
            #está dentro del rango
            break
        else:
            limpiarConsola()
            print("ERROR: El número de opción debe ser una de las enumeradas.\n")

    return opcionIndice

def printPausa(texto, nuevaLinea=True, pausa = 0.02):
    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(pausa)
    if nuevaLinea:
        print()

def obtenerFechasPlazo(plazo):
    fechaInicio = datetime.strptime(plazo["fecha"], "%Y-%m-%d")
    return fechaInicio + timedelta(days=int(plazo["plazoDias"]))

def calcularInteres(intMoto, intTasa, num):
    return intMoto + intMoto * intTasa / num
