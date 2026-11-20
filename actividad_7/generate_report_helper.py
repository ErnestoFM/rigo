"""
================================================================================
ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
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

DOCX_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A7_SemanticoTablaSimbolosTipos.docx"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_7"


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

    r_act = p_title.add_run("ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS\n")
    r_act.font.name = "Arial"
    r_act.font.size = Pt(15.5)
    r_act.font.bold = True
    r_act.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_sub = p_title.add_run(
        "Implementación de la Gestión Jerárquica de Ámbitos (Scope Global y Local)\n"
        "Estructura de la Tabla de Símbolos, Verificación Estricta de Tipos y Detección de Errores Semánticos\n"
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
        "El análisis semántico es la fase del compilador responsable de comprobar que el código fuente "
        "cumpla con las reglas semánticas y de tipado que la gramática libre de contexto no puede expresar por sí sola. "
        "En esta etapa, el analizador semántico examina el Árbol de Sintaxis Abstracta (AST), interactúa con la "
        "<b>Tabla de Símbolos</b> para consultar y registrar información sobre identificadores (variables y funciones), "
        "gestiona la visibilidad o alcance (ámbitos globales y locales), e impone la estricta compatibilidad entre tipos de datos."
    )
    p_intro.paragraph_format.space_after = Pt(8)

    p_obj = doc.add_paragraph(
        "Objetivos específicos alcanzados:\n"
        "• Diseño e implementación de la estructura de la Tabla de Símbolos en Python, soportando 'inserten_simbolo' y 'busquen_simbolo'.\n"
        "• Gestión jerárquica de ámbitos (Scope): ámbito global y ámbitos locales de funciones con soporte para enmascaramiento.\n"
        "• Verificación estricta de tipos de datos en declaraciones, inicializaciones y sentencias de asignación (int, float, char, void).\n"
        "• Detección y reporte detallado de errores semánticos: variables no declaradas, asignaciones incompatibles y redeclaración en el mismo ámbito.\n"
        "• Interfaz gráfica (Tkinter) con visor de tabla de símbolos en vivo y ejecución por consola con bitácora oficial."
    )
    p_obj.paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 2: ESTRUCTURA DE LA TABLA DE SÍMBOLOS
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("2. Definición y Estructura de la Tabla de Símbolos", level=1)
    h2.style.font.name = "Arial"
    h2.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_struct = doc.add_paragraph(
        "Conforme a las instrucciones de la rúbrica oficial, la tabla de símbolos se diseñó estructurada en diccionarios y objetos con las propiedades:"
    )
    p_struct.paragraph_format.space_after = Pt(6)

    struct_spec = (
        "tabla_simbolos -> {\n"
        "    identificador: {\n"
        "        tipo: tipo_de_dato,       // 'int' | 'float' | 'char' | 'void'\n"
        "        alcance: global | local,  // 'global' para archivo, 'local' para funciones\n"
        "        ambito_nombre: str,       // 'global' o nombre de la función contenedora\n"
        "        nivel: int,               // 0 (global), 1 (función), 2+ (bloques internos)\n"
        "        valor: valor_asignado,    // Constante o valor evaluado en tiempo de compilación\n"
        "        linea: int, columna: int  // Coordenadas exactas en el archivo fuente\n"
        "    }\n"
        "}\n\n"
        "Funciones Oficiales Implementadas:\n"
        "• inserten_simbolo(identificador, tipo_de_dato, alcance, valor, linea, columna)\n"
        "• busquen_simbolo(identificador) -> Realiza búsqueda jerárquica (local -> padre -> global)"
    )
    add_code_block(doc, struct_spec)

    # --------------------------------------------------------------------------
    # SECCIÓN 3: VERIFICACIÓN DE TIPOS Y GESTIÓN DE ÁMBITOS
    # --------------------------------------------------------------------------
    h3 = doc.add_heading("3. Verificación de Tipos de Datos y Control de Ámbitos", level=1)
    h3.style.font.name = "Arial"
    h3.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_rules = doc.add_paragraph(
        "Se implementaron las reglas semánticas y de compatibilidad estipuladas por el profesor:\n"
        "1. <b>Equivalencia de Tipos Estricta:</b> La asignación entre tipos dispares (por ejemplo, float a int o int a float) genera un error semántico explícito.\n"
        "2. <b>Resolución de Ámbitos:</b> Una variable declarada en el ámbito global es visible y modificable desde funciones. "
        "Las variables declaradas dentro de una función pertenecen exclusivamente a su ámbito local y son invisibles en el ámbito global.\n"
        "3. <b>Enmascaramiento (Shadowing):</b> Si una variable local comparte identificador con una global, la local toma prioridad dentro de su bloque sin generar colisión.\n"
        "4. <b>Unicidad en el Mismo Ámbito:</b> Se prohíbe redeclarar un identificador dentro del mismo entorno léxico."
    )
    p_rules.paragraph_format.space_after = Pt(10)

    rules_table = doc.add_table(rows=5, cols=3)
    rules_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rules_table.autofit = False
    rules_table.columns[0].width = Inches(2.0)
    rules_table.columns[1].width = Inches(2.0)
    rules_table.columns[2].width = Inches(2.5)

    r_headers = ["Categoría Semántica", "Patrón de Código", "Resultado / Diagnóstico"]
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
        ("Asignación de float a int", "int x; float y = 3.5; x = y;", "Error: Tipo de dato incompatible en la asignación a 'x'."),
        ("Asignación de int a float", "int a = 5; float b; b = a;", "Error: Tipo de dato incompatible en la asignación a 'b'."),
        ("Variable No Declarada", "c = 10;", "Error: Identificador 'c' no declarado en la línea 1."),
        ("Violación de Ámbito Local", "void f() { int loc = 10; } loc = 20;", "Error: Identificador 'loc' no declarado en ámbito global.")
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
    # SECCIÓN 4: BATERÍA DE PRUEBAS
    # --------------------------------------------------------------------------
    h4 = doc.add_heading("4. Batería de Pruebas y Validación Experimental", level=1)
    h4.style.font.name = "Arial"
    h4.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    summary_table = doc.add_table(rows=11, cols=4)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    summary_table.autofit = False
    summary_table.columns[0].width = Inches(0.6)
    summary_table.columns[1].width = Inches(2.7)
    summary_table.columns[2].width = Inches(1.9)
    summary_table.columns[3].width = Inches(1.3)

    s_headers = ["ID", "Descripción del Caso de Prueba", "Regla Evaluada", "Resultado"]
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
        ("01", "Asignación y operaciones homogéneas int", "Tipos Válidos", "APROBADO (Tabla)"),
        ("02", "Variable global y local en función miFuncion()", "Ámbitos Válidos", "APROBADO (Tabla)"),
        ("03", "Variables float y char con operaciones válidas", "Tipos Válidos", "APROBADO (Tabla)"),
        ("04", "Enmascaramiento de variable global en ámbito local", "Shadowing Válido", "APROBADO (Tabla)"),
        ("05", "Bucle while y condicional if con tipos correctos", "Control Válido", "APROBADO (Tabla)"),
        ("06", "int x; float y = 3.5; x = y; (float a int)", "Error Tipos", "APROBADO (Error)"),
        ("07", "int a; float b; b = a; (int a float)", "Error Tipos", "APROBADO (Error)"),
        ("08", "c = 10; (identificador sin declarar)", "Error Declaración", "APROBADO (Error)"),
        ("09", "Uso de variable_local fuera de miFuncion()", "Error Ámbito", "APROBADO (Error)"),
        ("10", "int saldo = 100; int saldo = 200; (duplicada)", "Error Redeclaración", "APROBADO (Error)")
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
                    r.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) if "Tabla" in res else RGBColor(0x1E, 0x29, 0x3B)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # SECCIÓN 5: SALIDA DE CONSOLA
    # --------------------------------------------------------------------------
    h5 = doc.add_heading("5. Registro Oficial de Ejecución de Consola", level=1)
    h5.style.font.name = "Arial"
    h5.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Salida_Ejecucion_Consola.txt")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    else:
        log_content = "[AVISO: Ejecute 'python main.py' para generar la bitácora.]"

    add_code_block(doc, log_content)

    # --------------------------------------------------------------------------
    # SECCIÓN 6: CÓDIGO FUENTE PRINCIPAL
    # --------------------------------------------------------------------------
    doc.add_page_break()
    h6 = doc.add_heading("6. Código Fuente de los Módulos Principales", level=1)
    h6.style.font.name = "Arial"
    h6.style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    source_files = [
        ("symbol_table.py", "Gestión de la Tabla de Símbolos y Ámbitos"),
        ("semantic_analyzer.py", "Analizador Semántico y Comprobación de Tipos"),
        ("semantic_errors.py", "Manejador y Diagnósticos de Errores Semánticos")
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
        "La implementación de la Actividad 7 consolida los pilares semánticos esenciales en la construcción "
        "del compilador en C. La tabla de símbolos estructurada jerárquicamente permite no solo aislar los entornos "
        "léxicos locales de las funciones respecto al ámbito global, sino también resolver variables con enmascaramiento "
        "de manera natural y eficiente.\n\n"
        "La verificación estricta de tipos de datos en sentencias de declaración y asignación garantiza la detección temprana "
        "de discrepancias lógicas, protegiendo al programador contra pérdidas de precisión no intencionadas y asegurando que las "
        "instrucciones que posteriormente se traduzcan a código intermedio o ensamblador cuenten con operandos plenamente válidos."
    )
    p_conc.paragraph_format.space_after = Pt(12)

    out_docx_path = os.path.join(base_dir, DOCX_NAME)
    doc.save(out_docx_path)
    print(f"[OK] Reporte Word generado exitosamente: {out_docx_path}")


if __name__ == "__main__":
    build_docx_report()
