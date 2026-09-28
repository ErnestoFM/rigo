# GUÍA Y GUION PARA LA GRABACIÓN DEL VIDEO DEMOSTRATIVO
## Actividad 6: Análisis Sintáctico de Métodos y Clases
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Fecha de Entrega:** 18 de septiembre, 23:59  
**Ponderación:** 100 puntos  

**Integrantes del Equipo (Orden Alfabético por Primer Apellido):**
1. Díaz Torres Jazmín Montserrat
2. Fierro Meléndez Ernesto Hatuey
3. Hernández García Héctor Gabriel
4. Millán Guerrero Oswaldo Josué

---

## ⚠️ REQUISITOS OBLIGATORIOS SEGÚN LA RÚBRICA OFICIAL
1. **Duración:** Máximo **5 minutos** (ideal: entre 3:30 y 4:30 minutos).
2. **Resolución:** Mínimo **720p** (recomendado: 1080p).
3. **Audio:** Voz clara con micrófono explicando el objetivo, las reglas de la gramática y el funcionamiento.
4. **Pantalla completa obligatoria:** Se debe grabar **toda la pantalla del equipo de cómputo**, asegurando que la **barra de tareas de Windows con la fecha y hora** sea claramente visible en todo momento.
5. **Código y salida legibles:** Tamaño de fuente adecuado en terminal y GUI.
6. **Software de grabación sugerido:**
   - **Xbox Game Bar (Windows nativo):** Presiona `Windows + Alt + R` para iniciar y detener la grabación.
   - **OBS Studio:** Captura de pantalla completa sin recortar bordes.

---

## 🕒 CRONOGRAMA MINUTO A MINUTO (GUION DE VOZ Y ACCIONES)

| Tiempo | Sección | Acción en Pantalla | Qué decir (Guion de voz sugerido) |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:35** | **Introducción y Objetivos** | Pantalla completa con reloj/fecha visible en la barra de tareas. Terminal abierta en la carpeta `actividad_6`. | *"Buen día, profesor Rigoberto Cárdenas. Somos el equipo integrado por Jazmín Díaz, Ernesto Fierro, Héctor Hernández y Oswaldo Millán. Presentamos la Actividad 6: Análisis sintáctico de métodos y clases. El objetivo de esta práctica es implementar la fase de parsing para la definición formal de métodos y clases, asegurando la correcta identificación estructural, la construcción del Árbol de Sintaxis Abstracta (AST) y una gestión robusta de errores sintácticos conforme a la gramática asignada."* |
| **0:35 - 1:45** | **Ejecución CLI (`main.py`) - Casos Válidos** | Ejecutar `python main.py` en la terminal. Desplazarse al inicio de la salida. | *"Al ejecutar `main.py`, la primera instrucción obligatoria imprime en consola las firmas completas de los integrantes en orden alfabético por primer apellido. En la Sección 1 demostramos los casos válidos, iniciando con el caso oficial de la práctica: `class MiClase` con `miMetodo(int a, float b)` y `otroMetodo()`, observando cómo el parser desglosa los tipos de retorno, los parámetros y genera un AST jerárquico impecable con 0 errores. También validamos clases con variables de campo, múltiples clases y sentencias de control en los métodos."* |
| **1:45 - 2:50** | **Ejecución CLI - Errores Sintácticos** | Desplazarse en la terminal a la Sección 2 de casos inválidos. | *"En la Sección 2 demostramos la gestión y reporte de errores sintácticos requeridos en la rúbrica oficial. En el caso oficial con falta de coma entre parámetros (`int a float b`), el analizador reporta con precisión milimétrica la línea, columna y el mensaje: 'Error: Parámetro inválido en la declaración de método'. En el caso sin paréntesis (`void otroMetodo {`), detecta la omisión de '(' y ')'. Además, demostramos el reporte exacto de 'Cuerpo de clase inválido', 'Tipo de retorno inválido' y 'Llaves desbalanceadas'. Al finalizar la ejecución, la última instrucción obligatoria vuelve a imprimir los nombres de los integrantes."* |
| **2:50 - 4:15** | **Demostración Interactiva en GUI (`gui.py`)** | Ejecutar `python gui.py`. Mostrar la interfaz gráfica moderna. | *"Ahora pasamos a la demostración de la interfaz gráfica interactiva. En el encabezado superior se aprecian los datos de los 4 integrantes y la materia. En el selector cargamos el caso válido oficial y damos clic en 'ANALIZAR SINTAXIS', apreciando el Árbol AST expandido, la tabla detallada de tokens léxicos y la pestaña con las reglas formales EBNF. Posteriormente, seleccionamos el caso inválido de falta de comas entre parámetros y observamos cómo la tabla de errores detalla de forma inmediata el número de línea, columna, categoría y sugerencia pedagógica."* |
| **4:15 - 4:45** | **Conclusión y Cierre** | Mostrar nuevamente la fecha/hora en la barra de tareas y despedida. | *"Concluimos verificando que el analizador cumple al 100% con todos los requerimientos de gramática formal, parsing, jerarquía de AST, gestión de errores y formato de entrega. Muchas gracias por su atención."* |

---

## 💻 SECUENCIA DE COMANDOS EXACTOS PARA LA TERMINAL

Abre una terminal (**PowerShell** o **CMD**) en pantalla completa y ejecuta en orden:

### Paso 1: Entrar a la carpeta de la Actividad 6
```powershell
cd "C:\Users\erfierro\chingado\rigo\actividad_6"
```

### Paso 2: Ejecutar la suite completa por consola (CLI)
```powershell
python main.py
```
> **Puntos clave a señalar con el cursor durante el video:**
> 1. Sube al inicio del texto: Señala que la **primera instrucción** son los nombres de los 4 integrantes en orden alfabético por primer apellido.
> 2. Muestra los casos válidos:
>    - **Caso 01 (Oficial):** `class MiClase { int miMetodo(int a, float b) { } void otroMetodo() { } }` -> Estado [CORRECTO] y Árbol AST.
>    - **Caso 02:** Clase con atributos de instancia y métodos de cálculo (`base`, `altura`, `calcularArea`).
>    - **Caso 03:** Múltiples clases en un solo archivo (`Punto`, `Circulo`).
> 3. Muestra los casos inválidos y sus diagnósticos:
>    - **Caso 07 (Oficial 1):** `int miMetodo(int a float b)` -> *Error: Parámetro inválido en la declaración de método*.
>    - **Caso 08 (Oficial 2):** `void otroMetodo {` -> *Error: Falta paréntesis en la declaración de método*.
>    - **Caso 09 (Oficial Rúbrica):** `class MiClase int x;` -> *Error: Cuerpo de clase inválido en la declaración de 'class'*.
>    - **Caso 10 (Oficial Rúbrica):** `123 miMetodo(...)` -> *Error: Tipo de retorno inválido en la declaración de método*.
>    - **Caso 11 (Oficial Rúbrica):** `void procesar(int)` -> *Error: Parámetro inválido en la declaración de método*.
> 4. Baja al final del texto: Señala que la **última instrucción** vuelve a imprimir las firmas de los integrantes.

---

### Paso 3: Ejecutar la Interfaz Gráfica (GUI)
```powershell
python gui.py
```
> **Puntos clave a mostrar en la GUI:**
> 1. Encabezado superior con los 4 integrantes y datos de la materia.
> 2. En el desplegable **"Cargar Caso de Prueba"**, selecciona:
>    - `[VÁLIDO] Caso 01: Caso Válido Oficial: Definición de Clases y Métodos Estándar`
>    - Clic en el botón verde **`▶ ANALIZAR SINTAXIS`**.
>    - Muestra la pestaña **`🌳 Árbol Sintáctico (AST)`** y luego la pestaña **`🔍 Tokens Léxicos`**.
> 3. En el desplegable, selecciona:
>    - `[INVÁLIDO] Caso 07: Caso Inválido Oficial 1: Falta de Coma entre Parámetros`
>    - Clic en **`▶ ANALIZAR SINTAXIS`**.
>    - Observa cómo se activa la pestaña **`❌ Errores Sintácticos`** mostrando la tabla de diagnóstico.
> 4. En el desplegable, selecciona:
>    - `[INVÁLIDO] Caso 08: Caso Inválido Oficial 2: Faltan Paréntesis en Declaración de Método`
>    - Clic en **`▶ ANALIZAR SINTAXIS`** -> Muestra la fila con el error de falta de paréntesis.
> 5. Cierra la ventana de la GUI.

---

## 📤 SUBIDA A YOUTUBE Y REPORTE FINAL
1. Guarda el video en formato **MP4** con resolución mínima de 720p o 1080p.
2. Súbelo a YouTube configurándolo como **"No listado"** (Unlisted) o **"Público"**.
3. Abre el archivo Word generado:
   `DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A6_SintacticoMetodosYClases.docx`
4. En la **Sección 1**, sustituye `https://www.youtube.com/watch?v=TU_ENLACE_AQUI` por el enlace público real de tu video.
5. Guarda como **PDF** desde Word (`Archivo > Guardar como > Formato PDF`) para entregar el archivo único solicitado.
