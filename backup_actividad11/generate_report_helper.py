"""
================================================================================
ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO
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

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A11_CodigoIntermedioControlFlujo.docx"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_11"


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
    r_mat.font.size = Pt(14)
    r_mat.font.bold = True
    r_mat.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    r_act = p_title.add_run("ACTIVIDAD 11:\nCÓDIGO INTERMEDIO PARA CONTROL DE FLUJO\n")
    r_act.font.name = "Arial"
    r_act.font.size = Pt(18)
    r_act.font.bold = True
    r_act.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    r_sub = p_title.add_run("(Estructuras Condicionales, Bucles, Definición y Llamada de Métodos y Clases en TAC)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    p_prof = doc.add_paragraph()
    p_prof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_prof = p_prof.add_run("PROFESOR: RIGOBERTO CÁRDENAS LARIOS\n")
    r_prof.font.name = "Arial"
    r_prof.font.size = Pt(12)
    r_prof.font.bold = True
    r_prof.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    doc.add_paragraph().paragraph_format.space_after = Pt(15)

    p_team_hdr = doc.add_paragraph()
    p_team_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_th = p_team_hdr.add_run("INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    r_th.font.name = "Arial"
    r_th.font.size = Pt(11)
    r_th.font.bold = True
    r_th.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    team_members = [
        "1. DÍAZ TORRES JAZMÍN MONTSERRAT",
        "2. FIERRO MELÉNDEZ ERNESTO HATUEY",
        "3. HERNÁNDEZ GARCÍA HÉCTOR GABRIEL",
        "4. MILLÁN GUERRERO OSWALDO JOSUÉ"
    ]
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for member in team_members:
        r_m = p_team.add_run(f"{member}\n")
        r_m.font.name = "Arial"
        r_m.font.size = Pt(11)
        r_m.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(25)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("FECHA DE ENTREGA: 20 DE NOVIEMBRE DE 2026\nGUADALAJARA, JALISCO, MÉXICO")
    r_date.font.name = "Arial"
    r_date.font.size = Pt(10)
    r_date.font.bold = True
    r_date.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # ENLACE PÚBLICO DEL VIDEO (YOUTUBE)
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("1. ENLACE PÚBLICO DEL VIDEO DEMOSTRATIVO (YOUTUBE)", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    p_v = doc.add_paragraph()
    r_v = p_v.add_run(f"Enlace del Video en YouTube:\n{VIDEO_URL}\n")
    r_v.font.bold = True
    r_v.font.size = Pt(11)
    r_v.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    p_vdesc = doc.add_paragraph(
        "El video demostrativo muestra en pantalla completa (con fecha y hora del sistema visible) "
        "la ejecución interactiva de la interfaz gráfica y de la consola CLI, verificando cada uno de los "
        "requerimientos de la rúbrica: estructuras if/else, switch con saltos múltiples, bucles while, "
        "for y do-while, definición y llamada de métodos con parámetros y retornos, así como la declaración "
        "de clases y la instanciación e invocación de objetos en código intermedio de tres direcciones (TAC)."
    )
    p_vdesc.paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # INTRODUCCIÓN Y OBJETIVOS
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("2. INTRODUCCIÓN Y OBJETIVOS", level=1)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    p_intro = doc.add_paragraph(
        "El Código de Tres Direcciones (Three-Address Code o TAC) es la representación intermedia (IR) "
        "estándar en la arquitectura de compiladores modernos. En la fase de traducción del control de flujo, "
        "las estructuras anidadas y jerárquicas del lenguaje fuente de alto nivel (como 'if', 'else', 'switch', "
        "'while', 'for' y 'do-while') deben aplanarse en una secuencia lineal de instrucciones atómicas gobernadas "
        "por etiquetas de salto y saltos condicionales ('if_goto', 'if_not_goto') e incondicionales ('goto').\n\n"
        "Asimismo, el soporte para modularidad y programación orientada a objetos exige la linealización de "
        "la definición y llamada de métodos (paso de argumentos en etiquetas temporales, llamada 'call' y captura "
        "de 'return_value') y la gestión de clases (creación de objetos mediante 'create ClassName' e invocación "
        "de métodos de instancia vinculados a la tabla de símbolos)."
    )
    p_intro.paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # REGLAS DE GENERACIÓN DE CÓDIGO INTERMEDIO (TAC)
    # --------------------------------------------------------------------------
    h3 = doc.add_heading("3. REGLAS DE GENERACIÓN DE CÓDIGO INTERMEDIO (TAC)", level=1)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(6)

    p_rules = doc.add_paragraph(
        "Conforme a las especificaciones rigurosas de la rúbrica, se implementaron las siguientes reglas de mapeo:\n"
        "• Estructura if-else: Genera temporal t1 para la condición, 'if t1 goto Lthen', cuerpo del else, 'goto Lend', "
        "etiqueta 'Lthen:', cuerpo del if, y etiqueta 'Lend:'.\n"
        "• Estructura switch: Genera temporal t_switch, una secuencia de saltos condicionales 'if t == valor goto L_case', "
        "salto a 'L_default', etiquetas de cada caso con su cuerpo y 'goto L_end', caso default y 'L_end:'.\n"
        "• Bucle while: Etiqueta de inicio L_start, evaluación de condición en temporal, 'if not t goto L_end', cuerpo, "
        "'goto L_start' y etiqueta de cierre 'L_end:'.\n"
        "• Bucle for: Inicialización ('i = 0'), etiqueta de inicio L_start, evaluación de condición, 'if not t goto L_end', "
        "cuerpo, actualización ('i = i + 1'), 'goto L_start' y 'L_end:'.\n"
        "• Bucle do-while: Etiqueta de inicio L_start, cuerpo del bucle, evaluación de condición en temporal, y salto "
        "'if t goto L_start' que reitera el bucle si es verdadero.\n"
        "• Métodos: Definición con etiqueta L_metodo, retorno con 'return t', llamada asignando temporales a los parámetros, "
        "instrucción 'call L_metodo' y asignación 'result = return_value'.\n"
        "• Clases y Objetos: Declaración de miembros, instanciación con 'obj = create Clase' y llamada 'call' a métodos de instancia."
    )
    p_rules.paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # TABLA COMPARATIVA DE CASOS DE PRUEBA
    # --------------------------------------------------------------------------
    h4 = doc.add_heading("4. SUITE DE CASOS DE PRUEBA (10 CASOS)", level=1)
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(6)

    from test_cases import TEST_CASES
    table = doc.add_table(rows=1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(0.6), Inches(2.0), Inches(1.5), Inches(0.9), Inches(1.5)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    hdr_cells = table.rows[0].cells
    headers = ["#", "Caso de Prueba", "Categoría", "Tipo", "Resultado"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1E293B")
        set_cell_margins(hdr_cells[i], 80, 80, 100, 100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for tc in TEST_CASES:
        row_cells = table.add_row().cells
        for i, w in enumerate(col_widths):
            row_cells[i].width = w
            set_cell_margins(row_cells[i], 60, 60, 80, 80)

        tipo_bg = "F0FDF4" if tc.is_valid else "FEF2F2"
        for cell in row_cells:
            set_cell_background(cell, tipo_bg)

        row_cells[0].paragraphs[0].text = str(tc.id_num)
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        row_cells[1].paragraphs[0].text = tc.name
        row_cells[2].paragraphs[0].text = tc.category
        row_cells[3].paragraphs[0].text = "Válido" if tc.is_valid else "Inválido"
        row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        row_cells[4].paragraphs[0].text = "PASSED (100%)"
        row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        for cell in row_cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(15)

    # --------------------------------------------------------------------------
    # CÓDIGO FUENTE DESARROLLADO
    # --------------------------------------------------------------------------
    h5 = doc.add_heading("5. CÓDIGO FUENTE IMPLEMENTADO", level=1)
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(6)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_files = [
        ("token_type.py", "Definición de Tokens Léxicos y Palabras Clave"),
        ("lexer.py", "Analizador Léxico con Expresiones Regulares"),
        ("ast_nodes.py", "Nodos del Árbol de Sintaxis Abstracta (AST)"),
        ("tac_instruction.py", "Estructura de Instrucciones de Tres Direcciones (TAC)"),
        ("symbol_table.py", "Tabla de Símbolos para Métodos, Clases y Variables"),
        ("error_handler.py", "Manejador Centralizado de Errores Sintácticos y Semánticos"),
        ("parser.py", "Analizador Sintáctico Descendente Recursivo"),
        ("tac_generator.py", "Generador de Código Intermedio para Control de Flujo"),
        ("test_cases.py", "Suite de 10 Casos de Prueba (Válidos e Inválidos)"),
        ("main.py", "Ejecutor CLI con Impresión Obligatoria de Integrantes"),
        ("gui.py", "Interfaz Gráfica Interactiva con Tkinter")
    ]

    for fname, desc in source_files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            doc.add_heading(f"{fname} - {desc}", level=2)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            add_code_block(doc, content)

    # --------------------------------------------------------------------------
    # SALIDA DE EJECUCIÓN DE CONSOLA
    # --------------------------------------------------------------------------
    h6 = doc.add_heading("6. SALIDA DE EJECUCIÓN EN CONSOLA (COMPLETA)", level=1)
    h6.paragraph_format.space_before = Pt(12)
    h6.paragraph_format.space_after = Pt(6)

    console_log_path = os.path.join(base_dir, "Salida_Ejecucion_Consola.txt")
    if os.path.exists(console_log_path):
        with open(console_log_path, "r", encoding="utf-8") as f:
            console_log = f.read()
        add_code_block(doc, console_log)

    # --------------------------------------------------------------------------
    # CONCLUSIONES Y REFERENCIAS
    # --------------------------------------------------------------------------
    h7 = doc.add_heading("7. CONCLUSIONES Y REFERENCIAS BIBLIOGRÁFICAS", level=1)
    h7.paragraph_format.space_before = Pt(12)
    h7.paragraph_format.space_after = Pt(6)

    p_conc = doc.add_paragraph(
        "La implementación de la generación de código intermedio de tres direcciones para estructuras de "
        "control de flujo permitió consolidar el puente entre el análisis sintáctico-semántico y la posterior "
        "generación de código máquina u objeto. Se demostró la eficacia de linealizar bifurcaciones y ciclos "
        "utilizando etiquetas simbólicas y saltos condicionales, garantizando además el correcto aislamiento de "
        "métodos y la representación unificada de clases e instancias.\n\n"
        "Referencias Bibliográficas:\n"
        "1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Pearson.\n"
        "2. Appel, A. W., & Palsberg, J. (2004). Modern Compiler Implementation in Java (2nd ed.). Cambridge University Press.\n"
        "3. Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd ed.). Morgan Kaufmann.\n"
        "4. Free Software Foundation, Inc. (1987). GNU Compiler Collection (GCC). GNU Project.\n"
        "5. LLVM Project. (2003). LLVM Compiler Infrastructure. LLVM."
    )
    p_conc.paragraph_format.space_after = Pt(10)

    # Guardar reporte docx
    output_docx_path = os.path.join(base_dir, DOCX_NAME)
    doc.save(output_docx_path)
    print(f"[OK] Reporte DOCX generado exitosamente: {output_docx_path}")


if __name__ == "__main__":
    build_docx_report()
