"""
================================================================================
PROYECTO FINAL: COMPILADOR INTEGRAL DE LENGUAJE C
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
from compiler_pipeline import CompilerPipeline, CompilationResult
from test_cases import TEST_CASES, TestCase


def print_team_header():
    """Imprime el encabezado oficial del equipo en orden alfabético por primer apellido."""
    print("=" * 80)
    print("PROYECTO FINAL: COMPILADOR INTEGRAL DE LENGUAJE C")
    print("MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES")
    print("PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print("\nINTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 80)


class TeeLogger:
    """Duplica la salida estándar a consola y al archivo Salida_Ejecucion_Consola.txt."""
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


def run_all_tests():
    # PRIMERA INSTRUCCIÓN: Imprimir integrantes del equipo
    print_team_header()

    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Salida_Ejecucion_Consola.txt")
    tee = TeeLogger(out_file)
    original_stdout = sys.stdout
    sys.stdout = tee

    try:
        # Repetir encabezado en el log
        print_team_header()
        print("\nINICIANDO BATERÍA DE PRUEBAS AUTOMATIZADAS DEL COMPILADOR INTEGRAL")
        print("Total de casos de prueba: 10 (5 Válidos con ejecución en VM, 5 Inválidos con diagnóstico de errores)")
        print("-" * 80)

        results_summary = []

        for idx, tc in enumerate(TEST_CASES, 1):
            print(f"\n{'=' * 80}")
            print(f"CASO DE PRUEBA {idx:02d} / 10: [{tc.id}] {tc.name}")
            print(f"CATEGORÍA: {tc.category} | FASE OBJETIVO: {tc.target_phase}")
            print(f"DESCRIPCIÓN: {tc.description}")
            print(f"{'-' * 80}")
            print("CÓDIGO FUENTE C:")
            print(tc.source_code.strip())
            print(f"{'-' * 80}")

            res = CompilerPipeline.compile_and_run(tc.source_code)

            if tc.expected_success:
                out_ok = (tc.expected_output in res.vm_output) if tc.expected_output else True
                passed = res.success and out_ok
                status_str = "EXITOSA (COMPILACIÓN Y EJECUCIÓN EN VM)" if passed else "FALLIDA"

                print(f"[FASE 1: LÉXICO] Tokens generados: {len(res.tokens)}")
                print(f"[FASE 2: SINTÁCTICO] Nodos en AST generados correctamente.")
                print(f"[FASE 3: SEMÁNTICO] Variables en tabla de símbolos: {len(res.symbols_list)}")
                print(f"[FASE 4: TAC ORIGINAL] Instrucciones de 3 direcciones: {len(res.tac_unoptimized)}")
                print(f"[FASE 5: TAC OPTIMIZADO] Instrucciones tras optimización: {len(res.tac_optimized)}")
                print(f"[FASE 6: GENERADOR CÓDIGO] Instrucciones máquina: {len(res.machine_code_opt)} (Ahorro: {res.code_metrics.get('instructions_saved', 0)} instrs, {res.code_metrics.get('efficiency_gain_pct', 0)}%)")
                print(f"[FASE 7: MÁQUINA VIRTUAL] Salida estándar:")
                for out_line in res.vm_output:
                    print(f"    {out_line}")
                print(f"[ESTADO FINAL REGISTROS Y BANDERAS]:\n{res.vm_registers_dump}")
                print(f"[MAPA DE MEMORIA RAM FINAL]:\n{res.vm_memory_dump}")
                print(f"VEREDICTO: {status_str} | Esperado: '{tc.expected_output}' | Obtenido: {res.vm_output}")
                results_summary.append((tc.id, tc.name, tc.category, passed, status_str))

            else:
                err_phases = [e.phase for e in res.errors]
                has_expected = any(tc.expected_error_type.lower() in p.lower() for p in err_phases)
                passed = (not res.success) and has_expected
                status_str = f"DETECCIÓN CORRECTA EN [{res.error_stage}]" if passed else "FALLO EN DETECCIÓN"

                print(f"FASE DE INTERRUPCIÓN: [{res.error_stage}]")
                print(f"ERRORES DIAGNOSTICADOS ({len(res.errors)}):")
                for err in res.errors:
                    print(f"    * {err}")
                print(f"VEREDICTO: {status_str} | Esperado: {tc.expected_error_type}")
                results_summary.append((tc.id, tc.name, tc.category, passed, status_str))

        # Tabla de Resumen Final
        print(f"\n{'=' * 80}")
        print("RESUMEN GLOBAL DE RESULTADOS DE PRUEBA")
        print(f"{'=' * 80}")
        print(f"| {'ID':<6} | {'Nombre del Caso':<45} | {'Tipo':<9} | {'Resultado':<12} |")
        print(f"|{'-' * 8}|{'-' * 47}|{'-' * 11}|{'-' * 14}|")
        all_passed = True
        for cid, cname, ccat, cpassed, cstatus in results_summary:
            res_str = "APROBADO" if cpassed else "REPROBADO"
            if not cpassed:
                all_passed = False
            print(f"| {cid:<6} | {cname:<45} | {ccat:<9} | {res_str:<12} |")
        print(f"{'=' * 80}")
        print(f"RESULTADO FINAL: {'¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE (10/10)!' if all_passed else 'FALLOS DETECTADOS'}")
        print(f"Bitácora guardada en: {out_file}")
        print(f"{'=' * 80}")

    finally:
        sys.stdout = original_stdout
        tee.close()

    # ÚLTIMA INSTRUCCIÓN: Imprimir integrantes del equipo
    print_team_header()


if __name__ == "__main__":
    run_all_tests()
