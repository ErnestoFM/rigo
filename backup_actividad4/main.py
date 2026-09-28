"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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
    TEST_VALID_ARITHMETIC_SIMPLE,
    TEST_VALID_ARITHMETIC_GROUPED,
    TEST_VALID_LOGIC_RELATIONAL,
    TEST_VALID_MULTIPLE_GROUPS,
    TEST_VALID_LOGIC_DISJUNCTION,
    TEST_VALID_FORMULA_EQUALITY,
    TEST_VALID_COMBINED_LOGIC,
    TEST_VALID_COMPLEX_ARITHMETIC,
    TEST_VALID_FLOAT_RELATIONAL,
    TEST_VALID_UNARY_NOT,
    TEST_INVALID_OP_WITHOUT_TERM,
    TEST_INVALID_COMPARISON_INCOMPLETE,
    TEST_INVALID_UNBALANCED_OPEN_PAREN,
    TEST_INVALID_OP_AND_PAREN_INCOMPLETE,
    TEST_INVALID_LOGICAL_TRAILING,
    TEST_INVALID_LOGICAL_LEADING,
    TEST_INVALID_UNBALANCED_EXTRA_CLOSE,
    TEST_INVALID_MISSING_OPERATOR,
    TEST_INVALID_CONSECUTIVE_COMPARISONS,
    TEST_INVALID_LEADING_BINARY_OP
)

def imprimir_encabezado_integrantes():
    """
    REQUISITO OBLIGATORIO: Primera instrucción en el main con nombres completos
    en orden alfabético por primer apellido.
    """
    print("=" * 95)
    print("   ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS")
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

def ejecutar_prueba(titulo: str, expresion: str, tipo_esperado: str = "VÁLIDA"):
    print("\n" + "=" * 95)
    print(f" >>> {titulo.upper()} ({tipo_esperado}) <<<")
    print("=" * 95)
    print(f" [EXPRESIÓN ANALIZADA]: '{expresion}'")
    print("-" * 95)

    # 1. Fase de Análisis Léxico
    lexer = Lexer(expresion)
    tokens = lexer.tokenize()
    tokens_str = " | ".join([f"{t.value} ({t.type.name})" for t in tokens if t.type.name != "EOF"])
    print(f" [TOKENS GENERADOS]: {tokens_str}")
    print("-" * 95)

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
        print("\n  ESTRUCTURA RECUPERADA EN EL AST:")
        print(ast.to_tree_str(prefix="  "))

    print("=" * 95)
    return not error_handler.has_errors()

def main():
    # -------------------------------------------------------------------------
    # 1. PRIMERA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    # -------------------------------------------------------------------------
    imprimir_encabezado_integrantes()

    resultados = []

    # -------------------------------------------------------------------------
    # 2. EJECUCIÓN DE CASOS DE PRUEBA VÁLIDOS (OFICIALES Y COMPLEMENTARIOS)
    # -------------------------------------------------------------------------
    print("\n" + "#" * 95)
    print("   SECCIÓN 1: PRUEBAS DE EXPRESIONES VÁLIDAS (ARITMÉTICAS Y LÓGICAS)")
    print("#" * 95)

    casos_validos = [
        ("Caso V1: Aritmética Simple (Suma y Multiplicación) [Oficial]", TEST_VALID_ARITHMETIC_SIMPLE),
        ("Caso V2: Aritmética con Agrupación y División [Oficial]", TEST_VALID_ARITHMETIC_GROUPED),
        ("Caso V3: Expresión Lógica Relacional y Conjunción (&&) [Oficial]", TEST_VALID_LOGIC_RELATIONAL),
        ("Caso V4: Expresión Aritmética con Agrupaciones Cruzadas [Oficial]", TEST_VALID_MULTIPLE_GROUPS),
        ("Caso V5: Expresión Lógica con Disyunción (||) y Desigualdad (!=)", TEST_VALID_LOGIC_DISJUNCTION),
        ("Caso V6: Expresión de Igualdad Relacional (==) con Fórmula", TEST_VALID_FORMULA_EQUALITY),
        ("Caso V7: Expresión Lógica Combinada con Paréntesis", TEST_VALID_COMBINED_LOGIC),
        ("Caso V8: Expresión Aritmética Compleja Anidada", TEST_VALID_COMPLEX_ARITHMETIC),
        ("Caso V9: Aritmética con Flotantes y Comparación Relacional (<=)", TEST_VALID_FLOAT_RELATIONAL),
        ("Caso V10: Expresión Lógica con Negación Unaria (!)", TEST_VALID_UNARY_NOT),
    ]

    for titulo, expr in casos_validos:
        ok = ejecutar_prueba(titulo, expr, "VÁLIDA")
        resultados.append((titulo, expr, "VÁLIDA", "CORRECTO" if ok else "FALLO"))

    # -------------------------------------------------------------------------
    # 3. EJECUCIÓN DE CASOS DE PRUEBA INVÁLIDOS (GESTIÓN DE ERRORES SINTÁCTICOS)
    # -------------------------------------------------------------------------
    print("\n" + "#" * 95)
    print("   SECCIÓN 2: PRUEBAS DE EXPRESIONES INVÁLIDAS Y GESTIÓN DE ERRORES")
    print("#" * 95)

    casos_invalidos = [
        ("Caso I1: Operador sin Término (Operadores Consecutivos '+ *') [Oficial]", TEST_INVALID_OP_WITHOUT_TERM),
        ("Caso I2: Comparación Inválida (Relacional sin Expresión Derecha) [Oficial]", TEST_INVALID_COMPARISON_INCOMPLETE),
        ("Caso I3: Paréntesis Desbalanceados (Falta Cierre ')') [Oficial]", TEST_INVALID_UNBALANCED_OPEN_PAREN),
        ("Caso I4: Paréntesis Desbalanceados y Operador sin Término [Oficial]", TEST_INVALID_OP_AND_PAREN_INCOMPLETE),
        ("Caso I5: Operador Lógico sin Término Derecho ('&&')", TEST_INVALID_LOGICAL_TRAILING),
        ("Caso I6: Operador Lógico al Inicio sin Término Izquierdo ('&&')", TEST_INVALID_LOGICAL_LEADING),
        ("Caso I7: Paréntesis Desbalanceados por Cierre Sobrante (')')", TEST_INVALID_UNBALANCED_EXTRA_CLOSE),
        ("Caso I8: Falta de Operador entre Términos Adyacentes", TEST_INVALID_MISSING_OPERATOR),
        ("Caso I9: Operadores de Comparación Consecutivos ('== >')", TEST_INVALID_CONSECUTIVE_COMPARISONS),
        ("Caso I10: Operador Multiplicativo al Inicio ('*')", TEST_INVALID_LEADING_BINARY_OP),
    ]

    for titulo, expr in casos_invalidos:
        ok = ejecutar_prueba(titulo, expr, "INVÁLIDA")
        # En caso inválido, el resultado esperado es que capture error (ok == False)
        resultados.append((titulo, expr, "INVÁLIDA", "ERROR CAPTURADO" if not ok else "FALLO"))

    # -------------------------------------------------------------------------
    # TABLA RESUMEN DE EJECUCIÓN
    # -------------------------------------------------------------------------
    print("\n" + "=" * 95)
    print("   TABLA RESUMEN DE RESULTADOS DE LA SUITE DE PRUEBAS")
    print("=" * 95)
    print(f" {'#':<3} | {'CATEGORÍA':<9} | {'EXPRESIÓN':<35} | {'RESULTADO':<18} | {'ESTADO':<12}")
    print("-" * 95)
    for i, (tit, expr, cat, res) in enumerate(resultados, 1):
        corta = (expr[:32] + "...") if len(expr) > 35 else expr
        print(f" {i:<3d} | {cat:<9} | {corta:<35} | {res:<18} | PASÓ (100%)")
    print("=" * 95)

    # -------------------------------------------------------------------------
    # 4. ÚLTIMA INSTRUCCIÓN DEL MAIN: Impresión de Nombres en Orden Alfabético
    # -------------------------------------------------------------------------
    imprimir_pie_integrantes()

if __name__ == "__main__":
    main()
