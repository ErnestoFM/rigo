# GUÍA Y COMANDOS PARA LA GRABACIÓN DEL VIDEO DEMOSTRATIVO
## Actividad 3: Análisis Sintáctico de Variables y Constantes
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Integrantes:**
1. Díaz Torres Jazmín Montserrat
2. Fierro Meléndez Ernesto Hatuey
3. Hernández García Héctor Gabriel
4. Millán Guerrero Oswaldo Josué

---

## ⚠️ REQUISITOS OBLIGATORIOS ANTES DE EMPEZAR A GRABAR
1. **Duración:** Menor a **5 minutos** (ideal: entre 3:30 y 4:30 min).
2. **Resolución:** Mínimo **720p** (preferiblemente 1080p).
3. **Audio:** Voz clara con micrófono explicando lo que se muestra.
4. **Pantalla completa:** Es **OBLIGATORIO** que se vea la pantalla completa de Windows, incluyendo la **barra de tareas con la fecha y hora** del sistema.
5. **Software para grabar recomendado:**
   - **Xbox Game Bar de Windows:** Presiona `Windows + Alt + R` para iniciar/detener grabación.
   - **OBS Studio:** Captura de pantalla completa.

---

## 💻 SECUENCIA DE COMANDOS EXACTOS

Abre una terminal (**PowerShell** o **CMD**) y sigue estos pasos:

### PASO 1: Entrar a la carpeta del proyecto
```powershell
cd "C:\Users\erfierro\chingado\rigo\actividad 1"
```

---

### PASO 2: Ejecutar la suite completa por consola (CLI)
Ejecuta el siguiente comando:
```powershell
python main.py
```

#### Qué mostrar y decir durante la ejecución de `main.py`:
1. **Inicio:**
   - Sube la terminal y resalta: *"Como primera instrucción del programa se imprimen los nombres completos de los integrantes en estricto orden alfabético por primer apellido"*.
2. **Casos Válidos (Casos 1 al 4):**
   - Muestra cómo el analizador valida:
     - Declaraciones simples (`entero x;`, `flotante y;`, `booleano activo;`, `cadena nombre;`).
     - Declaraciones con inicialización (`entero edad = 21;`, `flotante pi = 3.1416;`).
     - Declaraciones de constantes (`constante entero LIMITE = 100;`).
     - Uso de variables en sentencias de asignación y expresiones (`resultado = (x + y) * 2;`).
   - Resalta el **Árbol de Sintaxis Abstracta (AST)** generado en consola.
3. **Casos Inválidos y Manejo de Errores (Casos 5 al 10):**
   - Muestra las tablas detalladas de errores con número de **línea y columna**:
     - *Caso 5 (Identificadores inválidos):* `"Error: Identificador inválido '123x' en la línea 2, columna 8. Un identificador debe comenzar con una letra o guion bajo."`
     - *Caso 6 (Tipos no válidos):* `"Error: Tipo no válido 'flotando' en la línea 3, columna 1. Los tipos válidos son 'entero', 'flotante', 'booleano', y 'cadena'."`
     - *Caso 7 (Falta punto y coma):* `"Error: Se esperaba ';' al final de la declaración..."`
     - *Caso 8 (Constante no inicializada):* `"Error: La constante 'MAX' debe ser inicializada con un valor..."`
     - *Caso 10 (Suite combinada):* Destacar la recuperación sintáctica (*Panic Mode*) donde detecta 7 errores distintos sin abortar abruptamente el compilador.
4. **Final:**
   - Baja al final de la terminal y resalta: *"Como última instrucción del main, se vuelven a imprimir las firmas de los integrantes en orden alfabético"*.

---

### PASO 3: Demostración Interactiva con la Interfaz Gráfica (GUI)
Ejecuta el siguiente comando:
```powershell
python gui.py
```

Se abrirá una ventana gráfica moderna con selector de casos, visor de AST y tabla de errores.

#### Demostración rápida en la GUI (toma aprox. 1 minuto):
1. Muestra el encabezado superior con los nombres de los 4 integrantes.
2. En el menú desplegable **"Casos de Prueba"**, selecciona:
   - **`1. Válido: Declaraciones Simples`**
   - Haz clic en el botón verde **`▶ ANALIZAR SINTAXIS`**.
   - Muestra la pestaña **`🌳 Árbol Sintáctico (AST)`** generada exitosamente.
3. Ahora en el menú desplegable selecciona:
   - **`10. Suite Integral: Múltiples Errores Combinados`**
   - Haz clic en **`▶ ANALIZAR SINTAXIS`**.
   - Cambia a la pestaña **`❌ Errores Sintácticos`** y muestra cómo se listan en la tabla con sus números de línea, columna, token afectado y sugerencia.
4. *(Opcional - Demo en vivo):*
   - Haz clic en **`Limpiar Editor`**.
   - Escribe en vivo:
     ```c
     constante entero MAX;
     ```
   - Clic en **`▶ ANALIZAR SINTAXIS`** -> Se muestra el error de que la constante debe inicializarse.
   - Corrige escribiendo:
     ```c
     constante entero MAX = 100;
     ```
   - Clic en **`▶ ANALIZAR SINTAXIS`** -> Se genera el AST sin errores.
5. Cierra la ventana.

---

### PASO 4: Conclusión del video
- Menciona brevemente:
  - *"Con esto concluimos la demostración del análisis sintáctico para variables y constantes de la Actividad 3, cumpliendo con la gramática formal, la generación de AST y el reporte pedagógico de errores sintácticos."*
- Detén la grabación (debe haber durado menos de 5 minutos).

---

## 📤 PASOS POSTERIORES A LA GRABACIÓN
1. Sube el video a **YouTube** en modo **Público** u **Oculto** (No listado).
2. Abre el archivo Word generado:
   `DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A3_AnalisisSintacticoVariablesConstantes.docx`
3. En la Sección 1, reemplaza `https://www.youtube.com/watch?v=TU_ENLACE_AQUI` por el enlace real de YouTube.
4. Guarda el documento como **PDF** (`Archivo` > `Guardar como` > seleccionar formato `PDF (.pdf)`).
5. Sube el PDF a la plataforma escolar antes de la fecha límite (11 de septiembre, 23:59).
