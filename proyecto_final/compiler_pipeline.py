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

from typing import List, Dict, Optional, Any
from token_type import Token
from error_handler import CompilerError, CompilerErrorHandler
from lexer import Lexer
from ast_nodes import ProgramNode
from parser import Parser
from symbol_table import SymbolTable, Symbol
from semantic_analyzer import SemanticAnalyzer
from tac_instruction import TACInstruction
from tac_generator import TACGenerator
from optimizer import TACOptimizer
from code_generator import CodeGenerator, MachineInstruction
from virtual_machine import VirtualMachine, VMState


class CompilationResult:
    """
    Contenedor exhaustivo de resultados y artefactos de todas las fases de compilación.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.success = False
        self.error_stage: Optional[str] = None
        self.errors: List[CompilerError] = []
        self.tokens: List[Token] = []
        self.ast: Optional[ProgramNode] = None
        self.ast_tree_str: str = ""
        self.symbol_table: SymbolTable = SymbolTable()
        self.symbols_list: List[Symbol] = []
        self.tac_unoptimized: List[TACInstruction] = []
        self.tac_optimized: List[TACInstruction] = []
        self.optimization_log: List[str] = []
        self.machine_code_unopt: List[MachineInstruction] = []
        self.machine_code_opt: List[MachineInstruction] = []
        self.code_metrics: Dict[str, Any] = {}
        self.vm_output: List[str] = []
        self.vm_history: List[VMState] = []
        self.vm_memory_dump: str = ""
        self.vm_registers_dump: str = ""
        self.execution_error: Optional[str] = None


class CompilerPipeline:
    """
    Pipeline orquestador completo del compilador:
    Léxico -> Sintáctico -> Semántico -> TAC -> Optimización TAC -> Generación Código -> VM.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        pass

    @classmethod
    def compile_and_run(cls, source_code: str) -> CompilationResult:
        result = CompilationResult(source_code)
        error_handler = CompilerErrorHandler()

        # =========================================================================
        # FASE 1: ANÁLISIS LÉXICO
        # =========================================================================
        lexer = Lexer(source_code, error_handler)
        result.tokens = lexer.tokenize()

        if error_handler.has_errors:
            result.success = False
            result.error_stage = "LÉXICO"
            result.errors = error_handler.get_errors()
            return result

        # =========================================================================
        # FASE 2: ANÁLISIS SINTÁCTICO
        # =========================================================================
        parser = Parser(result.tokens, error_handler)
        result.ast = parser.parse_program()

        if error_handler.has_errors or result.ast is None:
            result.success = False
            result.error_stage = "SINTÁCTICO"
            result.errors = error_handler.get_errors()
            return result

        result.ast_tree_str = result.ast.to_tree_str()

        # =========================================================================
        # FASE 3: ANÁLISIS SEMÁNTICO
        # =========================================================================
        semantic = SemanticAnalyzer(error_handler)
        semantic.analyze(result.ast)
        result.symbol_table = semantic.symbol_table
        result.symbols_list = result.symbol_table.get_all_symbols()

        if error_handler.has_errors:
            result.success = False
            result.error_stage = "SEMÁNTICO"
            result.errors = error_handler.get_errors()
            return result

        # =========================================================================
        # FASE 4: CÓDIGO INTERMEDIO (TAC)
        # =========================================================================
        tac_gen = TACGenerator(result.symbol_table)
        result.tac_unoptimized = tac_gen.generate(result.ast)

        # =========================================================================
        # FASE 5: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO
        # =========================================================================
        optimizer = TACOptimizer()
        result.tac_optimized = optimizer.optimize(result.tac_unoptimized)
        result.optimization_log = optimizer.optimization_log

        # =========================================================================
        # FASE 6: GENERACIÓN DE CÓDIGO MÁQUINA / ENSAMBLADOR
        # =========================================================================
        code_gen = CodeGenerator(result.symbol_table)
        result.machine_code_unopt = code_gen.generate_unoptimized(result.tac_unoptimized)
        result.machine_code_opt = code_gen.generate_optimized(result.tac_optimized)
        result.code_metrics = code_gen.get_optimization_metrics()

        # =========================================================================
        # FASE 7: ENTORNO DE EJECUCIÓN (MÁQUINA VIRTUAL)
        # =========================================================================
        vm = VirtualMachine(max_cycles=3000)

        # Cargar valores iniciales de variables
        initial_data: Dict[int, int] = {}
        symbol_names: Dict[str, int] = {}
        for sym in result.symbols_list:
            if sym.address is not None:
                symbol_names[sym.name] = sym.address
                if sym.value is not None and isinstance(sym.value, (int, float, bool)):
                    initial_data[sym.address] = int(sym.value)

        # También incluir mapeo de temporales
        for sym_name, addr in code_gen.symbol_memory_map.items():
            symbol_names[sym_name] = addr

        # Ejecutamos las instrucciones optimizadas en la VM
        vm.load_from_memory_structures(
            instructions=result.machine_code_opt,
            initial_data=initial_data,
            symbol_names=symbol_names,
            entry_point=0x1000
        )

        exec_success = vm.run()
        result.vm_output = list(vm.output_buffer)
        result.vm_history = list(vm.execution_history)
        result.vm_memory_dump = vm.dump_memory_state()
        result.vm_registers_dump = vm.dump_registers_state()
        result.execution_error = vm.error_message

        result.success = exec_success
        if not exec_success and vm.error_message:
            result.error_stage = "EJECUCIÓN VM"

        return result
