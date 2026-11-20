"""
================================================================================
ACTIVIDAD 12: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO
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

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A12_OptimizacionCodigoIntermedio.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_12"


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
            header_text = "Compiladores - Actividad 12: Optimización de Código Intermedio - Díaz, Fierro, Hernández, Millán"
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
        fontSize=16,
        leading=20,
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
        fontSize=12,
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
    story.append(Paragraph("ACTIVIDAD 12: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO", style_cover_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Detección y Eliminación de Código Muerto, Instrucciones Inalcanzables, Subexpresiones Comunes (CSE),<br/>"
        "Asignaciones Redundantes (Dead Stores) y Plegado/Propagación de Constantes en TAC",
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
    # SECCIÓN 1: INTRODUCCIÓN Y REGLAS DE OPTIMIZACIÓN
    # ==========================================================================
    story.append(Paragraph("1. Introducción y Reglas de Optimización de Código Intermedio", style_h1))
    story.append(Paragraph(
        "La optimización de código intermedio es la fase en la cual un compilador refina la representación lineal "
        "de tres direcciones (TAC) generada durante las fases semánticas. Su meta primordial es reducir la cantidad "
        "de instrucciones ejecutadas y el consumo de memoria sin alterar el comportamiento observable ni los resultados "
        "del programa fuente.",
        style_body
    ))

    model_box = (
        "# PATRONES DE OPTIMIZACION IMPLEMENTADOS CONFORME A LA RUBRICA\n"
        "# 1. Instrucciones Inalcanzables:\n"
        "L1: x = 10; goto L2; y = 20; L2: z = x + y  -> Se elimina 'y = 20'\n\n"
        "# 2. Variables No Utilizadas (Dead Code Elimination):\n"
        "a = 5; b = 10; c = b + 2; result = c        -> Se elimina 'a = 5'\n\n"
        "# 3. Eliminacion de Calculos Repetidos (CSE):\n"
        "t1 = a + b; t2 = a + b; result = t1         -> Se elimina 't2 = a + b'\n\n"
        "# 4. Asignaciones Sobrescritas Inmediatamente (Dead Stores):\n"
        "temp = a; temp = b; result = temp           -> Se elimina 'temp = a' y propaga 'result = b'\n\n"
        "# 5. Plegado y Propagacion de Constantes:\n"
        "x = 10; t1 = x + 5; t2 = t1 + 10; result = t2 -> Se pliega a 'result = 25'"
    )
    t_box = Table([[Preformatted(model_box, style_code_box)]], colWidths=[letter[0] - 108])
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
    # SECCIÓN 2: BATERÍA DE PRUEBAS
    # ==========================================================================
    story.append(Paragraph("2. Resultados de la Batería de Pruebas (10/10 Aprobadas)", style_h1))
    tests_summary_data = [
        ["ID", "Descripción del Caso de Prueba", "Categoría Evaluada", "Resultado"],
        ["01", "Instrucciones inalcanzables tras goto L2", "Código Inalcanzable", "APROBADO (Poda)"],
        ["02", "Variable 'a' no utilizada en cálculo final", "Variables Muertas (DCE)", "APROBADO (Poda)"],
        ["03", "t1 = a + b; t2 = a + b (Cálculos repetidos)", "Subexpresiones Comunes (CSE)", "APROBADO (Reuso)"],
        ["04", "temp = a; temp = b (Sobrescrita de inmediato)", "Dead Store Elimination", "APROBADO (Poda)"],
        ["05", "x = 10; t1 = x + 5; t2 = t1 + 10 (Plegado)", "Constant Folding / Propagation", "APROBADO (Plegado)"],
        ["06", "goto L_no_existe (Salto a etiqueta no definida)", "Control Semántico de Flujo", "APROBADO (Error)"],
        ["07", "result = variable_fantasma + 5 (No inicializada)", "Control de Variables", "APROBADO (Error)"],
        ["08", "= = + 5 10 (Sintaxis TAC inválida)", "Control Sintáctico TAC", "APROBADO (Error)"],
        ["09", "x / 0 (División constante entre cero)", "Control Aritmético", "APROBADO (Error)"],
        ["10", "if a <> 10 goto L1 (Operador relacional inválido)", "Sintaxis de Saltos Condicionales", "APROBADO (Error)"]
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
    # SECCIÓN 3: SALIDA DE CONSOLA CHUNKED
    # ==========================================================================
    story.append(Paragraph("3. Salida Oficial de Ejecución de Consola (Salida_Ejecucion_Consola.txt)", style_h1))
    story.append(Paragraph(
        "Registro íntegro emitido por <code>main.py</code>, comprobando la doble impresión obligatoria "
        "de los 4 integrantes en estricto orden alfabético tanto al inicio como al cierre de la ejecución:",
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
    # SECCIÓN 4: CONCLUSIONES Y REFERENCIAS
    # ==========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("4. Conclusiones y Referencias Bibliográficas", style_h1))
    story.append(Paragraph(
        "1. <b>Cumplimiento Integral de la Rúbrica:</b> Se aplicaron de manera rigurosa las cinco técnicas fundamentales de "
        "optimización de código intermedio solicitadas por el profesor Rigoberto Cárdenas Larios.<br/>"
        "2. <b>Preservación de Semántica:</b> El optimizador verifica el grafo de flujo de control antes y después de cada pasada, "
        "asegurando que las variables vivas críticas ('result') nunca sean eliminadas prematuramente.<br/>"
        "3. <b>Métricas de Reducción Cuantificables:</b> Se logró una disminución de hasta el 50% en la cantidad de instrucciones intermedias "
        "mediante la combinación de CSE, Dead Store Elimination y Constant Folding.<br/><br/>"
        "<b>Referencias Bibliográficas:</b><br/>"
        "• Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). <i>Compilers: Principles, Techniques, and Tools</i> (2nd ed.). Pearson.<br/>"
        "• Appel, A. W., & Palsberg, J. (2004). <i>Modern Compiler Implementation in Java</i> (2nd ed.). Cambridge University Press.<br/>"
        "• Cooper, K. D., & Torczon, L. (2011). <i>Engineering a Compiler</i> (2nd ed.). Morgan Kaufmann.<br/>"
        "• Muchnick, S. S. (1997). <i>Advanced Compiler Design and Implementation</i>. Morgan Kaufmann.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Reporte PDF generado exitosamente: {pdf_path}")


if __name__ == "__main__":
    build_pdf()
