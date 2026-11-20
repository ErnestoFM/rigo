# GUÍA OFICIAL PARA GRABACIÓN DE VIDEO DE DEMOSTRACIÓN (YOUTUBE)
## PROYECTO FINAL: COMPILADOR INTEGRAL DE LENGUAJE C CON MÁQUINA VIRTUAL
**Materia:** Traductores de Lenguaje / Compiladores  
**Profesor:** Rigoberto Cárdenas Larios  
**Universidad:** Universidad de Guadalajara — CUCEI  

---

### INTEGRANTES DEL EQUIPO (ESTRICTO ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. **DÍAZ TORRES JAZMÍN MONTSERRAT**
2. **FIERRO MELÉNDEZ ERNESTO HATUEY**
3. **HERNÁNDEZ GARCÍA HÉCTOR GABRIEL**
4. **MILLÁN GUERRERO OSWALDO JOSUÉ**

---

## 1. REQUISITOS OBLIGATORIOS DE LA GRABACIÓN (RÚBRICA)
> [!IMPORTANT]
> 1. **Duración máxima:** El video debe durar **MENOS DE 5 MINUTOS** (tiempo recomendado: entre 4:00 y 4:45 minutos).
> 2. **Pantalla completa:** Grabar toda la pantalla sin recortar. La barra de tareas con la **fecha y reloj de Windows DEBE ser visible en todo momento** durante la grabación.
> 3. **Resolución mínima:** Full HD (1920x1080) a 30 o 60 FPS (usar OBS Studio, Xbox Game Bar `Win + Alt + R`, o software de captura preferido).
> 4. **Audio claro:** Voz audible explicando cada fase.
> 5. **Publicación:** Subir a YouTube en modo **Público** o **No Listado** (Oculto). Pegar el enlace en la portada y sección 1 del reporte PDF/Word.

---

## 2. GUION PASO A PASO CON TIEMPOS EXACTOS (4:30 MINUTOS TOTALES)

### Minuto 0:00 – 0:30 | Introducción y Presentación Formal
* **Acción en pantalla:** Tener abierta la aplicación `gui.py` maximizada en pantalla completa.
* **Qué decir:**
  > *"Buenas tardes, profesor Rigoberto Cárdenas Larios y compañeros. A continuación presentamos la demostración del Proyecto Final Integrador de la materia Traductores de Lenguaje en el CUCEI, Universidad de Guadalajara.*  
  > *El equipo de trabajo está integrado en estricto orden alfabético por:  
  > 1. Jazmín Montserrat Díaz Torres,  
  > 2. Ernesto Hatuey Fierro Meléndez,  
  > 3. Héctor Gabriel Hernández García, y  
  > 4. Oswaldo Josué Millán Guerrero.*  
  > *Nuestro proyecto es un compilador integral de lenguaje C con analizadores léxico, sintáctico y semántico, generación y optimización de código intermedio de tres direcciones, síntesis de código máquina y un entorno de ejecución en Máquina Virtual RISC de 32 bits."*

---

### Minuto 0:30 – 1:30 | Caso 1 (Expresiones Aritméticas) y Recorrido de las 8 Pestañas
* **Acción en pantalla:**
  1. En el menú desplegable seleccionar **`[CP01] Expresiones Aritméticas y Variables`** y hacer clic en **`Cargar Código`**.
  2. Presionar el botón **`▶ Compilar y Ejecutar`**.
  3. Ir mostrando secuencialmente cada una de las 8 pestañas:
     - **Pestaña 1 (Fuente C):** Mostrar el código con precedencia: `resultado = a + b * c - (a / b);`.
     - **Pestaña 2 (Tokens):** Mostrar la tabla con el flujo de tokens (líneas, columnas, identificadores, constantes).
     - **Pestaña 3 (AST):** Mostrar la estructura jerárquica en árbol del programa.
     - **Pestaña 4 (Tabla de Símbolos):** Mostrar las variables `a, b, c, resultado` con sus direcciones físicas asignadas en memoria RAM a partir de `0x2000`.
     - **Pestaña 5 (TAC Original):** Mostrar los cuádruplos de 3 direcciones generados (`t1 = b * c`, `t2 = a + t1`, etc.).
     - **Pestaña 6 (TAC Optimizado):** Mostrar el código optimizado y la bitácora de plegado de constantes y dead stores eliminados.
     - **Pestaña 7 (Ensamblador / Memoria):** Mostrar el código máquina traducido (`0x1000: LOAD`, `ADD`, `STORE`) y el porcentaje de reducción (más del 70% de instrucciones ahorradas).
     - **Pestaña 8 (Máquina Virtual):** Mostrar la salida en consola `> 22`, el estado de los registros (`R1: 22`), banderas (`ZF=0, SF=0`) y el volcado de memoria RAM.
* **Qué decir:**
  > *"Aquí observamos el pipeline completo en acción. El código fuente es tokenizado, parseado en un AST, verificado semánticamente asignando direcciones físicas en RAM 0x2000, traducido a código intermedio de tres direcciones, optimizado y finalmente convertido a instrucciones de máquina ejecutadas en nuestra Máquina Virtual con resultado exacto 22."*

---

### Minuto 1:30 – 2:30 | Control de Flujo (Casos 2 y 3) y Programación Modular (Casos 4 y 5)
* **Acción en pantalla:**
  1. Seleccionar **`[CP02] Estructuras de Control Condicional (If-Else y Switch-Case)`** -> `Compilar y Ejecutar` -> Mostrar salida en consola `> 500`.
  2. Seleccionar **`[CP03] Estructuras de Control Iterativas (Bucle While)`** -> `Compilar y Ejecutar` -> Mostrar la sumatoria iterativa en consola `> 15`.
  3. Seleccionar **`[CP04] Funciones con Parámetros`** -> `Compilar y Ejecutar` -> Mostrar llamada a función con call stack y salida `> 40`.
  4. Seleccionar **`[CP05] POO (Clases y Métodos)`** -> `Compilar y Ejecutar` -> Mostrar clase `Banco`, objeto instanciado y método `depositar` con salida `> 750`.
* **Qué decir:**
  > *"El compilador soporta estructuras de control complejas: aquí vemos bifurcaciones condicionales if-else y switch-case evaluadas con saltos JGT, JZ y JMP; bucles while que iteran sobre la memoria RAM; funciones modulares con paso de argumentos y valor de retorno; y programación orientada a objetos con clases, instanciación e invocación de métodos."*

---

### Minuto 2:30 – 3:30 | Diagnóstico y Gestión de Errores (Casos 6 al 10)
* **Acción en pantalla:**
  1. Seleccionar **`[CP06] Error Léxico`** -> Presionar `Compilar y Ejecutar` -> La GUI salta a la pestaña de Tokens y muestra la detección de caracteres ilegales `@` y `#`.
  2. Seleccionar **`[CP07] Error Sintáctico`** -> Presionar `Compilar y Ejecutar` -> La GUI muestra la falta del paréntesis de cierre en el `if`.
  3. Seleccionar **`[CP08] Error Semántico (Tipos)`** -> Presionar `Compilar y Ejecutar` -> Muestra error de tipo: asignación de `string` a `int`.
  4. Seleccionar **`[CP09] Error Semántico (Función No Declarada)`** -> Muestra error de función inexistente en la tabla de símbolos.
  5. Seleccionar **`[CP10] Error Semántico POO (Método Inexistente)`** -> Muestra error de método no definido en la clase.
* **Qué decir:**
  > *"El sistema implementa un robusto manejador de excepciones que detiene la compilación inmediatamente en la fase correspondiente. En el caso 6 diagnostica caracteres léxicos extraños; en el 7 errores de sintaxis; en el 8 incompatibilidad de tipos; y en los casos 9 y 10 funciones y métodos no declarados, ofreciendo sugerencias precisas al programador."*

---

### Minuto 3:30 – 4:15 | Demostración Paso a Paso (Single-Step en VM)
* **Acción en pantalla:**
  1. Seleccionar el Caso 1 o Caso 3.
  2. Presionar el botón **`⏭ Paso a Paso (VM)`** repetidamente (5 a 8 veces).
  3. Observar cómo en cada clic se ejecuta una única instrucción (Fetch -> Decode -> Execute), se actualiza el Program Counter `PC` (`0x1000`, `0x1004`, `0x1008`...), se actualizan los registros `R1` a `R8`, las banderas `ZF` y `SF`, y la tabla de memoria RAM.
* **Qué decir:**
  > *"Nuestra Máquina Virtual cuenta con un modo de depuración paso a paso. En cada pulso podemos observar el ciclo de reloj del procesador virtual, la actualización del Program Counter, la modificación de los registros de trabajo y el estado de las banderas lógicas de la ALU."*

---

### Minuto 4:15 – 4:40 | Conclusiones y Cierre
* **Acción en pantalla:** Regresar a la Pestaña 1 o mostrar el resumen de consola.
* **Qué decir:**
  > *"Como conclusión, se cumplió al 100% con los requerimientos de la materia. Se implementó el compilador completo, la optimización con métricas superiores al 70% de ahorro de instrucciones, la máquina virtual RISC y la suite de pruebas automatizada con 10/10 casos aprobados. Agradecemos la atención prestada."*

---

## 3. CÓMO INICIAR LA APLICACIÓN PARA GRABAR
Abre PowerShell o terminal de comandos en la carpeta del proyecto y ejecuta:

```powershell
cd c:\Users\erfierro\chingado\rigo\proyecto_final
python gui.py
```

Para verificar que la batería de pruebas en consola esté completa antes de grabar:
```powershell
python main.py
```
*(Verifica que imprima al inicio y al final a los 4 integrantes y que concluya con `10/10 APROBADO`).*
