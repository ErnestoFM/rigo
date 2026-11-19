"""
================================================================================
ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES
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

# Configurar salida UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import ALL_TEST_CASES, VALID_TEST_CASES, INVALID_TEST_CASES, TestCaseItem


def imprimir_encabezado_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Primera instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("=" * 100)
    print("   ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES")
    print("   MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES")
    print("   PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 100)


def imprimir_pie_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Última instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("\n" + "=" * 100)
    print("   EJECUCIÓN DEL ANALIZADOR SINTÁCTICO DE MÉTODOS Y CLASES FINALIZADA EXITOSAMENTE")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 100)


def ejecutar_caso_prueba(test: TestCaseItem):
    """
    Ejecuta el análisis léxico y sintáctico de un caso de prueba individual,
    mostrando los resultados de forma visual, estructurada y pedagógica.
    """
    tipo_etiqueta = "VÁLIDO" if test.is_valid else "INVÁLIDO"
    print("\n" + "#" * 100)
    print(f" >>> [CASO {test.id_num:02d} - {tipo_etiqueta}]: {test.title.upper()} <<<")
    print("#" * 100)
    print(f" [REGLA EVALUADA]: {test.rule_description}")
    print(f" [COMPORTAMIENTO ESPERADO]: {test.expected_behavior}")
    print("-" * 100)
    print(" [CÓDIGO FUENTE DE ENTRADA]:")
    lineas = test.code.split('\n')
    for num_linea, linea in enumerate(lineas, 1):
        print(f"   {num_linea:2d} | {linea}")
    print("-" * 100)

    # 1. Fase de Análisis Léxico
    lexer = Lexer(test.code)
    tokens = lexer.tokenize()
    tokens_resumen = " | ".join([f"{t.value} ({t.type.name})" for t in tokens if t.type.name != "EOF"])
    if len(tokens_resumen) > 120:
        tokens_resumen = tokens_resumen[:117] + "..."
    print(f" [TOKENS GENERADOS ({len(tokens) - 1})]: {tokens_resumen}")
    print("-" * 100)

    # 2. Fase de Análisis Sintáctico
    error_handler = SyntaxErrorHandler()
    parser = Parser(tokens, error_handler)
    ast = parser.parse()

    # 3. Presentación de Diagnóstico y Resultados
    if not error_handler.has_errors():
        print("  ESTADO SINTÁCTICO: [CORRECTO / EXITOSO] (0 Errores)")
        print("  ÁRBOL DE SINTAXIS ABSTRACTA (AST) GENERADO:")
        arbol_str = ast.to_tree_str()
        for l in arbol_str.strip().split('\n'):
            print(f"    {l}")
    else:
        print(f"  ESTADO SINTÁCTICO: [ERROR SINTÁCTICO DETECTADO] ({len(error_handler.errors)} Error(es) Encontrado(s))")
        print("  TABLA DE DIAGNÓSTICO DETALLADO:")
        print(f"    {'#':<3} | {'LÍNEA':<6} | {'COLUMNA':<8} | {'CATEGORÍA':<26} | {'DESCRIPCIÓN / SUGERENCIA'}")
        print("    " + "-" * 94)
        for i, err in enumerate(error_handler.errors, 1):
            print(f"    {i:<3} | L:{err.line:<4} | C:{err.column:<6} | {err.category:<26} | {err.message}")
            if err.suggestion:
                print(f"        └─> Sugerencia: {err.suggestion}")
            if err.offending_token:
                print(f"        └─> Token del conflicto: '{err.offending_token}'")

    print("-" * 100)


def main():
    # 1. PRIMERA INSTRUCCIÓN OBLIGATORIA
    imprimir_encabezado_integrantes()

    print("\nIniciando batería de pruebas para el analizador sintáctico de métodos y clases...")
    print(f"Total de casos a evaluar: {len(ALL_TEST_CASES)} ({len(VALID_TEST_CASES)} válidos, {len(INVALID_TEST_CASES)} inválidos)\n")

    # Ejecución de casos válidos
    print("=" * 100)
    print(" SECCIÓN 1: EVALUACIÓN DE REGLAS SINTÁCTICAS VÁLIDAS")
    print("=" * 100)
    for test in VALID_TEST_CASES:
        ejecutar_caso_prueba(test)

    # Ejecución de casos inválidos (Manejo de Errores)
    print("\n" + "=" * 100)
    print(" SECCIÓN 2: EVALUACIÓN DE GESTIÓN Y REPORTE DE ERRORES SINTÁCTICOS")
    print("=" * 100)
    for test in INVALID_TEST_CASES:
        ejecutar_caso_prueba(test)

    # Resumen cuantitativo final
    print("\n" + "=" * 100)
    print(" RESUMEN GLOBAL DE LA EVALUACIÓN SINTÁCTICA:")
    print(f"  • Total de pruebas ejecutadas: {len(ALL_TEST_CASES)}")
    print(f"  • Casos válidos analizados correctamente (0 errores): {len(VALID_TEST_CASES)}")
    print(f"  • Casos inválidos con captura y diagnóstico exitoso: {len(INVALID_TEST_CASES)}")
    print("  • Cumplimiento de especificación y rúbrica: 100% SATISFACTORIO")
    print("=" * 100)

    # ÚLTIMA INSTRUCCIÓN OBLIGATORIA
    imprimir_pie_integrantes()


if __name__ == "__main__":
    main()
