"""
================================================================================
ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - VERIFICACIÓN DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A8_SemanticoExpresionesAritmeticasLogicas.docx"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_8"


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

    r_act = p_title.add_run("ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - EXPRESIONES ARITMÉTICAS Y LÓGICAS\n")
    r_act.font.name = "Arial"
    r_act.font.size = Pt(15.5)
    r_act.font.bold = True
    r_act.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_sub = p_title.add_run(
        "Validación de Tipos en Expresiones, Compatibilidad de Operadores,\n"
        "Detección de División por Cero y Conversiones de Tipo (static_cast)\n"
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

    # Metadatos
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
        "La evaluación y validación semántica de expresiones es una tarea crítica dentro de un compilador. "
        "Su objetivo primordial es garantizar que los operadores aritméticos (+, -, *, /, %), lógicos (&&, ||, !) "
        "y relacionales (==, !=, <, >, <=, >=) se apliquen exclusivamente sobre operandos con tipos de datos válidos "
        "y consistentes, previniendo fallos en tiempo de ejecución como la división entre cero o la coerción inválida de cadenas."
    )
    p_intro.paragraph_format.space_after = Pt(8)

    p_obj = doc.add_paragraph(
        "Objetivos específicos alcanzados:\n"
        "• Verificación de tipos numéricos en expresiones aritméticas, impidiendo operaciones ilícitas con cadenas o booleanos.\n"
        "• Comprobación estricta de operandos booleanos para operadores lógicos (&&, ||, !), rechazando números o cadenas.\n"
        "• Validación de tipos en comparaciones relacionales, prohibiendo comparar cadenas con números.\n"
        "• Detección estática de divisiones por cero en expresiones evaluables en tiempo de compilación.\n"
        "• Soporte y validación para conversiones explícitas de tipo (static_cast<tipo> y cast estilo C).\n"
        "• Interfaz gráfica (Tkinter) interactiva y reporte automatizado en consola con bitácora oficial."
    )
    p_obj.paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 2: REGLAS SEMÁNTICAS Y CATÁLOGO DE OPERADORES
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("2. Reglas Semánticas y Validación de Operadores", level=1)
    h2.style.font.name = "Arial"
    h2.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    rules_table = doc.add_table(rows=6, cols=3)
    rules_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rules_table.autofit = False
    rules_table.columns[0].width = Inches(1.8)
    rules_table.columns[1].width = Inches(2.2)
    rules_table.columns[2].width = Inches(2.5)

    r_headers = ["Operación / Categoría", "Condición Válida vs Inválida", "Diagnóstico Emitido"]
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
        ("Aritmética (+, -, *, /)", "Válido: num + num\nError: edad + nombre", "Error: No se puede aplicar operador aritmético con una cadena de texto."),
        ("Lógica (&&, ||, !)", "Válido: bool && bool\nError: true && 1", "Error: El operador lógico requiere operandos de tipo booleano."),
        ("Relacional (==, !=, <)", "Válido: num == num\nError: '5' == 5", "Error: No se puede comparar una cadena con un número."),
        ("División por Cero", "Válido: 10 / 2\nError: 10 / 0", "Error: División por cero detectada en tiempo de compilación."),
        ("Conversión (static_cast)", "Válido: static_cast<float>(int)\nError: static_cast<int>(string)", "Error: Conversión inválida de 'string' a 'int'.")
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
    # SECCIÓN 3: BATERÍA DE PRUEBAS
    # --------------------------------------------------------------------------
    h3 = doc.add_heading("3. Batería de Pruebas y Validación Experimental", level=1)
    h3.style.font.name = "Arial"
    h3.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    summary_table = doc.add_table(rows=11, cols=4)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    summary_table.autofit = False
    summary_table.columns[0].width = Inches(0.6)
    summary_table.columns[1].width = Inches(2.7)
    summary_table.columns[2].width = Inches(1.9)
    summary_table.columns[3].width = Inches(1.3)

    s_headers = ["ID", "Caso de Prueba", "Regla Evaluada", "Resultado"]
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
        ("01", "Aritmética entera pura: a + b; 5 + 3;", "Aritmética Entera (Rúbrica)", "APROBADO (Eval: 15, 8)"),
        ("02", "Operadores lógicos: activo && inactivo; (10 > 5) && (3 < 8)", "Lógica Booleana (Rúbrica)", "APROBADO (Eval: False, True)"),
        ("03", "Comparaciones relacionales: 5 == 5; 3.14 < 6.28; 'Hola' == 'Hola'", "Comparación Homogénea", "APROBADO (Eval: True)"),
        ("04", "Expresión aritmética compleja: (10 + 20) * (30 - 15)", "Precedencia de Operadores", "APROBADO (Eval: 450)"),
        ("05", "Conversión explícita: static_cast<float>(entero) + 2.5", "Conversión Válida", "APROBADO (Eval: 12.5)"),
        ("06", "edad + nombre (int + string)", "Error Tipo No Numérico", "APROBADO (Error)"),
        ("07", "true && 1 (lógico con int)", "Error Operando No Booleano", "APROBADO (Error)"),
        ("08", "('5' == 5) (comparación string con int)", "Error Comparación", "APROBADO (Error)"),
        ("09", "10 / 0 (división entre cero)", "Error División por Cero", "APROBADO (Error)"),
        ("10", "10 + flag (int + bool)", "Error Operación Aritmética", "APROBADO (Error)")
    ]

    for row_idx, (t_id, desc, rule, res) in enumerate(tests_summary_data, start=1):
        row_cells = summary_table.rows[row_idx].cells
        row_cells[0].text = t_id
        row_cells[1].text = desc
        row_cells[2].text = rule
        row_cells[3].text = res
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for c in row_cells:
            set_cell_background(c, bg)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) if "Eval" in res else RGBColor(0x1E, 0x29, 0x3B)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 4: SALIDA DE CONSOLA
    # --------------------------------------------------------------------------
    h4 = doc.add_heading("4. Registro Oficial de Ejecución de Consola", level=1)
    h4.style.font.name = "Arial"
    h4.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Salida_Ejecucion_Consola.txt")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    else:
        log_content = "[AVISO: Ejecute 'python main.py' para generar la bitácora.]"

    add_code_block(doc, log_content)

    # --------------------------------------------------------------------------
    # SECCIÓN 5: CÓDIGO FUENTE
    # --------------------------------------------------------------------------
    doc.add_page_break()
    h5 = doc.add_heading("5. Código Fuente de los Módulos Principales", level=1)
    h5.style.font.name = "Arial"
    h5.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    source_files = [
        ("semantic_analyzer.py", "Validador de Expresiones Aritméticas y Lógicas"),
        ("parser.py", "Analizador Sintáctico con Precedencia de Expresiones"),
        ("semantic_errors.py", "Manejador y Diagnósticos de Errores")
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
    # SECCIÓN 6: CONCLUSIONES
    # --------------------------------------------------------------------------
    h6 = doc.add_heading("6. Conclusiones", level=1)
    h6.style.font.name = "Arial"
    h6.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_conc = doc.add_paragraph(
        "La realización de la Actividad 8 garantiza que el compilador no solo verifique la forma sintáctica de "
        "las expresiones, sino que valide en profundidad la coherencia de tipos entre los operandos y sus respectivos "
        "operadores. Se impidieron mezclas ilícitas de cadenas con números, operaciones lógicas con enteros y divisiones por cero "
        "evaluadas en tiempo de compilación.\n\n"
        "Esta verificación exhaustiva brinda certeza matemática y lógica al árbol sintáctico, asegurando que las etapas "
        "posteriores de generación de código intermedio y máquina cuenten con expresiones completamente saneadas."
    )
    p_conc.paragraph_format.space_after = Pt(12)

    out_docx_path = os.path.join(base_dir, DOCX_NAME)
    doc.save(out_docx_path)
    print(f"[OK] Reporte Word generado exitosamente: {out_docx_path}")


if __name__ == "__main__":
    build_docx_report()
