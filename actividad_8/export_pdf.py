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

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A8_SemanticoExpresionesAritmeticasLogicas.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_8"


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
            header_text = "Compiladores - Actividad 8: Semántico Expresiones Aritméticas y Lógicas - Díaz, Fierro, Hernández, Millán"
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
    story.append(Paragraph("ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - EXPRESIONES ARITMÉTICAS Y LÓGICAS", style_cover_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Validación de Tipos en Expresiones, Compatibilidad de Operadores,<br/>"
        "Detección Estática de División por Cero y Conversiones de Tipo (static_cast)",
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
    # SECCIÓN 1: INTRODUCCIÓN Y REGLAS DE VALIDACIÓN
    # ==========================================================================
    story.append(Paragraph("1. Introducción y Reglas de Tipado en Expresiones", style_h1))
    story.append(Paragraph(
        "La validación semántica de expresiones garantiza que cada operación matemática, lógica o relacional "
        "se realice respetando el sistema de tipos del lenguaje C. En esta práctica se implementó un evaluador y verificador "
        "que comprueba la compatibilidad entre operandos, prohíbe operaciones entre cadenas y números, restringe los "
        "operadores lógicos a valores booleanos, detecta estáticamente divisiones por cero y valida conversiones explícitas (static_cast).",
        style_body
    ))

    rules_box = (
        "/* REGLAS SEMANTICAS PARA EXPRESIONES (RUBRICA OFICIAL) */\n"
        "1. Aritmética (+, -, *, /, %): Operandos estrictamente numéricos (int, float). Prohibido string y bool.\n"
        "2. Lógica (&&, ||, !):         Operandos estrictamente booleanos (bool). Prohibido mezclar con enteros.\n"
        "3. Relacional (==, !=, <, >):  Operandos de tipos homogéneos. Prohibido comparar cadenas con números.\n"
        "4. División por Cero:          Detección estática en tiempo de compilación si el denominador es cero constante.\n"
        "5. Conversiones (static_cast):  Conversiones válidas entre números. Prohibido static_cast de string a numérico."
    )
    t_box = Table([[Preformatted(rules_box, style_code_box)]], colWidths=[letter[0] - 108])
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
    # SECCIÓN 2: CATÁLOGO DE OPERADORES Y ERRORES
    # ==========================================================================
    story.append(Paragraph("2. Catálogo de Operadores y Diagnósticos de Error", style_h1))
    rules_table_data = [
        ["Operador", "Escenario de Violación", "Mensaje de Diagnóstico Emitido"],
        ["Aritmético (+)", "edad + nombre (int + string)", "Error: No se puede aplicar el operador '+' con una cadena de texto."],
        ["Lógico (&&)", "true && 1 (bool && int)", "Error: El operador lógico '&&' requiere operandos de tipo booleano."],
        ["Relacional (==)", "('5' == 5) (string == int)", "Error: No se puede comparar una cadena con un número mediante '=='."],
        ["División (/)", "10 / 0 (denominador cero)", "Error: División por cero detectada en tiempo de compilación con '/'."],
        ["Aritmético (+)", "10 + flag (int + bool)", "Error: No se puede realizar una operación aritmética con un booleano."]
    ]
    t_rules = Table(rules_table_data, colWidths=[90, 160, 254])
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
    tests_summary_data = [
        ["ID", "Descripción del Caso", "Regla Evaluada", "Resultado"],
        ["01", "Aritmética entera pura: a + b; 5 + 3;", "Aritmética Entera (Rúbrica)", "APROBADO (Eval: 15, 8)"],
        ["02", "Operadores lógicos: activo && inactivo; (10 > 5) && (3 < 8)", "Lógica Booleana (Rúbrica)", "APROBADO (Eval: False, True)"],
        ["03", "Comparaciones: 5 == 5; 3.14 < 6.28; 'Hola' == 'Hola'", "Comparación Homogénea", "APROBADO (Eval: True)"],
        ["04", "Expresión compleja: (10 + 20) * (30 - 15)", "Precedencia de Operadores", "APROBADO (Eval: 450)"],
        ["05", "static_cast<float>(entero) + 2.5", "Conversión Explícita", "APROBADO (Eval: 12.5)"],
        ["06", "edad + nombre (int + string)", "Error: Cadena en Aritmética", "APROBADO (Error)"],
        ["07", "true && 1 (bool con int)", "Error: Operando No Booleano", "APROBADO (Error)"],
        ["08", "('5' == 5) (cadena con número)", "Error: Comparación Inválida", "APROBADO (Error)"],
        ["09", "10 / 0 (división entre cero)", "Error: División por Cero", "APROBADO (Error)"],
        ["10", "10 + flag (int con bool)", "Error: Booleano en Aritmética", "APROBADO (Error)"]
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
        "Transcripción oficial generada por <code>main.py</code>, verificando la impresión obligatoria "
        "de los integrantes del equipo en orden alfabético estricto al inicio y al final:",
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
        "1. <b>Validación Estricta de Operadores:</b> Se aseguró que los operadores aritméticos, lógicos y relacionales "
        "se apliquen exclusivamente sobre tipos consistentes, eliminando riesgos de fallas por incompatibilidad de tipos.<br/>"
        "2. <b>Detección Estática de División por Cero:</b> La evaluación constante estática permitió detectar errores matemáticos "
        "críticos antes de la fase de generación de código.<br/>"
        "3. <b>Soporte de Conversiones Explícitas:</b> La incorporación de <code>static_cast</code> y conversiones tipo C "
        "habilita la coexistencia armónica entre enteros y flotantes cuando el programador lo solicita explícitamente.<br/>"
        "4. <b>Consolidación del Compilador:</b> Con esta actividad se complementan las fases de análisis léxico, sintáctico y semántico, "
        "preparando la base para la generación de código intermedio y máquina en el proyecto integral.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Reporte PDF generado exitosamente: {pdf_path}")


if __name__ == "__main__":
    build_pdf()
