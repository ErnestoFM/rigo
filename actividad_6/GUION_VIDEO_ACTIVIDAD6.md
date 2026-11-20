# GUION DE GRABACIÓN - ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES
**Profesor:** Rigoberto Cárdenas Larios  
**Equipo:**
1. Díaz Torres Jazmín Montserrat
2. Fierro Meléndez Ernesto Hatuey
3. Hernández García Héctor Gabriel
4. Millán Guerrero Oswaldo Josué

---

## 📌 Checklist antes de presionar Grabar:
- [ ] Grabar **PANTALLA COMPLETA** (la barra de tareas con **fecha y hora** de Windows debe verse todo el tiempo).
- [ ] Duración objetivo: **3 a 4 minutos** (límite máximo: 5 minutos).
- [ ] Tener lista la terminal en la carpeta `actividad_6` y una ventana para la interfaz gráfica.

---

## 🎬 GUION PASO A PASO (QUÉ HACER Y QUÉ DECIR)

### MINUTO 0:00 - 0:40 | Introducción y Objetivo
> **Qué hacer en pantalla:**
> - Pantalla completa visible, mostrando la terminal abierta en `actividad_6` y el reloj de Windows abajo a la derecha.

> **Qué decir:**
> *"Buen día profesor Rigoberto Cárdenas. Somos el equipo conformado por Jazmín Díaz Torres, Ernesto Hatuey Fierro, Héctor Gabriel Hernández y Oswaldo Josué Millán.*
>
> *Presentamos la Actividad 6: Análisis sintáctico de métodos y clases. El objetivo de esta práctica es implementar el analizador sintáctico para validar la definición de clases y métodos, generar el árbol de sintaxis abstracta (AST) y gestionar de manera precisa los errores sintácticos según la gramática formal establecida."*

---

### MINUTO 0:40 - 2:00 | Demostración por Consola (CLI - `main.py`)
> **Qué hacer en pantalla:**
> - En la terminal ejecuta: `python main.py` (o con tu ruta de Python).
> - Haz scroll hacia arriba hasta el puro inicio de la salida.

> **Qué decir:**
> *"Iniciamos ejecutando `main.py`. Como lo exige la rúbrica, la primera instrucción que se imprime en consola son los nombres completos de los integrantes en orden alfabético por primer apellido.*
>
> *En la primera sección probamos los casos válidos:*
> - *Aquí vemos el **Caso Oficial de la práctica**: la clase `MiClase` con el método `miMetodo` que recibe parámetros `int a, float b`, y `otroMetodo` sin parámetros.*
> - *El analizador reconoce correctamente la estructura de la clase, los tipos de retorno, los parámetros y genera el Árbol Sintáctico (AST) con cero errores.*
> - *También validamos clases con variables y atributos, y definición de múltiples clases en un mismo archivo.*"

> **Qué hacer en pantalla:**
> - Desplázate hacia abajo a la sección de **Casos Inválidos**.

> **Qué decir:**
> *"En la sección de casos inválidos, comprobamos el manejo de errores que pide la rúbrica:*
> - *En el **Caso 7 (Oficial)** donde falta una coma entre `int a` y `float b`, el sistema reporta exactamente: **'Error: Parámetro inválido en la declaración de método'** con su línea y columna.*
> - *En el **Caso 8 (Oficial)** donde `void otroMetodo` no tiene paréntesis, se detecta de inmediato la falta de paréntesis.*
> - *También demostramos los errores de **'Cuerpo de clase inválido'** y **'Tipo de retorno inválido'**.*
>
> *Y al finalizar la ejecución, como solicita el profesor, la última instrucción vuelve a imprimir nuestras firmas completas."*

---

### MINUTO 2:00 - 3:30 | Demostración en la Interfaz Gráfica (`gui.py`)
> **Qué hacer en pantalla:**
> - En la terminal ejecuta: `python gui.py`
> - Se abrirá la ventana gráfica.

> **Qué decir:**
> *"Ahora abrimos la interfaz gráfica interactiva del compilador. En la parte superior se identifican los datos del equipo y la materia.*
>
> *1. Primero cargamos el **Caso 01 (Válido Oficial)** desde el menú desplegable y damos clic en **'ANALIZAR SINTAXIS'**.*
> *Podemos observar en el panel derecho el Árbol AST jerárquico totalmente estructurado y la tabla de tokens reconocidos con éxito.*
>
> *2. Ahora seleccionamos el **Caso 07 (Inválido Oficial 1: Falta de coma entre parámetros)** y presionamos analizar.*
> *Vemos cómo la pestaña de Errores Sintácticos resalta la falla en rojo, indicando la línea 2, columna 28, el mensaje exacto y una sugerencia de corrección.*
>
> *3. Finalmente probamos el **Caso 08 (Inválido Oficial 2: Faltan paréntesis)**, donde el parser captura la ausencia de la signatura de parámetros."*

---

### MINUTO 3:30 - 4:00 | Conclusión y Cierre
> **Qué hacer en pantalla:**
> - Cierra la ventana gráfica y muestra nuevamente tu pantalla con la fecha y hora.

> **Qué decir:**
> *"Con esto demostramos que el analizador sintáctico cumple con todas las reglas gramaticales, la jerarquía de clases y métodos, el reporte detallado de errores y todos los lineamientos de la rúbrica.*
>
> *Muchas gracias por su atención."*
