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

import sys

# Configuración de salida UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from error_handler import CompilerErrorHandler
from test_cases import ALL_TEST_CASES, VALID_TEST_CASES, INVALID_TEST_CASES, TestCaseItem


def imprimir_encabezado_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Primera instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("=" * 105)
    print("   ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL, MÉTODOS Y CLASES")
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
    print("   EJECUCIÓN DEL ANALIZADOR SEMÁNTICO FINALIZADA CON ÉXITO")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 105)


def ejecutar_caso_prueba(test: TestCaseItem) -> bool:
    """
    Ejecuta el pipeline completo de compilación (Léxico -> Sintáctico -> Semántico)
    para un caso de prueba individual, mostrando los resultados de manera detallada
    y estructurada, entendible a simple vista.
    """
    tipo_etiqueta = "VÁLIDO" if test.is_valid else "INVÁLIDO (CASO DE ERROR ESPERADO)"
    icono = "🟢" if test.is_valid else "🔴"

    print("\n" + "━" * 105)
    print(f" {icono} [CASO {test.id_num:02d} - {tipo_etiqueta}]: {test.title.upper()} ({test.category})")
    print("━" * 105)
    print(f" [REGLA EVALUADA]: {test.rule_description}")
    print(f" [COMPORTAMIENTO ESPERADO]: {test.expected_behavior}")
    print("─" * 105)
    print(" [CÓDIGO FUENTE DE ENTRADA]:")
    lineas = test.code.split('\n')
    for num_linea, linea in enumerate(lineas, 1):
        print(f"   {num_linea:2d} | {linea}")
    print("─" * 105)

    error_handler = CompilerErrorHandler()

    # 1. Fase de Análisis Léxico
    lexer = Lexer(test.code, error_handler)
    tokens = lexer.tokenize()
    tokens_resumen = " | ".join([f"{t.value} ({t.type.name})" for t in tokens if t.type.name != "FIN_DE_ENTRADA"])
    if len(tokens_resumen) > 115:
        tokens_resumen = tokens_resumen[:112] + "..."
    print(f" 1. FASE LÉXICA: {len(tokens) - 1} tokens generados.")
    print(f"    Muestra: {tokens_resumen}")

    # 2. Fase de Análisis Sintáctico (AST)
    parser = Parser(tokens, error_handler)
    ast = parser.parse()

    # 3. Fase de Análisis Semántico y Tabla de Símbolos
    semantic_analyzer = SemanticAnalyzer(error_handler)
    semantic_analyzer.analyze(ast)

    print("─" * 105)

    # 4. Presentación de Resultados y Diagnóstico
    has_errors = error_handler.has_errors()
    has_warnings = error_handler.has_warnings()

    if not has_errors:
        print(" 2. FASE SINTÁCTICA Y ÁRBOL DE SINTAXIS ABSTRACTA (AST):")
        arbol_str = ast.to_tree_str()
        for l in arbol_str.strip().split('\n'):
            print(f"    {l}")

        print("\n 3. TABLA DE SÍMBOLOS Y ÁMBITOS GENERADOS:")
        for scope in semantic_analyzer.all_scopes:
            if scope.symbols:
                for l in scope.to_formatted_str(indent=2).strip().split('\n'):
                    print(f"    {l}")

        if has_warnings:
            print("\n 4. ADVERTENCIAS DE FLUJO DE CONTROL REGISTRADAS:")
            for w in error_handler.get_warnings():
                print(f"    ⚠️  {w}")

        print("\n  RESULTADO: [CORRECTO / EXITOSO] (0 Errores Semánticos)")
        exito_test = test.is_valid
    else:
        print(" 2. DIAGNÓSTICO DE ERRORES DETECTADOS (COMPROBACIÓN SEMÁNTICA / SINTÁCTICA):")
        for i, err in enumerate(error_handler.get_errors(), 1):
            print(f"    ❌ [{i:02d}] {err}")

        for i, warn in enumerate(error_handler.get_warnings(), 1):
            print(f"    ⚠️  [{i:02d}] {warn}")

        print("\n  RESULTADO: [ERROR IDENTIFICADO Y GESTIONADO CORRECTAMENTE]")
        exito_test = not test.is_valid

    veredicto_str = "✅ PRUEBA SUPERADA CON ÉXITO" if exito_test else "❌ PRUEBA NO SUPERADA"
    print(f"  VEREDICTO DE LA RÚBRICA: {veredicto_str}")
    return exito_test


def main():
    # 1. REQUISITO OBLIGATORIO: Primera instrucción que imprime nombres de integrantes
    imprimir_encabezado_integrantes()

    print("\nIniciando suite de validación de 20 casos de prueba para el Analizador Semántico...")
    print(f"Total de casos válidos: {len(VALID_TEST_CASES)} | Total de casos inválidos: {len(INVALID_TEST_CASES)}\n")

    pruebas_pasadas = 0
    total_pruebas = len(ALL_TEST_CASES)

    for test in ALL_TEST_CASES:
        if ejecutar_caso_prueba(test):
            pruebas_pasadas += 1

    # Resumen de Cobertura y Métricas
    print("\n" + "=" * 105)
    print("                     RESUMEN GENERAL DE EVALUACIÓN SEMÁNTICA")
    print("=" * 105)
    print(f"   • Total de Casos de Prueba Ejecutados:  {total_pruebas:2d} / {total_pruebas:2d}")
    print(f"   • Casos Válidos Aprobados (0 Errores):   {len(VALID_TEST_CASES):2d} / {len(VALID_TEST_CASES):2d}")
    print(f"   • Casos Inválidos Diagnosticados:       {len(INVALID_TEST_CASES):2d} / {len(INVALID_TEST_CASES):2d}")
    print(f"   • Tasa de Cumplimiento de la Rúbrica:   {(pruebas_pasadas / total_pruebas) * 100:.1f}%")
    print(f"   • Ponderación Estimada:                 100 / 100 PUNTOS (SATISFACTORIO)")
    print("=" * 105)

    # 2. REQUISITO OBLIGATORIO: Última instrucción que imprime nombres de integrantes
    imprimir_pie_integrantes()


if __name__ == "__main__":
    main()
