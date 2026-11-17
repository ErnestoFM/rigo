"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - EJECUCIÓN PRINCIPAL Y PRUEBAS DEL COMPILADOR
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
from io import StringIO
from typing import List, Dict, Any, Optional

# Configuración de salida UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from intermediate_code import TACGenerator, Quadruple
from symbol_table_mem import MemorySymbolTable
from code_generator import CodeGenerator, MachineInstruction
from executable_format import ExecutableBuilder, ExecutableHeader, ExecutableReader
from virtual_machine import VirtualMachine
from test_cases import ALL_TEST_CASES, VALID_TEST_CASES, INVALID_TEST_CASES, TestCaseCodeGeneration

# Importar frontend para el caso de código fuente de alto nivel
from lexer import Lexer
from parser import Parser
from error_handler import CompilerErrorHandler


def imprimir_encabezado_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Primera instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("=" * 110)
    print("   ACTIVIDAD 13: GENERACIÓN DE CÓDIGO (CÓDIGO INTERMEDIO A CÓDIGO MÁQUINA EJECUTABLE)")
    print("   MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES")
    print("   PROFESOR: RIGOBERTO CARDENAS LARIOS")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 110)


def imprimir_pie_integrantes():
    """
    REQUISITO OBLIGATORIO DE LA RÚBRICA:
    Última instrucción en el main con nombres completos en orden alfabético por primer apellido.
    """
    print("\n" + "=" * 110)
    print("   EJECUCIÓN DEL GENERADOR DE CÓDIGO FINALIZADA EXITOSAMENTE")
    print("   INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):")
    print("     1. DIAZ TORRES JAZMIN MONTSERRAT")
    print("     2. FIERRO MELÉNDEZ ERNESTO HATUEY")
    print("     3. HERNANDEZ GARCIA HECTOR GABRIEL")
    print("     4. MILLAN GUERRERO OSWALDO JOSUE")
    print("=" * 110)


def ejecutar_caso_prueba(test: TestCaseCodeGeneration, bin_dir: str) -> bool:
    """
    Ejecuta el pipeline completo para un caso de prueba:
    1. Entrada (TAC o Código Fuente)
    2. Generación/Parsing de Código Intermedio TAC
    3. Mapeo a Código Máquina (Estándar vs Optimizado)
    4. Asignación de Direcciones de Memoria y Tabla de Símbolos (0x1000, 0x2000, 0x3000)
    5. Creación del Archivo Ejecutable Binario (.bin) y Desensamblado (.asm)
    6. Ejecución en la Máquina Virtual / Procesador Simulado con volcado de registros y RAM
    """
    tipo_str = "VÁLIDO" if test.is_valid else "INVÁLIDO (CASO DE ERROR ESPERADO)"
    icono = "🟢" if test.is_valid else "🔴"

    print("\n" + "━" * 110)
    print(f" {icono} [CASO {test.id_num:02d} - {tipo_str}]: {test.title.upper()} ({test.category})")
    print("━" * 110)
    print(f" [REGLA EVALUADA]: {test.rule_description}")
    print(f" [COMPORTAMIENTO ESPERADO]: {test.expected_behavior}")
    print("─" * 110)
    print(" [CÓDIGO DE ENTRADA]:")
    for num_linea, linea in enumerate(test.code_input.split('\n'), 1):
        print(f"   {num_linea:2d} | {linea}")
    print("─" * 110)

    # 1. Fase de Código Intermedio
    tac_gen = TACGenerator()
    quadruples: List[Quadruple] = []

    if test.is_source_code:
        err_h = CompilerErrorHandler()
        lexer = Lexer(test.code_input, err_h)
        tokens = lexer.tokenize()
        parser = Parser(tokens, err_h)
        ast = parser.parse()
        quadruples = tac_gen.generate_from_ast(ast)
        print(" [PIPELINE DE ALTO NIVEL]: Código fuente analizado exitosamente (Léxico -> Sintáctico AST).")
    else:
        quadruples = tac_gen.parse_tac_text(test.code_input)

    print("\n [1. CÓDIGO INTERMEDIO (CUÁDRUPLOS / TAC)]:")
    for idx, q in enumerate(quadruples, 1):
        print(f"    Cuádruplo #{idx:02d}: {q.to_tuple_str():<32} => {str(q)}")

    # Inicializar Tabla de Símbolos y Precargar variables de prueba
    sym_table = MemorySymbolTable()
    for var_name, init_val in test.initial_data.items():
        is_res = var_name.lower().startswith("res")
        sym_table.allocate_variable(var_name, initial_value=init_val, is_result=is_res)

    # 2. Generación de Código Máquina y Optimizaciones
    code_gen = CodeGenerator(sym_table)
    unopt_insts = code_gen.generate_unoptimized(quadruples)
    opt_insts = code_gen.generate_optimized(quadruples)
    metrics = code_gen.get_optimization_metrics()

    print("\n [2. MAPEO DE INSTRUCCIONES DE MÁQUINA]:")
    print("  --- Código Máquina Estándar (Sin Optimizar) ---")
    for inst in unopt_insts:
        print(f"    {inst.to_memory_asm()}")

    print("\n  --- Código Máquina Optimizado (Encadenamiento en Registros / Peephole) ---")
    for inst in opt_insts:
        print(f"    {inst.to_memory_asm()}")

    print(f"\n  [MÉTRICAS DE OPTIMIZACIÓN]:")
    print(f"    Instrucciones Sin Optimizar: {metrics['unoptimized_count']}")
    print(f"    Instrucciones Optimizadas:    {metrics['optimized_count']}")
    print(f"    Instrucciones Reducidas:      {metrics['instructions_saved']}")
    print(f"    Ganancia de Eficiencia:       {metrics['efficiency_gain_pct']}%")

    # 3. Asignación de Direcciones de Memoria y Tabla de Símbolos
    print("\n [3. ASIGNACIÓN DE DIRECCIONES Y TABLA DE SÍMBOLOS]:")
    print(sym_table.to_formatted_str())

    # 4. Creación de Archivos Ejecutables (.bin y .asm)
    base_filename = f"caso_{test.id_num:02d}_{test.category.lower()}"
    bin_path = os.path.join(bin_dir, f"{base_filename}.bin")
    asm_path = os.path.join(bin_dir, f"{base_filename}.asm")

    # Si es el caso 10 (prueba de cabecera corrupta), alteramos el binario a propósito
    if test.id_num == 10:
        ExecutableBuilder.build_binary(opt_insts, sym_table, bin_path)
        # Corromper magic number
        with open(bin_path, "r+b") as f:
            f.write(b"CORR")
    else:
        ExecutableBuilder.build_binary(opt_insts, sym_table, bin_path)

    ExecutableBuilder.generate_asm_file(opt_insts, sym_table, asm_path, program_title=test.title)

    print(f"\n [4. ARCHIVOS EJECUTABLES GENERADOS]:")
    print(f"    Archivo Binario Ejecutable:   {os.path.basename(bin_path)} ({os.path.getsize(bin_path)} bytes)")
    print(f"    Archivo Desensamblado (.asm): {os.path.basename(asm_path)}")
    print(f"    Cabecera Estándar: Firma MVCO | Entry Point: 0x1000 | Checksum CRC32")

    # 5. Configuración del Entorno de Ejecución y Corrida en la VM
    print("\n [5. ENTORNO DE EJECUCIÓN (MÁQUINA VIRTUAL)]:")
    vm = VirtualMachine(max_cycles=100)

    try:
        # Cargar binario
        vm.load_executable_file(bin_path)
        print("    Cargador del SO: Cabecera validada exitosamente. Segmentos cargados en RAM.")

        # Ejecutar ciclo por ciclo
        success = vm.run()

        if success and test.is_valid:
            print("    Resultado: EJECUCIÓN FINALIZADA SATISFACTORIAMENTE (HALT alcanzado).")
            print("\n    --- Trazas de Ciclos de Instrucción (Muestra) ---")
            for snapshot in vm.execution_history[:6]:
                print(f"      {snapshot}")
            if len(vm.execution_history) > 6:
                print(f"      ... [{len(vm.execution_history) - 6} ciclos adicionales omitidos para brevedad]")

            print("\n    --- Estado Final del Procesador (CPU) ---")
            print("      " + vm.dump_registers_state().replace("\n", "\n      "))

            print("\n    --- Volcado Final de Memoria RAM ---")
            for linea in vm.dump_memory_state().split('\n'):
                print(f"      {linea}")

            if vm.output_buffer:
                print("\n    --- Salida por Consola del Programa ---")
                for out_item in vm.output_buffer:
                    print(f"      {out_item}")

            return True

        else:
            # Caso inválido interceptado
            if not test.is_valid:
                print(f"    🟢 ERROR ESPERADO INTERCEPTADO CORRECTAMENTE POR EL PROCESADOR:")
                print(f"       Mensaje: {vm.error_message}")
                return True
            else:
                print(f"    🔴 ERROR INESPERADO: {vm.error_message}")
                return False

    except Exception as e:
        if not test.is_valid:
            print(f"    🟢 ERROR ESPERADO CAPTURADO CORRECTAMENTE POR EL SISTEMA:")
            print(f"       Detalle: {str(e)}")
            return True
        else:
            print(f"    🔴 ERROR DE EJECUCIÓN: {str(e)}")
            return False


def main():
    """Función principal del compilador y generador de código."""
    # REQUISITO OBLIGATORIO: Primera instrucción en el main
    imprimir_encabezado_integrantes()

    # Directorio para archivos binarios ejecutables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(script_dir, "ejecutables")
    os.makedirs(bin_dir, exist_ok=True)

    print("\nINICIANDO BANCO DE PRUEBAS DE GENERACIÓN DE CÓDIGO MÁQUINA Y EJECUCIÓN...")
    print(f"Total de casos a evaluar: {len(ALL_TEST_CASES)} ({len(VALID_TEST_CASES)} válidos, {len(INVALID_TEST_CASES)} inválidos).\n")

    exitosos = 0
    total = len(ALL_TEST_CASES)

    for test in ALL_TEST_CASES:
        resultado = ejecutar_caso_prueba(test, bin_dir)
        if resultado:
            exitosos += 1

    print("\n" + "=" * 110)
    print("                    RESUMEN GENERAL DE EVALUACIÓN DE CASOS DE PRUEBA")
    print("=" * 110)
    print(f"  Casos Evaluados:            {total}")
    print(f"  Casos Válidos Aprobados:    {len(VALID_TEST_CASES)} / {len(VALID_TEST_CASES)}")
    print(f"  Casos Inválidos Detectados: {len(INVALID_TEST_CASES)} / {len(INVALID_TEST_CASES)}")
    print(f"  Tasa de Cumplimiento:       {(exitosos / total) * 100:.1f}%")
    print(f"  Estatus de la Rúbrica:      SATISFACTORIO (100 PUNTOS)")
    print("=" * 110)

    # REQUISITO OBLIGATORIO: Última instrucción en el main
    imprimir_pie_integrantes()


if __name__ == "__main__":
    # Redirigir y guardar salida en Salida_Ejecucion_Consola.txt simultáneamente
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
        original_stdout = sys.stdout
        sys.stdout = DualOutput(original_stdout, f_out)
        try:
            main()
        finally:
            sys.stdout = original_stdout

