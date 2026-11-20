# GUÍA Y GUION CRONOMETRADO PARA LA GRABACIÓN DEL VIDEO DEMOSTRATIVO
## Actividad 2: Manejo y Gestión de Errores Léxicos (Compilador Lenguaje C)
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Integrantes (Estricto Orden Alfabético por Primer Apellido):**
1. Díaz Torres Jazmín Montserrat
2. Fierro Meléndez Ernesto Hatuey
3. Hernández García Héctor Gabriel
4. Millán Guerrero Oswaldo Josué

---

## ⚠️ REQUISITOS OBLIGATORIOS DE LA RÚBRICA ANTES DE GRABAR
1. **Duración:** No mayor a **5 minutos** (Tiempo recomendado: **3:30 a 4:30 minutos**).
2. **Resolución:** Mínimo **720p** (1080p recomendado).
3. **Audio:** Voz clara con micrófono explicando la pantalla.
4. **Pantalla Completa:** Es **OBLIGATORIO** que se visualice la pantalla completa de Windows, incluyendo la **barra de tareas con la fecha y hora del sistema** durante todo el video.
5. **Software para grabar recomendado:**
   - **Xbox Game Bar (Windows):** Presiona `Windows + Alt + R` para iniciar y detener la grabación.
   - **OBS Studio:** Captura de pantalla completa.

---

## ⏱️ GUION PASO A PASO CRONOMETRADO (TOTAL: 4 MINUTOS)

### MINUTO 0:00 - 0:45 | INTRODUCCIÓN Y OBJETIVO
* **Qué mostrar en pantalla:**
  - Abre el documento de reporte oficial (PDF o Word) o el archivo `main.py` en tu editor de código.
  - Asegúrate de que la fecha y hora de la barra de tareas de Windows sea claramente visible.
* **Qué decir:**
  > "Buen día profesor Rigoberto Cárdenas Larios y compañeros. A continuación presentamos la demostración de la Actividad 2: Manejo de errores léxicos, correspondiente a la materia de Traductores de Lenguaje.  
  > Los integrantes del equipo en orden alfabético por primer apellido somos:  
  > 1. Díaz Torres Jazmín Montserrat  
  > 2. Fierro Meléndez Ernesto Hatuey  
  > 3. Hernández García Héctor Gabriel  
  > 4. Millán Guerrero Oswaldo Josué.  
  >  
  > El objetivo de esta práctica es implementar un mecanismo robusto para el manejo y reporte de errores léxicos durante la fase de análisis léxico en un compilador para el Lenguaje C desarrollado en Python, identificando caracteres no reconocidos, identificadores mal formados, números incorrectos y cadenas mal formadas."

---

### MINUTO 0:45 - 1:30 | EXPLICACIÓN DE ARQUITECTURA Y REGLAS DE ERROR
* **Qué mostrar en pantalla:**
  - Muestra rápidamente los archivos `lexer.py`, `token_type.py` y `error_handler.py`.
  - Resalta el comentario obligatorio al inicio de cada clase con los 4 nombres en orden alfabético.
* **Qué decir:**
  > "El analizador léxico está estructurado con las siguientes 4 reglas de errores léxicos:  
  > 1. Caracteres No Reconocidos: Símbolos fuera del alfabeto de C como $, @, ~, ¿, ñ.  
  > 2. Identificadores Mal Formados: Identificadores que inician erróneamente con dígitos como 123contador.  
  > 3. Literales Numéricos Incorrectos: Números con múltiples puntos flotantes (3.14.15), hexadecimales inválidos (0x12G4) o exponentes incompletos (1.5e+).  
  > 4. Cadenas Mal Formadas: Literales de texto que no cierran comillas antes de terminar la línea.  
  > Cada error incluye su número de línea, columna, descripción exacta y sugerencia de corrección."

---

### MINUTO 1:30 - 2:45 | EJECUCIÓN EN CONSOLA (CLI - `main.py`)
* **Comando a ejecutar en PowerShell / CMD:**
  ```powershell
  cd "C:\Users\erfierro\chingado\rigo\actividad_2"
  python main.py
  ```
* **Qué mostrar y decir:**
  1. **Inicio de la salida:**
     > "Como primera instrucción del main, se imprimen los nombres completos de los integrantes en estricto orden alfabético por primer apellido."
  2. **Caso 1 (Código C Válido de Control):**
     > "En el Caso 1 evaluamos un programa C válido con directivas de preprocesador (#include), palabras clave y printf. El resultado es 100% limpio con 0 errores léxicos."
  3. **Casos 2 al 5 (Errores Individuales):**
     > "Los casos 2 al 5 demuestran cada categoría de error: el caso 2 captura caracteres no reconocidos como el signo de dólar o arroba; el caso 3 aísla identificadores que inician con números; el caso 4 detecta números flotantes con doble punto o hexadecimales con letras fuera de A-F; y el caso 5 captura cadenas sin comilla de cierre."
  4. **Caso 6 (Evaluación Combinada) y Resumen:**
     > "El caso 6 junta todas las fallas en un solo módulo, generando un desglose estadístico completo con 100% de cumplimiento. Como última instrucción del programa, se imprimen nuevamente los nombres de los integrantes."

---

### MINUTO 2:45 - 3:45 | DEMOSTRACIÓN DE LA INTERFAZ GRÁFICA (GUI - `gui.py`)
* **Comando a ejecutar:**
  ```powershell
  python gui.py
  ```
* **Qué mostrar y decir:**
  1. **Encabezado:**
     > "Abrimos la interfaz gráfica interactiva en Tkinter donde se muestra el banner institucional y los nombres del equipo."
  2. **Selector de Casos:**
     > "Seleccionamos el Caso 1 y damos clic en 'Analizar Léxicamente'. Vemos cómo la tabla muestra los tokens generados con su línea, columna y categoría, arrojando 0 errores."
  3. **Demostración de Errores en GUI:**
     > "Seleccionamos ahora el Caso 6 con fallas combinadas y analizamos. La GUI cambia automáticamente a la pestaña 'Reporte de Errores Léxicos', mostrando la tabla con el lexema defectuoso, la descripción y la sugerencia de corrección."

---

### MINUTO 3:45 - 4:10 | CONCLUSIÓN
* **Qué decir:**
  > "Con esto se comprueba el cumplimiento satisfactorio de todos los lineamientos de la Actividad 2 para la calificación de 100 puntos. Agradecemos su atención."
* **Detén la grabación (Windows + Alt + R).**

---

## 🚀 PASOS FINALES PARA LA ENTREGA
1. Sube el video grabado a YouTube (público o no listado).
2. Pega el enlace en `generate_report_helper.py` y `export_pdf.py` en la variable `VIDEO_URL`.
3. Ejecuta ambos scripts para regenerar el reporte final con el enlace:
   ```powershell
   python generate_report_helper.py
   python export_pdf.py
   ```
4. Sube a la plataforma el PDF único:
   `DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A2_ManejoErroresLexicos.pdf`
