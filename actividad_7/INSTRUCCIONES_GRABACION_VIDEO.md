# GUÍA Y GUION DETALLADO PARA GRABACIÓN DE VIDEO DEMOSTRATIVO
## ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
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
  3. Explicación de la estructura de la tabla de símbolos y reglas semánticas.
  4. Código legible con comentarios y nombres de los integrantes.

---

## CRONOGRAMA MINUTO A MINUTO (DURACIÓN TOTAL ESTIMADA: 4:15 MIN)

```
0:00 ── 0:45  [Fase 1] Carátula, Presentación del Equipo y Objetivos
0:45 ── 1:45  [Fase 2] Explicación del Código: Tabla de Símbolos y Ámbitos
1:45 ── 3:15  [Fase 3] Demostración en Vivo en la Interfaz Gráfica (Tkinter)
3:15 ── 4:00  [Fase 4] Ejecución de la Batería en Consola (Salida_Ejecucion_Consola.txt)
4:00 ── 4:15  [Fase 5] Conclusiones y Reporte PDF
```

---

### FASE 1: INTRODUCCIÓN Y PRESENTACIÓN (0:00 - 0:45)
- **Qué mostrar en pantalla:** Portada del reporte PDF en pantalla completa, mostrando en la esquina inferior derecha la fecha y hora del sistema Windows.
- **Qué decir:**
  > *"Buen día profesor Rigoberto Cárdenas y compañeros. Presentamos la Actividad 7 de la materia Traductores de Lenguaje, enfocada en el Análisis Semántico: Gestión de la Tabla de Símbolos, Verificación de Tipos de Datos y Control de Ámbitos para el Lenguaje C.*  
  > *Nuestro equipo está integrado, en orden alfabético estricto por primer apellido, por:*  
  > *1. Jazmín Montserrat Díaz Torres*  
  > *2. Ernesto Hatuey Fierro Meléndez*  
  > *3. Héctor Gabriel Hernández García*  
  > *4. Oswaldo Josué Millán Guerrero.*  
  > *El objetivo es gestionar la tabla de símbolos jerárquica con las funciones `inserten_simbolo` y `busquen_simbolo`, administrar ámbitos globales y locales, y verificar estrictamente los tipos de datos en declaraciones y asignaciones."*

---

### FASE 2: EXPLICACIÓN DE LA ARQUITECTURA EN EL CÓDIGO (0:45 - 1:45)
- **Qué mostrar en pantalla:** El archivo `symbol_table.py` y `semantic_analyzer.py` en VS Code. Resaltar:
  1. El comentario inicial con los nombres completos en orden alfabético.
  2. Las clases `Symbol`, `Scope` y `SymbolTable` con los métodos `inserten_simbolo` y `busquen_simbolo`.
  3. En `semantic_analyzer.py`, la función `are_types_compatible` que aplica la regla estricta de la rúbrica (evitando asignaciones cruzadas entre float e int sin conversión).
- **Qué decir:**
  > *"En `symbol_table.py` estructuramos la tabla de símbolos siguiendo el modelo especificado por la rúbrica: cada identificador almacena su tipo de dato, alcance (global o local), ámbito contenedor, nivel de anidamiento, valor asignado y coordenadas de línea y columna.*  
  > *Implementamos las funciones oficiales `inserten_simbolo` y `busquen_simbolo`, permitiendo que las búsquedas asciendan desde el ámbito local hacia el global.*  
  > *En `semantic_analyzer.py` implementamos la verificación estricta de tipos: si intentamos asignar un float a un int o un int a un float, o usar una variable no declarada, el analizador detecta y reporta el error semántico exacto."*

---

### FASE 3: DEMOSTRACIÓN DE LA INTERFAZ GRÁFICA (1:45 - 3:15)
- **Qué mostrar en pantalla:** Ejecutar en terminal: `python gui.py`. Se abrirá la ventana de Tkinter con la tabla de símbolos en vivo.
- **Acciones y Qué decir:**
  1. **Seleccionar Caso #01 (Asignaciones válidas de int):**
     > *"Iniciamos con el caso #1. Al dar clic en 'Analizar Semántica', la tabla de símbolos se puebla en vivo mostrando las variables 'a', 'b' y 'c' registradas en el ámbito global con sus valores evaluados 5, 10 y 15."*
  2. **Seleccionar Caso #02 (Ámbito global y local en función - Ejemplo Rúbrica):**
     > *"El caso #2 es el ejemplo exacto de la rúbrica: `int variable_global; void miFuncion() { int variable_local; ... }`. Observen cómo la tabla de símbolos distingue perfectamente: `variable_global` pertenece al alcance global (nivel 0), mientras que `variable_local` pertenece al alcance local de `miFuncion` (nivel 1)."*
  3. **Seleccionar Caso #06 (Error de tipo: float a int):**
     > *"Pasamos a los casos de error. En el caso #6 tenemos `int x; float y = 3.5; x = y;`. El analizador conmuta automáticamente a la pestaña de errores y reporta: 'Error: Tipo de dato incompatible en la asignación a x: se esperaba int pero se obtuvo float'."*
  4. **Seleccionar Caso #07 (Error de tipo: int a float):**
     > *"En el caso #7 evaluamos la asignación inversa: `int a; float b; b = a;`. Se detecta de inmediato la incompatibilidad entre int y float."*
  5. **Seleccionar Caso #08 (Identificador no declarado):**
     > *"En el caso #8 evaluamos `c = 10;`. Como 'c' no existe en la tabla de símbolos, se reporta: 'Error: Identificador c no declarado en la línea 1, columna 1'."*
  6. **Seleccionar Caso #09 (Acceso a variable local fuera de función):**
     > *"En el caso #9 intentamos acceder a `variable_local` fuera de `miFuncion()`. El sistema comprueba que no existe en el ámbito global y bloquea la operación."*

---

### FASE 4: EJECUCIÓN EN CONSOLA Y ARCHIVO DE SALIDA (3:15 - 4:00)
- **Qué mostrar en pantalla:** Abrir PowerShell y ejecutar:
  ```powershell
  python main.py
  ```
- **Qué decir:**
  > *"Ejecutamos `python main.py` en la terminal. Como lo exige la rúbrica:*  
  > *1. La primera instrucción en consola imprime los nombres completos de los integrantes en orden alfabético por primer apellido.*  
  > *2. Se ejecutan los 10 casos de prueba (5 válidos y 5 inválidos), obteniendo un 100% de tasa de éxito.*  
  > *3. La última instrucción de salida vuelve a imprimir los nombres del equipo.*  
  > *Toda esta salida se almacena automáticamente en `Salida_Ejecucion_Consola.txt`."*

---

### FASE 5: CONCLUSIÓN Y REPORTE PDF (4:00 - 4:15)
- **Qué mostrar en pantalla:** Mostrar el PDF oficial generado `DiazTorresJazmin_..._A7_SemanticoTablaSimbolosTipos.pdf`.
- **Qué decir:**
  > *"Finalmente, aquí mostramos el reporte formal en PDF generado, con su portada institucional, tablas completas, códigos fuente y bitácora de ejecución. Muchas gracias por su atención."*

---

## RECOMENDACIONES TÉCNICAS:
1. Graba con OBS Studio o la barra de juegos de Windows (Win + G) seleccionando **"Pantalla Completa"** para asegurar la visibilidad del reloj de Windows.
2. Al subir a YouTube, coloca el enlace en la portada del reporte PDF.
