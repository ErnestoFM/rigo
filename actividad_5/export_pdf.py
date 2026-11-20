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

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A5_SintacticoEstructurasControl.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_5"


class NumberedCanvas(canvas.Canvas):
    """Agrega pie de página profesional con numeración dinámica 'Página X de Y' y encabezado."""
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
            header_text = "Compiladores - Actividad 5: Sintáctico Estructuras de Control - Díaz, Fierro, Hernández, Millán"
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

    # Estilos tipográficos personalizados
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
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )
    style_h1 = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )
    style_code_box = ParagraphStyle(
        'CodeBox',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ==========================================================================
    # PORTADA OFICIAL
    # ==========================================================================
    story.append(Paragraph(
        "UNIVERSIDAD DE GUADALAJARA<br/>"
        "CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS (CUCEI)<br/>"
        "DIVISIÓN DE ELECTRÓNICA Y COMPUTACIÓN<br/>"
        "DEPARTAMENTO DE CIENCIAS COMPUTACIONALES",
        style_cover_univ
    ))
    story.append(Spacer(1, 14))

    # Línea decorativa
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
    story.append(Paragraph("ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL", style_cover_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Implementación en Python de un Analizador Sintáctico Descendente Recursivo para C<br/>"
        "Validación Formal de Condicionales (if/else), Bucles (while, for), Bloques y Recuperación de Errores",
        style_cover_subtitle
    ))
    story.append(Spacer(1, 16))

    # Tabla de integrantes en orden alfabético
    story.append(Paragraph(
        "<b>INTEGRANTES DEL EQUIPO (Orden Alfabético Estricto por Primer Apellido):</b>",
        ParagraphStyle('TeamHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, alignment=1, textColor=colors.HexColor("#1E293B"))
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
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
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
        f"<b>Enlace Público de Video Demostrativo (YouTube):</b> <font color='#2563EB'><u>{VIDEO_URL}</u></font>"
    )
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, alignment=1, textColor=colors.HexColor("#334155"))))

    story.append(PageBreak())

    # ==========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y GRAMÁTICA FORMAL
    # ==========================================================================
    story.append(Paragraph("1. Introducción y Gramática Formal de Estructuras de Control", style_h1))
    story.append(Paragraph(
        "El análisis sintáctico valida la estructura jerárquica del código fuente frente a una Gramática Libre de Contexto (GLC). "
        "En la presente práctica se implementó un <b>Analizador Sintáctico Descendente Recursivo</b> (Recursive Descent Parser) "
        "para validar estructuras condicionales (<i>if</i>, <i>else</i>) y bucles iterativos (<i>while</i>, <i>for</i>) "
        "bajo la sintaxis del lenguaje C. Un aspecto central de la rúbrica es la obligatoriedad de delimitar bloques entre llaves <code>{ ... }</code>, "
        "impidiendo sentencias huérfanas de una sola línea y erradicando el problema clásico del 'dangling-else'.",
        style_body
    ))

    grammar_box = (
        "/* GRAMATICA FORMAL BNF IMPLEMENTADA (RUBRICA OFICIAL) */\n"
        "estructura_control -> sentencia_if | sentencia_while | sentencia_for\n"
        "sentencia_if       -> 'if' '(' expresion ')' '{' bloque '}' ( 'else' '{' bloque '}' )?\n"
        "sentencia_while    -> 'while' '(' expresion ')' '{' bloque '}'\n"
        "sentencia_for      -> 'for' '(' inicializacion ';' expresion ';' actualizacion ')' '{' bloque '}'\n"
        "bloque             -> ( sentencia )*\n"
        "sentencia          -> expresion ';' | estructura_control | declaracion ';' | asignacion ';' | return ';'\n"
        "inicializacion     -> declaracion | asignacion | ε\n"
        "actualizacion      -> expresion | asignacion | ε"
    )
    t_gram = Table([[Preformatted(grammar_box, style_code_box)]], colWidths=[letter[0] - 108])
    t_gram.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_gram)
    story.append(Spacer(1, 10))

    # ==========================================================================
    # SECCIÓN 2: GESTIÓN Y RECUPERACIÓN DE ERRORES SINTÁCTICOS
    # ==========================================================================
    story.append(Paragraph("2. Reglas Sintácticas y Gestión de Errores (Panic Mode)", style_h1))
    story.append(Paragraph(
        "El compilador implementa un mecanismo centralizado de manejo de errores sintácticos (<code>SyntaxErrorHandler</code>) "
        "con diagnóstico enriquecido que indica el número de línea, columna, estructura involucrada, descripción del problema "
        "y sugerencia directa de remediación. Para evitar colapsos en cascada, el parser activa recuperación en <i>Modo Pánico</i> "
        "sincronizando el puntero léxico hasta el siguiente delimitador seguro (<code>;</code>, <code>}</code> o palabras clave).",
        style_body
    ))

    rules_table_data = [
        ["Estructura", "Condición de Violación", "Mensaje y Sugerencia Reportada"],
        ["Condicional if", "Falta de '(' o ')' en condición", "Paréntesis desbalanceados en 'if'. Ej: if (condicion) { ... }"],
        ["Condicional if", "Omisión de llaves '{' o '}'", "Bloque sin llaves '{' obligatorias. Se rechazan sentencias sin '{'."],
        ["Bucle while", "Condición ausente o inválida", "Condición inválida o vacía en 'while'. Ej: while (y < 10) { ... }"],
        ["Bucle while", "Llave de cierre faltante", "Llave '}' faltante en bloque de 'while'. Diagnóstico con línea de apertura."],
        ["Bucle for", "Componente sin ';' o inválido", "Componente inválido en 'for'. Se valida 'for (init; cond; update) { ... }'"],
    ]
    t_rules = Table(rules_table_data, colWidths=[80, 180, 244])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563EB")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_rules)
    story.append(Spacer(1, 10))

    # ==========================================================================
    # SECCIÓN 3: BATERÍA DE PRUEBAS Y VALIDACIÓN EXPERIMENTAL
    # ==========================================================================
    story.append(Paragraph("3. Resultados de la Batería de Pruebas (10/10 Aprobadas)", style_h1))
    story.append(Paragraph(
        "Se diseñó una suite de 10 casos de prueba de alta fidelidad que cubren exhaustivamente los requisitos oficiales:",
        style_body
    ))

    tests_summary_data = [
        ["ID", "Descripción del Caso", "Categoría / Escenario", "Resultado Obtenido"],
        ["01", "if (x > 0) { x = x + 1; } else { x = x - 1; }", "Condicional Válido (Rúbrica)", "APROBADO (AST)"],
        ["02", "while (y < 10) { y = y + 1; }", "Iterativo Válido (Rúbrica)", "APROBADO (AST)"],
        ["03", "for (i = 0; i < 10; i = i + 1) { suma = suma + i; }", "Iterativo Válido (Rúbrica)", "APROBADO (AST)"],
        ["04", "for con if-else interno anidado en bucle", "Control Anidado Válido", "APROBADO (AST)"],
        ["05", "int main() con while, if y sentencia return", "Programa Completo Válido", "APROBADO (AST)"],
        ["06", "if (x > 0 { x = x + 1; }", "Error: Falta ')' en if", "APROBADO (Error)"],
        ["07", "while y < 10) { y = y + 1; }", "Error: Falta '(' en while", "APROBADO (Error)"],
        ["08", "for i = 0; i < 10; i = i + 1) { ... }", "Error: Falta '(' en for", "APROBADO (Error)"],
        ["09", "if (x > 0) x = x + 1; (Sin llaves obligatorias)", "Error: Bloque sin llaves", "APROBADO (Error)"],
        ["10", "while (y < 10) { y = y + 1; (Sin llave cierre)", "Error: Llave '}' faltante", "APROBADO (Error)"],
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
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_tests)

    story.append(PageBreak())

    # ==========================================================================
    # SECCIÓN 4: SALIDA OFICIAL DE EJECUCIÓN DE CONSOLA
    # ==========================================================================
    story.append(Paragraph("4. Salida Oficial de Ejecución de Consola (Salida_Ejecucion_Consola.txt)", style_h1))
    story.append(Paragraph(
        "Transcripción directa generada automáticamente durante la ejecución del módulo <code>main.py</code>. "
        "Se verifica el cumplimiento de imprimir los nombres de los integrantes al inicio y al final:",
        style_body
    ))

    log_path = os.path.join(base_dir, "Salida_Ejecucion_Consola.txt")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    else:
        log_content = "[AVISO: Ejecute 'python main.py' para generar la bitácora.]"

    # Dividir el log en bloques manejables para que ReportLab los pagine fluidamente
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
    story.append(Paragraph("5. Conclusiones y Logros Alcanzados", style_h1))
    story.append(Paragraph(
        "1. <b>Rigor Gramatical:</b> Se cumplieron a cabalidad todas las especificaciones de la rúbrica oficial, "
        "estableciendo que las estructuras condicionales (<i>if</i>/<i>else</i>) e iterativas (<i>while</i>, <i>for</i>) "
        "deben poseer obligatoriamente bloques delimitados por llaves <code>{ ... }</code>.<br/>"
        "2. <b>Árbol AST Jerárquico:</b> La construcción orientada a objetos del AST permite inspeccionar visualmente "
        "la ramificación de condiciones, cuerpos, inicializadores y actualizaciones en representaciones de árbol ASCII limpias.<br/>"
        "3. <b>Recuperación Robusta (Modo Pánico):</b> Ante la presencia de desbalances en paréntesis o llaves ausentes, "
        "el analizador emite reportes con línea y columna exacta, sugiriendo la corrección adecuada sin detener el análisis de las siguientes sentencias.<br/>"
        "4. <b>Integración del Proyecto Final:</b> Este analizador sintáctico se articula coherentemente con el analizador léxico de la Actividad 2 "
        "y el generador de código de la Actividad 13, avanzando hacia el compilador integral del Lenguaje C.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Reporte PDF generado exitosamente: {pdf_path}")


if __name__ == "__main__":
    build_pdf()
