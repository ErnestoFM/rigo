"""
================================================================================
ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES
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

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import (
    TEST_VALID_SIMPLE_VARS,
    TEST_VALID_INITIALIZED_VARS,
    TEST_VALID_CONSTANTS,
    TEST_VALID_USAGE_EXPRESSIONS,
    TEST_INVALID_IDENTIFIERS,
    TEST_INVALID_TYPES,
    TEST_MISSING_SEMICOLONS,
    TEST_UNINITIALIZED_CONSTANT,
    TEST_MALFORMED_ASSIGNMENT,
    TEST_COMBINED_ERRORS
)

def imprimir_encabezado_integrantes():
    """
    REQUISITO OBLIGATORIO: Primera instrucción en el main con nombres completos
    en orden alfabético por primer apellido.
    """
    print("=" * 95)
    print("   ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES")
    print("   MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES")
    print("   PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 95)

def imprimir_pie_integrantes():
    """
    REQUISITO OBLIGATORIO: Última instrucción en el main con nombres completos
    en orden alfabético por primer apellido.
    """
    print("\n" + "=" * 95)
    print("   EJECUCIÓN DEL ANALIZADOR SINTÁCTICO FINALIZADA EXITOSAMENTE")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 95)

def ejecutar_prueba(titulo: str, codigo_fuente: str):
    print("\n" + "=" * 95)
    print(f" >>> {titulo.upper()} <<<")
    print("=" * 95)
    
    print(" [CÓDIGO FUENTE ANALIZADO]:")
    for num_linea, linea in enumerate(codigo_fuente.strip().split("\n"), 1):
        print(f"   {num_linea:2d} | {linea}")
    print("-" * 95)

    # 1. Fase de Análisis Léxico
    lexer = Lexer(codigo_fuente)
    tokens = lexer.tokenize()

    # 2. Fase de Análisis Sintáctico
    error_handler = SyntaxErrorHandler()
    parser = Parser(tokens, error_handler)
    ast = parser.parse()

    # 3. Presentación de Resultados
    if not error_handler.has_errors():
        print("  ESTADO SINTÁCTICO: [CORRECTO] (0 Errores)")
        print("\n  ÁRBOL DE SINTAXIS ABSTRACTA (AST) GENERADO:")
        print(ast.to_tree_str(prefix="  "))
    else:
        print(f"  ESTADO SINTÁCTICO: [ERRORES DETECTADOS] ({len(error_handler.errors)} Errores)")
        error_handler.print_error_report()

    print("=" * 95)

def main():
    # -------------------------------------------------------------------------
    # 1. PRIMERA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    # -------------------------------------------------------------------------
    imprimir_encabezado_integrantes()

    # -------------------------------------------------------------------------
    # 2. EJECUCIÓN DE CASOS DE PRUEBA VÁLIDOS
    # -------------------------------------------------------------------------
    ejecutar_prueba("Caso 1: Declaraciones Simples de Variables", TEST_VALID_SIMPLE_VARS)
    ejecutar_prueba("Caso 2: Declaraciones de Variables con Inicialización", TEST_VALID_INITIALIZED_VARS)
    ejecutar_prueba("Caso 3: Declaraciones de Constantes (Obligatoriamente Inicializadas)", TEST_VALID_CONSTANTS)
    ejecutar_prueba("Caso 4: Uso de Variables y Constantes en Expresiones", TEST_VALID_USAGE_EXPRESSIONS)

    # -------------------------------------------------------------------------
    # 3. EJECUCIÓN DE CASOS DE PRUEBA INVÁLIDOS (REGLAS Y GESTIÓN DE ERRORES)
    # -------------------------------------------------------------------------
    ejecutar_prueba("Caso 5: Error - Identificadores Inválidos que Inician con Dígito", TEST_INVALID_IDENTIFIERS)
    ejecutar_prueba("Caso 6: Error - Tipos de Datos No Válidos", TEST_INVALID_TYPES)
    ejecutar_prueba("Caso 7: Error - Falta de Punto y Coma (;) al Final", TEST_MISSING_SEMICOLONS)
    ejecutar_prueba("Caso 8: Error - Constante No Inicializada", TEST_UNINITIALIZED_CONSTANT)
    ejecutar_prueba("Caso 9: Error - Expresión Rota o Asignación Incompleta", TEST_MALFORMED_ASSIGNMENT)
    ejecutar_prueba("Caso 10: Suite Integral Combinada con Múltiples Fallas", TEST_COMBINED_ERRORS)

    # -------------------------------------------------------------------------
    # 4. ÚLTIMA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    # -------------------------------------------------------------------------
    imprimir_pie_integrantes()

if __name__ == "__main__":
    main()
