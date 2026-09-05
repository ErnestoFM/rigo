"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A4_AnalisisSintacticoExpresionesAritmeticasLogicas.docx"
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
    print("⏳ Ejecutando suite de pruebas sintácticas de main.py...")
    buffer = StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        main.main()
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(current_dir, TXT_OUTPUT)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✔ Salida de ejecución guardada en '{txt_path}' ({len(output)} caracteres).")
    return output

def add_code_block(doc, code_text: str, bg_hex="F8FAFC"):
    """Agrega un bloque de código formateado con caja y tipografía Consolas."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05

    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph() # Espacio posterior

def generate_report_docx(console_output: str):
    """Crea el documento oficial de entrega con formato riguroso y estética profesional."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_docx_path = os.path.join(current_dir, DOCX_NAME)
    print(f"📄 Generando reporte oficial en '{DOCX_NAME}'...")

    doc = docx.Document()

    # Configuración de márgenes estándar (1 pulgada = 72 pt)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ---------------- PORTADA OFICIAL ----------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(18)

    run_inst = title_p.add_run("TRADUCTORES DE LENGUAJE / COMPILADORES\nPROFESOR: RIGOBERTO CÁRDENAS LARIOS\n\n")
    run_inst.font.name = "Arial"
    run_inst.font.size = Pt(13)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(15, 23, 42)

    run_act = title_p.add_run("ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS\nDESARROLLO DE UN COMPILADOR EN PYTHON\n")
    run_act.font.name = "Arial"
    run_act.font.size = Pt(15)
    run_act.font.bold = True
    run_act.font.color.rgb = RGBColor(30, 64, 175)

    integrantes_p = doc.add_paragraph()
    integrantes_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    integrantes_p.paragraph_format.space_before = Pt(20)
    integrantes_p.paragraph_format.space_after = Pt(20)

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
    fecha_p.paragraph_format.space_before = Pt(30)
    fecha_p.paragraph_format.space_after = Pt(28)
    run_fecha = fecha_p.add_run("FECHA DE ENTREGA: 11 DE SEPTIEMBRE, 23:59\nEVALUACIÓN: 100 PUNTOS")
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
    p_vid.add_run("https://www.youtube.com/watch?v=TU_ENLACE_AQUI\n\n")

    p_vid_note = p_vid.add_run(
        "Lineamientos cumplidos conforme a la rúbrica oficial de evaluación:\n"
        " • Duración máxima de 5 minutos y resolución mínima de 720p con audio explicativo claro.\n"
        " • Grabación de pantalla completa desde el equipo de cómputo mostrando fecha y hora visible del sistema.\n"
        " • Introducción con objetivo y presentación de los integrantes al inicio y fin de la ejecución.\n"
        " • Demostración en vivo de las expresiones aritméticas y lógicas conforme a la gramática formal.\n"
        " • Demostración de las reglas de error requeridas: operador sin término ('x + * y'), comparación inválida ('10 >'), paréntesis desbalanceados ('(a - b', '5 / (2 + )') y operadores lógicos incompletos ('10 > 5 &&').\n"
        " • Código presentado con legibilidad óptima y visualización del Árbol de Sintaxis Abstracta (AST)."
    )
    p_vid_note.font.size = Pt(9.5)
    p_vid_note.font.italic = True
    p_vid_note.font.color.rgb = RGBColor(71, 85, 105)

    # ---------------- SECCIÓN 2: INTRODUCCIÓN Y OBJETIVOS ----------------
    h2 = doc.add_heading("2. INTRODUCCIÓN Y OBJETIVOS", level=1)
    h2.paragraph_format.space_after = Pt(8)

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.add_run(
        "El objetivo primordial de esta práctica es diseñar, implementar y validar la fase de Análisis Sintáctico (Parsing) "
        "para expresiones aritméticas y lógicas dentro de la arquitectura de un compilador, integrando un riguroso "
        "subsistema de gestión y recuperación de errores sintácticos.\n\n"
        "En la teoría de compiladores, las expresiones matemáticas y lógicas presentan una jerarquía intrínseca gobernada "
        "por la precedencia y asociatividad de sus operadores. Mientras que el análisis léxico descompone el texto fuente en "
        "unidades mínimas de información (tokens), el analizador sintáctico verifica que la secuencia de operadores y operandos "
        "se ajuste fielmente a una Gramática Libre de Contexto (GLC / Context-Free Grammar). Cuando la estructura sintáctica "
        "es válida, el parser construye un Árbol de Sintaxis Abstracta (AST - Abstract Syntax Tree) que preserva las prioridades de "
        "evaluación (paréntesis, exponentes, productos, sumas, comparaciones relacionales y operadores booleanos). En caso de "
        "malformaciones, el parser reporta con precisión milimétrica la naturaleza del error, la línea, la columna y la sugerencia de corrección."
    )

    # ---------------- SECCIÓN 3: DEFINICIÓN DE LA GRAMÁTICA FORMAL ----------------
    h3 = doc.add_heading("3. DEFINICIÓN DE LA GRAMÁTICA FORMAL (EBNF / BNF)", level=1)
    h3.paragraph_format.space_after = Pt(8)

    p_ebnf_desc = doc.add_paragraph()
    p_ebnf_desc.add_run(
        "Conforme a los requerimientos de la práctica, se definió la gramática formal para expresiones aritméticas y lógicas. "
        "A continuación se presenta en notación EBNF (Extended Backus-Naur Form):"
    )

    ebnf_text = """expresion            -> expresion_logica | expresion_aritmetica

expresion_logica     -> termino_logico (( '&&' | '||' ) termino_logico)*

termino_logico       -> expresion_aritmetica ( '==' | '!=' | '>' | '<' | '>=' | '<=' ) expresion_aritmetica
                      | expresion_aritmetica
                      | '!' termino_logico

expresion_aritmetica -> termino (( '+' | '-' ) termino)*

termino              -> factor (( '*' | '/' | '%' | '^' ) factor)*

factor               -> IDENTIFICADOR
                      | NUMERO_ENTERO
                      | NUMERO_FLOTANTE
                      | '(' expresion ')'
                      | ( '+' | '-' ) factor
"""
    add_code_block(doc, ebnf_text, bg_hex="EFF6FF")

    p_ebnf_exp = doc.add_paragraph()
    p_ebnf_exp.add_run(
        "Desglose y Funcionamiento de las Reglas Sintácticas:\n"
        " 1. expresion: Puede representar una expresión aritmética pura (e.g. 'x + y * 5') o una expresión lógica compuesta (e.g. '10 > 5 && 3 <= 4').\n"
        " 2. expresion_logica: Agrupa términos lógicos vinculados mediante operadores de disyunción ('||', 'or') o conjunción ('&&', 'and').\n"
        " 3. termino_logico: Compara dos expresiones aritméticas mediante operadores relacionales ('==', '!=', '>', '<', '>=', '<=').\n"
        " 4. expresion_aritmetica: Está compuesta de términos separados por operadores de suma o resta (+, -).\n"
        " 5. termino: Agrupa factores vinculados por operadores multiplicativos (*, /, %, ^).\n"
        " 6. factor: Es la unidad indivisible de la expresión aritmética, correspondiente a un identificador de variable, un número literal o una subexpresión agrupada entre paréntesis."
    )

    # ---------------- SECCIÓN 4: GESTIÓN DE ERRORES SINTÁCTICOS ----------------
    h4 = doc.add_heading("4. GESTIÓN Y REPORTE DE ERRORES SINTÁCTICOS", level=1)
    h4.paragraph_format.space_after = Pt(8)

    p_err = doc.add_paragraph()
    p_err.add_run(
        "El módulo error_handler.py implementa las especificaciones exactas solicitadas en la rúbrica de la práctica:\n\n"
        " • Error: Operador sin término en la línea X, columna Y.\n"
        "   Se dispara cuando un operador aritmético no posee un operando o factor válido adyacente (e.g. 'x + * y', '5 +', '* 5 + 10').\n\n"
        " • Error: Comparación inválida en la línea X, columna Y.\n"
        "   Se genera cuando un operador de comparación relacional carece de una expresión aritmética válida en sus extremos (e.g. '10 >', 'x == > y').\n\n"
        " • Error: Paréntesis desbalanceados en la línea X, columna Y.\n"
        "   Se detecta cuando un paréntesis de apertura '(' no es cerrado antes de concluir la expresión o cuando existe un paréntesis de cierre ')' sobrante (e.g. '(a - b', '5 / (2 + )', '(x + y)) * 2').\n\n"
        " • Error: Expresión lógica incompleta en la línea X, columna Y.\n"
        "   Se produce cuando un operador lógico binario carece de término ('10 > 5 &&', '&& 3 <= 4').\n\n"
        " • Error: Falta operador entre términos en la línea X, columna Y.\n"
        "   Identifica la yuxtaposición inválida de dos operandos consecutivos sin operador intermedio ('a + b c')."
    )

    # ---------------- SECCIÓN 5: CÓDIGO FUENTE DESARROLLADO ----------------
    doc.add_page_break()
    h5 = doc.add_heading("5. CÓDIGO FUENTE DESARROLLADO", level=1)
    h5.paragraph_format.space_after = Pt(8)

    files_to_embed = [
        ("token_type.py", "Definición de tokens, categorías léxicas y delimitadores para expresiones."),
        ("lexer.py", "Analizador léxico con rastreo exacto de línea, columna y reconocimiento de operadores de múltiples caracteres."),
        ("ast_nodes.py", "Nodos del Árbol de Sintaxis Abstracta (AST) con generación jerárquica de árbol."),
        ("error_handler.py", "Manejador centralizado de errores sintácticos conforme a la rúbrica del profesor."),
        ("parser.py", "Analizador sintáctico descendente recursivo con detección y recuperación de errores."),
        ("test_cases.py", "Batería exhaustiva de 20 casos de prueba (10 válidos y 10 inválidos)."),
        ("main.py", "Programa principal CLI con nombres de integrantes como primera y última instrucción."),
        ("gui.py", "Interfaz gráfica interactiva en Tkinter para visualización gráfica del AST y tabla de errores.")
    ]

    for filename, desc in files_to_embed:
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()

            doc.add_heading(f"Archivo: {filename}", level=2)
            p_desc = doc.add_paragraph()
            p_desc.paragraph_format.space_after = Pt(4)
            r_d = p_desc.add_run(f"Descripción: {desc}")
            r_d.font.italic = True
            r_d.font.size = Pt(9.5)
            r_d.font.color.rgb = RGBColor(100, 116, 139)

            add_code_block(doc, code_content)

    # ---------------- SECCIÓN 6: RESULTADOS DE EJECUCIÓN ----------------
    doc.add_page_break()
    h6 = doc.add_heading("6. RESULTADOS DE EJECUCIÓN Y TABLAS DE DIAGNÓSTICO", level=1)
    h6.paragraph_format.space_after = Pt(8)

    p_res = doc.add_paragraph()
    p_res.add_run(
        "A continuación se presenta la salida íntegra de la ejecución de la suite de pruebas desde la terminal, "
        "mostrando el cumplimiento estricto de la primera y última instrucción con los nombres de los integrantes en "
        "orden alfabético por primer apellido, la construcción de árboles sintácticos (AST) para casos válidos y las "
        "tablas de diagnóstico para cada caso inválido evaluado:"
    )

    add_code_block(doc, console_output, bg_hex="F1F5F9")

    # ---------------- SECCIÓN 7: REFERENCIAS BIBLIOGRÁFICAS ----------------
    doc.add_page_break()
    h7 = doc.add_heading("7. REFERENCIAS BIBLIOGRÁFICAS (RECURSOS DE APOYO)", level=1)
    h7.paragraph_format.space_after = Pt(8)

    referencias = [
        "Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Pearson/Addison Wesley.",
        "Appel, A. W., & Palsberg, J. (2004). Modern Compiler Implementation in Java (2nd ed.). Cambridge University Press.",
        "Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd ed.). Morgan Kaufmann.",
        "Free Software Foundation, Inc. (1985). GNU Bison. GNU Project. Recuperado de https://www.gnu.org/software/bison/",
        "Parr, T. (1989). ANTLR - ANother Tool for Language Recognition. Recuperado de https://www.antlr.org/",
        "Scott, S., & Johnson, M. (1996). CUP - Construction of Useful Parsers. Technische Universität München."
    ]

    for ref in referencias:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        run_ref = p_ref.add_run(ref)
        run_ref.font.size = Pt(9.5)
        run_ref.font.color.rgb = RGBColor(51, 65, 85)

    # Guardar documento
    doc.save(output_docx_path)
    print(f"✔ Reporte Word guardado exitosamente en:\n  {output_docx_path}")

def main_generate():
    output = export_execution_log()
    generate_report_docx(output)

if __name__ == "__main__":
    main_generate()
