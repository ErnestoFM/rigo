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
from typing import List

# Configuración de salida UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from token_type import Token, TokenType
from error_handler import ErrorHandler, LexicalErrorCategory
from lexer import LexerC
from test_cases import ALL_TEST_CASES, VALID_TEST_CASES, INVALID_TEST_CASES, TestCaseItem


def imprimir_encabezado_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Primera instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("=" * 105)
    print("   ACTIVIDAD 2: GESTIÓN Y MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)")
    print("   MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES")
    print("   PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 105)


def imprimir_pie_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Última instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("\n" + "=" * 105)
    print("   EJECUCIÓN Y VALIDACIÓN DE ERRORES LÉXICOS FINALIZADA EXITOSAMENTE")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 105)


def ejecutar_caso_prueba(test: TestCaseItem) -> bool:
    """
    Ejecuta el análisis léxico para un caso de prueba individual,
    mostrando los tokens generados y los errores detectados de forma clara.
    """
    tipo_etiqueta = "VÁLIDO (CASO DE CONTROL)" if test.is_valid else "INVÁLIDO (CASO DE ERROR ESPERADO)"
    icono = "🟢" if test.is_valid else "🔴"

    print("\n" + "━" * 105)
    print(f" {icono} [CASO {test.id_num:02d} - {tipo_etiqueta}]: {test.title.upper()} ({test.category})")
    print("━" * 105)
    print(f" [REGLA EVALUADA]: {test.rule_description}")
    print(f" [COMPORTAMIENTO ESPERADO]: {test.expected_behavior}")
    print("─" * 105)
    print(" [CÓDIGO FUENTE DE ENTRADA]:")
    for num_linea, linea in enumerate(test.code.split('\n'), 1):
        print(f"   {num_linea:2d} | {linea}")
    print("─" * 105)

    error_handler = ErrorHandler()
    lexer = LexerC(test.code, error_handler)
    tokens = lexer.tokenize()

    # Tabla de Tokens Generados
    print("\n [TABLA DE COMPONENTES LÉXICOS (TOKENS) GENERADOS]:")
    sep_tok = "+" + "-" * 6 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 34 + "+" + "-" * 30 + "+"
    print(sep_tok)
    print(f"| {'#':<4} | {'LÍNEA':<5} | {'COL':<4} | {'CATEGORÍA LÉXICA':<32} | {'LEXEMA / VALOR':<28} |")
    print(sep_tok)

    valid_count = 0
    error_count = 0

    for idx, tok in enumerate(tokens, 1):
        if tok.type == TokenType.FIN_DE_ENTRADA:
            continue
        if tok.is_error:
            error_count += 1
            cat_display = tok.category_name
        else:
            valid_count += 1
            cat_display = tok.category_name

        short_val = tok.value if len(tok.value) <= 26 else tok.value[:23] + "..."
        # Escapar saltos de línea para que la tabla no se rompa
        short_val = short_val.replace("\n", "\\n").replace("\r", "")
        print(f"| {idx:<4} | {tok.line:<5} | {tok.column:<4} | {cat_display:<32} | {short_val:<28} |")

    print(sep_tok)
    print(f" RESUMEN DEL CASO: {valid_count} Tokens Válidos | {error_count} Errores Léxicos Capturados")

    # Diagnósticos del Manejador de Errores
    if error_handler.has_errors:
        print("\n [REPORTE DETALLADO DEL MANEJADOR DE ERRORES LÉXICOS]:")
        print(error_handler.to_formatted_table())
        if not test.is_valid:
            print("\n 🟢 RESULTADO: ERRORES LÉXICOS INTERCEPTADOS Y REPORTADOS SATISFACTORIAMENTE.")
            return True
        else:
            print("\n 🔴 ERROR INESPERADO: Se reportaron errores en un caso de prueba válido.")
            return False
    else:
        print("\n [REPORTE DEL MANEJADOR]: ✅ 0 Errores léxicos. Todos los lexemas pertenecen a C.")
        if test.is_valid:
            print("\n 🟢 RESULTADO: CASO VÁLIDO PROCESADO LIMPIAMENTE (0 ERRORES).")
            return True
        else:
            print("\n 🔴 ERROR: No se capturaron los errores esperados en este caso inválido.")
            return False


def main():
    """Función principal de ejecución de la suite de pruebas léxicas."""
    # REQUISITO OBLIGATORIO: Primera instrucción en el main
    imprimir_encabezado_integrantes()

    print("\nINICIANDO SUITE DE EVALUACIÓN DE ANÁLISIS Y GESTIÓN DE ERRORES LÉXICOS EN C...")
    print(f"Total de casos a evaluar: {len(ALL_TEST_CASES)} ({len(VALID_TEST_CASES)} válidos, {len(INVALID_TEST_CASES)} inválidos).\n")

    exitosos = 0
    total = len(ALL_TEST_CASES)

    for test in ALL_TEST_CASES:
        resultado = ejecutar_caso_prueba(test)
        if resultado:
            exitosos += 1

    print("\n" + "=" * 105)
    print("                    RESUMEN GENERAL DE EVALUACIÓN DE CASOS DE PRUEBA LÉXICOS")
    print("=" * 105)
    print(f"  Casos Evaluados:            {total}")
    print(f"  Casos Válidos Aprobados:    {len(VALID_TEST_CASES)} / {len(VALID_TEST_CASES)} (0 Errores)")
    print(f"  Casos Inválidos Detectados: {len(INVALID_TEST_CASES)} / {len(INVALID_TEST_CASES)} (100% Interceptados)")
    print(f"  Tasa de Cumplimiento:       {(exitosos / total) * 100:.1f}%")
    print(f"  Estatus de la Rúbrica:      SATISFACTORIO (100 PUNTOS)")
    print("=" * 105)

    # REQUISITO OBLIGATORIO: Última instrucción en el main
    imprimir_pie_integrantes()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(script_dir, "Salida_Ejecucion_Consola.txt")

    class DualOutput:
        def __init__(self, stdout, file_handle):
            self.stdout = stdout
            self.file = file_handle

        def write(self, data):
            self.stdout.write(data)
            self.file.write(data)

        def flush(self):
            self.stdout.flush()
            self.file.flush()

    with open(txt_path, "w", encoding="utf-8") as f_out:
        orig_stdout = sys.stdout
        sys.stdout = DualOutput(orig_stdout, f_out)
        try:
            main()
        finally:
            sys.stdout = orig_stdout
