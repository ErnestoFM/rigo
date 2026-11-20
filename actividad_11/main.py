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
from typing import List
from lexer import Lexer
from parser import Parser
from tac_generator import TACGenerator
from error_handler import CompilerErrorHandler
from test_cases import TEST_CASES, TestCase


def print_team_banner():
    """Imprime el listado obligatorio de integrantes en orden alfabético."""
    print("=" * 80)
    print("COMPILADOR C - TRADUCTORES DE LENGUAJE (CUCEI - UDG)")
    print("ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO")
    print("PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print("-" * 80)
    print("INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 80)


class DualWriter:
    """Duplica la salida estándar a consola y archivo de texto simultáneamente."""
    def __init__(self, filepath: str):
        self.terminal = sys.stdout
        self.log_file = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.close()


def run_test_suite():
    # PRIMERA INSTRUCCIÓN OBLIGATORIA
    print_team_banner()

    passed_count = 0
    total_tests = len(TEST_CASES)

    for tc in TEST_CASES:
        print("\n" + "=" * 80)
        tipo_str = "VÁLIDO" if tc.is_valid else "INVÁLIDO (CONTROL DE ERRORES)"
        print(f"CASO DE PRUEBA #{tc.id_num}: [{tipo_str}] {tc.name}")
        print(f"Categoría: {tc.category}")
        print("-" * 80)
        print("CÓDIGO FUENTE DE ENTRADA (C):")
        for line in tc.code.splitlines():
            print(f"    {line}")
        print("\nCOMPORTAMIENTO ESPERADO:")
        print(f"    {tc.expected_behavior}")
        print("-" * 80)

        err_handler = CompilerErrorHandler()
        lexer = Lexer(tc.code, err_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens, err_handler)
        ast = parser.parse()

        tac_gen = TACGenerator(err_handler)
        instructions = tac_gen.generate(ast)

        if tc.is_valid:
            if not err_handler.has_errors:
                print("RESULTADO: GENERACIÓN EXITOSA DE CÓDIGO INTERMEDIO (TAC):")
                print("-" * 80)
                for instr in instructions:
                    print(f"    {str(instr)}")
                print("-" * 80)
                print("ESTADO: [PASSED - Código intermedio generado conforme a la rúbrica]")
                passed_count += 1
            else:
                print("RESULTADO INESPERADO: Se encontraron errores en un caso válido:")
                print(err_handler.get_summary())
                print("ESTADO: [FAILED]")
        else:
            if err_handler.has_errors:
                print("RESULTADO: ERRORES SEMÁNTICOS / SINTÁCTICOS DETECTADOS CORRECTAMENTE:")
                print("-" * 80)
                for err in err_handler.errors:
                    print(f"    {str(err)}")
                print("-" * 80)
                print("INSTRUCCIONES TAC GENERADAS CON GUARDAS DE ERROR:")
                for instr in instructions:
                    print(f"    {str(instr)}")
                print("-" * 80)
                print("ESTADO: [PASSED - Error semántico interceptado y reportado adecuadamente]")
                passed_count += 1
            else:
                print("RESULTADO INESPERADO: El caso inválido no generó errores esperados.")
                print("ESTADO: [FAILED]")

    print("\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS DE LA SUITE DE PRUEBAS")
    print("=" * 80)
    print(f"Total de casos ejecutados: {total_tests}")
    print(f"Casos exitosos:           {passed_count} / {total_tests} ({(passed_count/total_tests)*100:.1f}%)")
    print(f"Casos fallidos:           {total_tests - passed_count}")

    if passed_count == total_tests:
        print(">> VERIFICACIÓN COMPLETA: TODOS LOS CASOS DE PRUEBA PASARON SATISFACTORIAMENTE <<")
    print("=" * 80)

    # ÚLTIMA INSTRUCCIÓN OBLIGATORIA
    print_team_banner()


if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(current_dir, "Salida_Ejecucion_Consola.txt")

    original_stdout = sys.stdout
    dual_writer = DualWriter(log_file_path)
    sys.stdout = dual_writer

    try:
        run_test_suite()
    finally:
        sys.stdout = original_stdout
        dual_writer.close()
        print(f"\n[INFO] Salida guardada exitosamente en: {log_file_path}")
