README TÉCNICA - Virtual Bank (parte técnica)

Fecha: 2025-10-03

## Resumen

Documento que describe la organización actual de datos y código del proyecto `virtual-bank`, las decisiones de diseño tomadas, y una propuesta de rediseño/mejoras para la versión final (archivos, validaciones, estructuras de datos). Este archivo es solo documentación: no realiza cambios en el código.

1. Estructura de datos - versión actual

---

Archivos relevantes en `db/`:

- `db/usuarios.py`

  - Define dos constantes de índice: `INDICE_USUARIO = 0`, `INDICE_CLAVES = 1`.
  - Contiene la variable global `USUARIOSCLAVES`, una lista de dos listas: la primera lista almacena los nombres de usuario y la segunda las contraseñas respectivamente por índice.
  - Funciones: `obtenerUsuarios()`, `obtenerIndexUsuario(nombre)`, `obtenerNombreUsuario(indice)`, `crearUsuarioClave(nombre, clave)`, `verificarClave(indiceUsuario, clave)`.
  - Comentario: la estructura es una lista de listas (matriz) indexada por constantes.

- `db/movimientos.py`
  - Define constantes de índice para las distintas subestructuras: `INDICE_PESOS`, `INDICE_DOLAR`, `INDICE_PLAZO_FIJO`, `INDICE_CREDITO`, `INDICE_TIPO_OPERACION`.
  - `TIPOS_OPERACIONES`: lista de categorías posibles.
  - `MOVIMIENTOS`: lista por usuario, donde cada entrada de usuario es una lista de cinco elementos: [movimientos pesos (lista de floats), tenencia dólar (lista), plazo fijo (lista), crédito (lista), lista de tipos de operación (lista de strings)].
  - Funciones: `crearMovimientos()` (intenta inicializar nueva entrada) y `operacionMonto(indiceUsuario, monto, tipoOperacion)` que añade el monto y tipo.
  - Comentarios: la representación usa una matriz anidada y constantes de índice. `crearMovimientos()` contiene un patrón problemático: `MOVIMIENTOS.append([[]] * 5)` — esto crea 5 referencias al mismo objeto lista, lo cual es un bug potencial.

Ventajas de la versión actual:

- Simple de implementar y suficiente para una entrega rápida.
- Acceso por índices es eficiente en tiempo.

Limitaciones y problemas conocidos:

- Uso intensivo de listas indexadas por posición: poco legible y propenso a errores si se confunden índices.
- `MOVIMIENTOS.append([[]] * 5)` produce referencias compartidas entre sublistas (bug).
- Almacenamiento en memoria solamente: no persiste al disco.
- Falta de validaciones robustas (ej. formato de usuario/clave, montos negativos cuando no aplica, límites, etc.).
- No hay separación clara entre la capa de persistencia (modelos/DB) y la lógica de negocio.

2. Idea para la versión final (rediseño)

---

Objetivo: migrar a estructuras más explícitas, persistentes y seguras.

Estructura de datos propuesta (ficheros + tipos):

- `db/usuarios.json` (archivo JSON) - almacenamiento persistente de usuarios.

  - Formato propuesto: lista o diccionario con user-id:
    - Lista de diccionarios: [{"id": 0, "username": "Ana", "password": "..."}, ...]
    - O bien diccionario: {"Ana": {"id": 0, "password": "..."}}

- `db/movimientos.json` (archivo JSON)

  - Estructura más clara por usuario, por ejemplo un diccionario por usuario:
    {
    "0": {
    "pesos": [1000, -200, -500],
    "dolares": [100],
    "plazo_fijo": [],
    "creditos": [],
    "tipos": ["Deposito","Gastos","Servicio"]
    },
    "1": { ... }
    }

- Alternativa: usar `shelve` o `sqlite3` si se desea mayor robustez sin introducir dependencias externas.

- En memoria, usar estructuras más expresivas: diccionarios y tuplas o dataclasses.

  - Ejemplo (dataclass):
    @dataclass
    class Usuario:
    id: int
    username: str
    password: str

    @dataclass
    class MovimientosUsuario:
    pesos: List[float]
    dolares: List[float]
    plazo_fijo: List[float]
    creditos: List[float]
    tipos: List[str]

Motivación:

- Legibilidad: acceder a campos por nombre, no por índice numérico.
- Persistencia: conservar datos entre ejecuciones.
- Evitar bugs con referencias compartidas.

3. Criterios seguidos para dividir el código en funciones

---

Observaciones del código existente:

- Las funciones en `funciones.py` agrupan acciones de la interfaz (entrada/salida y lógica simple): inicio de sesión, creación de usuario, menú, operaciones, ver movimientos, compra/venta de dólar, etc.
- `utilidades.py` contiene utilidades de consola (limpieza y selección de opciones).
- `db/` actúa como un "mini-modelo": funciones para manipular listas globales.

Criterios actuales (implícitos):

- Funciones por tarea del flujo de trabajo: cada acción del menú corresponde a una función.
- Separación básica entre utilidades (I/O) y lógica de dominio.

Oportunidades de mejora en la división de funciones:

- Separar capa de persistencia (acceso a datos) de lógica de dominio y de la capa de presentación (I/O). Separar responsabilidades en módulos claros:
  - db_layer.py: funciones puras para CRUD sobre usuarios y movimientos (carga/guardado).
  - services.py: lógica de negocio (operar montos, validaciones entre cuentas, reglas de negocio).
  - ui.py / cli.py: manejo de interacción con el usuario (inputs, menus). Esto facilita tests unitarios.
- Reducir funciones demasiado largas y mover validaciones a funciones dedicadas (p. ej. `validar_monto`, `validar_usuario_unico`).
- Evitar lambdas con estado implícito en `main` y usar funciones nombradas o métodos de una clase `CLI` para mantener el estado del usuario actual.

4. Mejoras técnicas a incorporar en el futuro

---

Priorizadas y justificadas:

Alta prioridad

- Persistencia de datos: migrar a archivos JSON o SQLite.
- Corregir `crearMovimientos()` para evitar listas compartidas: inicializar con `MOVIMIENTOS.append([[], [], [], [], []])` o usar `copy`.
- Validaciones robustas: entradas numéricas, rangos, fronteras (saldo insuficiente), y sanitización de strings.
- Manejo de errores: capturar excepciones esperadas y dar mensajes amigables; logs para errores inesperados (módulo `logging`).

Mediana prioridad

- Refactor: separar en `db_layer.py`, `services.py`, `cli.py` y tests unitarios.
- Uso de dataclasses y tipos (mypy o anotaciones) para mayor claridad.
- Tests automáticos: unitarios para la lógica de operaciones y de validaciones.

Baja prioridad / Opcionales

- Interfaz web mínima (Flask) o TUI con `curses` para mejor UX.
- Internacionalización/soporte de múltiples monedas con cotizaciones reales (APIs), si es necesario.

5. Ejemplo de estructura de proyecto (propuesta)

---

virtual-bank/
├─ db/
│ ├─ usuarios.json
│ └─ movimientos.json
├─ src/
│ ├─ db_layer.py # carga/guarda y modelos de datos (serialización)
│ ├─ services.py # lógica del banco (operar, transferir, validar)
│ ├─ cli.py # interacción con usuario (entrada/salida)
│ ├─ utilidades.py # utilidades de consola ya existentes
│ └─ main.py # orquestador (invoca cli)
├─ tests/
│ ├─ test_services.py
│ └─ test_db_layer.py
├─ requirements.txt
└─ README_TECNICA.md # (este archivo)

6. Riesgos y edge-cases detectados hoy

---

- `MOVIMIENTOS.append([[]] * 5)` crea 5 referencias a la misma lista, por lo que modificar una modificará todas.
- Contraseñas en texto plano: problema de seguridad.
- Falta de persistencia: pérdidas de datos entre ejecuciones.
- Entradas del usuario no validadas en profundidad (p. ej. float() en `realizarOperacion` puede lanzar ValueError — ya lo manejan, pero hay más casos).

7. Recomendaciones concretas inmediatas (para la próxima clase)

---

- Cambiar `crearMovimientos()` a `MOVIMIENTOS.append([[], [], [], [], []])` para evitar el bug.
- Guardar/leer los datos desde archivos JSON al inicio/fin del programa (ejecutar backup al guardar).
- Añadir logging básico:
  import logging
  logging.basicConfig(level=logging.INFO)

8. Tareas futuras sugeridas (roadmap rápido)

---

- (1 día) Corregir bug de listas compartidas y cambiar funciones de db para leer/escribir JSON.
- (2 días) Introducir dataclasses y refactorizar lógica en `services.py`.
- (2 días) Añadir tests unitarios para operaciones y validaciones.
- (1 día) Mejorar CLI y agregar confirmaciones en operaciones que alteren saldo.

9. Cierre

---

Este archivo documenta la situación actual y una propuesta de mejora. Si querés, puedo:

- crear un branch y aplicar los cambios mínimos (corregir `crearMovimientos()` y añadir persistencia JSON),
- o sólo generar fragmentos de código y tests para que los integren.

No modifiqué nada del código como pediste.

---

Fin del README técnico
