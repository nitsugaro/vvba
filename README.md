# virtual-bank

📄 Informe del Proyecto
Vanguardia Virtual del Banco Argentino
Proyecto integrador de Programación I

## 1. Módulo usuarios.py

Contiene constantes globales:
MOVIMIENTOS: matriz con registros por usuario (pesos, dólares, plazos fijos, créditos, tipos de gasto).
TIPOCATEGORIA: categorías de operaciones (Sueldo, Depósito, Servicio, Gastos, etc.).

## 2. Módulo db

Aquí se simulan las “bases de datos” del sistema.

#### 📌 db.usuarios

- usuarios: lista que guarda los nombres de usuario.
- claves: lista paralela que guarda contraseñas.
- obtenerIndexUsuario(nombre) → devuelve el índice del usuario si existe, o -1 si no.
- verificarClave(indice, clave) → compara clave ingresada con la registrada.
- crearUsuarioClave(nombre, clave) → agrega un usuario y su contraseña a las listas.
- obtenerUsuarios() → retorna la lista de usuarios.
- obtenerNombreUsuario(indice) → devuelve el nombre del usuario según índice.

#### 📌 db.movimientos

- MOVIMIENTOS: matriz de operaciones por usuario (referencia a const).
- TIPOS_OPERACIONES: lista de tipos de operaciones válidas (Depósito, Gastos, Servicio, Deuda, etc.).
- crearMovimientos() → inicializa la estructura de movimientos para un nuevo usuario.
- operacionMonto(intId, monto, tipoOperacion) → registra en MOVIMIENTOS el monto y tipo de gasto/ingreso.

## 3. Módulo funciones.py

Define la lógica principal del banco:

- iniciarSesion() → valida usuario y contraseña.
- crearUsuario() → crea nuevo usuario y movimientos.
- menuInicio() → opciones iniciales.
- menuPrincipal(intId) → menú principal con saldos y operaciones.
- calcularSaldo(matriz, id, tipo) → calcula saldo de pesos o dólares.
- realizarOperacion(intId) → gestiona depósitos y gastos.
- verMovimientos(intId) → lista los últimos 5 movimientos.
- creditos() y plazoFijo() → pendientes de implementación.
- compraVentaDolar(intId) → compra/venta dólares con validación de saldos.
- gastosClasificacion(intId, categorias) → muestra gastos agrupados por categoría.
- listarUsuario() → búsqueda de usuarios por nombre parcial.
- salir(intId) → mensaje de cierre.

## 4. Módulo main.py

Archivo de ejecución:
Llama a menuInicio() y gestiona la creación o login de usuario.
Una vez logueado, abre un bucle con menuPrincipal() hasta que se elija “Salir”.

## 5. Módulo utilidades.py

Funciones auxiliares:
limpiarConsola() → limpia la pantalla.
elegirOpcion(prompt, opciones, preText) → muestra menú numerado, valida input y devuelve índice.

## 6. Módulo validaciones.py

Se encarga de validaciones de entradas:

- validarNombreUsuario(usuario) → impide duplicados.
- validarContraseña(clave) → exige mínimo 5 caracteres y 1 número.
- validarNumeroPositivo(num) → asegura que el monto sea > 0.
- validarTransaccion(...) → verifica saldo suficiente antes de registrar la operación.

### Conclusión

El proyecto Virtual Bank es una simulación de un sistema bancario virtual desarrollado en Python.
Integra múltiples módulos (db, funciones, utilidades, validaciones, const, main) que trabajan de manera conjunta para ofrecer una experiencia de usuario completa, desde la creación y gestión de cuentas hasta la realización de operaciones financieras como depósitos, gastos y compra/venta de dólares.

### Ejecutar

Usuario de prueba

##### Nombre: Ana

##### Clave: Pass123!

```py
python main.py
```
