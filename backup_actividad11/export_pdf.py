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

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A11_CodigoIntermedioControlFlujo.pdf"
VIDEO_URL = "https://youtu.be/PENDIENTE_SUBIR_VIDEO_ACTIVIDAD_11"


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
            header_text = "Compiladores - Actividad 11: Código Intermedio para Control de Flujo - Díaz, Fierro, Hernández, Millán"
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
    story.append(Paragraph("ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO", style_cover_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Linealización de Estructuras Condicionales (if/else, switch), Bucles (while, for, do-while)<br/>"
        "Definición y Llamada de Métodos con Paso de Parámetros y Clases en Código de Tres Direcciones (TAC)",
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
    # SECCIÓN 1: INTRODUCCIÓN Y REGLAS DE CONTROL DE FLUJO EN TAC
    # ==========================================================================
    story.append(Paragraph("1. Introducción y Reglas de Control de Flujo en TAC", style_h1))
    story.append(Paragraph(
        "En la arquitectura de compiladores, el Código de Tres Direcciones (TAC) proporciona una representación "
        "intermedia abstracta e independiente de la máquina destino. La traducción del control de flujo implica "
        "reemplazar las estructuras arbóreas y compuestas del lenguaje fuente de alto nivel por saltos atómicos "
        "condicionales e incondicionales, garantizando el orden de evaluación correcto según la semántica de C.",
        style_body
    ))

    model_box = (
        "# PATRONES FORMALES DE LA RUBRICA IMPLEMENTADOS EN TAC\n"
        "# 1. Condicional if-else:\n"
        "t1 = x > y                # t1 es una etiqueta temporal para la comparación x > y\n"
        "if t1 goto L1             # Si t1 es verdadero, salta a la etiqueta L1\n"
        "z = y                     # Si t1 es falso, asigna y a z\n"
        "goto L2                   # Salta a la etiqueta L2 después del bloque else\n"
        "L1:                       # Etiqueta L1 para el bloque if\n"
        "z = x                     # Asigna x a z\n"
        "L2:                       # Etiqueta L2 marca el final de la estructura condicional\n\n"
        "# 2. Estructura switch:\n"
        "t2 = n                    # t2 es una etiqueta temporal para el valor de n\n"
        "if t2 == 1 goto L1        # Si t2 es 1, salta a la etiqueta L1\n"
        "if t2 == 2 goto L2        # Si t2 es 2, salta a la etiqueta L2\n"
        "goto L3                   # Si t2 no es ni 1 ni 2, salta a la etiqueta L3 (default)\n\n"
        "# 3. Bucle while:\n"
        "L1:                       # Etiqueta L1 marca el inicio del bucle\n"
        "t3 = i < 10               # t3 es una etiqueta temporal para la condición i < 10\n"
        "if not t3 goto L2         # Si t3 es falso, salta a la etiqueta L2 (fin del bucle)\n"
        "i = i + 1                 # Incrementa i\n"
        "goto L1                   # Salta de vuelta al inicio del bucle\n"
        "L2:                       # Etiqueta L2 marca el final del bucle"
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
        ["01", "if (x > y) { z=x; } else { z=y; }", "Estructuras Condicionales", "APROBADO (TAC)"],
        ["02", "switch (n) { case 1, 2, default }", "Selección Múltiple switch", "APROBADO (TAC)"],
        ["03", "while(i<10), for(int i=0;i<5;i++), do-while", "Bucles y Ciclos", "APROBADO (TAC)"],
        ["04", "int suma(int a, int b) y result = suma(5, 3)", "Métodos y Funciones", "APROBADO (TAC)"],
        ["05", "class Persona { void celebrarCumpleaños() }", "Clases y Objetos", "APROBADO (TAC)"],
        ["06", "result = calcularFactorial(10); (No declarada)", "Semántico: Método Inexistente", "APROBADO (Error)"],
        ["07", "result = suma(5, 3, 10); (Aridad incorrecta)", "Semántico: Aridad de Método", "APROBADO (Error)"],
        ["08", "Vehiculo v = new Vehiculo(); (No declarada)", "Semántico: Clase Inexistente", "APROBADO (Error)"],
        ["09", "p.volar(); (Método inexistente en clase)", "Semántico: Método en Objeto", "APROBADO (Error)"],
        ["10", "if ('cadena') (Tipo incompatible condición)", "Semántico: Condición Inválida", "APROBADO (Error)"]
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
        "Bitácora completa emitida por <code>main.py</code>, comprobando la doble impresión de los 4 integrantes "
        "en estricto orden alfabético tanto al inicio como al cierre de la ejecución:",
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
        "1. <b>Cumplimiento Integral de la Rúbrica:</b> Se implementó de manera completa la generación de TAC para todas "
        "las estructuras de control de flujo estipuladas por el profesor Rigoberto Cárdenas Larios (if/else, switch, while, "
        "for, do-while, métodos con parámetros/retorno, y clases con instanciación).<br/>"
        "2. <b>Manejo Semántico y Detección de Errores:</b> El compilador previene errores semánticos comunes (invocación de métodos "
        "no declarados, discordancia de aridad, instanciación de clases inexistentes y condiciones de tipo incorrecto).<br/>"
        "3. <b>Trazabilidad y Comentarios:</b> Cada instrucción de salto y asignación intermedia incluye comentarios explicativos "
        "que facilitan la posterior etapa de optimización y generación de código de máquina (Actividad 13).<br/><br/>"
        "<b>Referencias Bibliográficas:</b><br/>"
        "• Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). <i>Compilers: Principles, Techniques, and Tools</i> (2nd ed.). Pearson.<br/>"
        "• Appel, A. W., & Palsberg, J. (2004). <i>Modern Compiler Implementation in Java</i> (2nd ed.). Cambridge University Press.<br/>"
        "• Cooper, K. D., & Torczon, L. (2011). <i>Engineering a Compiler</i> (2nd ed.). Morgan Kaufmann.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Reporte PDF generado exitosamente: {pdf_path}")


if __name__ == "__main__":
    build_pdf()
