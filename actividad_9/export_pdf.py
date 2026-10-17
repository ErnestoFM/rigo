"""
================================================================================
ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL,
             MÉTODOS Y CLASES
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
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Preformatted,
    PageBreak,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_NAME = "DiazTorresJazmin_FierroMelendezErnesto_HernandezGarciaHector_MillanGuerreroOswaldo_A9_SemanticoEstructurasMetodosClases.pdf"
VIDEO_URL = "https://youtu.be/lsQ1FTXLaiM"


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
            header_text = "Compiladores - Actividad 9: Analisis Semantico - Diaz, Fierro, Hernandez, Millan"
            self.drawString(54, 750, header_text)
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 745, letter[0] - 54, 745)

            # Pie de página
            page_text = f"Pagina {self._pageNumber} de {page_count}"
            self.drawRightString(letter[0] - 54, 38, page_text)
            self.drawString(54, 38, "Reporte Final - Traductores de Lenguaje")
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

    # Estilos tipográficos
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1, # Centrado
        textColor=colors.HexColor("#1E3A8A")
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
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )

    team_names_style = ParagraphStyle(
        'CoverTeamNames',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )

    date_style = ParagraphStyle(
        'CoverDate',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#64748B")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#1E3A8A")
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.HexColor("#0F172A")
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        spaceAfter=8,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=6,
        borderRadius=3,
        spaceAfter=10
    )

    console_style = ParagraphStyle(
        'ConsoleStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=7.8,
        textColor=colors.HexColor("#F8FAFC"),
        backColor=colors.HexColor("#0F172A"),
        borderColor=colors.HexColor("#334155"),
        borderWidth=1,
        borderPadding=8,
        borderRadius=4,
        spaceAfter=12
    )

    story = []

    # =========================================================================
    # PORTADA OFICIAL
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("TRADUCTORES DE LENGUAJE / COMPILADORES<br/>PROFESOR: RIGOBERTO CÁRDENAS LARIOS", inst_style))
    story.append(Spacer(1, 25))
    story.append(Paragraph(
        "ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL, MÉTODOS Y CLASES<br/>"
        "<font size=11 color='#3B82F6'>DESARROLLO DE UN COMPILADOR EN PYTHON</font>",
        title_style
    ))
    story.append(Spacer(1, 35))

    story.append(Paragraph("INTEGRANTES DEL EQUIPO<br/>(Orden Alfabético por Primer Apellido):", team_title_style))
    story.append(Spacer(1, 12))

    nombres_html = (
        "1. DIAZ TORRES JAZMIN MONTSERRAT<br/>"
        "2. FIERRO MELÉNDEZ ERNESTO HATUEY<br/>"
        "3. HERNANDEZ GARCIA HECTOR GABRIEL<br/>"
        "4. MILLAN GUERRERO OSWALDO JOSUE"
    )
    story.append(Paragraph(nombres_html, team_names_style))
    story.append(Spacer(1, 45))

    story.append(Paragraph("FECHA DE ENTREGA: 23 DE OCTUBRE, 23:59<br/>EVALUACIÓN: 100 PUNTOS", date_style))
    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 1: ENLACE DEL VIDEO DEMOSTRATIVO
    # =========================================================================
    story.append(Paragraph("1. ENLACE PÚBLICO AL VIDEO DEMOSTRATIVO (YOUTUBE)", h1_style))

    vid_box_content = [
        [Paragraph(f"<b>Enlace Público al Video Demostrativo (YouTube):</b><br/>"
                   f"<font color='#2563EB'><u>{VIDEO_URL}</u></font><br/><br/>"
                   f"<b>Lineamientos cumplidos según la rúbrica oficial:</b><br/>"
                   f"• Duración máxima no mayor a 5 minutos en resolución mínima de 720p con audio explicativo.<br/>"
                   f"• Grabación de pantalla completa desde el equipo de cómputo con fecha y hora del sistema visible en la barra de tareas.<br/>"
                   f"• Demostración del compilador en ejecución por CLI (main.py) y GUI (gui.py).<br/>"
                   f"• Nombres de los integrantes al inicio y fin de la ejecución como primera y última instrucción obligatoria.", body_style)]
    ]
    vid_table = Table(vid_box_content, colWidths=[letter[0] - 108])
    vid_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3B82F6")),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(vid_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECCIÓN 2: INTRODUCCIÓN Y OBJETIVOS
    # =========================================================================
    story.append(Paragraph("2. INTRODUCCIÓN Y OBJETIVOS DE LA PRÁCTICA", h1_style))
    story.append(Paragraph(
        "El objetivo primordial de esta práctica es diseñar, implementar y validar la fase de <b>Análisis Semántico</b> "
        "para estructuras de control (condicionales e iterativas), métodos y clases, asegurando la correcta "
        "identificación, tipado estático, comprobación de condiciones lógicas y gestión de errores semánticos y de flujo de control.<br/><br/>"
        "En la teoría de construcción de compiladores (Aho et al., Dragon Book), mientras que el analizador léxico y el analizador sintáctico "
        "verifican que los caracteres y tokens respeten la Gramática Libre de Contexto generando el Árbol de Sintaxis Abstracta (AST), "
        "el análisis semántico es responsable de dotar de coherencia y validez lógica al código mediante:<br/>"
        "<b>1. Comprobación de condiciones lógicas:</b> Asegurar que las condiciones en estructuras <code>if</code> y <code>while</code> "
        "sean estrictamente expresiones de tipo booleano (<code>boolean</code>).<br/>"
        "<b>2. Validación de flujo de control:</b> Detección de bucles infinitos estáticos (<code>while (true)</code> sin escape), sentencias "
        "<code>return</code> fuera del cuerpo de métodos y código inalcanzable (<i>unreachable code</i>).<br/>"
        "<b>3. Verificación de métodos:</b> Coincidencia en número de argumentos (aridad), compatibilidad estricta de tipos de parámetros "
        "y congruencia del valor retornado con la signatura declarada.<br/>"
        "<b>4. Gestión de ámbitos (Scopes) y Tabla de Símbolos:</b> Resolución jerárquica de símbolos (Global, Clases, Métodos, Bloques locales).",
        body_style
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 3: ESPECIFICACIÓN DE REGLAS SEMÁNTICAS
    # =========================================================================
    story.append(Paragraph("3. ESPECIFICACIÓN FORMAL DE REGLAS SEMÁNTICAS Y FLUJO", h1_style))
    story.append(Paragraph(
        "A continuación se detallan las reglas implementadas conforme a la rúbrica de evaluación:<br/><br/>"
        "<b>A. Validación de Estructuras de Control:</b><br/>"
        "• <i>Regla 1 (Sintaxis y Delimitadores):</i> Las estructuras <code>if</code> y <code>while</code> requieren llaves delimitadoras <code>{ ... }</code> obligatorias.<br/>"
        "• <i>Regla 2 (Condiciones Lógicas Booleanas):</i> La condición dentro de <code>if</code> y <code>while</code> debe ser de tipo <code>boolean</code>. "
        "Expresiones de tipo <code>string</code> (ej. <code>if (\"texto\")</code>) o <code>int</code> son rechazadas.<br/>"
        "• <i>Regla 3 (Flujo y Bucles Infinitos):</i> Una estructura <code>while (true)</code> sin condiciones de escape (break / return) es clasificada como bucle infinito estático.<br/>"
        "• <i>Regla 4 (Accesibilidad de Flujo):</i> Sentencias posteriores a un <code>return</code> incondicional en un bloque secuencial se reportan como código inalcanzable.<br/><br/>"
        "<b>B. Validación de Métodos y Funciones:</b><br/>"
        "• <i>Regla 5 (Definición y Resolución):</i> Registro en tabla de símbolos; la invocación debe resolver a un método existente en el ámbito.<br/>"
        "• <i>Regla 6 (Chequeo de Aridad):</i> El número de argumentos pasados debe coincidir exactamente con el número de parámetros formales declarados (ej. <code>imprimirMensaje(\"Hola\", \"Mundo\")</code> con 2 en vez de 1).<br/>"
        "• <i>Regla 7 (Chequeo de Tipos de Parámetros):</i> Cada argumento debe ser de un tipo compatible con el parámetro formal (ej. <code>dividir(10, \"texto\")</code> rechazado).<br/>"
        "• <i>Regla 8 (Tipos de Retorno):</i> El valor retornado por <code>return expr;</code> debe ser compatible con la declaración (ej. <code>obtenerEdad()</code> retornando <code>\"Veinte\"</code> genera error). Métodos <code>void</code> no pueden retornar valor.<br/>"
        "• <i>Regla 9 (Return Fuera de Lugar):</i> Toda sentencia <code>return</code> fuera de métodos genera error semántico.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 4: CÓDIGOS FUENTE DESARROLLADOS
    # =========================================================================
    story.append(Paragraph("4. CÓDIGOS FUENTE DESARROLLADOS", h1_style))

    archivos_codigo = [
        ("token_type.py", "Definición de Tokens Léxicos y Tipos"),
        ("error_handler.py", "Gestor Centralizado de Errores y Diagnósticos"),
        ("lexer.py", "Analizador Léxico (Scanner)"),
        ("ast_nodes.py", "Nodos del Árbol de Sintaxis Abstracta (AST)"),
        ("symbol_table.py", "Sistema de Tipos y Tabla de Símbolos"),
        ("semantic_analyzer.py", "Analizador Semántico en Dos Pasadas y Verificador de Flujo"),
        ("parser.py", "Analizador Sintáctico Descendente Recursivo"),
        ("test_cases.py", "Batería de 20 Casos de Prueba Oficiales"),
        ("main.py", "Ejecutable CLI con firmas obligatorias"),
        ("gui.py", "Interfaz Gráfica Interactiva Moderna (Tkinter)")
    ]

    for fname, desc in archivos_codigo:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            story.append(Paragraph(f"<b>Módulo: {fname}</b> — <i>{desc}</i>", h2_style))
            story.append(Preformatted(content.strip(), code_style))
            story.append(Spacer(1, 8))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 5: SALIDAS DE EJECUCIÓN EN CONSOLA
    # =========================================================================
    story.append(Paragraph("5. RESULTADOS Y SALIDAS COMPLETAS DE EJECUCIÓN EN CONSOLA", h1_style))
    story.append(Paragraph(
        "A continuación se presenta la salida íntegra generada al ejecutar <code>python main.py</code>. "
        "Como se aprecia, la primera y última instrucción imprimen los nombres completos de los 4 integrantes en "
        "orden alfabético por primer apellido. Los 20 casos de prueba (9 válidos y 11 inválidos) son evaluados "
        "con una tasa de éxito y cumplimiento del 100%:",
        body_style
    ))

    txt_log_path = os.path.join(base_dir, "Salida_Ejecucion_Consola.txt")
    if os.path.exists(txt_log_path):
        with open(txt_log_path, "r", encoding="utf-8") as f:
            console_log = f.read()

        story.append(Preformatted(console_log.strip(), console_style))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 6: CONCLUSIONES Y REFERENCIAS
    # =========================================================================
    story.append(Paragraph("6. CONCLUSIONES Y REFERENCIAS BIBLIOGRÁFICAS", h1_style))
    story.append(Paragraph(
        "<b>CONCLUSIONES:</b><br/>"
        "La implementación de la fase de análisis semántico constituye el puente decisivo entre la estructura sintáctica "
        "y la correcta semántica de ejecución de un compilador. Mediante un analizador semántico en dos pasadas apoyado en "
        "tablas de símbolos jerárquicas con enlace estático, se logró verificar con rigor matemático:<br/>"
        "• La naturaleza booleana indispensable de los predicados condicionales e iterativos (<code>if</code> y <code>while</code>).<br/>"
        "• La sanidad del flujo de control, detectando tempranamente bucles infinitos estáticos y código inalcanzable.<br/>"
        "• La rigurosidad de las llamadas a métodos respecto a aridad, compatibilidad de tipos y tipos de retorno.<br/>"
        "• El aislamiento y diagnóstico descriptivo de errores, reportando número de línea, columna y sugerencias pedagógicas "
        "sin interrumpir abruptamente el análisis.<br/><br/>"
        "<b>REFERENCIAS BIBLIOGRÁFICAS:</b><br/>"
        "• Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). <i>Compilers: Principles, Techniques, and Tools</i> (2nd ed.). Pearson/Addison Wesley.<br/>"
        "• Appel, A. W., & Palsberg, J. (2004). <i>Modern Compiler Implementation in Java</i> (2nd ed.). Cambridge University Press.<br/>"
        "• Cooper, K. D., & Torczon, L. (2011). <i>Engineering a Compiler</i> (2nd ed.). Morgan Kaufmann.<br/>"
        "• Scott, M. L. (2015). <i>Programming Language Pragmatics</i> (4th ed.). Morgan Kaufmann.",
        body_style
    ))

    # Construir documento final con NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Documento PDF generado exitosamente: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
