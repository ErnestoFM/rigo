# GUÍA Y GUION DETALLADO PARA GRABACIÓN DE VIDEO DEMOSTRATIVO
## ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - EXPRESIONES ARITMÉTICAS Y LÓGICAS
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
  3. Explicación de la validación de expresiones aritméticas, lógicas y conversiones de tipo.
  4. Código legible con comentarios y nombres de los integrantes.

---

## CRONOGRAMA MINUTO A MINUTO (DURACIÓN TOTAL ESTIMADA: 4:15 MIN)

```
0:00 ── 0:45  [Fase 1] Carátula, Presentación del Equipo y Objetivos
0:45 ── 1:45  [Fase 2] Explicación del Código: Reglas y Validador Semántico
1:45 ── 3:15  [Fase 3] Demostración en Vivo en la Interfaz Gráfica (Tkinter)
3:15 ── 4:00  [Fase 4] Ejecución de la Batería en Consola (Salida_Ejecucion_Consola.txt)
4:00 ── 4:15  [Fase 5] Conclusiones y Reporte PDF
```

---

### FASE 1: INTRODUCCIÓN Y PRESENTACIÓN (0:00 - 0:45)
- **Qué mostrar en pantalla:** Portada del reporte PDF en pantalla completa, mostrando en la esquina inferior derecha la fecha y hora del sistema Windows.
- **Qué decir:**
  > *"Buen día profesor Rigoberto Cárdenas y compañeros. Presentamos la Actividad 8 de la materia Traductores de Lenguaje, correspondiente a la Validación Semántica de Expresiones Aritméticas, Lógicas y Conversiones de Tipo para C.*  
  > *Nuestro equipo está conformado, en estricto orden alfabético por primer apellido, por:*  
  > *1. Jazmín Montserrat Díaz Torres*  
  > *2. Ernesto Hatuey Fierro Meléndez*  
  > *3. Héctor Gabriel Hernández García*  
  > *4. Oswaldo Josué Millán Guerrero.*  
  > *El objetivo principal es asegurar que los operadores matemáticos y lógicos se apliquen únicamente sobre tipos válidos y compatibles, detectar división por cero en compilación y controlar conversiones explícitas como static_cast."*

---

### FASE 2: EXPLICACIÓN DE LA ARQUITECTURA EN EL CÓDIGO (0:45 - 1:45)
- **Qué mostrar en pantalla:** El archivo `semantic_analyzer.py` y `ast_nodes.py` en VS Code. Resaltar:
  1. El comentario inicial con los nombres completos en orden alfabético.
  2. Los métodos `_validate_binary_op` y `_validate_unary_op`.
  3. Las comprobaciones de tipos:
     - `left_t == 'string' or right_t == 'string'` en aritmética $\rightarrow$ Error de tipo no numérico.
     - `left_t != 'bool' or right_t != 'bool'` en operadores lógicos `&&` y `||` $\rightarrow$ Error de operando no booleano.
     - `r_val == 0` en divisiones $\rightarrow$ Error de división por cero.
- **Qué decir:**
  > *"En `semantic_analyzer.py` implementamos las reglas formales de la rúbrica:*  
  > *• En operaciones aritméticas (`+`, `-`, `*`, `/`), ambos operandos deben ser numéricos; si alguno es cadena o booleano, se emite un error semántico.*  
  > *• Además, evaluamos en tiempo de compilación el denominador; si es cero, se reporta inmediatamente una división por cero.*  
  > *• En operadores lógicos (`&&`, `||`, `!`), exigimos que ambos operandos sean de tipo bool.*  
  > *• En comparaciones relacionales (`==`, `<`, `>`), prohibimos comparar cadenas con números.*  
  > *• Y en conversiones explícitas (`static_cast`), validamos la coherencia entre el tipo origen y destino."*

---

### FASE 3: DEMOSTRACIÓN DE LA INTERFAZ GRÁFICA (1:45 - 3:15)
- **Qué mostrar en pantalla:** Ejecutar en terminal: `python gui.py`. Se abrirá la ventana de Tkinter.
- **Acciones y Qué decir:**
  1. **Seleccionar Caso #01 (Aritmética homogénea):**
     > *"Iniciamos con el caso #1 de la rúbrica: `int a = 10, b = 5; int resultado = a + b; int suma = 5 + 3;`. Damos clic en 'Validar Expresiones' y vemos en la tabla de símbolos los valores evaluados correctamente: 15 y 8."*
  2. **Seleccionar Caso #02 (Lógica booleana pura):**
     > *"En el caso #2 probamos `activo && inactivo` y `(10 > 5) && (3 < 8)`. Ambos evalúan sobre tipos bool generando False y True."*
  3. **Seleccionar Caso #05 (Conversión explícita con static_cast):**
     > *"En el caso #5 usamos `static_cast<float>(entero) + 2.5`. La conversión se valida con éxito y el resultado evaluado es 12.5."*
  4. **Seleccionar Caso #06 (Error: suma de número con cadena):**
     > *"Pasamos a los casos de error. En el caso #6 tenemos `edad + nombre` (int + string). El analizador conmuta a la pestaña de errores y reporta: 'Error: No se puede aplicar el operador aritmético '+' con una cadena de texto'."*
  5. **Seleccionar Caso #07 (Error: operador lógico con int):**
     > *"En el caso #7 evaluamos `true && 1`. Como exige la rúbrica, se reporta: 'El operador lógico '&&' requiere operandos booleanos; '1' no es un valor booleano'."*
  6. **Seleccionar Caso #08 (Error: comparación string con número):**
     > *"En el caso #8 evaluamos `('5' == 5)`. Se reporta: 'No se puede comparar una cadena con un número mediante '=='."*
  7. **Seleccionar Caso #09 (Error: división por cero):**
     > *"En el caso #9 tenemos `10 / 0`. El compilador detecta en tiempo estático la división por cero y previene el fallo en tiempo de ejecución."*

---

### FASE 4: EJECUCIÓN EN CONSOLA Y ARCHIVO DE SALIDA (3:15 - 4:00)
- **Qué mostrar en pantalla:** En PowerShell ejecutar:
  ```powershell
  python main.py
  ```
- **Qué decir:**
  > *"Ejecutamos `python main.py`. Observen que:*  
  > *1. La primera instrucción en consola imprime los nombres completos de los integrantes en orden alfabético por primer apellido.*  
  > *2. Se ejecutan los 10 casos de prueba, obteniendo 100% de tasa de aprobación.*  
  > *3. La última instrucción de salida vuelve a imprimir los nombres del equipo.*  
  > *Toda esta salida queda respaldada en `Salida_Ejecucion_Consola.txt`."*

---

### FASE 5: CONCLUSIÓN Y REPORTE PDF (4:00 - 4:15)
- **Qué mostrar en pantalla:** El archivo `DiazTorresJazmin_..._A8_SemanticoExpresionesAritmeticasLogicas.pdf`.
- **Qué decir:**
  > *"Concluimos mostrando el reporte formal en PDF con su carátula institucional, tablas de validación y conclusiones. Muchas gracias por su atención."*

---

## RECOMENDACIONES TÉCNICAS:
1. Graba con OBS Studio o la barra de juegos de Windows (Win + G) seleccionando **"Pantalla Completa"** para asegurar la visibilidad del reloj de Windows.
2. Al subir a YouTube, coloca el enlace en la portada del reporte PDF.
