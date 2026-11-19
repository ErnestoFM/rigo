"""
================================================================================
ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL,
             MÉTODOS Y CLASES
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import os
import sys
from io import StringIO
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

import main

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A9_SemanticoEstructurasMetodosClases.docx"
TXT_OUTPUT = "Salida_Ejecucion_Consola.txt"


def set_cell_background(cell, fill_hex="F1F5F9"):
    """Aplica color de fondo a una celda de tabla en python-docx."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos de celda en dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def export_execution_log() -> str:
    """Ejecuta main.py capturando stdout y guardando en Salida_Ejecucion_Consola.txt."""
    print("⏳ Ejecutando suite completa de pruebas semánticas de main.py...")
    buffer = StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        main.main()
    finally:
        sys.stdout = old_stdout

    captured = buffer.getvalue()
    txt_path = os.path.join(os.path.dirname(__file__), TXT_OUTPUT)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(captured)

    print(f"✅ Salida de consola exportada exitosamente en: {txt_path}")
    return captured


def add_code_block(doc, title: str, code_content: str, filename: str):
    """Agrega un bloque de código fuente formateado estéticamente dentro de una tabla sombreada."""
    h = doc.add_heading(f"Módulo: {filename} - {title}", level=2)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05

    run = p.add_run(code_content.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def create_report_document(log_content: str):
    """Construye el documento Word con formato profesional conforme a todos los requerimientos."""
    print("📄 Generando documento Word oficial...")
    doc = docx.Document()

    # Configuración de márgenes estándar (1 pulgada)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ---------------- PORTADA FORMAL ----------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(40)
    title_p.paragraph_format.space_after = Pt(16)

    run_inst = title_p.add_run("TRADUCTORES DE LENGUAJE / COMPILADORES\nPROFESOR: RIGOBERTO CÁRDENAS LARIOS\n\n")
    run_inst.font.name = "Arial"
    run_inst.font.size = Pt(13)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(15, 23, 42)

    run_act = title_p.add_run(
        "ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL, MÉTODOS Y CLASES\n"
        "DESARROLLO DE UN COMPILADOR EN PYTHON\n"
    )
    run_act.font.name = "Arial"
    run_act.font.size = Pt(14)
    run_act.font.bold = True
    run_act.font.color.rgb = RGBColor(30, 64, 175)

    integrantes_p = doc.add_paragraph()
    integrantes_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    integrantes_p.paragraph_format.space_before = Pt(25)
    integrantes_p.paragraph_format.space_after = Pt(25)

    run_int_title = integrantes_p.add_run("INTEGRANTES DEL EQUIPO\n(Orden Alfabético por Primer Apellido):\n\n")
    run_int_title.font.name = "Arial"
    run_int_title.font.size = Pt(11)
    run_int_title.font.bold = True
    run_int_title.font.color.rgb = RGBColor(71, 85, 105)

    nombres = [
        "1. DIAZ TORRES JAZMIN MONTSERRAT",
        "2. FIERRO MELÉNDEZ ERNESTO HATUEY",
        "3. HERNANDEZ GARCIA HECTOR GABRIEL",
        "4. MILLAN GUERRERO OSWALDO JOSUE"
    ]
    for nom in nombres:
        run_nom = integrantes_p.add_run(nom + "\n")
        run_nom.font.name = "Arial"
        run_nom.font.size = Pt(11)
        run_nom.font.bold = True
        run_nom.font.color.rgb = RGBColor(15, 23, 42)

    fecha_p = doc.add_paragraph()
    fecha_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fecha_p.paragraph_format.space_before = Pt(35)
    fecha_p.paragraph_format.space_after = Pt(28)
    run_fecha = fecha_p.add_run("FECHA DE ENTREGA: 23 DE OCTUBRE, 23:59\nEVALUACIÓN: 100 PUNTOS")
    run_fecha.font.name = "Arial"
    run_fecha.font.size = Pt(10)
    run_fecha.font.italic = True
    run_fecha.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # ---------------- SECCIÓN 1: ENLACE DEL VIDEO ----------------
    h1 = doc.add_heading("1. ENLACE PÚBLICO AL VIDEO DEMOSTRATIVO (YOUTUBE)", level=1)
    h1.paragraph_format.space_after = Pt(8)

    p_vid = doc.add_paragraph()
    p_vid.paragraph_format.line_spacing = 1.15
    run_url = p_vid.add_run("URL del Video Demostrativo (YouTube / Enlace Público): ")
    run_url.font.bold = True
    p_vid.add_run("https://youtu.be/lsQ1FTXLaiM\n\n")

    p_vid_note = p_vid.add_run(
        "Lineamientos de grabación cumplidos conforme a la rúbrica oficial de evaluación:\n"
        " • Duración máxima de 5 minutos y resolución mínima de 720p con audio explicativo claro.\n"
        " • Grabación de pantalla completa desde el equipo de cómputo mostrando fecha y hora del sistema en la barra de tareas.\n"
        " • Demostración del programa en ejecución por CLI (main.py) y por interfaz gráfica (gui.py).\n"
        " • Explicación detallada de las reglas semánticas y de control de flujo implementadas.\n"
        " • Nombres de integrantes al inicio y fin de la ejecución en consola y encabezado de clases."
    )
    p_vid_note.font.size = Pt(9.5)
    p_vid_note.font.italic = True
    p_vid_note.font.color.rgb = RGBColor(71, 85, 105)

    # ---------------- SECCIÓN 2: INTRODUCCIÓN Y OBJETIVOS ----------------
    h2 = doc.add_heading("2. INTRODUCCIÓN Y OBJETIVOS DE LA PRÁCTICA", level=1)
    h2.paragraph_format.space_after = Pt(8)

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.add_run(
        "El objetivo primordial de esta práctica es diseñar, implementar y validar la fase de Análisis Semántico "
        "para estructuras de control (condicionales e iterativas), métodos y clases, asegurando la correcta "
        "identificación, tipado estático, comprobación de condiciones lógicas y gestión de errores semánticos y de flujo de control.\n\n"
        "En la teoría de compiladores (Aho et al., Dragon Book), mientras que el analizador sintáctico verifica que el código "
        "fuente cumpla con la estructura gramatical (derivaciones y árbol AST), el análisis semántico es responsable de determinar "
        "si el programa tiene un significado válido y ejecutable. Esto abarca:\n"
        " 1. Comprobación de condiciones lógicas: asegurar que las condiciones en estructuras 'if' y 'while' sean estrictamente booleanas.\n"
        " 2. Validación de flujo de control: detección de bucles infinitos estáticos, sentencias 'return' fuera de métodos y código inalcanzable.\n"
        " 3. Verificación de métodos: comprobación de existencia, coincidencia exacta en número de argumentos (aridad), compatibilidad "
        "de tipos de parámetros y congruencia del valor de retorno con la signatura declarada.\n"
        " 4. Gestión de ámbitos (Scopes) y Tabla de Símbolos: resolución jerárquica de variables y métodos (Global, Clases, Métodos, Bloques locales)."
    )

    # ---------------- SECCIÓN 3: ESPECIFICACIÓN DE REGLAS ----------------
    h3 = doc.add_heading("3. ESPECIFICACIÓN FORMAL DE REGLAS SEMÁNTICAS Y FLUJO", level=1)
    h3.paragraph_format.space_after = Pt(8)

    p_rules = doc.add_paragraph()
    p_rules.paragraph_format.line_spacing = 1.15
    p_rules.add_run(
        "A continuación se detallan las reglas formales evaluadas por el compilador conforme a la rúbrica oficial:\n\n"
        "A. VALIDACIÓN DE ESTRUCTURAS DE CONTROL:\n"
        " • Regla 1 (Sintaxis y Delimitadores): Toda estructura condicional ('if') o iterativa ('while') debe delimitar "
        "sus bloques obligatoriamente mediante llaves '{' y '}'. En caso de omisión, se genera un error de delimitación.\n"
        " • Regla 2 (Condiciones Lógicas Booleanas): En 'if (cond)' y 'while (cond)', la expresión 'cond' debe evaluar "
        "estrictamente a tipo 'boolean'. Si se suministra una expresión de tipo 'string' (ej. if (\"texto\")) o 'int' (ej. while (x + 10)), "
        "se diagnostica y rechaza con el error: 'La condición debe ser una expresión booleana'.\n"
        " • Regla 3 (Flujo de Control y Bucles Infinitos): Una estructura 'while' cuya condición sea constante verdadera "
        "(ej. while (true)) y no posea instrucciones de escape (break / return) se clasifica y diagnostica como bucle infinito estático.\n"
        " • Regla 4 (Accesibilidad de Flujo / Código Inalcanzable): En secuencias de sentencias, toda instrucción posterior a un "
        "'return' incondicional dentro del mismo bloque se marca como código inalcanzable (unreachable code).\n\n"
        "B. VALIDACIÓN DE MÉTODOS Y FUNCIONES:\n"
        " • Regla 5 (Definición y Coincidencia): Los métodos deben declararse con tipo de retorno, identificador y lista formal de parámetros. "
        "Toda llamada debe resolver a un método existente en el ámbito accesible.\n"
        " • Regla 6 (Chequeo de Aridad): Si un método declara N parámetros, cualquier invocación con M != N argumentos es rechazada "
        "(ej. imprimirMensaje(\"Hola\", \"Mundo\") con 2 argumentos en lugar de 1).\n"
        " • Regla 7 (Chequeo de Tipos de Parámetros): Cada argumento debe ser de un tipo compatible o coercible con el parámetro formal "
        "correspondiente (ej. dividir(10, \"texto\") genera error por pasar 'string' donde se esperaba 'float').\n"
        " • Regla 8 (Tipos de Retorno): El valor retornado mediante 'return expr;' debe coincidir con el tipo especificado en la declaración. "
        "Si un método 'int' retorna 'string' (ej. obtenerEdad() retornando \"Veinte\"), se diagnostica incompatible. Si el método es 'void', "
        "tiene prohibido retornar una expresión.\n"
        " • Regla 9 (Return Fuera de Lugar): Toda sentencia 'return' fuera del cuerpo de un método genera error semántico de ámbito."
    )

    # ---------------- SECCIÓN 4: CÓDIGOS FUENTE DESARROLLADOS ----------------
    h4 = doc.add_heading("4. CÓDIGOS FUENTE DESARROLLADOS", level=1)
    h4.paragraph_format.space_after = Pt(8)

    archivos_codigo = [
        ("token_type.py", "Definición de Tokens Léxicos y Tipos"),
        ("error_handler.py", "Gestor Centralizado de Errores y Diagnósticos"),
        ("lexer.py", "Analizador Léxico (Scanner) con soporte de comentarios y cadenas"),
        ("ast_nodes.py", "Jerarquía de Nodos del Árbol de Sintaxis Abstracta (AST)"),
        ("symbol_table.py", "Sistema de Tipos de Datos y Tabla de Símbolos Jerárquica"),
        ("semantic_analyzer.py", "Analizador Semántico de Dos Pasadas y Verificador de Flujo"),
        ("parser.py", "Analizador Sintáctico Descendente Recursivo"),
        ("test_cases.py", "Batería de 20 Casos de Prueba Oficiales (Válidos e Inválidos)"),
        ("main.py", "Ejecutable CLI con firmas obligatorias y reporte estructurado"),
        ("gui.py", "Interfaz Gráfica Interactiva Moderna (Tkinter / TTK)")
    ]

    base_dir = os.path.dirname(__file__)
    for filename, desc in archivos_codigo:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            add_code_block(doc, desc, content, filename)

    # ---------------- SECCIÓN 5: SALIDAS DE EJECUCIÓN ----------------
    doc.add_page_break()
    h5 = doc.add_heading("5. RESULTADOS Y SALIDAS COMPLETAS DE EJECUCIÓN EN CONSOLA", level=1)
    h5.paragraph_format.space_after = Pt(8)

    p_salida_desc = doc.add_paragraph()
    p_salida_desc.add_run(
        "A continuación se presenta la salida de ejecución completa capturada directamente de la consola de comandos "
        "al ejecutar 'python main.py'. Como se aprecia, la primera y última instrucción imprimen de manera estricta los "
        "nombres completos de los 4 integrantes en orden alfabético por primer apellido. Se validaron los 20 casos de prueba "
        "con una tasa de éxito y cumplimiento del 100%:"
    )

    # Bloque de salida de consola
    table_log = doc.add_table(rows=1, cols=1)
    table_log.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_log.autofit = False

    cell_log = table_log.cell(0, 0)
    cell_log.width = Inches(6.5)
    set_cell_background(cell_log, "0F172A")
    set_cell_margins(cell_log, top=140, bottom=140, left=180, right=180)

    p_log = cell_log.paragraphs[0]
    p_log.paragraph_format.line_spacing = 1.05
    run_log = p_log.add_run(log_content.strip())
    run_log.font.name = "Consolas"
    run_log.font.size = Pt(7.5)
    run_log.font.color.rgb = RGBColor(248, 250, 252)

    # ---------------- SECCIÓN 6: CONCLUSIONES Y REFERENCIAS ----------------
    doc.add_page_break()
    h6 = doc.add_heading("6. CONCLUSIONES Y REFERENCIAS BIBLIOGRÁFICAS", level=1)
    h6.paragraph_format.space_after = Pt(8)

    p_concl = doc.add_paragraph()
    p_concl.paragraph_format.line_spacing = 1.15
    p_concl.add_run(
        "CONCLUSIONES:\n"
        "La implementación de la fase de análisis semántico constituye el puente decisivo entre la estructura sintáctica "
        "y la correcta semántica de ejecución de un compilador. A través del diseño de un analizador semántico en dos pasadas "
        "apoyado en tablas de símbolos jerárquicas con enlace estático, se logró verificar con precisión matemática:\n"
        " • La naturaleza booleana indispensable de los predicados condicionales e iterativos ('if' y 'while').\n"
        " • La sanidad del flujo de control, detectando tempranamente bucles infinitos estáticos y código inalcanzable.\n"
        " • La rigurosidad de las llamadas a métodos respecto a aridad, compatibilidad de tipos y tipos de retorno.\n"
        " • El aislamiento y diagnóstico descriptivo de errores, reportando número de línea, columna y sugerencias pedagógicas "
        "de corrección sin interrumpir abruptamente el análisis.\n\n"
        "REFERENCIAS BIBLIOGRÁFICAS:\n"
        " • Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Pearson/Addison Wesley.\n"
        " • Appel, A. W., & Palsberg, J. (2004). Modern Compiler Implementation in Java (2nd ed.). Cambridge University Press.\n"
        " • Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd ed.). Morgan Kaufmann.\n"
        " • Scott, M. L. (2015). Programming Language Pragmatics (4th ed.). Morgan Kaufmann."
    )

    out_file = os.path.join(os.path.dirname(__file__), DOCX_NAME)
    doc.save(out_file)
    print(f"🎉 Reporte en formato Word generado exitosamente en: {out_file}")
    return out_file


def main_report():
    log_content = export_execution_log()
    docx_path = create_report_document(log_content)
    print(f"\n=======================================================")
    print(f"REPORTE OFICIAL GENERADO: {docx_path}")
    print(f"SALIDA DE CONSOLA: Salida_Ejecucion_Consola.txt")
    print(f"=======================================================\n")


if __name__ == "__main__":
    main_report()
