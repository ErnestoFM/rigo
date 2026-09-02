"""
================================================================================
ACTIVIDAD 1: DEFINICIÓN DE TOKENS Y EXPRESIONES REGULARES (ANALIZADOR LÉXICO C)
MATERIA: COMPILADORES
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
from test_cases import C_VALID_TEST_1, C_VALID_TEST_2, C_INVALID_TEST

def imprimir_encabezado_integrantes():
    print("=" * 80)
    print("   ACTIVIDAD 1: DEFINICIÓN DE TOKENS Y EXPRESIONES REGULARES (ANALIZADOR LÉXICO C)")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 80)

def imprimir_pie_integrANTES():
    print("=" * 80)
    print("   EJECUCIÓN FINALIZADA EXITOSAMENTE")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 80)

def imprimir_tabla_tokens(titulo: str, code: str):
    print(f"\n" + "-" * 80)
    print(f" >>> {titulo.upper()} <<<")
    print("-" * 80)
    
    lexer = LexerC(code)
    tokens = lexer.tokenize()

    header = f"| {'#':<4} | {'LÍNEA':<6} | {'COL':<5} | {'CATEGORÍA LÉXICA':<24} | {'LEXEMA / VALOR':<25} |"
    divider = "+" + "-" * 6 + "+" + "-" * 8 + "+" + "-" * 7 + "+" + "-" * 26 + "+" + "-" * 27 + "+"
    
    print(divider)
    print(header)
    print(divider)

    total_tokens = 0
    total_errores = 0

    for idx, token in enumerate(tokens, 1):
        # Truncar o limpiar lexema para presentación en tabla de consola
        lex_repr = repr(token.value)[1:-1] if '\n' in token.value or '\t' in token.value else token.value
        if len(lex_repr) > 24:
            lex_repr = lex_repr[:21] + "..."
            
        tipo_str = token.type.value
        if token.type == TokenType.ERROR_LEXICO:
            tipo_str = "!!! ERROR LÉXICO !!!"
            total_errores += 1
        else:
            total_tokens += 1

        print(f"| {idx:<4} | {token.line:<6} | {token.column:<5} | {tipo_str:<24} | {lex_repr:<25} |")

    print(divider)
    print(f" RESUMEN: {total_tokens} Tokens Válidos Identificados | {total_errores} Errores Léxicos Detectados\n")

def main():
    # 1. PRIMERA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    imprimir_encabezado_integrantes()

    # 2. Demostración de Ejecución del Analizador Léxico para Lenguaje C
    imprimir_tabla_tokens("Caso de Prueba Válido 1: Factorial, Structs y Bucles en C", C_VALID_TEST_1)
    imprimir_tabla_tokens("Caso de Prueba Válido 2: Bits, Notación Científica y Switch en C", C_VALID_TEST_2)
    imprimir_tabla_tokens("Caso de Prueba 3: Demostración de Detección de Errores Léxicos", C_INVALID_TEST)

    # 3. ÚLTIMA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    imprimir_pie_integrANTES()

if __name__ == "__main__":
    main()
