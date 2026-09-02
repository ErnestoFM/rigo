"""
================================================================================
ACTIVIDAD 2: MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import sys
from lexer import LexerC
from token_type import TokenType
from test_cases import (
    C_VALID_TEST,
    C_TEST_UNRECOGNIZED_CHARS,
    C_TEST_MALFORMED_IDENTIFIERS,
    C_TEST_INCORRECT_NUMBERS,
    C_TEST_UNCLOSED_STRINGS,
    C_TEST_COMBINED_ERRORS
)

def imprimir_encabezado_integrantes():
    print("=" * 85)
    print("   ACTIVIDAD 2: GESTIÓN Y MANEJO DE ERRORES LÉXICOS (ANALIZADOR LÉXICO C)")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 85)

def imprimir_pie_integrantes():
    print("=" * 85)
    print("   EJECUCIÓN Y VALIDACIÓN DE ERRORES LÉXICOS FINALIZADA EXITOSAMENTE")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 85)

def ejecutar_prueba(titulo: str, code: str):
    print(f"\n" + "=" * 85)
    print(f" >>> {titulo.upper()} <<<")
    print("=" * 85)
    
    lexer = LexerC(code)
    tokens = lexer.tokenize()

    header = f"| {'#':<4} | {'LÍNEA':<5} | {'COL':<4} | {'CATEGORÍA / ESTADO LÉXICO':<32} | {'LEXEMA / VALOR':<25} |"
    divider = "+" + "-" * 6 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 34 + "+" + "-" * 27 + "+"
    
    print(divider)
    print(header)
    print(divider)

    total_validos = 0
    total_errores = 0

    for idx, token in enumerate(tokens, 1):
        lex_repr = repr(token.value)[1:-1] if '\n' in token.value or '\t' in token.value else token.value
        if len(lex_repr) > 24:
            lex_repr = lex_repr[:21] + "..."
            
        tipo_str = token.type.value
        if token.is_error:
            tipo_str = f"❌ {token.type.value}"
            total_errores += 1
        else:
            total_validos += 1

        print(f"| {idx:<4} | {token.line:<5} | {token.column:<4} | {tipo_str:<32} | {lex_repr:<25} |")

    print(divider)
    print(f" RESUMEN: {total_validos} Tokens Válidos | {total_errores} Errores Léxicos Capturados")

    # Imprimir reporte detallado del ErrorHandler
    lexer.error_handler.print_error_report()

def main():
    # 1. PRIMERA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    imprimir_encabezado_integrantes()

    # 2. Ejecución de las 6 Suites de Prueba
    ejecutar_prueba("Caso de Prueba 1: Código C Válido (Sin Errores)", C_VALID_TEST)
    ejecutar_prueba("Caso de Prueba 2: Caracteres No Reconocidos (@, $, #, ~, ¿, ñ)", C_TEST_UNRECOGNIZED_CHARS)
    ejecutar_prueba("Caso de Prueba 3: Identificadores Mal Formados (123var, 8promedio)", C_TEST_MALFORMED_IDENTIFIERS)
    ejecutar_prueba("Caso de Prueba 4: Literales Numéricos Incorrectos (3.14.15, 0x12G4)", C_TEST_INCORRECT_NUMBERS)
    ejecutar_prueba("Caso de Prueba 5: Cadenas Mal Formadas / Sin Comilla de Cierre", C_TEST_UNCLOSED_STRINGS)
    ejecutar_prueba("Caso de Prueba 6: Suite Combinada con Múltiples Fallas Léxicas", C_TEST_COMBINED_ERRORS)

    # 3. ÚLTIMA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    imprimir_pie_integrantes()

if __name__ == "__main__":
    main()
