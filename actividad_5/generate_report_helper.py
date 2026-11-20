"""
================================================================================
ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL (LENGUAJE C EN PYTHON)
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
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A5_SintacticoEstructurasControl.docx"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_5"


def set_cell_background(cell, fill_hex: str):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_code_block(doc, text: str):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)

    cell = table.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def build_docx_report():
    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # --------------------------------------------------------------------------
    # PORTADA
    # --------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(
        "UNIVERSIDAD DE GUADALAJARA\n"
        "CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS (CUCEI)\n"
        "DIVISIÓN DE ELECTRÓNICA Y COMPUTACIÓN\n"
        "DEPARTAMENTO DE CIENCIAS COMPUTACIONALES\n"
    )
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("―" * 45)
    r_div.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    r_div.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_mat = p_title.add_run("TRADUCTORES DE LENGUAJE / COMPILADORES\n\n")
    r_mat.font.name = "Arial"
    r_mat.font.size = Pt(13)
    r_mat.font.bold = True
    r_mat.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    r_act = p_title.add_run("ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL\n")
    r_act.font.name = "Arial"
    r_act.font.size = Pt(16)
    r_act.font.bold = True
    r_act.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_sub = p_title.add_run(
        "Implementación en Python de un Analizador Sintáctico Descendente Recursivo para C\n"
        "Validación Formal de Condicionales (if/else), Bucles (while, for), Bloques y Recuperación de Errores\n"
    )
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Tabla de Integrantes
    p_team_hdr = doc.add_paragraph()
    p_team_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_thdr = p_team_hdr.add_run("INTEGRANTES DEL EQUIPO\n(Orden Alfabético Estricto por Primer Apellido):")
    r_thdr.font.name = "Arial"
    r_thdr.font.size = Pt(10.5)
    r_thdr.font.bold = True
    r_thdr.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    team_table = doc.add_table(rows=5, cols=2)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_table.autofit = False
    team_table.columns[0].width = Inches(4.5)
    team_table.columns[1].width = Inches(1.8)

    members = [
        ("DÍAZ TORRES JAZMÍN MONTSERRAT", "Estudiante de Ing. en Computación"),
        ("FIERRO MELÉNDEZ ERNESTO HATUEY", "Estudiante de Ing. en Computación"),
        ("HERNÁNDEZ GARCÍA HÉCTOR GABRIEL", "Estudiante de Ing. en Computación"),
        ("MILLÁN GUERRERO OSWALDO JOSUÉ", "Estudiante de Ing. en Computación")
    ]

    hdr_cells = team_table.rows[0].cells
    hdr_cells[0].text = "Nombre Completo del Alumno"
    hdr_cells[1].text = "Rol / Programa"
    for c in hdr_cells:
        set_cell_background(c, "1E293B")
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, (name, rol) in enumerate(members, 1):
        row_cells = team_table.rows[i].cells
        row_cells[0].text = f"{i}. {name}"
        row_cells[1].text = rol
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for c in row_cells:
            set_cell_background(c, bg)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(9)
                    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Metadatos del Curso
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run(
        "PROFESOR: RIGOBERTO CÁRDENAS LARIOS\n"
        "SEMESTRE: 2026-B | GUADALAJARA, JALISCO\n"
        f"ENLACE PÚBLICO AL VIDEO DEMOSTRATIVO: {VIDEO_URL}\n"
    )
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(9.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECCIÓN 1: INTRODUCCIÓN Y OBJETIVOS
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("1. Introducción y Objetivos de la Práctica", level=1)
    h1.style.font.name = "Arial"
    h1.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_intro = doc.add_paragraph(
        "El análisis sintáctico constituye la segunda fase fundamental en la arquitectura de un compilador "
        "o traductor de lenguaje. En esta etapa, el flujo de componentes léxicos (tokens) producido por el "
        "analizador léxico (Lexer) se evalúa contra las reglas gramaticales formales del lenguaje de programación objetivo. "
        "El propósito central de la presente práctica es diseñar, implementar y validar un Analizador Sintáctico "
        "Descendente Recursivo (Recursive Descent Parser) especializado en el reconocimiento riguroso de las "
        "estructuras de control condicionales ('if', 'else') e iterativas ('while', 'for') pertenecientes a un subconjunto "
        "estricto del Lenguaje C, conforme a las directrices de la rúbrica oficial."
    )
    p_intro.paragraph_format.space_after = Pt(8)

    p_obj = doc.add_paragraph(
        "Objetivos específicos alcanzados:\n"
        "• Definición formal de la Gramática Libre de Contexto (GLC) para sentencias condicionales e iterativas.\n"
        "• Construcción de un Árbol de Sintaxis Abstracta (AST) con jerarquía orientada a objetos (ProgramNode, IfNode, WhileNode, ForNode, BlockNode).\n"
        "• Detección precisa de discrepancias sintácticas: paréntesis desbalanceados/faltantes, condiciones inválidas, bloques sin llaves requeridas y componentes de bucle ausentes.\n"
        "• Mecanismo de recuperación de errores en modo pánico (Panic Mode) que previene la interrupción abruptly del compilador.\n"
        "• Interfaz gráfica interactiva en Tkinter y ejecución automatizada por línea de comandos con generación de bitácora."
    )
    p_obj.paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 2: DEFINICIÓN DE LA GRAMÁTICA FORMAL
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("2. Definición Formal de la Gramática para Estructuras de Control", level=1)
    h2.style.font.name = "Arial"
    h2.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_gram = doc.add_paragraph(
        "La gramática implementada se fundamenta en la notación BNF (Backus-Naur Form) estipulada en la rúbrica oficial de la materia:"
    )
    p_gram.paragraph_format.space_after = Pt(6)

    grammar_spec = (
        "estructura_control -> sentencia_if | sentencia_while | sentencia_for\n"
        "sentencia_if       -> 'if' '(' expresion ')' '{' bloque '}' ( 'else' '{' bloque '}' )?\n"
        "sentencia_while    -> 'while' '(' expresion ')' '{' bloque '}'\n"
        "sentencia_for      -> 'for' '(' inicializacion ';' expresion ';' actualizacion ')' '{' bloque '}'\n"
        "bloque             -> ( sentencia )*\n"
        "sentencia          -> expresion ';' | estructura_control | declaracion ';' | asignacion ';' | return ';' \n"
        "inicializacion     -> declaracion | asignacion | ε\n"
        "actualizacion      -> expresion | asignacion | ε\n"
        "expresion          -> expresion_logica_or\n"
        "expresion_rel      -> expresion_aditiva ( ('<' | '<=' | '>' | '>=' | '==' | '!=') expresion_aditiva )*"
    )
    add_code_block(doc, grammar_spec)

    # --------------------------------------------------------------------------
    # SECCIÓN 3: REGLAS SINTÁCTICAS Y GESTIÓN DE ERRORES
    # --------------------------------------------------------------------------
    h3 = doc.add_heading("3. Reglas Sintácticas y Catálogo de Detección de Errores", level=1)
    h3.style.font.name = "Arial"
    h3.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    rules_table = doc.add_table(rows=6, cols=3)
    rules_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rules_table.autofit = False
    rules_table.columns[0].width = Inches(1.8)
    rules_table.columns[1].width = Inches(2.2)
    rules_table.columns[2].width = Inches(2.5)

    r_headers = ["Estructura / Regla", "Condición de Violación", "Mensaje y Sugerencia Reportada"]
    for idx, text in enumerate(r_headers):
        cell = rules_table.rows[0].cells[idx]
        cell.text = text
        set_cell_background(cell, "2563EB")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(9)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    rules_data = [
        ("Condicional 'if'", "Falta de '(' o ')' en la condición", "Paréntesis desbalanceados / faltantes en 'if'. Sugerencia: if (condicion) { ... }"),
        ("Condicional 'if' / 'else'", "Omisión de llaves '{' o '}' en bloque", "Bloque sin llaves '{' obligatorias. La rúbrica prohíbe sentencias de una línea sin llaves."),
        ("Iterativa 'while'", "Falta de condición o paréntesis", "Condición inválida o vacía en 'while'. Sugerencia: while (condicion) { ... }"),
        ("Iterativa 'while'", "Llave de cierre faltante al final", "Llave de cierre '}' faltante en bloque. Se indica la línea de apertura original."),
        ("Iterativa 'for'", "Componentes inválidos o sin ';'", "Componente inválido en estructura 'for'. Se valida 'for (init; cond; update)'.")
    ]

    for row_idx, data in enumerate(rules_data, start=1):
        row_cells = rules_table.rows[row_idx].cells
        for col_idx, val in enumerate(data):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            for p in row_cells[col_idx].paragraphs:
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECCIÓN 4: RESULTADOS DE LA BATERÍA DE PRUEBAS
    # --------------------------------------------------------------------------
    h4 = doc.add_heading("4. Batería de Pruebas y Validación Experimental", level=1)
    h4.style.font.name = "Arial"
    h4.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_tests_intro = doc.add_paragraph(
        "Se evaluaron 10 casos de prueba independientes que abarcan exhaustivamente los escenarios exigidos "
        "en la rúbrica oficial (5 casos de sintaxis válida con generación de AST y 5 casos con errores sintácticos controlados):"
    )
    p_tests_intro.paragraph_format.space_after = Pt(6)

    # Tabla resumen de pruebas
    summary_table = doc.add_table(rows=11, cols=4)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    summary_table.autofit = False
    summary_table.columns[0].width = Inches(0.6)
    summary_table.columns[1].width = Inches(2.6)
    summary_table.columns[2].width = Inches(2.0)
    summary_table.columns[3].width = Inches(1.3)

    s_headers = ["ID", "Descripción del Caso", "Tipo de Estructura", "Resultado"]
    for idx, text in enumerate(s_headers):
        cell = summary_table.rows[0].cells[idx]
        cell.text = text
        set_cell_background(cell, "1E293B")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(9)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tests_summary_data = [
        ("01", "if-else completo con bloques entre llaves", "Condicional Válido", "APROBADO (AST)"),
        ("02", "Bucle while estándar con bloque entre llaves", "Iterativo Válido", "APROBADO (AST)"),
        ("03", "Bucle for con init, condición y actualización", "Iterativo Válido", "APROBADO (AST)"),
        ("04", "for con estructura if-else anidada interna", "Anidamiento Válido", "APROBADO (AST)"),
        ("05", "Programa completo con int main(), while e if", "Programa Válido", "APROBADO (AST)"),
        ("06", "if con paréntesis de cierre ')' faltante", "Error Paréntesis", "APROBADO (Error)"),
        ("07", "while con paréntesis de apertura '(' faltante", "Error Paréntesis", "APROBADO (Error)"),
        ("08", "for con paréntesis de apertura '(' faltante", "Error Paréntesis", "APROBADO (Error)"),
        ("09", "if sin llaves obligatorias '{ ... }'", "Error Bloque", "APROBADO (Error)"),
        ("10", "while con llave de cierre '}' faltante al EOF", "Error Llaves", "APROBADO (Error)")
    ]

    for row_idx, (t_id, desc, struct, res) in enumerate(tests_summary_data, start=1):
        row_cells = summary_table.rows[row_idx].cells
        row_cells[0].text = t_id
        row_cells[1].text = desc
        row_cells[2].text = struct
        row_cells[3].text = res
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for c in row_cells:
            set_cell_background(c, bg)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) if "AST" in res else RGBColor(0x1E, 0x29, 0x3B)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 5: SALIDA COMPLETA DE EJECUCIÓN DE CONSOLA
    # --------------------------------------------------------------------------
    h5 = doc.add_heading("5. Registro Oficial de Ejecución de Consola", level=1)
    h5.style.font.name = "Arial"
    h5.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_log_intro = doc.add_paragraph(
        "A continuación se incluye la transcripción íntegra del archivo generado 'Salida_Ejecucion_Consola.txt', "
        "certificando la impresión de los nombres en orden alfabético estricto como primera y última instrucción:"
    )
    p_log_intro.paragraph_format.space_after = Pt(6)

    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Salida_Ejecucion_Consola.txt")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    else:
        log_content = "[AVISO: Ejecute 'python main.py' para generar la bitácora oficial.]"

    add_code_block(doc, log_content)

    # --------------------------------------------------------------------------
    # SECCIÓN 6: CÓDIGO FUENTE DE LOS MÓDULOS PRINCIPALES
    # --------------------------------------------------------------------------
    doc.add_page_break()
    h6 = doc.add_heading("6. Código Fuente del Analizador Sintáctico", level=1)
    h6.style.font.name = "Arial"
    h6.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    source_files = [
        ("error_handler.py", "Manejador y Reportador de Errores Sintácticos"),
        ("ast_nodes.py", "Jerarquía de Nodos del Árbol de Sintaxis Abstracta (AST)"),
        ("parser.py", "Analizador Sintáctico Descendente Recursivo")
    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    for fname, desc in source_files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            h_sub = doc.add_heading(f"Módulo: {fname} ({desc})", level=2)
            h_sub.style.font.name = "Arial"
            h_sub.style.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
            with open(fpath, "r", encoding="utf-8") as sf:
                code_text = sf.read()
            add_code_block(doc, code_text)

    # --------------------------------------------------------------------------
    # SECCIÓN 7: CONCLUSIONES
    # --------------------------------------------------------------------------
    h7 = doc.add_heading("7. Conclusiones", level=1)
    h7.style.font.name = "Arial"
    h7.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_conc = doc.add_paragraph(
        "La culminación exitosa de la Actividad 5 demuestra la eficacia del paradigma de análisis descendente "
        "recursivo para estructurar y validar gramaticalmente las sentencias más críticas de un lenguaje imperativo como C. "
        "Se verificó la exigencia de bloques acotados por llaves obligatorias '{ ... }', lo cual elimina ambigüedades clásicas "
        "del condicional colgante ('dangling-else') y asegura un código predecible y robusto.\n\n"
        "Asimismo, el diseño de la recuperación de errores mediante modo pánico garantizó que los errores sintácticos "
        "no provoquen un fallo catastrófico del analizador, proporcionando a los desarrolladores diagnósticos claros con "
        "ubicación exacta (línea y columna) y sugerencias directas de solución."
    )
    p_conc.paragraph_format.space_after = Pt(12)

    # Guardar documento
    out_docx_path = os.path.join(base_dir, DOCX_NAME)
    doc.save(out_docx_path)
    print(f"[OK] Reporte Word generado exitosamente: {out_docx_path}")


if __name__ == "__main__":
    build_docx_report()
