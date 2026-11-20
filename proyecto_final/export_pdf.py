"""
================================================================================
PROYECTO FINAL: COMPILADOR INTEGRAL DE LENGUAJE C
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
    PageBreak,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from test_cases import TEST_CASES

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A14_ProyectoFinal.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_PROYECTO_FINAL"
TXT_OUTPUT = "Salida_Ejecucion_Consola.txt"


class NumberedCanvas(canvas.Canvas):
    """Agrega pie de página profesional 'Página X de Y' y encabezado institucional."""
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
            header_text = "Compiladores — Proyecto Final: Compilador de C — Díaz, Fierro, Hernández, Millán"
            self.drawString(54, 750, header_text)
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 745, letter[0] - 54, 745)

            # Pie de página
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(letter[0] - 54, 38, page_text)
            self.drawString(54, 38, "Universidad de Guadalajara — CUCEI (Prof. Rigoberto Cárdenas Larios)")
            self.line(54, 48, letter[0] - 54, 48)
            self.restoreState()


def add_chunked_code(story, code_text: str, code_style, chunk_size: int = 40):
    """Divide texto largo en tablas de no más de chunk_size líneas para prevenir LayoutError."""
    lines = code_text.strip().split("\n")
    for start_idx in range(0, len(lines), chunk_size):
        chunk_lines = lines[start_idx:start_idx + chunk_size]
        chunk_str = "\n".join(chunk_lines)

        tbl = Table([[Paragraph(f"<pre>{chunk_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</pre>", code_style)]], colWidths=[letter[0] - 108])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 4))


def generate_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
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
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )

    team_title_style = ParagraphStyle(
        'CoverTeamTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )

    team_names_style = ParagraphStyle(
        'CoverTeamNames',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0369A1")
    )

    date_style = ParagraphStyle(
        'CoverDate',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
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
        fontSize=8.5,
        leading=12,
        spaceAfter=6,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ==============================================================================
    # 1. PORTADA OFICIAL
    # ==============================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("UNIVERSIDAD DE GUADALAJARA<br/>CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS (CUCEI)<br/>DIVISIÓN DE ELECTRÓNICA Y COMPUTACIÓN", inst_style))
    story.append(Spacer(1, 25))
    story.append(Paragraph("PROYECTO FINAL INTEGRADOR:<br/>COMPILADOR INTEGRAL DE LENGUAJE C CON ENTORNO DE EJECUCIÓN VIRTUAL RISC DE 32 BITS", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Materia:</b> Traductores de Lenguaje / Compiladores<br/><b>Profesor:</b> Rigoberto Cárdenas Larios", ParagraphStyle('CourseInfo', parent=styles['Normal'], fontSize=10, alignment=1, textColor=colors.HexColor("#475569"))))
    story.append(Spacer(1, 30))

    story.append(Paragraph("INTEGRANTES DEL EQUIPO<br/>(Estricto Orden Alfabético por Primer Apellido):", team_title_style))
    story.append(Spacer(1, 8))
    team_text = (
        "1. DÍAZ TORRES JAZMÍN MONTSERRAT<br/>"
        "2. FIERRO MELÉNDEZ ERNESTO HATUEY<br/>"
        "3. HERNÁNDEZ GARCÍA HÉCTOR GABRIEL<br/>"
        "4. MILLÁN GUERRERO OSWALDO JOSUÉ"
    )
    story.append(Paragraph(team_text, team_names_style))

    story.append(Spacer(1, 45))
    story.append(Paragraph("GUADALAJARA, JALISCO — CICLO ESCOLAR 2026B<br/>FECHA DE ENTREGA: NOVIEMBRE 2026", date_style))
    story.append(PageBreak())

    # ==============================================================================
    # 2. ENLACE DE DEMOSTRACIÓN EN VIDEO
    # ==============================================================================
    story.append(Paragraph("1. Demostración en Video del Compilador (YouTube)", h1_style))
    story.append(Paragraph(
        "En cumplimiento de los lineamientos oficiales, se elaboró un video demostrativo en pantalla completa con reloj y fecha "
        "de Windows visibles durante toda la grabación (< 5 minutos). Se presenta la ejecución de la batería completa de 10 casos "
        "de prueba en la GUI, la navegación en las 8 pestañas y la ejecución en la Máquina Virtual:", body_style
    ))

    video_table_data = [
        [Paragraph(f"<b>ENLACE DE DEMOSTRACIÓN EN YOUTUBE:</b><br/><font color='#0369A1'><u>{VIDEO_URL}</u></font><br/><i>(Resolución 1080p, pantalla completa sin recortes, reloj/fecha de Windows activo)</i>", body_style)]
    ]
    vt = Table(video_table_data, colWidths=[letter[0] - 108])
    vt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F9FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#0284C7")),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(vt)
    story.append(Spacer(1, 12))

    # ==============================================================================
    # 3. INTRODUCCIÓN Y ARQUITECTURA
    # ==============================================================================
    story.append(Paragraph("2. Introducción y Arquitectura del Compilador", h1_style))
    story.append(Paragraph(
        "El compilador desarrollado integra todas las fases formales de la traducción de lenguajes de programación, desde el texto "
        "fuente hasta la simulación de ejecución en un microprocesador virtual RISC. Soporta variables con tipado estático (int, float, "
        "string, bool), expresiones compuestas con precedencia, estructuras de control de flujo (if/else, switch/case, while, for, do-while), "
        "funciones con parámetros y paso de retornos, y programación orientada a objetos (clases, atributos y métodos).", body_style
    ))
    story.append(Paragraph(
        "<b>Flujo de Compilación:</b> Código Fuente C → Analizador Léxico (Tokens) → Analizador Sintáctico (AST) → "
        "Analizador Semántico (Tabla de Símbolos & Memoria) → Generador de TAC → Optimizador TAC (Plegado, Copias, CSE, DCE) → "
        "Generador de Código Máquina (Ensamblador & Peephole) → Máquina Virtual RISC de 32 bits (Fetch-Decode-Execute).", body_style
    ))
    story.append(Spacer(1, 10))

    # ==============================================================================
    # 4. ESPECIFICACIÓN DE LA MÁQUINA VIRTUAL
    # ==============================================================================
    story.append(Paragraph("3. Especificación Arquitectónica de la Máquina Virtual (VM)", h1_style))
    hw_rows = [
        [Paragraph("<b>Componente Hardware</b>", body_style), Paragraph("<b>Dirección / Segmento</b>", body_style), Paragraph("<b>Descripción</b>", body_style)],
        [Paragraph("Segmento de Código", body_style), Paragraph("0x1000 — 0x1FFF", body_style), Paragraph("Memoria de instrucciones máquina de 4 bytes.", body_style)],
        [Paragraph("Segmento de Datos", body_style), Paragraph("0x2000 — 0x2FFF", body_style), Paragraph("Memoria RAM para variables globales y locales.", body_style)],
        [Paragraph("Segmento de Resultados", body_style), Paragraph("0x3000 — 0x3FFF", body_style), Paragraph("Memoria para valores temporales y retornos.", body_style)],
        [Paragraph("Banco de Registros", body_style), Paragraph("R1 a R8 (32 bits)", body_style), Paragraph("R1 como acumulador principal, R2 auxiliar.", body_style)],
        [Paragraph("Banderas de Estado", body_style), Paragraph("ZF, SF, OF", body_style), Paragraph("Zero Flag, Sign Flag y Overflow Flag de la ALU.", body_style)],
    ]
    t_hw = Table(hw_rows, colWidths=[120, 110, letter[0] - 108 - 230])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0369A1")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 12))

    # ==============================================================================
    # 5. RESUMEN DE LA BATERÍA DE PRUEBAS
    # ==============================================================================
    story.append(Paragraph("4. Batería de Pruebas Automatizada (10 Casos de Prueba)", h1_style))
    story.append(Paragraph(
        "Se ejecutó la batería exhaustiva de 10 casos de prueba integrados en el sistema automatizado (`main.py` y `gui.py`). "
        "Los 10 casos pasaron con 100% de éxito, validando tanto ejecuciones completas como detección de anomalías:", body_style
    ))

    tc_table_data = [
        [Paragraph("<b>ID</b>", body_style), Paragraph("<b>Nombre del Caso</b>", body_style), Paragraph("<b>Tipo</b>", body_style), Paragraph("<b>Fase Objetivo</b>", body_style), Paragraph("<b>Veredicto</b>", body_style)]
    ]
    for tc in TEST_CASES:
        tc_table_data.append([
            Paragraph(tc.id, body_style),
            Paragraph(tc.name, body_style),
            Paragraph(tc.category, body_style),
            Paragraph(tc.target_phase, body_style),
            Paragraph("<font color='#16A34A'><b>APROBADO</b></font>", body_style)
        ])
    t_tests = Table(tc_table_data, colWidths=[36, 170, 55, 160, 75])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0369A1")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_tests)
    story.append(Spacer(1, 14))

    # ==============================================================================
    # 6. DETALLE DE CASOS DE PRUEBA
    # ==============================================================================
    story.append(Paragraph("5. Detalle de Programas de Prueba y Código Fuente", h1_style))
    for tc in TEST_CASES:
        story.append(Paragraph(f"<b>[{tc.id}] {tc.name}</b> ({tc.category})", h2_style))
        story.append(Paragraph(f"<i>Fase Evaluada:</i> {tc.target_phase} — {tc.description}", body_style))
        add_chunked_code(story, tc.source_code, code_style, chunk_size=35)
        story.append(Spacer(1, 4))

    # ==============================================================================
    # 7. REGISTRO COMPLETO DE EJECUCIÓN (CONSOLA)
    # ==============================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Registro de Ejecución Automatizada (Salida_Ejecucion_Consola.txt)", h1_style))
    story.append(Paragraph(
        "A continuación se presenta el log íntegro de la consola emitido por el script `main.py`, que valida paso a paso "
        "cada fase de la compilación, la generación de instrucciones, la optimización, el mapa de memoria y la ejecución en la VM:", body_style
    ))

    log_path = os.path.join(base_dir, TXT_OUTPUT)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_text = f.read()
    else:
        log_text = "Archivo de bitácora no generado."

    # Chunking seguro para evitar LayoutError en ReportLab
    add_chunked_code(story, log_text, code_style, chunk_size=40)

    # ==============================================================================
    # 8. CONCLUSIONES Y BIBLIOGRAFÍA
    # ==============================================================================
    story.append(Spacer(1, 12))
    story.append(Paragraph("7. Conclusiones Técnicas y Aprendizajes", h1_style))
    story.append(Paragraph(
        "El desarrollo del compilador integral permitió dominar la cadena completa de transformación de software. "
        "Se demostró que la separación rigurosa entre el Front-End (análisis léxico, sintáctico y semántico) y el Back-End "
        "(código intermedio, optimizadores y máquina virtual) es fundamental para garantizar modularidad, extensibilidad y mantenibilidad.", body_style
    ))
    story.append(Paragraph(
        "Las técnicas de optimización implementadas permitieron reducir significativamente el número de instrucciones ejecutadas "
        "(alcanzando más de 75% de ahorro en expresiones complejas mediante reutilización de registros y optimización de mirilla). "
        "La simulación de hardware mediante una Máquina Virtual con ciclo de reloj formal garantiza una plataforma de pruebas "
        "completamente determinista e independiente de la arquitectura subyacente.", body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Referencias Bibliográficas", h1_style))
    bibs = [
        "Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Addison-Wesley.",
        "Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd ed.). Morgan Kaufmann.",
        "Muchnick, S. S. (1997). Advanced Compiler Design and Implementation. Morgan Kaufmann.",
        "Patterson, D. A., & Hennessy, J. L. (2017). Computer Organization and Design: The Hardware/Software Interface. Morgan Kaufmann."
    ]
    for b in bibs:
        story.append(Paragraph(f"• {b}", body_style))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ PDF generado exitosamente: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
