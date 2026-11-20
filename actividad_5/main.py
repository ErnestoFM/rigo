"""
================================================================================
ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL (LENGUAJE C EN PYTHON)
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
import os
from typing import List
from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import TEST_CASES, TestCase


def print_team_header():
    """
    Imprime los nombres completos de los integrantes en orden alfabético
    por primer apellido conforme al mandato estricto de la rúbrica oficial.
    """
    border = "=" * 80
    print(border)
    print(" CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERIAS")
    print(" DIVISION DE ELECTRONICA Y COMPUTACION")
    print(" DEPARTAMENTO DE CIENCIAS COMPUTACIONALES")
    print(" MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES")
    print(" PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print(" ACTIVIDAD 5: ANALISIS SINTACTICO DE ESTRUCTURAS DE CONTROL")
    print(" INTEGRANTES DEL EQUIPO (ORDEN ALFABETICO POR PRIMER APELLIDO):")
    print("   1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("   2. FIERRO MELENDEZ ERNESTO HATUEY")
    print("   3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("   4. MILLAN GUERRERO OSWALDO JOSUE")
    print(border)


class DualOutput:
    """Duplica la salida estándar a la consola y a un archivo de texto."""
    def __init__(self, filename: str):
        self.terminal = sys.stdout
        self.log_file = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.close()


def run_test(test: TestCase) -> bool:
    """Ejecuta un caso de prueba individual y reporta los resultados detallados."""
    separator = "-" * 80
    print(f"\n{separator}")
    validity_tag = "[CASO VALIDO]" if test.is_valid else "[CASO INVALIDO CON ERRORES]"
    print(f"TEST #{test.id_num:02d}: {test.name} {validity_tag}")
    print(f"Categoria: {test.category}")
    print(f"Comportamiento Esperado: {test.expected_behavior}")
    print(separator)
    print("CODIGO FUENTE EVALUADO:")
    for line_idx, line in enumerate(test.code.splitlines(), start=1):
        print(f"  {line_idx:2d} | {line}")
    print(separator)

    # 1. Fase de Análisis Léxico
    lexer = Lexer(test.code)
    tokens = lexer.tokenize()

    # 2. Fase de Análisis Sintáctico
    error_handler = SyntaxErrorHandler()
    parser = Parser(tokens, error_handler)
    ast = parser.parse()

    passed = False
    if test.is_valid:
        if not error_handler.has_errors:
            passed = True
            print(">>> RESULTADO DEL ANALISIS: EXITOSO (0 ERRORES SINTACTICOS)")
            print("\nARBOL DE SINTAXIS ABSTRACTA (AST) GENERADO:")
            print(ast.to_tree_str())
        else:
            passed = False
            print(">>> RESULTADO DEL ANALISIS: FALLIDO (Se esperaba éxito pero se detectaron errores):")
            print(error_handler.to_formatted_table())
    else:
        if error_handler.has_errors:
            passed = True
            print(f">>> RESULTADO DEL ANALISIS: EXITOSO (Deteccion correcta de {len(error_handler.errors)} error(es) sintactico(s))")
            print("\nTABLA DE ERRORES SINTACTICOS DETECTADOS:")
            print(error_handler.to_formatted_table())
            print("\nDIAGNOSTICOS CON SUGERENCIAS DE CORRECCION:")
            for err in error_handler.errors:
                print(err.to_diagnostic_string())
        else:
            passed = False
            print(">>> RESULTADO DEL ANALISIS: FALLIDO (Se esperaba detectar errores pero no se hallaron)")

    print(separator)
    status_label = "[APROBADO]" if passed else "[FALLADO]"
    print(f"ESTADO DE PRUEBA #{test.id_num}: {status_label}")
    return passed


def main():
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Salida_Ejecucion_Consola.txt")
    dual_out = DualOutput(log_path)
    original_stdout = sys.stdout
    sys.stdout = dual_out

    try:
        # PRIMERA INSTRUCCION: Imprimir nombres completos de integrantes en orden alfabetico
        print_team_header()

        total = len(TEST_CASES)
        passed_count = 0

        print(f"\nIniciando Bateria de Pruebas del Analizador Sintactico ({total} casos en total)...")

        for test in TEST_CASES:
            if run_test(test):
                passed_count += 1

        print("\n" + "=" * 80)
        print(" RESUMEN GENERAL DE EJECUCION DE PRUEBAS")
        print("=" * 80)
        print(f" Total de Casos Evaluados: {total}")
        print(f" Casos Aprobados         : {passed_count}")
        print(f" Casos Fallados          : {total - passed_count}")
        print(f" Tasa de Exito           : {(passed_count / total) * 100:.1f}%")
        print("=" * 80)

        # ULTIMA INSTRUCCION: Imprimir nombres completos de integrantes en orden alfabetico
        print_team_header()

    finally:
        sys.stdout = original_stdout
        dual_out.close()
        print(f"\n[OK] Salida de ejecucion guardada exitosamente en: {log_path}")


if __name__ == "__main__":
    main()
