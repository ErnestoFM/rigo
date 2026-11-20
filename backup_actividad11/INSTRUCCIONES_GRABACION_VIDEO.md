# INSTRUCCIONES Y GUION PARA GRABACIÓN DE VIDEO (YOUTUBE)
## ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO
### MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES (CUCEI - UDG)
### PROFESOR: RIGOBERTO CÁRDENAS LARIOS

---

## 1. REQUISITOS OBLIGATORIOS DE LA RÚBRICA
1. **Duración:** Menor a 5 minutos (estrictamente no mayor a 5 minutos).
2. **Resolución:** Mínimo 720p (se recomienda grabar a 1080p a 60 fps).
3. **Pantalla Completa:** Debe grabarse la pantalla completa de Windows, asegurando que el **reloj y fecha del sistema** (en la esquina inferior derecha de la barra de tareas) sean perfectamente visibles en todo momento.
4. **Audio:** Audio claro con micrófono explicando cada punto.
5. **Plataforma:** Subir a YouTube (público o no listado) y colocar el enlace en la portada y cuerpo del reporte.

---

## 2. INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO OBLIGATORIO)
1. **DÍAZ TORRES JAZMÍN MONTSERRAT**
2. **FIERRO MELÉNDEZ ERNESTO HATUEY**
3. **HERNÁNDEZ GARCÍA HÉCTOR GABRIEL**
4. **MILLÁN GUERRERO OSWALDO JOSUÉ**

---

## 3. GUION CRONOMETRADO (TOTAL: ~4 MINUTOS Y 20 SEGUNDOS)

### Bloque 1: Presentación y Objetivos (0:00 - 0:35)
* **Visual:** Pantalla completa mostrando el escritorio con VS Code / Terminal y el reloj de Windows visible.
* **Audio:**
  > "Buenas tardes, profesor Rigoberto Cárdenas Larios y compañeros. Presentamos la Actividad 11 de Traductores de Lenguaje: Código Intermedio para Control de Flujo.
  > Nuestro equipo está integrado por:
  > 1. Díaz Torres Jazmín Montserrat,
  > 2. Fierro Meléndez Ernesto Hatuey,
  > 3. Hernández García Héctor Gabriel, y
  > 4. Millán Guerrero Oswaldo Josué.
  > El objetivo de esta práctica es transformar las estructuras de control de flujo del lenguaje C (condicionales if/else y switch, bucles while, for y do-while, así como definición y llamada de métodos y clases) en una representación intermedia de tres direcciones (TAC) con saltos, etiquetas y temporales descriptivos."

### Bloque 2: Ejecución de la Suite de Pruebas CLI (0:35 - 1:45)
* **Visual:** Abrir la terminal PowerShell en la carpeta `actividad_11` y ejecutar:
  ```powershell
  python main.py
  ```
* **Audio:**
  > "Procedemos a ejecutar la suite de pruebas automatizada desde la terminal.
  > Como primera instrucción obligatoria, el programa imprime el encabezado formal con nuestros cuatro integrantes en orden alfabético estricto.
  > Vemos en pantalla la ejecución de los 10 casos de prueba:
  > - En el Caso 1, el condicional if-else evalúa `x > y` en un temporal `t1`, genera el salto condicional `if t1 goto L1`, ejecuta el else y salta con `goto L2`, garantizando el flujo exacto solicitado.
  > - En el Caso 2, la estructura `switch` genera saltos `if t1 == 1 goto L1`, `if t1 == 2 goto L2` y `goto L3` para el default.
  > - En el Caso 3, se linealizan bucles `while`, `for` y `do-while` con sus respectivas etiquetas de inicio, condiciones de parada con `if not` y actualización de contadores.
  > - En el Caso 4, se desglosa la definición del método `suma` con su etiqueta de inicio y retorno, y su llamada pasando argumentos en temporales `t2` y `t3`, llamada `call L1` y captura de `result = return_value`.
  > - En el Caso 5, se define la clase `Persona`, su método `celebrarCumpleaños`, la creación del objeto con `obj = create Persona` y la llamada al método de instancia.
  > - En los Casos 6 al 10, probamos el control semántico de errores: métodos inexistentes, aridad incorrecta, clases no declaradas y condiciones inválidas, emitiendo guardas de error y reportes detallados.
  > Al final, como última instrucción obligatoria, se imprimen nuevamente nuestros nombres completos y confirmamos el 100% de casos aprobados."

### Bloque 3: Demostración de la Interfaz Gráfica GUI (1:45 - 3:20)
* **Visual:** Ejecutar en terminal:
  ```powershell
  python gui.py
  ```
* **Audio:**
  > "Ahora abrimos la interfaz gráfica desarrollada en Tkinter.
  > En la parte superior encontramos el encabezado con nuestros datos y el selector interactivo de casos de prueba.
  > Seleccionamos el Caso 1 (if-else): damos clic en 'Compilar y Generar TAC' y observamos a la derecha las instrucciones de tres direcciones generadas con sus comentarios explicativos.
  > Seleccionamos el Caso 2 (switch-case): compilamos y vemos la tabla de saltos múltiples y las etiquetas L1, L2, L3 y L4.
  > Seleccionamos el Caso 4 (métodos): observamos el paso ordenado de argumentos y la llamada al método.
  > Seleccionamos el Caso 5 (clases): vemos la instrucción `obj = create Persona` y `call L1`.
  > Por último, seleccionamos el Caso 7 (aridad incorrecta): al compilar, el panel inferior nos reporta que la función esperaba 2 argumentos pero se pasaron 3, insertando la guarda de error en el TAC.
  > Podemos presionar el botón 'Ejecutar 10 Casos' y verificar que todos los casos aprueban en tiempo real."

### Bloque 4: Breve Revisión de la Arquitectura del Código (3:20 - 4:05)
* **Visual:** Mostrar rápidamente en VS Code los archivos:
  - `tac_instruction.py`: clase `TACInstruction` con formato de saltos y comentarios.
  - `parser.py`: análisis sintáctico de sentencias de control.
  - `tac_generator.py`: lógica de generación de etiquetas y temporales.
  - `symbol_table.py`: registro jerárquico de ámbitos, firmas de métodos y miembros de clases.
* **Audio:**
  > "El proyecto está estructurado de manera modular y limpia.
  > Cada clase contiene como docstring obligatorio nuestros nombres completos en orden alfabético.
  > El módulo `tac_generator.py` implementa el recorrido del AST emitiendo instrucciones de tres direcciones normalizadas, administrando la tabla de símbolos para enlazar llamadas a métodos y clases, y capturando cualquier violación de tipos o aridad."

### Bloque 5: Conclusiones y Despedida (4:05 - 4:25)
* **Visual:** Volver a mostrar la pantalla completa con el reloj de Windows visible.
* **Audio:**
  > "Con esto demostramos el correcto funcionamiento del generador de código intermedio para control de flujo, cumpliendo al 100% con las especificaciones y la rúbrica de la práctica. Muchas gracias por su atención."

---

## 4. CHECKLIST ANTES DE SUBIR EL VIDEO
- [ ] ¿El video dura menos de 5:00 minutos?
- [ ] ¿Es visible la fecha y hora de Windows en la barra de tareas?
- [ ] ¿Se mencionaron los 4 integrantes en orden alfabético?
- [ ] ¿Se mostraron tanto la consola CLI (`main.py`) como la GUI (`gui.py`)?
- [ ] ¿Se demostraron casos válidos e inválidos?
- [ ] ¿El enlace de YouTube fue colocado en el reporte PDF y DOCX?
