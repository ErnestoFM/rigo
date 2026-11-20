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

# Configurar salida UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Preformatted,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A7_SemanticoTablaSimbolosTipos.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_7"


class NumberedCanvas(canvas.Canvas):
    """Agrega encabezado y pie de página profesional con numeración 'Página X de Y'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))

            # Encabezado
            header_text = "Compiladores - Actividad 7: Semántico Tabla de Símbolos y Tipos - Díaz, Fierro, Hernández, Millán"
            self.drawString(54, 750, header_text)
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 745, letter[0] - 54, 745)

            # Pie de página
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(letter[0] - 54, 38, page_text)
            self.drawString(54, 38, "Reporte Final - Traductores de Lenguaje (Prof. Rigoberto Cárdenas Larios)")
            self.line(54, 48, letter[0] - 54, 48)
            self.restoreState()


def build_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, PDF_NAME)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    style_cover_univ = ParagraphStyle(
        'CoverUniv',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#1E293B")
    )
    style_cover_course = ParagraphStyle(
        'CoverCourse',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#2563EB")
    )
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15.5,
        leading=19,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )
    style_h1 = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )
    style_code_box = ParagraphStyle(
        'CodeBox',
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ==========================================================================
    # PORTADA
    # ==========================================================================
    story.append(Paragraph(
        "UNIVERSIDAD DE GUADALAJARA<br/>"
        "CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS (CUCEI)<br/>"
        "DIVISIÓN DE ELECTRÓNICA Y COMPUTACIÓN<br/>"
        "DEPARTAMENTO DE CIENCIAS COMPUTACIONALES",
        style_cover_univ
    ))
    story.append(Spacer(1, 14))

    divider_table = Table([[""]], colWidths=[letter[0] - 108], rowHeights=[2])
    divider_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2563EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(divider_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("TRADUCTORES DE LENGUAJE / COMPILADORES", style_cover_course))
    story.append(Spacer(1, 6))
    story.append(Paragraph("ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS", style_cover_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Gestión Jerárquica de Ámbitos (Scope Global y Local)<br/>"
        "Estructura de la Tabla de Símbolos, Verificación de Tipos y Detección de Inconsistencias Semánticas",
        style_cover_subtitle
    ))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "<b>INTEGRANTES DEL EQUIPO (Orden Alfabético Estricto por Primer Apellido):</b>",
        ParagraphStyle('TeamHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=1, textColor=colors.HexColor("#1E293B"))
    ))
    story.append(Spacer(1, 6))

    team_data = [
        ["#", "Nombre Completo del Alumno", "Carrera / Institución"],
        ["1", "DÍAZ TORRES JAZMÍN MONTSERRAT", "Ingeniería en Computación - CUCEI"],
        ["2", "FIERRO MELÉNDEZ ERNESTO HATUEY", "Ingeniería en Computación - CUCEI"],
        ["3", "HERNÁNDEZ GARCÍA HÉCTOR GABRIEL", "Ingeniería en Computación - CUCEI"],
        ["4", "MILLÁN GUERRERO OSWALDO JOSUÉ", "Ingeniería en Computación - CUCEI"],
    ]
    team_table = Table(team_data, colWidths=[24, 280, 200])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 16))

    meta_text = (
        "<b>Profesor Titular:</b> Rigoberto Cárdenas Larios<br/>"
        "<b>Ciclo Escolar:</b> 2026-B | Guadalajara, Jalisco<br/>"
        f"<b>Enlace Público al Video Demostrativo (YouTube):</b> <font color='#2563EB'><u>{VIDEO_URL}</u></font>"
    )
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, alignment=1, textColor=colors.HexColor("#334155"))))

    story.append(PageBreak())

    # ==========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y ESTRUCTURA DE LA TABLA DE SÍMBOLOS
    # ==========================================================================
    story.append(Paragraph("1. Introducción y Estructura Formal de la Tabla de Símbolos", style_h1))
    story.append(Paragraph(
        "El análisis semántico examina el Árbol de Sintaxis Abstracta (AST) para verificar que las construcciones sintácticas "
        "posean un significado lógico válido. Una pieza central de esta fase es la <b>Tabla de Símbolos</b>, "
        "la cual mantiene un registro riguroso de cada identificador declarado, su tipo asociado, su alcance o ámbito "
        "(global o local), su nivel de anidamiento y su valor asignado en tiempo de compilación.",
        style_body
    ))

    struct_box = (
        "/* ESPECIFICACION FORMAL DE LA TABLA DE SIMBOLOS (RUBRICA OFICIAL) */\n"
        "tabla_simbolos -> {\n"
        "    identificador -> {\n"
        "        tipo:          tipo_de_dato,       // 'int' | 'float' | 'char' | 'void'\n"
        "        alcance:       global | local,     // Alcance de visibilidad\n"
        "        ambito_nombre: str,                // 'global' o nombre de función contenedora\n"
        "        nivel:         int,                // 0 (global), 1 (función), 2+ (bloques)\n"
        "        valor:         valor_asignado      // Valor constante evaluado\n"
        "    }\n"
        "}\n\n"
        "Funciones Oficiales Implementadas:\n"
        "• inserten_simbolo(identificador, tipo_de_dato, alcance, valor, linea, columna)\n"
        "• busquen_simbolo(identificador) -> Búsqueda ascendente (local -> padre -> global)"
    )
    t_box = Table([[Preformatted(struct_box, style_code_box)]], colWidths=[letter[0] - 108])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 10))

    # ==========================================================================
    # SECCIÓN 2: VERIFICACIÓN DE TIPOS Y GESTIÓN DE ÁMBITOS
    # ==========================================================================
    story.append(Paragraph("2. Reglas de Verificación de Tipos y Control de Ámbitos (Scope)", style_h1))
    story.append(Paragraph(
        "Se implementaron las reglas semánticas y de compatibilidad prescritas por el profesor:<br/>"
        "• <b>Equivalencia Estricta de Tipos:</b> Se prohíbe la asignación directa entre tipos incompatibles como <i>float a int</i> o <i>int a float</i>.<br/>"
        "• <b>Acceso a Variables Globales:</b> Las funciones pueden acceder y modificar variables globales libremente.<br/>"
        "• <b>Confinamiento Local:</b> Las variables locales pertenecen exclusivamente a su función y son inaccesibles en el ámbito global.<br/>"
        "• <b>Enmascaramiento (Shadowing):</b> Las variables locales pueden enmascarar a globales con el mismo identificador sin conflicto.",
        style_body
    ))

    rules_table_data = [
        ["Categoría Semántica", "Patrón de Código", "Resultado / Diagnóstico Reportado"],
        ["Asignación de float a int", "int x; float y = 3.5; x = y;", "Error: Tipo de dato incompatible en la asignación a 'x'."],
        ["Asignación de int a float", "int a = 5; float b; b = a;", "Error: Tipo de dato incompatible en la asignación a 'b'."],
        ["Variable No Declarada", "c = 10;", "Error: Identificador 'c' no declarado en la línea 1."],
        ["Violación de Ámbito Local", "void f() { int loc = 10; } loc = 20;", "Error: Identificador 'loc' no declarado en ámbito global."],
        ["Redeclaración en Ámbito", "int saldo = 100; int saldo = 200;", "Error: El identificador 'saldo' ya fue declarado en ámbito global."]
    ]
    t_rules = Table(rules_table_data, colWidths=[110, 160, 234])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563EB")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rules)
    story.append(Spacer(1, 10))

    # ==========================================================================
    # SECCIÓN 3: BATERÍA DE PRUEBAS
    # ==========================================================================
    story.append(Paragraph("3. Resultados de la Batería de Pruebas (10/10 Aprobadas)", style_h1))
    story.append(Paragraph(
        "Se diseñaron 10 casos de prueba independientes que evalúan exhaustivamente todos los requisitos de la rúbrica:",
        style_body
    ))

    tests_summary_data = [
        ["ID", "Descripción del Caso", "Regla Evaluada", "Resultado"],
        ["01", "Asignación y operaciones homogéneas int", "Tipos Válidos (Rúbrica)", "APROBADO (Tabla)"],
        ["02", "Variable global y local en función miFuncion()", "Ámbitos Válidos (Rúbrica)", "APROBADO (Tabla)"],
        ["03", "Variables float y char con operaciones válidas", "Tipos Primitivos Válidos", "APROBADO (Tabla)"],
        ["04", "Enmascaramiento de variable global por local", "Shadowing Válido", "APROBADO (Tabla)"],
        ["05", "Bucle while y condicional con tipos correctos", "Control de Flujo Válido", "APROBADO (Tabla)"],
        ["06", "int x; float y = 3.5; x = y; (float a int)", "Error Tipos (Rúbrica)", "APROBADO (Error)"],
        ["07", "int a; float b; b = a; (int a float)", "Error Tipos (Rúbrica)", "APROBADO (Error)"],
        ["08", "c = 10; (identificador sin declarar)", "Error Declaración (Rúbrica)", "APROBADO (Error)"],
        ["09", "Uso de variable_local fuera de miFuncion()", "Error Ámbito (Rúbrica)", "APROBADO (Error)"],
        ["10", "int saldo = 100; int saldo = 200; (duplicada)", "Error Redeclaración", "APROBADO (Error)"]
    ]
    t_tests = Table(tests_summary_data, colWidths=[20, 240, 144, 100])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7.5),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_tests)

    story.append(PageBreak())

    # ==========================================================================
    # SECCIÓN 4: SALIDA DE CONSOLA
    # ==========================================================================
    story.append(Paragraph("4. Salida Oficial de Ejecución de Consola (Salida_Ejecucion_Consola.txt)", style_h1))
    story.append(Paragraph(
        "Registro íntegro generado por <code>main.py</code>, verificando la impresión obligatoria "
        "de los nombres de los integrantes en orden alfabético por primer apellido al inicio y al final:",
        style_body
    ))

    log_path = os.path.join(base_dir, "Salida_Ejecucion_Consola.txt")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    else:
        log_content = "[AVISO: Ejecute 'python main.py' para generar la bitácora.]"

    lines = log_content.splitlines()
    chunk_size = 45
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]
        chunk_text = "\n".join(chunk_lines)
        t_chunk = Table([[Preformatted(chunk_text, style_code_box)]], colWidths=[letter[0] - 108])
        t_chunk.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38BDF8")),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_chunk)
        story.append(Spacer(1, 4))

    # ==========================================================================
    # SECCIÓN 5: CONCLUSIONES
    # ==========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Conclusiones y Logros Alcanzados", style_h1))
    story.append(Paragraph(
        "1. <b>Gestión Jerárquica de Ámbitos:</b> Se cumplió el objetivo de estructurar la tabla de símbolos "
        "mediante entornos en árbol, soportando acceso de funciones a variables globales y manteniendo variables locales protegidas.<br/>"
        "2. <b>Verificación Estricta de Tipos:</b> Se implementaron las funciones <code>inserten_simbolo</code> y <code>busquen_simbolo</code>, "
        "garantizando la detección precisa de incompatibilidades de tipo como asignaciones de float a int o viceversa.<br/>"
        "3. <b>Manejo Integral de Errores:</b> El compilador genera mensajes de diagnóstico con coordenadas exactas (línea y columna) "
        "y sugerencias comprensibles a simple vista.<br/>"
        "4. <b>Articulación con el Proyecto Final:</b> Esta actividad se acopla armoniosamente con la Actividad 2 (errores léxicos), "
        "Actividad 5 (sintaxis de control) y Actividad 13 (generación de código y máquina virtual).",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Reporte PDF generado exitosamente: {pdf_path}")


if __name__ == "__main__":
    build_pdf()
