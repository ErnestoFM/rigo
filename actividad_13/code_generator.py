"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - MAPEO DE INSTRUCCIONES Y OPTIMIZACIÓN
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Dict, Optional, Tuple, Any
from intermediate_code import Quadruple
from symbol_table_mem import MemorySymbolTable, MemorySymbol


class MachineInstruction:
    """
    Representa una instrucción de código máquina con dirección física (0x1000...),
    nemónico, operandos simbólicos y físicos, y comentario descriptivo.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        opcode: str,
        operands: Optional[List[str]] = None,
        address: int = 0,
        comment: str = "",
        symbolic_operands: Optional[List[str]] = None
    ):
        self.opcode = opcode.upper()
        self.operands = operands or []
        self.address = address
        self.comment = comment
        self.symbolic_operands = symbolic_operands or list(self.operands)

    @property
    def hex_address(self) -> str:
        return f"0x{self.address:04X}"

    def to_symbolic_asm(self) -> str:
        """Formato con nombres de variables (como en la Sección 1 de la rúbrica)."""
        ops_str = ", ".join(self.symbolic_operands)
        line = f"{self.opcode:<6} {ops_str:<18}"
        if self.comment:
            line = f"{line:<26} # {self.comment}"
        return line

    def to_memory_asm(self) -> str:
        """Formato con direcciones físicas (como en la Sección 2 de la rúbrica)."""
        ops_str = ", ".join(self.operands)
        inst_str = f"{self.opcode:<6} {ops_str:<16}"
        line = f"{self.hex_address}: {inst_str}"
        if self.comment:
            line = f"{line:<32} # {self.comment}"
        return line

    def __str__(self) -> str:
        return self.to_memory_asm()


class CodeOptimizer:
    """
    Optimizador de código máquina. Aplica:
    1. Reutilización y encadenamiento de registros (evita temporales y cargas/descargas intermedias).
    2. Optimización de Mirilla (Peephole) para eliminar instrucciones redundantes (STORE seguido de LOAD).
    3. Eliminación de operaciones neutras y código inútil.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    @staticmethod
    def optimize_chaining(quadruples: List[Quadruple]) -> List[Quadruple]:
        """
        Aplica encadenamiento en el código intermedio para reducir el número de cuádruplos
        cuando hay operaciones sucesivas como:
            t1 = a + b
            t2 = t1 * c
            result = t2
        """
        optimized: List[Quadruple] = []
        temp_map: Dict[str, str] = {}  # t1 -> expresión acumulada

        for q in quadruples:
            if q.op in ("+", "-", "*", "/", "%"):
                # Si arg1 es un temporal previo
                arg1 = temp_map.get(q.arg1, q.arg1)
                optimized.append(Quadruple(q.op, arg1, q.arg2, q.result))
            elif q.op == "=" and q.arg1 in temp_map:
                optimized.append(Quadruple("=", temp_map[q.arg1], None, q.result))
            else:
                optimized.append(q)

        return optimized

    @staticmethod
    def peephole_optimize(instructions: List[MachineInstruction]) -> List[MachineInstruction]:
        """
        Optimización de mirilla a nivel de instrucciones de máquina:
        - Elimina pares STORE [addr], R1 inmediatamente seguidos de LOAD R1, [addr].
        - Elimina operaciones algebraicas neutras (ADD R1, 0 o MUL R1, 1).
        """
        if not instructions:
            return []

        cleaned: List[MachineInstruction] = []
        i = 0
        while i < len(instructions):
            current = instructions[i]

            # 1. Regla: STORE [addr], Rx seguido de LOAD Rx, [addr]
            if i + 1 < len(instructions):
                nxt = instructions[i + 1]
                if (current.opcode == "STORE" and nxt.opcode == "LOAD" and
                    len(current.operands) == 2 and len(nxt.operands) == 2):
                    addr_store, reg_store = current.operands[0], current.operands[1]
                    reg_load, addr_load = nxt.operands[0], nxt.operands[1]
                    if addr_store == addr_load and reg_store == reg_load:
                        # Mantener el STORE pero eliminar el LOAD redundante
                        cleaned.append(current)
                        i += 2
                        continue

            # 2. Operaciones algebraicas neutras
            if current.opcode == "ADD" and len(current.operands) == 2 and current.operands[1] in ("0", "#0"):
                i += 1
                continue
            if current.opcode == "MUL" and len(current.operands) == 2 and current.operands[1] in ("1", "#1"):
                i += 1
                continue

            cleaned.append(current)
            i += 1

        return cleaned


class CodeGenerator:
    """
    Generador de Código Máquina y Asignador de Direcciones Físicas.
    Convierte cuádruplos de código intermedio en instrucciones de máquina,
    asigna direcciones de memoria y permite generar tanto la versión estándar
    (sin optimizar) como la versión optimizada con métricas de comparación.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, symbol_table: Optional[MemorySymbolTable] = None):
        self.symbol_table = symbol_table or MemorySymbolTable()
        self.unoptimized_instructions: List[MachineInstruction] = []
        self.optimized_instructions: List[MachineInstruction] = []
        self.default_reg = "R1"

    def _resolve_operand(self, op_val: str, is_target: bool = False) -> Tuple[str, str]:
        """
        Retorna la representación de dirección física (hex) y simbólica.
        Si es número literal, retorna '#' + valor.
        Si es variable, garantiza asignación en la tabla de símbolos.
        """
        if op_val is None:
            return "", ""

        # Número literal
        if op_val.lstrip('-').replace('.', '', 1).isdigit():
            return f"#{op_val}", op_val

        # Registro
        if op_val.upper().startswith("R") and len(op_val) <= 3 and op_val[1:].isdigit():
            return op_val.upper(), op_val.upper()

        # Variable o Temporal
        sym = self.symbol_table.allocate_variable(op_val, is_result=is_target)
        return sym.hex_address, op_val

    def generate_unoptimized(self, quadruples: List[Quadruple]) -> List[MachineInstruction]:
        """
        Genera código máquina estándar directo sin optimizaciones (traducción 1 a 1 de cuádruplos).
        """
        instructions: List[MachineInstruction] = []
        label_positions: Dict[str, int] = {}

        for q in quadruples:
            if q.op == "LABEL":
                # Marcar posición de etiqueta
                label_positions[q.result] = len(instructions)
                continue

            elif q.op in ("+", "-", "*", "/", "%"):
                # t = a op b
                addr1, sym1 = self._resolve_operand(q.arg1)
                addr2, sym2 = self._resolve_operand(q.arg2)
                addr_res, sym_res = self._resolve_operand(q.result)

                op_name = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}[q.op]
                verb = {"+": "Sumen el valor de", "-": "Resten el valor de", "*": "Multipliquen por", "/": "Dividan entre", "%": "Módulo con"}[q.op]

                # 1. LOAD R1, a
                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr1],
                    comment=f"Carguen el valor de {sym1} en el registro {self.default_reg}",
                    symbolic_operands=[self.default_reg, sym1]
                ))
                # 2. OP R1, b
                instructions.append(MachineInstruction(
                    opcode=op_name,
                    operands=[self.default_reg, addr2],
                    comment=f"{verb} {sym2} al registro {self.default_reg}",
                    symbolic_operands=[self.default_reg, sym2]
                ))
                # 3. STORE t, R1
                instructions.append(MachineInstruction(
                    opcode="STORE",
                    operands=[addr_res, self.default_reg],
                    comment=f"Almacenen el resultado temporal en {sym_res}",
                    symbolic_operands=[sym_res, self.default_reg]
                ))

            elif q.op == "=":
                addr_src, sym_src = self._resolve_operand(q.arg1)
                addr_dst, sym_dst = self._resolve_operand(q.result, is_target=True)

                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr_src],
                    comment=f"Carguen {sym_src} en {self.default_reg}",
                    symbolic_operands=[self.default_reg, sym_src]
                ))
                instructions.append(MachineInstruction(
                    opcode="STORE",
                    operands=[addr_dst, self.default_reg],
                    comment=f"Almacenen en {sym_dst}",
                    symbolic_operands=[sym_dst, self.default_reg]
                ))

            elif q.op.startswith("IF_"):
                # Salto condicional
                addr1, sym1 = self._resolve_operand(q.arg1)
                addr2, sym2 = self._resolve_operand(q.arg2) if q.arg2 else ("#0", "0")

                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr1],
                    comment=f"Carguen {sym1} para comparar",
                    symbolic_operands=[self.default_reg, sym1]
                ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, addr2],
                    comment=f"Comparen {self.default_reg} con {sym2}",
                    symbolic_operands=[self.default_reg, sym2]
                ))

                jump_map = {
                    "IF_GT": "JGT", "IF_LT": "JLT", "IF_GE": "JGE",
                    "IF_LE": "JLE", "IF_EQ": "JZ", "IF_NE": "JNZ", "IF_GOTO": "JNZ"
                }
                jump_op = jump_map.get(q.op, "JNZ")
                instructions.append(MachineInstruction(
                    opcode=jump_op,
                    operands=[q.result],  # Será resuelto a dirección de memoria después
                    comment=f"Salto condicional a {q.result}",
                    symbolic_operands=[q.result]
                ))

            elif q.op == "GOTO":
                instructions.append(MachineInstruction(
                    opcode="JMP",
                    operands=[q.result],
                    comment=f"Salto incondicional a {q.result}",
                    symbolic_operands=[q.result]
                ))

            elif q.op == "PRINT":
                addr, sym = self._resolve_operand(q.arg1)
                instructions.append(MachineInstruction(
                    opcode="PRINT",
                    operands=[addr],
                    comment=f"Imprimir el valor de {sym}",
                    symbolic_operands=[sym]
                ))

            elif q.op == "HALT":
                instructions.append(MachineInstruction(
                    opcode="HALT",
                    operands=[],
                    comment="Fin de ejecución del programa",
                    symbolic_operands=[]
                ))

        # Agregar HALT si no existe
        if not instructions or instructions[-1].opcode != "HALT":
            instructions.append(MachineInstruction(opcode="HALT", operands=[], comment="Fin de ejecución", symbolic_operands=[]))

        # Asignar direcciones físicas de código (0x1000, 0x1004, ...) y resolver etiquetas
        self._assign_addresses_and_labels(instructions, label_positions)
        self.unoptimized_instructions = instructions
        return instructions

    def generate_optimized(self, quadruples: List[Quadruple]) -> List[MachineInstruction]:
        """
        Genera código máquina con encadenamiento de registros, eliminación de temporales
        y optimización de mirilla (peephole), idéntico al modelo solicitado por el profesor.
        """
        instructions: List[MachineInstruction] = []
        label_positions: Dict[str, int] = {}
        reg_holds: Optional[str] = None  # Qué variable/temporal reside en R1 actualmente

        i = 0
        while i < len(quadruples):
            q = quadruples[i]

            if q.op == "LABEL":
                label_positions[q.result] = len(instructions)
                reg_holds = None
                i += 1
                continue

            elif q.op in ("+", "-", "*", "/", "%"):
                # Detectar si podemos encadenar en R1 directamente
                addr1, sym1 = self._resolve_operand(q.arg1)
                addr2, sym2 = self._resolve_operand(q.arg2)
                addr_res, sym_res = self._resolve_operand(q.result)

                op_name = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}[q.op]
                verb = {"+": "Sumen", "-": "Resten", "*": "Multipliquen por", "/": "Dividan entre", "%": "Módulo con"}[q.op]

                # Si el primer operando ya está cargado en R1, no volvemos a emitir LOAD R1
                if reg_holds == sym1:
                    instructions.append(MachineInstruction(
                        opcode=op_name,
                        operands=[self.default_reg, addr2],
                        comment=f"{verb} {sym2} a {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))
                else:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Carguen el valor de {sym1} en {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                    instructions.append(MachineInstruction(
                        opcode=op_name,
                        operands=[self.default_reg, addr2],
                        comment=f"{verb} el valor de {sym2} al registro {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))

                # Registrar que R1 ahora contiene el resultado q.result
                reg_holds = q.result

                # Revisar si la siguiente instrucción es una asignación final: result = q.result
                if i + 1 < len(quadruples) and quadruples[i + 1].op == "=" and quadruples[i + 1].arg1 == q.result:
                    next_q = quadruples[i + 1]
                    addr_final, sym_final = self._resolve_operand(next_q.result, is_target=True)
                    instructions.append(MachineInstruction(
                        opcode="STORE",
                        operands=[addr_final, self.default_reg],
                        comment=f"Almacenen el resultado en {sym_final}",
                        symbolic_operands=[sym_final, self.default_reg]
                    ))
                    reg_holds = sym_final
                    i += 2  # Consumir ambas instrucciones de una vez
                    continue
                elif not (q.result.startswith("t") and q.result[1:].isdigit()):
                    # Si el resultado es una variable real del usuario (acum, contador), persistir en RAM
                    instructions.append(MachineInstruction(
                        opcode="STORE",
                        operands=[addr_res, self.default_reg],
                        comment=f"Almacenen el resultado en {sym_res}",
                        symbolic_operands=[sym_res, self.default_reg]
                    ))
                    reg_holds = sym_res

            elif q.op == "=":
                addr_src, sym_src = self._resolve_operand(q.arg1)
                addr_dst, sym_dst = self._resolve_operand(q.result, is_target=True)

                if reg_holds != sym_src:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr_src],
                        comment=f"Carguen {sym_src} en {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym_src]
                    ))
                instructions.append(MachineInstruction(
                    opcode="STORE",
                    operands=[addr_dst, self.default_reg],
                    comment=f"Almacenen en {sym_dst}",
                    symbolic_operands=[sym_dst, self.default_reg]
                ))
                reg_holds = sym_dst

            elif q.op.startswith("IF_"):
                addr1, sym1 = self._resolve_operand(q.arg1)
                addr2, sym2 = self._resolve_operand(q.arg2) if q.arg2 else ("#0", "0")

                if reg_holds != sym1:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Carguen {sym1} para comparar",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, addr2],
                    comment=f"Comparen {self.default_reg} con {sym2}",
                    symbolic_operands=[self.default_reg, sym2]
                ))

                jump_map = {
                    "IF_GT": "JGT", "IF_LT": "JLT", "IF_GE": "JGE",
                    "IF_LE": "JLE", "IF_EQ": "JZ", "IF_NE": "JNZ", "IF_GOTO": "JNZ"
                }
                jump_op = jump_map.get(q.op, "JNZ")
                instructions.append(MachineInstruction(
                    opcode=jump_op,
                    operands=[q.result],
                    comment=f"Salto condicional a {q.result}",
                    symbolic_operands=[q.result]
                ))
                reg_holds = None

            elif q.op == "GOTO":
                instructions.append(MachineInstruction(
                    opcode="JMP",
                    operands=[q.result],
                    comment=f"Salto incondicional a {q.result}",
                    symbolic_operands=[q.result]
                ))
                reg_holds = None

            elif q.op == "PRINT":
                addr, sym = self._resolve_operand(q.arg1)
                instructions.append(MachineInstruction(
                    opcode="PRINT",
                    operands=[addr],
                    comment=f"Imprimir {sym}",
                    symbolic_operands=[sym]
                ))

            elif q.op == "HALT":
                instructions.append(MachineInstruction(opcode="HALT", operands=[], comment="Fin de ejecución", symbolic_operands=[]))
                reg_holds = None

            i += 1

        if not instructions or instructions[-1].opcode != "HALT":
            instructions.append(MachineInstruction(opcode="HALT", operands=[], comment="Fin de ejecución", symbolic_operands=[]))

        # Pasada 2: Optimización de mirilla
        instructions = CodeOptimizer.peephole_optimize(instructions)

        # Asignar direcciones físicas y resolver etiquetas
        self._assign_addresses_and_labels(instructions, label_positions)
        self.optimized_instructions = instructions
        return instructions

    def _assign_addresses_and_labels(self, instructions: List[MachineInstruction], label_positions: Dict[str, int]):
        """Asigna direcciones hex de 4 bytes a cada instrucción y resuelve etiquetas."""
        current_addr = self.symbol_table.code_base

        # Paso 1: Asignar dirección a cada instrucción
        addr_map: Dict[int, int] = {}
        for idx, inst in enumerate(instructions):
            inst.address = current_addr
            addr_map[idx] = current_addr
            current_addr += 4

        # Registrar etiquetas en la tabla de símbolos
        for lbl_name, inst_idx in label_positions.items():
            target_addr = addr_map.get(inst_idx, current_addr)
            self.symbol_table.register_label(lbl_name, target_addr)

        # Paso 2: Reemplazar nombres de etiquetas en operandos de saltos con su dirección hex
        for inst in instructions:
            if inst.opcode in ("JMP", "JZ", "JNZ", "JGT", "JLT", "JGE", "JLE"):
                if inst.operands:
                    target_lbl = inst.operands[0]
                    resolved_addr = self.symbol_table.get_address(target_lbl)
                    if resolved_addr is not None:
                        inst.operands[0] = f"0x{resolved_addr:04X}"
                    elif target_lbl.startswith("0x"):
                        pass
                    else:
                        # Si no se encuentra la etiqueta, se marca como no resuelta para pruebas de error
                        pass

    def get_optimization_metrics(self) -> Dict[str, Any]:
        """Calcula métricas de reducción y eficiencia entre la versión estándar y optimizada."""
        unopt_count = len(self.unoptimized_instructions)
        opt_count = len(self.optimized_instructions)
        reduction = unopt_count - opt_count
        pct = (reduction / unopt_count * 100) if unopt_count > 0 else 0.0

        return {
            "unoptimized_count": unopt_count,
            "optimized_count": opt_count,
            "instructions_saved": max(0, reduction),
            "efficiency_gain_pct": round(pct, 2)
        }
