# GUÍA Y GUION DETALLADO PARA GRABACIÓN DE VIDEO DEMOSTRATIVO
## ACTIVIDAD 10: CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
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
  3. Explicación de las reglas de código intermedio (temporales para constantes, expresiones aritméticas, lógicas y guardas).
  4. Código legible con comentarios y nombres de los integrantes.

---

## CRONOGRAMA MINUTO A MINUTO (DURACIÓN TOTAL ESTIMADA: 4:15 MIN)

```
0:00 ── 0:45  [Fase 1] Carátula, Presentación del Equipo y Objetivos
0:45 ── 1:45  [Fase 2] Explicación del Código: Generador TAC y Guardas
1:45 ── 3:15  [Fase 3] Demostración en Vivo en la Interfaz Gráfica (Tkinter)
3:15 ── 4:00  [Fase 4] Ejecución de la Batería en Consola (Salida_Ejecucion_Consola.txt)
4:00 ── 4:15  [Fase 5] Conclusiones y Reporte PDF
```

---

### FASE 1: INTRODUCCIÓN Y PRESENTACIÓN (0:00 - 0:45)
- **Qué mostrar en pantalla:** Portada del reporte PDF en pantalla completa, mostrando en la esquina inferior derecha la fecha y hora del sistema Windows.
- **Qué decir:**
  > *"Buen día profesor Rigoberto Cárdenas y compañeros. Presentamos la Actividad 10 de la materia Traductores de Lenguaje, enfocada en la Generación de Código Intermedio de Tres Direcciones (Three-Address Code - TAC).*  
  > *Nuestro equipo está integrado, en orden alfabético estricto por primer apellido, por:*  
  > *1. Jazmín Montserrat Díaz Torres*  
  > *2. Ernesto Hatuey Fierro Meléndez*  
  > *3. Héctor Gabriel Hernández García*  
  > *4. Oswaldo Josué Millán Guerrero.*  
  > *El objetivo principal es traducir asignaciones, constantes y expresiones aritméticas y lógicas en instrucciones lineales de tres direcciones, asignando cada constante a una etiqueta temporal e introduciendo guardas de validación."*

---

### FASE 2: EXPLICACIÓN DE LA ARQUITECTURA EN EL CÓDIGO (0:45 - 1:45)
- **Qué mostrar en pantalla:** El archivo `tac_generator.py` y `tac_instruction.py` en VS Code. Resaltar:
  1. El comentario inicial con los nombres completos en orden alfabético.
  2. El método `_gen_assignment_core` que genera la asignación de constantes mediante etiquetas temporales (`t1 = 5; x = t1`).
  3. La inserción de instrucciones de guarda:
     - `if b == 0 then error "Division by zero"`
     - `if type(a) != integer or type("string") != integer then error "Type mismatch"`
- **Qué decir:**
  > *"En `tac_generator.py` implementamos con exactitud las especificaciones de la rúbrica:*  
  > *• Cada constante se aloja primero en una etiqueta temporal intermedia antes de asignarse a la variable destino.*  
  > *• Las expresiones aritméticas y lógicas anidadas se aplanan en operaciones atómicas de máximo dos operandos.*  
  > *• En operaciones de división o cuando se detectan tipos dispares, el compilador emite instrucciones de guarda que validan los operandos antes de proceder."*

---

### FASE 3: DEMOSTRACIÓN DE LA INTERFAZ GRÁFICA (1:45 - 3:15)
- **Qué mostrar en pantalla:** Ejecutar en terminal: `python gui.py`. Se abrirá la ventana de Tkinter con la salida TAC.
- **Acciones y Qué decir:**
  1. **Seleccionar Caso #01 (Asignación de constantes a variables):**
     > *"Iniciamos con el caso #1 de la rúbrica: `x = 5; y = 10;`. Al dar clic en 'Generar Código Intermedio', observen cómo se generan las instrucciones con comentarios explicativos: `t1 = 5`, `x = t1`, `t2 = 10`, `y = t2`."*
  2. **Seleccionar Caso #03 (Expresión aritmética agrupada):**
     > *"En el caso #3 tenemos `result = a * (b + c);`. El generador desglosa la suma interna en `t1 = b + c`, luego la multiplicación en `t2 = a * t1`, y finalmente `result = t2`."*
  3. **Seleccionar Caso #04 (Expresiones lógicas y comparaciones):**
     > *"En el caso #4 probamos `flag = (x > y) && (z < 10);`. Se aplanan las comparaciones en `t1 = x > y` y `t3 = z < t2`, para luego combinarlas con la operación lógica AND."*
  4. **Seleccionar Caso #06 (Validación de división por cero con guarda):**
     > *"En el caso #6 evaluamos `result = a / b;`. Observen la instrucción de guarda emitida: `if b == 0 then error 'Division by zero'` antes de ejecutar la división en `t1 = a / b`."*
  5. **Seleccionar Caso #07 (Error de tipos: a + 'string'):**
     > *"En el caso #7 evaluamos la operación inválida `total = a + 'string';`. El generador emite la guarda de discrepancia de tipos y bloquea la operación para proteger la fase de ejecución."*

---

### FASE 4: EJECUCIÓN EN CONSOLA Y ARCHIVO DE SALIDA (3:15 - 4:00)
- **Qué mostrar en pantalla:** Abrir PowerShell y ejecutar:
  ```powershell
  python main.py
  ```
- **Qué decir:**
  > *"Ejecutamos `python main.py`. Noten que:*  
  > *1. La primera instrucción en consola imprime los nombres completos de los integrantes en orden alfabético por primer apellido.*  
  > *2. Se ejecutan los 10 casos de prueba, obteniendo 100% de tasa de éxito.*  
  > *3. La última instrucción de salida vuelve a imprimir los nombres del equipo.*  
  > *Toda esta salida queda respaldada en `Salida_Ejecucion_Consola.txt`."*

---

### FASE 5: CONCLUSIÓN Y REPORTE PDF (4:00 - 4:15)
- **Qué mostrar en pantalla:** El archivo `DiazTorresJazmin_..._A10_CodigoIntermedio.pdf`.
- **Qué decir:**
  > *"Concluimos mostrando el reporte formal en PDF generado. Esta actividad se integra perfectamente con la Actividad 13 para la generación de código máquina final. Muchas gracias por su atención."*

---

## RECOMENDACIONES TÉCNICAS:
1. Graba con OBS Studio o la barra de juegos de Windows (Win + G) seleccionando **"Pantalla Completa"** para asegurar la visibilidad del reloj de Windows.
2. Al subir a YouTube, coloca el enlace en la portada del reporte PDF.
