# GUÍA Y GUION CRONOMETRADO PARA LA GRABACIÓN DEL VIDEO DEMOSTRATIVO
## Actividad 13: Generación de Código (Traducción a Código Máquina y Entorno de Ejecución)
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Integrantes (Estricto Orden Alfabético por Primer Apellido):**
1. Díaz Torres Jazmín Montserrat
2. Fierro Meléndez Ernesto Hatuey
3. Hernández García Héctor Gabriel
4. Millán Guerrero Oswaldo Josué

---

## ⚠️ REQUISITOS OBLIGATORIOS DE LA RÚBRICA ANTES DE GRABAR
1. **Duración:** No mayor a **5 minutos** (Tiempo ideal recomendado: **3:45 a 4:30 minutos**).
2. **Resolución:** Mínimo **720p** (1080p recomendado).
3. **Audio:** Explicación clara con micrófono.
4. **Pantalla Completa:** Es **ESTRICTAMENTE OBLIGATORIO** que se visualice la pantalla completa de Windows, incluyendo la **barra de tareas con la fecha y hora del sistema** durante todo el video.
5. **Software para grabar recomendado:**
   - **Xbox Game Bar (Integrado en Windows):** Presiona `Windows + Alt + R` para iniciar y terminar la grabación.
   - **OBS Studio:** Captura de pantalla completa.

---

## ⏱️ GUION PASO A PASO CRONOMETRADO (TOTAL: 4 MINUTOS Y MEDIO)

### MINUTO 0:00 - 0:40 | INTRODUCCIÓN Y OBJETIVO
* **Qué mostrar en pantalla:**
  - Abre el documento de reporte oficial (PDF o Word) o el archivo `main.py` en tu editor de código (VS Code, Cursor, etc.).
  - Asegúrate de que la fecha y hora de la barra de tareas de Windows sea claramente visible.
* **Qué decir:**
  > "Buen día profesor Rigoberto Cárdenas Larios y compañeros. A continuación presentamos la demostración de la Actividad 13: Generación de Código, correspondiente a la materia de Traductores de Lenguaje.  
  > Los integrantes del equipo en orden alfabético por primer apellido somos:  
  > 1. Díaz Torres Jazmín Montserrat  
  > 2. Fierro Meléndez Ernesto Hatuey  
  > 3. Hernández García Héctor Gabriel  
  > 4. Millán Guerrero Oswaldo Josué.  
  >  
  > El objetivo de esta práctica es transformar el código intermedio en código máquina ejecutable por un procesador objetivo. Implementamos el mapeo de instrucciones, optimizaciones como encadenamiento de registros, asignación de memoria física en los rangos 0x1000, 0x2000 y 0x3000, generación de ejecutables binarios con cabecera estándar y emulación en un entorno de ejecución."

---

### MINUTO 0:40 - 1:30 | EXPLICACIÓN DE ARQUITECTURA Y REGLAS
* **Qué mostrar en pantalla:**
  - Muestra rápidamente los archivos del proyecto (`intermediate_code.py`, `code_generator.py`, `symbol_table_mem.py`, `executable_format.py`, `virtual_machine.py`).
  - Resalta el comentario obligatorio al inicio de cada clase con los 4 nombres en orden alfabético.
* **Qué decir:**
  > "El proyecto consta de módulos desacoplados y cada clase contiene al inicio los nombres del equipo.  
  > 1. En `intermediate_code.py` modelamos cuádruplos de tres direcciones (TAC).  
  > 2. En `code_generator.py` implementamos el conjunto de instrucciones del procesador: LOAD, STORE, ADD, SUB, MUL, DIV, CMP, saltos JMP, JZ, JGT y HALT. Incluimos el optimizador que encadena operaciones directamente en el registro R1 para eliminar temporales innecesarios.  
  > 3. En `symbol_table_mem.py` asignamos direcciones hexadecimales de 4 bytes: 0x1000 para código, 0x2000 para datos y 0x3000 para resultados.  
  > 4. En `executable_format.py` generamos binarios empaquetados con cabecera de 32 bytes con la firma 'MVCO', entry point y Checksum CRC32.  
  > 5. Y en `virtual_machine.py` emulamos el hardware con ciclo Fetch-Decode-Execute."

---

### MINUTO 1:30 - 2:45 | EJECUCIÓN EN CONSOLA (CLI - `main.py`)
* **Comando a ejecutar en PowerShell / CMD:**
  ```powershell
  cd "C:\Users\erfierro\chingado\rigo\actividad_13"
  python main.py
  ```
* **Qué mostrar y decir:**
  1. **Inicio de la salida:**
     > "Como primera instrucción obligatoria en el main, imprimimos los nombres completos de los integrantes en estricto orden alfabético por primer apellido."
  2. **Caso 01 (Mapeo Directo de la Práctica):**
     > "En el Caso 1 observamos la traducción del ejemplo oficial de la rúbrica: t1 = a + b, t2 = t1 * c, result = t2. Vemos cómo se asignan las direcciones 0x1000, 0x1004, 0x1008 y 0x100C, y cómo la máquina virtual ejecuta las instrucciones arrojando el resultado exacto de 30."
  3. **Caso 02 (Optimización por Encadenamiento):**
     > "En el Caso 2 se aplica la optimización de encadenamiento de registros pedida por el profesor. El optimizador reduce de 10 a 6 instrucciones, logrando un 40% de mejora en eficiencia al reutilizar el registro R1."
  4. **Caso 03 y 04 (Saltos y Bucles):**
     > "El Caso 3 demuestra la resolución de etiquetas de saltos condicionales IF-ELSE (CMP, JGT, JMP). El Caso 4 ejecuta un bucle iterativo WHILE con saltos hacia atrás calculando un acumulador iterativo hasta alcanzar 10."
  5. **Caso 05 (Pipeline Completo):**
     > "El Caso 5 compila código fuente completo desde el análisis léxico y sintáctico hasta código máquina y ejecución final."
  6. **Casos Inválidos (Casos 6 al 10):**
     > "Para garantizar los 20 puntos de pruebas válidas e inválidas, los Casos 6 al 10 demuestran la captura de errores: salto a etiqueta no definida, variables no asignadas, división por cero en hardware, violación de memoria y rechazo de ejecutables corruptos."
  7. **Pie de consola:**
     > "Como última instrucción del main, se vuelven a imprimir los nombres del equipo en orden alfabético."

---

### MINUTO 2:45 - 3:45 | DEMOSTRACIÓN DE LA INTERFAZ GRÁFICA (GUI)
* **Comando a ejecutar:**
  ```powershell
  python gui.py
  ```
* **Qué mostrar y decir:**
  1. **Encabezado:**
     > "Mostramos la interfaz gráfica interactiva desarrollada en Tkinter con el banner institucional y los nombres del equipo."
  2. **Pestaña 1 (Entrada) y 2 (TAC):**
     > "Seleccionamos el Caso 1 y pulsamos 'Compilar y Mapear'. En la pestaña de Código Intermedio vemos los cuádruplos generados en una tabla interactiva."
  3. **Pestaña 3 (Código Máquina):**
     > "En la pestaña 3 vemos la comparativa lado a lado del código estándar contra el código optimizado y las métricas de ganancia en instrucciones."
  4. **Pestaña 4 (Tabla de Símbolos y Memoria):**
     > "En la pestaña 4 se aprecian las variables mapeadas en las direcciones físicas 0x2000 y 0x3000 con sus tipos y valores."
  5. **Pestaña 5 (Emulador de CPU / Máquina Virtual):**
     > "En la pestaña 5 pulsamos 'Paso a Paso (Step)' o 'Ejecutar VM Completa'. Vemos cómo se actualiza el Program Counter, los registros R1..R8, las banderas ZF y SF, y el volcado de memoria RAM en tiempo real."
  6. **Exportación:**
     > "Presionamos 'Exportar .bin / .asm' para generar el archivo binario ejecutable y su desensamblado legible."

---

### MINUTO 3:45 - 4:15 | EJECUTABLE PARA EL SISTEMA OPERATIVO Y CONCLUSIÓN
* **Comando a ejecutar en la consola:**
  ```powershell
  .\run_program.bat ejecutables\caso_01_mapeo_instrucciones.bin
  ```
* **Qué mostrar y decir:**
  > "Finalmente, probamos el cargador de ejecutables para el sistema operativo mediante el archivo por lotes `run_program.bat`. El sistema operativo carga el binario `.bin`, verifica la cabecera, mapea la memoria y corre el programa de forma autónoma.  
  > Con esto cubrimos el 100% de los requerimientos de la Actividad 13. Agradecemos su atención."
* **Detén la grabación (Windows + Alt + R).**

---

## 🚀 PASOS FINALES PARA LA ENTREGA
1. Sube el video grabado a YouTube (puedes ponerlo como **No listado** o **Público**).
2. Abre `actividad_13/generate_report_helper.py` y `actividad_13/export_pdf.py` y reemplaza la variable `VIDEO_URL` con tu enlace real de YouTube:
   ```python
   VIDEO_URL = "https://youtu.be/TU_ENLACE_AQUI"
   ```
3. Ejecuta ambos scripts para regenerar el PDF y Word finales actualizados:
   ```powershell
   python generate_report_helper.py
   python export_pdf.py
   ```
4. Sube a la plataforma de entrega el archivo PDF único:
   `DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A13_GeneracionCodigo.pdf`

