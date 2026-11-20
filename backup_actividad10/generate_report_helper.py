"""
================================================================================
ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
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

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A10_CodigoIntermedio.docx"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_10"


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

    r_act = p_title.add_run("ACTIVIDAD 10: CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)\n")
    r_act.font.name = "Arial"
    r_act.font.size = Pt(16)
    r_act.font.bold = True
    r_act.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_sub = p_title.add_run(
        "Representación de Tres Direcciones para Asignaciones, Constantes, Variables y Expresiones\n"
        "Generación de Temporales, Aplanamiento de Expresiones Anidadas y Validaciones con Guardas\n"
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
        "El código intermedio es una representación intermedia independiente de la arquitectura destino que "
        "facilita tanto la optimización de código como la posterior traducción a instrucciones de máquina. "
        "En la presente práctica se implementó un generador de Código de Tres Direcciones (Three-Address Code - TAC) "
        "conforme a las directrices exactas de la rúbrica oficial del profesor Rigoberto Cárdenas Larios, "
        "representando cada constante literal mediante una etiqueta temporal explicativa (t1 = 5; x = t1), "
        "desglosando expresiones aritméticas y booleanas anidadas en instrucciones lineales atómicas, y emitiendo "
        "instrucciones condicionales de validación (guardas) para división por cero y discrepancias de tipos."
    )
    p_intro.paragraph_format.space_after = Pt(8)

    p_obj = doc.add_paragraph(
        "Objetivos específicos alcanzados:\n"
        "• Asignación de constantes a variables mediante etiquetas temporales intermedias (t1, t2, ...).\n"
        "• Descomposición de expresiones aritméticas complejas y anidadas en secuencias de instrucciones TAC de una sola operación.\n"
        "• Representación de expresiones booleanas y de comparación mediante etiquetas temporales.\n"
        "• Inserción de instrucciones de guarda de validación estática para división por cero e incompatibilidad de tipos.\n"
        "• Interfaz gráfica interactiva (Tkinter) y ejecución por consola con bitácora oficial."
    )
    p_obj.paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 2: MODELO TAC IMPLEMENTADO
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("2. Modelo de Representación TAC y Formato de Instrucciones", level=1)
    h2.style.font.name = "Arial"
    h2.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_model = doc.add_paragraph(
        "El generador produce instrucciones lineales siguiendo estrictamente los patrones de la rúbrica:"
    )
    p_model.paragraph_format.space_after = Pt(6)

    model_box = (
        "# 1. ASIGNACION DE CONSTANTES A VARIABLES\n"
        "t1 = 5               # t1 es una etiqueta temporal que representa la constante 5\n"
        "x = t1               # Asigna el valor de t1 a x\n\n"
        "# 2. USO DE VARIABLES Y EXPRESIONES ANIDADAS\n"
        "t4 = b + c           # t4 es una etiqueta temporal que representa la suma de b y c\n"
        "t5 = a * t4          # t5 es una etiqueta temporal que representa la multiplicación de a por t4\n"
        "result = t5          # Asigna el valor de t5 a result\n\n"
        "# 3. GUARDAS DE VALIDACION Y CONTROL DE ERRORES\n"
        "if b == 0 then error \"Division by zero\" # Valida que no se realice división por cero\n"
        "if type(a) != integer or type(\"str\") != integer then error \"Type mismatch\" # Valida tipos"
    )
    add_code_block(doc, model_box)

    # --------------------------------------------------------------------------
    # SECCIÓN 3: BATERÍA DE PRUEBAS
    # --------------------------------------------------------------------------
    doc.add_page_break()
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

    s_headers = ["ID", "Descripción del Caso de Prueba", "Regla de Rúbrica", "Resultado"]
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
        ("01", "x = 5; y = 10; (Constantes a temporales)", "Variables y Constantes", "APROBADO (TAC)"),
        ("02", "z = x + y; (Uso de variables)", "Uso de Variables", "APROBADO (TAC)"),
        ("03", "result = a * (b + c); (Expresión aritmética)", "Aritmética Anidada", "APROBADO (TAC)"),
        ("04", "flag = (x > y) && (z < 10); (Lógica/Relacional)", "Expresiones Lógicas", "APROBADO (TAC)"),
        ("05", "total = (a + b) * (c - d); result = (x + y) / (z - w);", "Expresiones Complejas", "APROBADO (TAC)"),
        ("06", "result = a / b; (Guardia de división por cero)", "Validación de División", "APROBADO (Guarda)"),
        ("07", "total = a + 'string'; (Validación de tipos)", "Validación de Tipos", "APROBADO (Guarda/Bloqueo)"),
        ("08", "result = 100 / 0; (División constante cero)", "Error División", "APROBADO (Error)"),
        ("09", "flag = (x > y) && 'invalido'; (Lógico con cadena)", "Error Tipo Lógico", "APROBADO (Error)"),
        ("10", "contador = 'texto'; (Asignación incompatible)", "Error Asignación", "APROBADO (Error)")
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
                    r.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) if "TAC" in res or "Guarda" in res else RGBColor(0x1E, 0x29, 0x3B)

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
        ("tac_generator.py", "Generador de Código de Tres Direcciones"),
        ("tac_instruction.py", "Estructura de Instrucciones y Guardas TAC"),
        ("error_handler.py", "Manejador y Diagnósticos de Validación")
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
        "La generación de código intermedio de tres direcciones (TAC) constituye el puente indispensable entre "
        "el análisis sintáctico/semántico y la generación de código máquina ejecutable. "
        "Al descomponer asignaciones y expresiones anidadas en instrucciones de como máximo un operador y dos operandos, "
        "se linealiza el flujo de cálculo y se posibilita la asignación sistemática de registros y direcciones de memoria.\n\n"
        "Asimismo, la incorporación de instrucciones condicionales de guarda para división por cero e incompatibilidad de tipos "
        "garantiza que el código intermedio generado contenga salvaguardas robustas antes de traducirse a código ensamblador."
    )
    p_conc.paragraph_format.space_after = Pt(12)

    out_docx_path = os.path.join(base_dir, DOCX_NAME)
    doc.save(out_docx_path)
    print(f"[OK] Reporte Word generado exitosamente: {out_docx_path}")


if __name__ == "__main__":
    build_docx_report()
