# GUÍA Y COMANDOS PARA LA GRABACIÓN DEL VIDEO DEMOSTRATIVO
## Actividad 4: Análisis Sintáctico de Expresiones Aritméticas y Lógicas
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Fecha de Entrega:** 11 de septiembre, 23:59  
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
3. **Audio:** Voz clara con micrófono explicando el objetivo, reglas y funcionamiento.
4. **Pantalla completa obligatoria:** Se debe grabar toda la pantalla del equipo de cómputo donde se aprecie claramente la **barra de tareas de Windows con la fecha y hora** del sistema.
5. **Código y salida legibles:** Tamaño de fuente adecuado en terminal y GUI.
6. **Software de grabación sugerido:**
   - **Xbox Game Bar (Windows nativo):** Presiona `Windows + Alt + R` para iniciar y detener.
   - **OBS Studio:** Captura de pantalla completa sin recortar bordes.

---

## 🕒 CRONOGRAMA MINUTO A MINUTO (GUION DE GRABACIÓN)

| Tiempo | Sección | Acción en Pantalla | Qué decir (Guion de voz) |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:30** | Introducción | Pantalla completa con reloj visible. Terminal abierta en `actividad_4`. | *"Buen día, profesor Rigoberto Cárdenas. Somos el equipo integrado por Jazmín Díaz, Ernesto Fierro, Héctor Hernández y Oswaldo Millán. Presentamos la Actividad 4: Análisis sintáctico de expresiones aritméticas y lógicas. Nuestro objetivo es implementar la fase de parsing con construcción de AST y gestión de errores con la gramática libre de contexto requerida."* |
| **0:30 - 1:45** | Ejecución CLI (`main.py`) | Ejecutar `python main.py` en la terminal. | *"Al ejecutar `main.py`, la primera instrucción obligatoria imprime las firmas de los integrantes en orden alfabético. Vemos la validación de las 4 expresiones oficiales: `x + y * 5`, `(a - b) / c`, `10 > 5 && 3 <= 4` y `(x + y) * (z - w)`, construyendo el Árbol de Sintaxis Abstracta con la precedencia exacta de operadores."* |
| **1:45 - 2:45** | Errores en CLI | Desplazarse por la terminal a la sección de casos inválidos. | *"En la sección de errores sintácticos, demostramos los casos solicitados: `x + * y` genera 'Error: Operador sin término en la línea 1, columna 3'; `10 >` genera 'Error: Comparación inválida en la línea 1, columna 4'; `(a - b` y `5 / (2 + )` reportan 'Error: Paréntesis desbalanceados' con número exacto de línea y columna. Al final de la salida, la última instrucción obligatoria vuelve a imprimir los integrantes del equipo."* |
| **2:45 - 4:15** | Demostración GUI (`gui.py`) | Ejecutar `python gui.py`. Mostrar interfaz gráfica. | *"Ahora ejecutamos la interfaz gráfica interactiva. En el encabezado apreciamos los datos del equipo. En el selector cargamos un caso válido como `10 > 5 && 3 <= 4` y damos clic en 'ANALIZAR SINTAXIS', apreciando el AST generado, la tabla de tokens y las reglas formales EBNF. Ahora seleccionamos el caso inválido `x + * y` y observamos cómo la tabla de errores detalla la ubicación, categoría y sugerencia pedagógica."* |
| **4:15 - 4:45** | Conclusión y Cierre | Mostrar de nuevo reloj del sistema y consola. | *"Concluimos verificando que el analizador cumple al 100% con los requerimientos de gramática, AST, gestión de errores y rúbrica de evaluación. Muchas gracias."* |

---

## 💻 SECUENCIA DE COMANDOS EXACTOS PARA LA TERMINAL

Abre una terminal (**PowerShell** o **CMD**) en pantalla completa y ejecuta:

### Paso 1: Ingresar a la carpeta de la Actividad 4
```powershell
cd "C:\Users\erfierro\chingado\rigo\actividad_4"
```

### Paso 2: Ejecutar la suite completa por consola (CLI)
```powershell
python main.py
```
> **Puntos clave a señalar en el video:**
> 1. Sube al inicio del texto: Señala que la **primera instrucción** son los nombres de los integrantes en orden alfabético.
> 2. Muestra los casos válidos oficiales:
>    - `x + y * 5` (Aritmética simple con precedencia de `*` sobre `+`).
>    - `(a - b) / c` (Agrupación con paréntesis y división).
>    - `10 > 5 && 3 <= 4` (Expresión lógica compuesta con operadores relacionales `>` y `<=` y conjunción `&&`).
>    - `(x + y) * (z - w)` (Multiplicación de expresiones agrupadas).
> 3. Muestra las tablas de errores de los casos inválidos oficiales:
>    - `x + * y` -> **Error: Operador sin término en la línea 1, columna 3.**
>    - `10 >` -> **Error: Comparación inválida en la línea 1, columna 4.**
>    - `(a - b` -> **Error: Paréntesis desbalanceados en la línea 1, columna 1.**
>    - `5 / (2 + )` -> **Error: Operador sin término / Paréntesis desbalanceados.**
> 4. Baja al final del texto: Señala que la **última instrucción** vuelve a imprimir los nombres completos de los integrantes en orden alfabético.

---

### Paso 3: Ejecutar la Interfaz Gráfica (GUI)
```powershell
python gui.py
```
> **Puntos clave a mostrar en la GUI (aprox. 1 minuto):**
> 1. Encabezado superior con los 4 integrantes y datos de la materia.
> 2. En **"Cargar Caso de Prueba"**, selecciona:
>    - `[VÁL] Caso 3: Expresión lógica relacional (10 > 5 && 3 <= 4) [Oficial]`
>    - Clic en **`▶ ANALIZAR SINTAXIS`**.
>    - Muestra la pestaña **`🌳 Árbol Sintáctico (AST)`** y la pestaña **`🔍 Tokens Léxicos`**.
> 3. En **"Cargar Caso de Prueba"**, selecciona:
>    - `[INV] Caso 1: Operador sin término (x + * y) [Oficial]`
>    - Clic en **`▶ ANALIZAR SINTAXIS`**.
>    - Cambia a la pestaña **`❌ Errores Sintácticos`** para mostrar la tabla con Línea, Columna, Token, Mensaje y Sugerencia.
> 4. En **"Cargar Caso de Prueba"**, selecciona:
>    - `[INV] Caso 2: Comparación incompleta (10 >) [Oficial]`
>    - Clic en **`▶ ANALIZAR SINTAXIS`** -> Muestra el error de comparación inválida.
> 5. Cierra la ventana.

---

## 📤 SUBIDA A YOUTUBE Y REPORTE
1. Guarda el video en formato **MP4** con resolución 720p o 1080p.
2. Súbelo a YouTube configurándolo como **"No listado"** (Unlisted) o **"Público"**.
3. Copia el enlace obtenido y pégalo en la Sección 1 del documento Word:
   `DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A4_AnalisisSintacticoExpresionesAritmeticasLogicas.docx`
4. Guarda como **PDF** desde Word (`Archivo > Guardar como > Formato PDF`) para entregar el archivo único solicitado.
