# INSTRUCCIONES Y GUION PARA GRABACIÓN DE VIDEO (YOUTUBE)
## ACTIVIDAD 12: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO
### MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES (CUCEI - UDG)
### PROFESOR: RIGOBERTO CÁRDENAS LARIOS

---

## 1. REQUISITOS OBLIGATORIOS DE LA RÚBRICA
1. **Duración:** Menor a 5 minutos (estrictamente no mayor a 5 minutos).
2. **Resolución:** Mínimo 720p (se recomienda 1080p a 60 fps).
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

## 3. GUION CRONOMETRADO (TOTAL: ~4 MINUTOS Y 15 SEGUNDOS)

### Bloque 1: Presentación y Objetivos (0:00 - 0:35)
* **Visual:** Pantalla completa mostrando el escritorio de Windows con el reloj visible y la terminal lista.
* **Audio:**
  > "Buenas tardes, profesor Rigoberto Cárdenas Larios y compañeros. Presentamos la Actividad 12 de Traductores de Lenguaje: Optimización de Código Intermedio.
  > Nuestro equipo de trabajo está integrado por:
  > 1. Díaz Torres Jazmín Montserrat,
  > 2. Fierro Meléndez Ernesto Hatuey,
  > 3. Hernández García Héctor Gabriel, y
  > 4. Millán Guerrero Oswaldo Josué.
  > El objetivo de esta práctica es analizar y optimizar el código intermedio de tres direcciones (TAC), eliminando instrucciones inalcanzables tras saltos incondicionales, podando variables muertas no utilizadas, suprimiendo cálculos repetidos (CSE), removiendo asignaciones sobrescritas inmediatamente (dead stores) y aplicando plegado con propagación de constantes sin alterar los resultados finales del programa."

### Bloque 2: Ejecución de la Suite de Pruebas CLI (0:35 - 1:45)
* **Visual:** Abrir la terminal PowerShell en la carpeta `actividad_12` y ejecutar:
  ```powershell
  python main.py
  ```
* **Audio:**
  > "Procedemos a ejecutar la suite automatizada desde la terminal.
  > Como primera instrucción obligatoria, el programa imprime el encabezado con nuestros cuatro integrantes en estricto orden alfabético.
  > A continuación, la suite ejecuta los 10 casos de prueba:
  > - En el Caso 1, el análisis de código inalcanzable detecta que tras `goto L2`, la instrucción `y = 20` nunca se ejecuta y la elimina.
  > - En el Caso 2, el análisis de variables no utilizadas identifica que `a = 5` no interviene en el cálculo final y la descarta.
  > - En el Caso 3, la eliminación de subexpresiones comunes (CSE) detecta que `a + b` ya fue calculado en `t1`, eliminando la recomputación en `t2`.
  > - En el Caso 4, se detecta que `temp = a` es sobrescrita inmediatamente por `temp = b` sin ser leída, eliminando el dead store y propagando la copia a `result = b`.
  > - En el Caso 5, el plegado y propagación de constantes evalúa `x = 10`, `t1 = 15` y `t2 = 25`, reduciendo el cálculo final a `result = 25`.
  > - En los Casos 6 al 10, probamos el control semántico y sintáctico de errores: saltos a etiquetas inexistentes, variables no inicializadas, sintaxis TAC inválida, división entre cero durante optimización y operadores relacionales incorrectos.
  > Al final, como última instrucción obligatoria, se imprimen nuevamente nuestros nombres completos, confirmando el 100% de casos aprobados."

### Bloque 3: Demostración de la Interfaz Gráfica GUI (1:45 - 3:20)
* **Visual:** Ejecutar en terminal:
  ```powershell
  python gui.py
  ```
* **Audio:**
  > "Abrimos la interfaz gráfica interactiva desarrollada en Tkinter.
  > Observamos en la parte superior el membrete con nuestros datos y el selector desplegable de casos.
  > En el Caso 1, damos clic en 'Optimizar Código Intermedio' y apreciamos en el panel derecho cómo desaparece la instrucción `y = 20`, mientras que la consola inferior detalla la bitácora de optimización y la reducción del 14.3%.
  > En el Caso 2, compilamos y vemos que `a = 5` y `b = 10` son eliminadas, reduciendo el código en un 50%.
  > En el Caso 3, observamos la reutilización de `t1` y la eliminación de `t2`.
  > En el Caso 4, comprobamos la eliminación de la asignación redundante a `temp`.
  > En el Caso 5, vemos el plegado directo a `result = 25`.
  > Finalmente, probamos el Caso 6 y vemos cómo el panel de errores nos alerta del salto a una etiqueta no definida.
  > Podemos presionar 'Ejecutar 10 Casos' y comprobar que toda la suite aprueba satisfactoriamente."

### Bloque 4: Breve Revisión de la Arquitectura del Código (3:20 - 4:00)
* **Visual:** Mostrar en VS Code los módulos:
  - `tac_instruction.py`: modelo de instrucción y análisis de variables leídas/escritas.
  - `optimizer.py`: pasadas de optimización multipasada (`eliminate_unreachable_code`, `eliminate_dead_stores`, `eliminate_common_subexpressions`, `propagate_and_fold_constants`, `eliminate_dead_variables`).
  - `tac_parser.py`: análisis sintáctico de código intermedio.
* **Audio:**
  > "El código fue diseñado con un enfoque modular y formal.
  > Cada clase cuenta con el docstring obligatorio con nuestros cuatro integrantes en orden alfabético.
  > El motor `TACOptimizer` implementa un ciclo de punto fijo que itera las cinco reglas de optimización hasta que no existan más reducciones posibles, asegurando la máxima eficiencia del código intermedio."

### Bloque 5: Conclusiones y Despedida (4:00 - 4:20)
* **Visual:** Volver a enfocar el escritorio completo con la fecha y hora de Windows visible.
* **Audio:**
  > "Con esto demostramos el correcto funcionamiento del optimizador de código intermedio, cumpliendo al 100% con los requerimientos y la rúbrica del profesor Rigoberto Cárdenas Larios. Muchas gracias."

---

## 4. CHECKLIST ANTES DE SUBIR EL VIDEO
- [ ] ¿El video dura menos de 5:00 minutos?
- [ ] ¿Es visible la fecha y hora de Windows en la barra de tareas?
- [ ] ¿Se mencionaron los 4 integrantes en orden alfabético al inicio?
- [ ] ¿Se mostraron tanto la consola CLI (`main.py`) como la GUI (`gui.py`)?
- [ ] ¿Se demostraron casos válidos e inválidos?
- [ ] ¿El enlace de YouTube fue colocado en el reporte PDF y DOCX?
