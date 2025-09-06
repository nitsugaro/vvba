def login(matriz):
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")
        for i in range (len(matriz[0])):
            if matriz[0][i] == usuario:
                if matriz[1][i] == contraseña:
                   return usuario
        print("Error en los datos ingresados")
