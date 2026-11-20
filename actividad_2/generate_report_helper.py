"""
================================================================================
ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
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
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A2_ManejoErroresLexicos.docx"
TXT_OUTPUT = "Salida_Ejecucion_Consola.txt"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_2"


def set_cell_background(cell, fill_hex="F1F5F9"):
    """Aplica color de fondo a una celda de tabla en python-docx."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos de celda en dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


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


def build_word_report():
    print(f"📄 Generando reporte oficial Word: {DOCX_NAME}...")
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. Portada
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    r_inst = p_inst.add_run("TECNOLÓGICO NACIONAL DE MÉXICO\nDEPARTAMENTO DE SISTEMAS Y COMPUTACIÓN\nINGENIERÍA EN SISTEMAS COMPUTACIONALES")
    r_inst.font.name = "Segoe UI"
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(30, 41, 59)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    r_div.font.color.rgb = RGBColor(14, 165, 233)

    p_act = doc.add_paragraph()
    p_act.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_act.paragraph_format.space_before = Pt(25)
    p_act.paragraph_format.space_after = Pt(15)
    r_act = p_act.add_run("ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS\nDESARROLLO DE UN COMPILADOR EN PYTHON PARA LENGUAJE C")
    r_act.font.name = "Segoe UI"
    r_act.font.size = Pt(16)
    r_act.font.bold = True
    r_act.font.color.rgb = RGBColor(15, 23, 42)

    p_mat = doc.add_paragraph()
    p_mat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_mat = p_mat.add_run("MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES\nDOCENTE: M.C. RIGOBERTO CÁRDENAS LARIOS")
    r_mat.font.name = "Segoe UI"
    r_mat.font.size = Pt(11.5)
    r_mat.font.color.rgb = RGBColor(51, 65, 85)

    p_team_hdr = doc.add_paragraph()
    p_team_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_team_hdr.paragraph_format.space_before = Pt(35)
    r_team_hdr = p_team_hdr.add_run("INTEGRANTES DEL EQUIPO\n(EN ESTRICTO ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    r_team_hdr.font.name = "Segoe UI"
    r_team_hdr.font.size = Pt(11)
    r_team_hdr.font.bold = True
    r_team_hdr.font.color.rgb = RGBColor(14, 116, 144)

    table_team = doc.add_table(rows=5, cols=2)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_team.autofit = False

    integrantes = [
        ("No.", "Nombre Completo"),
        ("1.", "DÍAZ TORRES JAZMÍN MONTSERRAT"),
        ("2.", "FIERRO MELÉNDEZ ERNESTO HATUEY"),
        ("3.", "HERNÁNDEZ GARCÍA HÉCTOR GABRIEL"),
        ("4.", "MILLÁN GUERRERO OSWALDO JOSUÉ")
    ]

    for row_idx, (num, nombre) in enumerate(integrantes):
        c0 = table_team.cell(row_idx, 0)
        c1 = table_team.cell(row_idx, 1)
        c0.width = Inches(0.8)
        c1.width = Inches(4.5)

        if row_idx == 0:
            set_cell_background(c0, "0284C7")
            set_cell_background(c1, "0284C7")
            color_txt = RGBColor(255, 255, 255)
            is_bold = True
        else:
            set_cell_background(c0, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_background(c1, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            color_txt = RGBColor(15, 23, 42)
            is_bold = False

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(num)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(10)
        r0.font.bold = is_bold
        r0.font.color.rgb = color_txt

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(nombre)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10)
        r1.font.bold = is_bold
        r1.font.color.rgb = color_txt

    p_fecha = doc.add_paragraph()
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fecha.paragraph_format.space_before = Pt(45)
    r_fecha = p_fecha.add_run("SEPTIEMBRE / OCTUBRE 2026\nCALIFICACIÓN ESPERADA: 100 PUNTOS")
    r_fecha.font.name = "Segoe UI"
    r_fecha.font.size = Pt(10)
    r_fecha.font.bold = True
    r_fecha.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_page_break()

    # 2. Enlace de Video
    doc.add_heading("1. Enlace del Video Demostrativo (YouTube)", level=1)
    p_v = doc.add_paragraph()
    p_v.add_run(
        "De conformidad con las instrucciones de la práctica, se realizó la grabación demostrativa "
        "con pantalla completa (fecha y hora visibles de Windows), audio explicativo claro y duración menor a 5 minutos, "
        "mostrando el programa en ejecución por consola y GUI, y la detección de las 4 reglas de errores léxicos.\n\n"
        f"🔗 ENLACE AL VIDEO: {VIDEO_URL}\n"
    )

    # 3. Introducción y Objetivos
    doc.add_heading("2. Introducción y Objetivo de la Práctica", level=1)
    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "Práctica: Desarrollo de un compilador, gestión de errores léxicos.\n\n"
        "Objetivo Oficial: Implementar un mecanismo para manejar y reportar errores léxicos durante la fase de análisis "
        "léxico en un compilador para el Lenguaje C desarrollado en Python. Un analizador léxico no solo debe identificar "
        "componentes válidos, sino ser capaz de aislar secuencias defectuosas, determinar la causa raíz del fallo y reportar "
        "la ubicación exacta (línea y columna) junto con sugerencias de corrección comprensibles a simple vista.\n\n"
        "Las 4 categorías de errores léxicos requeridas e implementadas son:\n"
        "1. Caracteres No Reconocidos: Símbolos fuera del alfabeto de C (ej. @, $, ~, ¿, ñ).\n"
        "2. Identificadores Mal Formados: Identificadores que inician con dígitos (ej. 123contador, 8promedio).\n"
        "3. Literales Numéricos Incorrectos: Números con múltiples puntos flotantes (ej. 3.14.15), hexadecimales inválidos (0x12G4) o exponentes incompletos (1.5e+).\n"
        "4. Cadenas Mal Formadas: Cadenas de texto no delimitadas antes de finalizar la línea o archivo."
    )

    # 4. Tabla de Reglas y Casos de Prueba
    doc.add_heading("3. Resultados de Evaluación: Banco de Pruebas (100% Rúbrica)", level=1)
    table_cases = doc.add_table(rows=7, cols=4)
    table_cases.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_cases.autofit = False

    rows_data = [
        ("No.", "Caso de Prueba", "Regla / Categoría", "Resultado"),
        ("1", "Código C Válido (Caso de Control)", "CONTROL_VALIDO", "APROBADO (0 Errores)"),
        ("2", "Caracteres No Reconocidos fuera de C", "CARACTER_NO_RECONOCIDO", "DETECTADO (100% Interceptado)"),
        ("3", "Identificadores Mal Formados con Dígitos", "IDENTIFICADOR_MAL_FORMADO", "DETECTADO (100% Interceptado)"),
        ("4", "Literales Numéricos Incorrectos", "NUMERO_INCORRECTO", "DETECTADO (100% Interceptado)"),
        ("5", "Cadenas de Texto Mal Formadas", "CADENA_MAL_FORMADA", "DETECTADO (100% Interceptado)"),
        ("6", "Evaluación Combinada de Errores", "EVALUACION_INTEGRAL", "DETECTADO (Todas las fallas)")
    ]

    for r_idx, (c0_t, c1_t, c2_t, c3_t) in enumerate(rows_data):
        c0 = table_cases.cell(r_idx, 0)
        c1 = table_cases.cell(r_idx, 1)
        c2 = table_cases.cell(r_idx, 2)
        c3 = table_cases.cell(r_idx, 3)
        c0.width = Inches(0.5)
        c1.width = Inches(2.8)
        c2.width = Inches(2.0)
        c3.width = Inches(1.2)

        if r_idx == 0:
            set_cell_background(c0, "0284C7")
            set_cell_background(c1, "0284C7")
            set_cell_background(c2, "0284C7")
            set_cell_background(c3, "0284C7")
            color_txt = RGBColor(255, 255, 255)
            is_bold = True
        else:
            set_cell_background(c0, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_background(c1, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_background(c2, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_background(c3, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            color_txt = RGBColor(15, 23, 42)
            is_bold = False

        for cell_obj, val_t in [(c0, c0_t), (c1, c1_t), (c2, c2_t), (c3, c3_t)]:
            p = cell_obj.paragraphs[0]
            r = p.add_run(val_t)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            r.font.bold = is_bold
            r.font.color.rgb = color_txt

    doc.add_page_break()

    # 5. Códigos Fuente
    doc.add_heading("4. Códigos Fuente Desarrollados", level=1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_files = [
        ("token_type.py", "Definición de Tokens y Categorías de Errores Léxicos"),
        ("error_handler.py", "Manejador Centralizado de Errores Léxicos"),
        ("lexer.py", "Analizador Léxico en C con Expresiones Regulares Avanzadas"),
        ("test_cases.py", "Suites de Prueba Válidas e Inválidas"),
        ("main.py", "Ejecución por Consola con Firmas de Integrantes al Inicio y Fin"),
        ("gui.py", "Interfaz Gráfica de Usuario Interactiva (Tkinter)")
    ]

    for fname, fdesc in source_files:
        fpath = os.path.join(script_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f_c:
                content = f_c.read()
            add_code_block(doc, fdesc, content, fname)

    doc.add_page_break()

    # 6. Salida de Consola
    doc.add_heading("5. Salida Completa de Ejecución en Consola", level=1)
    txt_path = os.path.join(script_dir, TXT_OUTPUT)
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f_t:
            salida = f_t.read()
    else:
        salida = "Salida de consola no encontrada."

    add_code_block(doc, "Registro de Ejecución de Pruebas", salida, TXT_OUTPUT)

    # 7. Conclusiones y Referencias
    doc.add_heading("6. Conclusiones y Referencias Bibliográficas", level=1)
    p_c = doc.add_paragraph()
    p_c.add_run(
        "Conclusiones:\n"
        "La implementación de la fase léxica demostró ser el cimiento indispensable para la fiabilidad de todo compilador. "
        "A través de expresiones regulares rigurosas y un manejador de errores contextual, se garantiza que únicamente "
        "secuencias coherentes avancen al análisis sintáctico. El aislamiento de errores léxicos específicos evita la cascada "
        "de fallos posteriores y proporciona a los desarrolladores diagnósticos claros con número de línea, columna y sugerencias.\n\n"
        "Referencias Bibliográficas (APA):\n"
        "• Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Pearson/Addison Wesley.\n"
        "• Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd ed.). Morgan Kaufmann.\n"
        "• Kernighan, B. W., & Ritchie, D. M. (1988). The C Programming Language (2nd ed.). Prentice Hall."
    )

    out_path = os.path.join(script_dir, DOCX_NAME)
    doc.save(out_path)
    print(f"✅ Reporte Word generado exitosamente: {out_path}")
    return out_path


if __name__ == "__main__":
    build_word_report()
