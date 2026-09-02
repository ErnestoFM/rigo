"""
================================================================================
ACTIVIDAD 2: MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
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
from io import StringIO
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import main
from lexer import LexerC
from test_cases import (
    C_VALID_TEST,
    C_TEST_UNRECOGNIZED_CHARS,
    C_TEST_MALFORMED_IDENTIFIERS,
    C_TEST_INCORRECT_NUMBERS,
    C_TEST_UNCLOSED_STRINGS,
    C_TEST_COMBINED_ERRORS
)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_report_docx():
    doc = docx.Document()
    
    # Configurar márgenes
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    PRIMARY_NAVY = RGBColor(24, 43, 73)
    SECONDARY_BLUE = RGBColor(41, 128, 185)
    DARK_TEXT = RGBColor(44, 62, 80)
    ERROR_RED = RGBColor(192, 57, 43)

    # ---------------------------------------------------------
    # 1. PORTADA OFICIAL
    # ---------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = title_p.add_run("MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES\nPROFESOR: RIGOBERTO CÁRDENAS LARIOS\n\n")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(12)
    run_sub.font.bold = True
    run_sub.font.color.rgb = SECONDARY_BLUE

    run_title = title_p.add_run("ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS\nDESARROLLO DE UN COMPILADOR EN PYTHON PARA LENGUAJE C\n")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_NAVY

    doc.add_paragraph() # Spacing

    team_p = doc.add_paragraph()
    team_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_team_head = team_p.add_run("INTEGRANTES DEL EQUIPO\n(Orden Alfabético por Primer Apellido):\n\n")
    run_team_head.font.name = 'Arial'
    run_team_head.font.size = Pt(12)
    run_team_head.font.bold = True
    run_team_head.font.color.rgb = PRIMARY_NAVY

    members = [
        "1. DIAZ TORRES JAZMIN MONTSERRAT",
        "2. FIERRO MELÉNDEZ ERNESTO HATUEY",
        "3. HERNANDEZ GARCIA HECTOR GABRIEL",
        "4. MILLAN GUERRERO OSWALDO JOSUE"
    ]

    for m in members:
        mp = doc.add_paragraph()
        mp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        mrun = mp.add_run(m)
        mrun.font.name = 'Arial'
        mrun.font.size = Pt(12)
        mrun.font.bold = True
        mrun.font.color.rgb = DARK_TEXT

    doc.add_paragraph()

    date_p = doc.add_paragraph()
    date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    drun = date_p.add_run("FECHA DE ENTREGA: 4 DE SEPTIEMBRE, 23:59")
    drun.font.name = 'Arial'
    drun.font.size = Pt(11)
    drun.font.italic = True
    drun.font.color.rgb = SECONDARY_BLUE

    doc.add_page_break()

    # ---------------------------------------------------------
    # 2. ENLACE AL VIDEO DEMOSTRATIVO
    # ---------------------------------------------------------
    h1 = doc.add_heading("1. ENLACE PÚBLICO AL VIDEO DEMOSTRATIVO (YOUTUBE)", level=1)
    h1.runs[0].font.color.rgb = PRIMARY_NAVY

    vp = doc.add_paragraph()
    vrun1 = vp.add_run("URL del Video (YouTube / Plataforma pública): ")
    vrun1.font.bold = True
    vrun2 = vp.add_run("https://www.youtube.com/watch?v=TU_ENLACE_AQUI\n")
    vrun2.font.color.rgb = SECONDARY_BLUE
    vrun2.font.underline = True

    note_p = doc.add_paragraph()
    nrun = note_p.add_run("Nota: El video incluye audio explícito, grabación a pantalla completa con reloj de sistema de Windows, explicación de las reglas de error y ejecución en vivo de los 6 casos de prueba (CLI y GUI).")
    nrun.font.italic = True

    # ---------------------------------------------------------
    # 3. INTRODUCCIÓN Y MARCO TEÓRICO
    # ---------------------------------------------------------
    h2 = doc.add_heading("2. INTRODUCCIÓN Y OBJETIVOS", level=1)
    h2.runs[0].font.color.rgb = PRIMARY_NAVY

    intro_text = (
        "El objetivo de esta práctica es implementar un mecanismo robusto para el manejo y reporte de errores léxicos "
        "durante la fase de tokenización de un compilador para el Lenguaje C. "
        "Un analizador léxico no solo debe identificar componentes válidos, sino ser capaz de aislar secuencias defectuosas, "
        "determinar la causa raíz del fallo y reportar la ubicación exacta (línea y columna) junto con sugerencias de corrección.\n\n"
        "Las 4 categorías de errores léxicos requeridas e implementadas son:\n"
        "1. Caracteres No Reconocidos: Símbolos fuera del alfabeto de C (ej. @, $, #, ~, ¿, ñ).\n"
        "2. Identificadores Mal Formados: Identificadores que inician con dígitos (ej. 123contador).\n"
        "3. Literales Numéricos Incorrectos: Números con múltiples puntos flotantes (ej. 3.14.15), hexadecimales inválidos (0x12G4) o exponentes incompletos (1.5e+).\n"
        "4. Cadenas Mal Formadas: Cadenas de texto no delimitadas antes de finalizar la línea o archivo."
    )
    doc.add_paragraph(intro_text)

    # ---------------------------------------------------------
    # 4. CÓDIGO FUENTE DESARROLLADO
    # ---------------------------------------------------------
    h3 = doc.add_heading("3. CÓDIGO FUENTE DESARROLLADO", level=1)
    h3.runs[0].font.color.rgb = PRIMARY_NAVY

    files_info = [
        ("error_handler.py", "c:/Users/hatue/Documents/rigo/error_handler.py", "Manejador centralizado de errores léxicos."),
        ("token_type.py", "c:/Users/hatue/Documents/rigo/token_type.py", "Definición de tokens y subtipos de errores léxicos."),
        ("lexer.py", "c:/Users/hatue/Documents/rigo/lexer.py", "Analizador léxico con expresiones regulares avanzadas."),
        ("test_cases.py", "c:/Users/hatue/Documents/rigo/test_cases.py", "Suites de prueba válidas e inválidas."),
        ("main.py", "c:/Users/hatue/Documents/rigo/main.py", "Ejecutable CLI con firmas de integrantes en inicio y fin."),
        ("gui.py", "c:/Users/hatue/Documents/rigo/gui.py", "Interfaz gráfica interactiva en Tkinter para diagnóstico.")
    ]

    for fname, fpath, fdesc in files_info:
        fh = doc.add_heading(f"Archivo: {fname}", level=2)
        fh.runs[0].font.color.rgb = SECONDARY_BLUE
        
        dp = doc.add_paragraph(f"Descripción: {fdesc}")
        dp.runs[0].font.italic = True

        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                code_content = f.read()

            table = doc.add_table(rows=1, cols=1)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = table.cell(0, 0)
            set_cell_background(cell, "F2F4F4")
            
            p = cell.paragraphs[0]
            run = p.add_run(code_content)
            run.font.name = 'Consolas'
            run.font.size = Pt(8.5)
            run.font.color.rgb = DARK_TEXT
            
        doc.add_paragraph()

    # ---------------------------------------------------------
    # 5. SALIDAS DE EJECUCIÓN Y REPORTES DE ERRORES
    # ---------------------------------------------------------
    h4 = doc.add_heading("4. RESULTADOS DE EJECUCIÓN Y TABLAS DE DIAGNÓSTICO", level=1)
    h4.runs[0].font.color.rgb = PRIMARY_NAVY

    # Capturar la salida completa de main.py
    buffer = StringIO()
    sys.stdout = buffer
    main.main()
    sys.stdout = sys.__stdout__
    raw_output = buffer.getvalue()

    p_log_intro = doc.add_paragraph("A continuación se muestra el registro estructurado generado durante la ejecución de las 6 suites de prueba:")
    
    table_log = doc.add_table(rows=1, cols=1)
    table_log.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_log = table_log.cell(0, 0)
    set_cell_background(cell_log, "1E1E2E")
    
    p_log = cell_log.paragraphs[0]
    run_log = p_log.add_run(raw_output)
    run_log.font.name = 'Consolas'
    run_log.font.size = Pt(8.0)
    run_log.font.color.rgb = RGBColor(205, 214, 244)

    # Guardar documento Word
    output_filename = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A2_ManejoErroresLexicos.docx"
    doc.save(output_filename)
    print(f"✔ Documento Word generado exitosamente: '{output_filename}'")

if __name__ == "__main__":
    create_report_docx()
