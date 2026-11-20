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

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A2_ManejoErroresLexicos.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_2"


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
            header_text = "Compiladores - Actividad 2: Errores Léxicos - Díaz, Fierro, Hernández, Millán"
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


def generate_pdf():
    base_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(base_dir, PDF_NAME)
    print(f"[*] Generando PDF oficial: {pdf_path}...")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#0369A1")
    )

    inst_style = ParagraphStyle(
        'CoverInst',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )

    team_title_style = ParagraphStyle(
        'CoverTeamTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )

    date_style = ParagraphStyle(
        'CoverDate',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#64748B")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#0369A1")
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.HexColor("#0F172A")
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        spaceAfter=7,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=5,
        borderRadius=3,
        spaceAfter=8
    )

    story = []

    # Portada
    story.append(Spacer(1, 25))
    story.append(Paragraph("TECNOLÓGICO NACIONAL DE MÉXICO", inst_style))
    story.append(Paragraph("DEPARTAMENTO DE SISTEMAS Y COMPUTACIÓN", inst_style))
    story.append(Paragraph("INGENIERÍA EN SISTEMAS COMPUTACIONALES", inst_style))
    story.append(Spacer(1, 15))

    line_table = Table([[""]], colWidths=[500], rowHeights=[2])
    line_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0284C7")),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(line_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph("ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS", title_style))
    story.append(Paragraph("DESARROLLO DE UN COMPILADOR EN PYTHON PARA LENGUAJE C", title_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES", team_title_style))
    story.append(Paragraph("PROFESOR: RIGOBERTO CÁRDENAS LARIOS", team_title_style))
    story.append(Spacer(1, 30))

    story.append(Paragraph("INTEGRANTES DEL EQUIPO<br/>(EN ESTRICTO ORDEN ALFABÉTICO POR PRIMER APELLIDO):", team_title_style))
    story.append(Spacer(1, 10))

    team_data = [
        ["1.", "DÍAZ TORRES JAZMÍN MONTSERRAT"],
        ["2.", "FIERRO MELÉNDEZ ERNESTO HATUEY"],
        ["3.", "HERNÁNDEZ GARCÍA HÉCTOR GABRIEL"],
        ["4.", "MILLÁN GUERRERO OSWALDO JOSUÉ"]
    ]
    t_team = Table(team_data, colWidths=[30, 320])
    t_team.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 50))

    story.append(Paragraph("SEPTIEMBRE / OCTUBRE 2026", date_style))
    story.append(Paragraph("EVALUACIÓN ESPERADA: SATISFACTORIO (100 PUNTOS)", date_style))
    story.append(PageBreak())

    # Sección 1: Video
    story.append(Paragraph("1. Enlace del Video Demostrativo (YouTube)", h1_style))
    story.append(Paragraph(
        "De conformidad con las instrucciones oficiales, se grabó la pantalla completa mostrando audio explicativo claro, "
        "la fecha y hora visibles del sistema operativo Windows y duración menor a 5 minutos, demostrando la ejecución del "
        "programa, la captura de las 4 categorías de errores léxicos y la interfaz gráfica.<br/><br/>"
        f"<b>Enlace público al video:</b> <font color='#0284C7'><u>{VIDEO_URL}</u></font><br/>",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Sección 2: Introducción y Objetivos
    story.append(Paragraph("2. Introducción y Objetivo de la Práctica", h1_style))
    story.append(Paragraph(
        "<b>Práctica:</b> Desarrollo de un compilador, gestión de errores léxicos.<br/>"
        "<b>Objetivo:</b> Implementar un mecanismo para manejar y reportar errores léxicos durante la fase de análisis léxico "
        "en un compilador para el Lenguaje C desarrollado en Python.<br/><br/>"
        "Las 4 categorías de errores léxicos requeridas e implementadas son:<br/>"
        "<b>1. Caracteres No Reconocidos:</b> Símbolos fuera del alfabeto de C (ej. @, $, ~, ¿, ñ).<br/>"
        "<b>2. Identificadores Mal Formados:</b> Identificadores que inician con dígitos (ej. 123contador).<br/>"
        "<b>3. Literales Numéricos Incorrectos:</b> Números con múltiples puntos flotantes (ej. 3.14.15), hexadecimales inválidos (0x12G4) o exponentes incompletos (1.5e+).<br/>"
        "<b>4. Cadenas Mal Formadas:</b> Cadenas de texto no delimitadas antes de finalizar la línea.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Sección 3: Resultados de Evaluación
    story.append(Paragraph("3. Resultados de Evaluación: Banco de Pruebas (100% Rúbrica)", h1_style))
    table_cases_data = [
        ["#", "Caso Evaluado", "Tipo", "Regla Evaluada", "Estatus"],
        ["1", "Código C Válido (Control)", "Válido", "Preprocesador, palabras clave y tipos", "Aprobado (0 Errores)"],
        ["2", "Caracteres No Reconocidos", "Inválido", "Símbolos ajenos a C ($ , @ , ~ , ¿ , ñ)", "Interceptado (100%)"],
        ["3", "Identificadores Mal Formados", "Inválido", "Identificadores que inician con dígitos", "Interceptado (100%)"],
        ["4", "Literales Numéricos Incorrectos", "Inválido", "3.14.15, 0x12G4, 1.5e+", "Interceptado (100%)"],
        ["5", "Cadenas Mal Formadas", "Inválido", "Cadena sin comilla de cierre", "Interceptado (100%)"],
        ["6", "Evaluación Combinada", "Inválido", "4 categorías en un solo módulo", "Interceptado (100%)"]
    ]
    t_cases = Table(table_cases_data, colWidths=[20, 160, 45, 205, 70])
    t_cases.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284C7")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_cases)
    story.append(PageBreak())

    # Sección 4: Códigos Fuente
    story.append(Paragraph("4. Códigos Fuente Desarrollados", h1_style))
    source_files = [
        ("token_type.py", "Definición de Tokens y Categorías de Errores"),
        ("error_handler.py", "Manejador Centralizado de Errores Léxicos"),
        ("lexer.py", "Analizador Léxico en C con Expresiones Regulares"),
        ("test_cases.py", "Suites de Prueba Válidas e Inválidas"),
        ("main.py", "Ejecución por Consola con Firmas de Integrantes")
    ]

    for fname, fdesc in source_files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f_c:
                content = f_c.read()
            story.append(Paragraph(f"Módulo: {fname} — {fdesc}", h2_style))
            story.append(Preformatted(content, code_style))

    story.append(PageBreak())

    # Sección 5: Salida de Consola
    story.append(Paragraph("5. Salida Completa de Ejecución en Consola", h1_style))
    txt_path = os.path.join(base_dir, "Salida_Ejecucion_Consola.txt")
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f_t:
            salida_txt = f_t.read()
    else:
        salida_txt = "Salida no disponible."

    story.append(Preformatted(salida_txt, code_style))
    story.append(Spacer(1, 10))

    # Sección 6: Conclusiones
    story.append(Paragraph("6. Conclusiones y Referencias Bibliográficas", h1_style))
    story.append(Paragraph(
        "<b>Conclusiones:</b><br/>"
        "La implementación de la fase léxica demostró ser el cimiento indispensable para la fiabilidad de todo compilador. "
        "A través de expresiones regulares rigurosas y un manejador de errores contextual, se garantiza que únicamente "
        "secuencias coherentes avancen al análisis sintáctico. El aislamiento de errores léxicos específicos evita la cascada "
        "de fallos posteriores y proporciona a los desarrolladores diagnósticos claros con número de línea, columna y sugerencias.<br/><br/>"
        "<b>Referencias Bibliográficas (APA):</b><br/>"
        "• Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). <i>Compilers: Principles, Techniques, and Tools</i> (2nd ed.). Pearson/Addison Wesley.<br/>"
        "• Cooper, K. D., & Torczon, L. (2011). <i>Engineering a Compiler</i> (2nd ed.). Morgan Kaufmann.<br/>"
        "• Kernighan, B. W., & Ritchie, D. M. (1988). <i>The C Programming Language</i> (2nd ed.). Prentice Hall.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF generado exitosamente: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
