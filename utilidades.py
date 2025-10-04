import os

def limpiarConsola():
    os.system('cls' if os.name == 'nt' else 'clear')

def elegirOpcion(prompt, listOpciones, preText = ""):
    '''
        Presenta al usuario un prompt y una serie de opciones enumeradas del 1 a N. Devuelve el INDICE de la opción elegida.
    '''

    while True:
        if preText != "":
            print(preText)

        #mostrar opciones
        for i in range(len(listOpciones)):
            print(f"{i + 1}. {listOpciones[i]}")

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