# GUÍA Y GUION DETALLADO PARA GRABACIÓN DE VIDEO DEMOSTRATIVO
## ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Semestre:** 2026-B | CUCEI - Universidad de Guadalajara  

---

### INTEGRANTES DEL EQUIPO (Orden Alfabético por Primer Apellido):
1. **DÍAZ TORRES JAZMÍN MONTSERRAT**
2. **FIERRO MELÉNDEZ ERNESTO HATUEY**
3. **HERNÁNDEZ GARCÍA HÉCTOR GABRIEL**
4. **MILLÁN GUERRERO OSWALDO JOSUÉ**

---

## ⚠️ REQUISITOS CRÍTICOS DE LA RÚBRICA OFICIAL
- **Duración Máxima:** Menor o igual a **5 minutos** (ideal: 3:30 - 4:30 min).
- **Resolución:** Mínimo **720p** (recomendado: 1080p).
- **Audio:** Voz clara con micrófono.
- **Pantalla Completa:** Debe grabarse la pantalla completa de Windows, mostrando en todo momento la **fecha y hora** de la barra de tareas en la esquina inferior derecha.
- **Contenido Obligatorio:**
  1. Introducción y objetivo de la práctica.
  2. Demostración en ejecución (interfaz gráfica `gui.py` y consola `main.py`).
  3. Explicación de la gramática y reglas sintácticas.
  4. Código legible con comentarios y nombres de los integrantes.

---

## CRONOGRAMA MINUTO A MINUTO (DURACIÓN TOTAL ESTIMADA: 4:15 MIN)

```
0:00 ── 0:45  [Fase 1] Carátula, Presentación del Equipo y Objetivos
0:45 ── 1:45  [Fase 2] Explicación de la Gramática y Reglas en el Código
1:45 ── 3:15  [Fase 3] Demostración en Vivo en la Interfaz Gráfica (Tkinter)
3:15 ── 4:00  [Fase 4] Ejecución de la Batería en Consola (Salida_Ejecucion_Consola.txt)
4:00 ── 4:15  [Fase 5] Conclusiones y Despedida
```

---

### FASE 1: INTRODUCCIÓN Y PRESENTACIÓN (0:00 - 0:45)
- **Qué mostrar en pantalla:** Ventana de VS Code o navegador con el PDF del reporte abierto en la portada donde se observan los nombres del equipo. En la esquina inferior derecha debe verse la fecha y hora del sistema.
- **Qué decir:**
  > *"Buen día profesor Rigoberto Cárdenas y compañeros. Presentamos la Actividad 5 de la materia Traductores de Lenguaje, correspondiente al Análisis Sintáctico de Estructuras de Control para un subconjunto del Lenguaje C.*  
  > *Nuestro equipo está conformado, en orden alfabético por primer apellido, por:*  
  > *1. Jazmín Montserrat Díaz Torres*  
  > *2. Ernesto Hatuey Fierro Meléndez*  
  > *3. Héctor Gabriel Hernández García*  
  > *4. Oswaldo Josué Millán Guerrero.*  
  > *El objetivo principal de esta práctica es implementar un analizador sintáctico descendente recursivo capaz de reconocer condicionales if-else y bucles while y for, garantizando la exigencia de bloques entre llaves obligatorias y una gestión robusta de errores sintácticos con recuperación en modo pánico."*

---

### FASE 2: EXPLICACIÓN DE LA GRAMÁTICA Y CÓDIGO FUENTE (0:45 - 1:45)
- **Qué mostrar en pantalla:** El archivo `parser.py` en VS Code. Resaltar:
  1. El comentario inicial con los nombres completos en orden alfabético.
  2. Los métodos `_if_statement()`, `_while_statement()`, `_for_statement()` y `_block()`.
  3. El manejo de errores con `SyntaxErrorHandler` y el método `synchronize()` (Panic Mode).
- **Qué decir:**
  > *"La gramática formal implementada en `parser.py` sigue rigurosamente la rúbrica oficial:*  
  > *• Sentencia if: 'if' '(' expresion ')' '{' bloque '}' seguido opcionalmente de 'else' '{' bloque '}'.*  
  > *• Sentencia while: 'while' '(' expresion ')' '{' bloque '}'.*  
  > *• Sentencia for: 'for' '(' init ';' cond ';' update ')' '{' bloque '}'.*  
  > *Una regla fundamental de nuestra implementación es que todo bloque debe estar estrictamente acotado entre llaves obligatorias. Si un usuario escribe un `if` de una sola línea sin llaves, nuestro analizador reporta un error sintáctico específico indicando la necesidad de llaves.*  
  > *Asimismo, el parser cuenta con recuperación en modo pánico sincronizando en puntos y comas o llaves de cierre para continuar el análisis de errores subsiguientes sin colapsar."*

---

### FASE 3: DEMOSTRACIÓN DE LA INTERFAZ GRÁFICA (1:45 - 3:15)
- **Qué mostrar en pantalla:** Ejecutar en terminal: `python gui.py`. Se abrirá la ventana de Tkinter con el selector de casos de prueba.
- **Acciones y Qué decir:**
  1. **Seleccionar Caso #01 (if-else válido):**
     > *"Iniciamos con el caso #1 de la rúbrica: un if-else clásico. Damos clic en 'Analizar Sintaxis' y observamos en la pestaña de la derecha cómo se genera el Árbol de Sintaxis Abstracta (AST), mostrando la rama de la condición, el Bloque Then y el Bloque Else con sus respectivas asignaciones."*
  2. **Seleccionar Caso #03 (bucle for válido):**
     > *"En el caso #3 evaluamos un bucle for tradicional. El AST desglosa claramente la inicialización, la condición de parada y la expresión de actualización."*
  3. **Seleccionar Caso #06 (Error en if: falta paréntesis de cierre):**
     > *"Pasamos a los casos de error. En el caso #6 tenemos `if (x > 0 {` donde omitimos el paréntesis de cierre. El analizador detecta la discrepancia, se posiciona en la línea 1 y columna 10, y genera un diagnóstico claro con sugerencia de corrección."*
  4. **Seleccionar Caso #09 (Error en if: bloque sin llaves):**
     > *"El caso #9 es crucial: `if (x > 0) x = x + 1;` sin llaves. Como exige la rúbrica, se reporta inmediatamente: 'Error: Bloque de sentencias faltante o sin llaves en la estructura if en la línea 2, columna 5'."*
  5. **Seleccionar Caso #10 (Error en while: llave de cierre faltante):**
     > *"En el caso #10 abrimos un bloque de while con '{' pero nunca lo cerramos. El manejador de errores reporta 'Llave de cierre faltante en bloque', recordando la línea exacta donde se abrió el bloque."*

---

### FASE 4: EJECUCIÓN EN CONSOLA Y ARCHIVO DE SALIDA (3:15 - 4:00)
- **Qué mostrar en pantalla:** Abrir la terminal de PowerShell y ejecutar:
  ```powershell
  python main.py
  ```
- **Qué decir:**
  > *"Ahora ejecutamos `python main.py` en la terminal. Como lo exige la rúbrica:*  
  > *1. La primera instrucción en consola imprime los nombres completos de los integrantes en orden alfabético por primer apellido.*  
  > *2. Se ejecutan los 10 casos de prueba (5 válidos y 5 con errores sintácticos controlados), logrando un 100% de tasa de aprobación.*  
  > *3. La última instrucción de salida vuelve a imprimir los nombres completos en orden alfabético.*  
  > *Toda esta ejecución se vuelca automáticamente en el archivo `Salida_Ejecucion_Consola.txt` para respaldo del profesor."*

---

### FASE 5: CONCLUSIÓN Y CIERRE (4:00 - 4:15)
- **Qué mostrar en pantalla:** El archivo `DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A5_SintacticoEstructurasControl.pdf` generado.
- **Qué decir:**
  > *"Con esto demostramos el correcto funcionamiento del analizador sintáctico para estructuras de control y la entrega íntegra del reporte PDF formal. Muchas gracias por su atención."*

---

## RECOMENDACIONES TÉCNICAS PARA OBS / GRABADOR DE PANTALLA:
1. En OBS Studio o la barra de juegos de Windows (Win + G), selecciona **"Capturar Pantalla Completa"** (Display Capture), **NO** capturar ventana individual, para que el reloj y calendario de Windows permanezcan visibles.
2. Verifica que el micrófono no esté saturado y mantén el puntero del mouse señalando los elementos que vas describiendo.
3. Al terminar, sube el video a YouTube en modo **"No listado"** (Unlisted) o **"Público"** (Public) y copia la URL en la portada del reporte.
