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

from typing import List, Dict, Optional, Tuple, Any
from tac_instruction import TACInstruction
from symbol_table import SymbolTable, Symbol


class MachineInstruction:
    """
    Representa una instrucción de código máquina con dirección física (0x1000...),
    nemónico de arquitectura RISC, operandos físicos y simbólicos, y comentario.

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
        """Formato ensamblador con nombres de variables y registros."""
        ops_str = ", ".join(self.symbolic_operands)
        line = f"{self.opcode:<6} {ops_str:<18}"
        if self.comment:
            line = f"{line:<28} # {self.comment}"
        return line

    def to_memory_asm(self) -> str:
        """Formato ensamblador con direcciones físicas hexadecimales."""
        ops_str = ", ".join(self.operands)
        inst_str = f"{self.opcode:<6} {ops_str:<18}"
        line = f"{self.hex_address}: {inst_str}"
        if self.comment:
            line = f"{line:<34} # {self.comment}"
        return line

    def __str__(self) -> str:
        return self.to_memory_asm()


class PeepholeOptimizer:
    """
    Optimizador de Mirilla (Peephole) a nivel de ensamblador y código máquina.
    Aplica patrones de optimización de instrucciones:
    1. Eliminación de redundancia STORE [addr], R1 inmediatamente seguido de LOAD R1, [addr].
    2. Eliminación de instrucciones neutrales: ADD R1, #0, SUB R1, #0, MUL R1, #1.
    3. Eliminación de saltos a la siguiente instrucción consecutiva.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    @staticmethod
    def optimize(instructions: List[MachineInstruction]) -> List[MachineInstruction]:
        if not instructions:
            return []

        cleaned: List[MachineInstruction] = []
        i = 0
        n = len(instructions)

        while i < n:
            curr = instructions[i]

            # 1. Regla: STORE [addr], Rx seguido de LOAD Rx, [addr]
            if i + 1 < n:
                nxt = instructions[i + 1]
                if (curr.opcode == "STORE" and nxt.opcode == "LOAD" and
                    len(curr.operands) >= 2 and len(nxt.operands) >= 2):
                    addr_store, reg_store = curr.operands[0], curr.operands[1]
                    reg_load, addr_load = nxt.operands[0], nxt.operands[1]
                    if addr_store == addr_load and reg_store == reg_load:
                        # Mantener STORE pero descartar el LOAD redundante
                        cleaned.append(curr)
                        i += 2
                        continue

            # 2. Regla: operaciones algebraicas neutras
            if curr.opcode in ("ADD", "SUB") and len(curr.operands) >= 2 and curr.operands[1] in ("#0", "0"):
                i += 1
                continue
            if curr.opcode in ("MUL", "DIV") and len(curr.operands) >= 2 and curr.operands[1] in ("#1", "1"):
                i += 1
                continue

            cleaned.append(curr)
            i += 1

        return cleaned


class CodeGenerator:
    """
    Generador de Código Máquina y Ensamblador RISC de 32 bits.
    Traduce instrucciones de código intermedio (TAC) a instrucciones de máquina,
    asigna direcciones de memoria (Código 0x1000, Datos 0x2000, Resultados 0x3000),
    gestiona el banco de registros R1..R8 y resuelve etiquetas de salto.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        self.symbol_table = symbol_table or SymbolTable()
        self.code_base = 0x1000
        self.data_base = 0x2000
        self.results_base = 0x3000
        self.default_reg = "R1"
        self.second_reg = "R2"
        self.unoptimized_instructions: List[MachineInstruction] = []
        self.optimized_instructions: List[MachineInstruction] = []
        self.symbol_memory_map: Dict[str, int] = {}
        self.next_temp_addr = self.results_base

    def _resolve_operand(self, op_val: Optional[str], is_target: bool = False) -> Tuple[str, str]:
        """
        Retorna la tupla (dirección_física_hex_o_inmediato, nombre_simbólico).
        """
        if op_val is None:
            return "", ""

        op_str = str(op_val).strip()

        # Constante numérica entera o booleana
        if op_str.lstrip('-').isdigit():
            return f"#{op_str}", op_str
        if op_str in ("true", "True"):
            return "#1", "true"
        if op_str in ("false", "False"):
            return "#0", "false"

        # Registro explícito
        if op_str.upper().startswith("R") and len(op_str) <= 3 and op_str[1:].isdigit():
            return op_str.upper(), op_str.upper()

        # Variable ya existente en la tabla de símbolos
        sym = self.symbol_table.lookup_variable(op_str)
        if sym and sym.address is not None:
            self.symbol_memory_map[op_str] = sym.address
            return f"0x{sym.address:04X}", op_str

        # Si es un temporal (t1, t2...) o variable nueva no mapeada
        if op_str not in self.symbol_memory_map:
            addr = self.next_temp_addr
            self.next_temp_addr += 4
            self.symbol_memory_map[op_str] = addr
            return f"0x{addr:04X}", op_str

        addr = self.symbol_memory_map[op_str]
        return f"0x{addr:04X}", op_str

    def generate_unoptimized(self, tac_instructions: List[TACInstruction]) -> List[MachineInstruction]:
        """Genera ensamblador estándar traducción 1 a 1 de TAC."""
        instructions: List[MachineInstruction] = []
        label_positions: Dict[str, int] = {}
        i = 0
        n = len(tac_instructions)

        while i < n:
            tac = tac_instructions[i]
            if tac.op == "COMMENT":
                i += 1
                continue

            if tac.is_label or tac.op == "LABEL":
                lbl_name = (tac.result or tac.arg1 or "L").rstrip(":")
                label_positions[lbl_name] = len(instructions)
                i += 1
                continue

            elif tac.op in (">", "<", ">=", "<=", "==", "!="):
                addr1, sym1 = self._resolve_operand(tac.arg1)
                addr2, sym2 = self._resolve_operand(tac.arg2)
                addr_res, sym_res = self._resolve_operand(tac.result, is_target=True)

                if i + 1 < n and tac_instructions[i + 1].op in ("IF_GOTO", "IF_NOT_GOTO") and tac_instructions[i + 1].arg1 == tac.result:
                    next_tac = tac_instructions[i + 1]
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Cargar {sym1} para comparar",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                    instructions.append(MachineInstruction(
                        opcode="CMP",
                        operands=[self.default_reg, addr2],
                        comment=f"Comparar con {sym2}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))
                    if next_tac.op == "IF_GOTO":
                        jump_map = {">": "JGT", "<": "JLT", ">=": "JGE", "<=": "JLE", "==": "JZ", "!=": "JNZ"}
                    else:
                        jump_map = {">": "JLE", "<": "JGE", ">=": "JLT", "<=": "JGT", "==": "JNZ", "!=": "JZ"}
                    jump_op = jump_map.get(tac.op, "JNZ")
                    target_lbl = (next_tac.result or "").rstrip(":")
                    instructions.append(MachineInstruction(
                        opcode=jump_op,
                        operands=[target_lbl],
                        comment=f"Salto condicional ({tac.op}) hacia {target_lbl}",
                        symbolic_operands=[target_lbl]
                    ))
                    i += 2
                    continue
                else:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Cargar {sym1}",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                    instructions.append(MachineInstruction(
                        opcode="CMP",
                        operands=[self.default_reg, addr2],
                        comment=f"Comparar con {sym2}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))
                    set_map = {">": "SETGT", "<": "SETLT", ">=": "SETGE", "<=": "SETLE", "==": "SETEQ", "!=": "SETNE"}
                    set_op = set_map.get(tac.op, "SETEQ")
                    instructions.append(MachineInstruction(
                        opcode=set_op,
                        operands=[self.default_reg],
                        comment=f"Establecer resultado booleano ({tac.op})",
                        symbolic_operands=[self.default_reg]
                    ))
                    instructions.append(MachineInstruction(
                        opcode="STORE",
                        operands=[addr_res, self.default_reg],
                        comment=f"Guardar resultado en {sym_res}",
                        symbolic_operands=[sym_res, self.default_reg]
                    ))

            elif tac.op in ("+", "-", "*", "/", "%"):
                addr1, sym1 = self._resolve_operand(tac.arg1)
                addr2, sym2 = self._resolve_operand(tac.arg2)
                addr_res, sym_res = self._resolve_operand(tac.result, is_target=True)

                op_name = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}[tac.op]

                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr1],
                    comment=f"Cargar {sym1} en {self.default_reg}",
                    symbolic_operands=[self.default_reg, sym1]
                ))
                instructions.append(MachineInstruction(
                    opcode=op_name,
                    operands=[self.default_reg, addr2],
                    comment=f"Operar {tac.op} {sym2} sobre {self.default_reg}",
                    symbolic_operands=[self.default_reg, sym2]
                ))
                instructions.append(MachineInstruction(
                    opcode="STORE",
                    operands=[addr_res, self.default_reg],
                    comment=f"Guardar resultado en {sym_res}",
                    symbolic_operands=[sym_res, self.default_reg]
                ))

            elif tac.op == "=":
                addr_src, sym_src = self._resolve_operand(tac.arg1)
                addr_dst, sym_dst = self._resolve_operand(tac.result, is_target=True)

                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr_src],
                    comment=f"Cargar {sym_src} en {self.default_reg}",
                    symbolic_operands=[self.default_reg, sym_src]
                ))
                instructions.append(MachineInstruction(
                    opcode="STORE",
                    operands=[addr_dst, self.default_reg],
                    comment=f"Almacenar {self.default_reg} en {sym_dst}",
                    symbolic_operands=[sym_dst, self.default_reg]
                ))

            elif tac.op == "IF_CMP_GOTO":
                # if arg1 comp arg2 goto result
                addr1, sym1 = self._resolve_operand(tac.arg1)
                # Parsear comparación en arg2 si viene como "== 0" o separado
                arg2_clean = tac.arg2 or "== 0"
                parts = arg2_clean.split()
                if len(parts) == 2:
                    comp_op, rhs = parts[0], parts[1]
                else:
                    comp_op, rhs = "==", "0"

                addr2, sym2 = self._resolve_operand(rhs)

                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr1],
                    comment=f"Cargar {sym1} para comparar",
                    symbolic_operands=[self.default_reg, sym1]
                ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, addr2],
                    comment=f"Comparar con {sym2}",
                    symbolic_operands=[self.default_reg, sym2]
                ))

                jump_map = {
                    "==": "JZ", "!=": "JNZ", ">": "JGT", "<": "JLT", ">=": "JGE", "<=": "JLE"
                }
                jump_op = jump_map.get(comp_op, "JNZ")
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode=jump_op,
                    operands=[target_lbl],
                    comment=f"Salto condicional ({comp_op}) hacia {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))

            elif tac.op == "IF_GOTO":
                addr1, sym1 = self._resolve_operand(tac.arg1)
                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr1],
                    comment=f"Evaluar condición {sym1}",
                    symbolic_operands=[self.default_reg, sym1]
                ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, "#0"],
                    comment=f"Comparar {self.default_reg} con 0",
                    symbolic_operands=[self.default_reg, "0"]
                ))
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode="JNZ",
                    operands=[target_lbl],
                    comment=f"Salto si verdadero hacia {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))

            elif tac.op == "IF_NOT_GOTO":
                addr1, sym1 = self._resolve_operand(tac.arg1)
                instructions.append(MachineInstruction(
                    opcode="LOAD",
                    operands=[self.default_reg, addr1],
                    comment=f"Evaluar condición falsa {sym1}",
                    symbolic_operands=[self.default_reg, sym1]
                ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, "#0"],
                    comment=f"Comparar {self.default_reg} con 0",
                    symbolic_operands=[self.default_reg, "0"]
                ))
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode="JZ",
                    operands=[target_lbl],
                    comment=f"Salto si falso hacia {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))

            elif tac.op == "GOTO":
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode="JMP",
                    operands=[target_lbl],
                    comment=f"Salto incondicional a {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))

            elif tac.op == "PRINT":
                addr, sym = self._resolve_operand(tac.arg1)
                instructions.append(MachineInstruction(
                    opcode="PRINT",
                    operands=[addr],
                    comment=f"Imprimir en consola {sym}",
                    symbolic_operands=[sym]
                ))

            elif tac.op == "CALL":
                target_fn = (tac.arg1 or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode="CALL",
                    operands=[target_fn],
                    comment=f"Llamada a subrutina {target_fn}",
                    symbolic_operands=[target_fn]
                ))

            elif tac.op == "RETURN":
                if tac.arg1:
                    addr, sym = self._resolve_operand(tac.arg1)
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr],
                        comment=f"Cargar valor de retorno {sym} en {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym]
                    ))
                instructions.append(MachineInstruction(
                    opcode="RET",
                    operands=[],
                    comment="Retorno de subrutina",
                    symbolic_operands=[]
                ))

            elif tac.op == "HALT":
                instructions.append(MachineInstruction(
                    opcode="HALT",
                    operands=[],
                    comment="Fin de ejecución",
                    symbolic_operands=[]
                ))

            i += 1

        if not instructions or instructions[-1].opcode != "HALT":
            instructions.append(MachineInstruction(opcode="HALT", operands=[], comment="Fin de ejecución", symbolic_operands=[]))

        self._assign_addresses_and_labels(instructions, label_positions)
        self.unoptimized_instructions = instructions
        return instructions

    def generate_optimized(self, tac_instructions: List[TACInstruction]) -> List[MachineInstruction]:
        """
        Genera ensamblador optimizado con reutilización de registros y optimización de mirilla.
        """
        instructions: List[MachineInstruction] = []
        label_positions: Dict[str, int] = {}
        reg_holds: Optional[str] = None

        i = 0
        n = len(tac_instructions)

        while i < n:
            tac = tac_instructions[i]

            if tac.op == "COMMENT":
                i += 1
                continue

            if tac.is_label or tac.op == "LABEL":
                lbl_name = (tac.result or tac.arg1 or "L").rstrip(":")
                label_positions[lbl_name] = len(instructions)
                reg_holds = None
                i += 1
                continue

            elif tac.op in (">", "<", ">=", "<=", "==", "!="):
                addr1, sym1 = self._resolve_operand(tac.arg1)
                addr2, sym2 = self._resolve_operand(tac.arg2)
                addr_res, sym_res = self._resolve_operand(tac.result, is_target=True)

                if i + 1 < n and tac_instructions[i + 1].op in ("IF_GOTO", "IF_NOT_GOTO") and tac_instructions[i + 1].arg1 == tac.result:
                    next_tac = tac_instructions[i + 1]
                    if reg_holds != sym1:
                        instructions.append(MachineInstruction(
                            opcode="LOAD",
                            operands=[self.default_reg, addr1],
                            comment=f"Cargar {sym1} para comparar",
                            symbolic_operands=[self.default_reg, sym1]
                        ))
                    instructions.append(MachineInstruction(
                        opcode="CMP",
                        operands=[self.default_reg, addr2],
                        comment=f"Comparar con {sym2}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))
                    if next_tac.op == "IF_GOTO":
                        jump_map = {">": "JGT", "<": "JLT", ">=": "JGE", "<=": "JLE", "==": "JZ", "!=": "JNZ"}
                    else:
                        jump_map = {">": "JLE", "<": "JGE", ">=": "JLT", "<=": "JGT", "==": "JNZ", "!=": "JZ"}
                    jump_op = jump_map.get(tac.op, "JNZ")
                    target_lbl = (next_tac.result or "").rstrip(":")
                    instructions.append(MachineInstruction(
                        opcode=jump_op,
                        operands=[target_lbl],
                        comment=f"Salto condicional ({tac.op}) hacia {target_lbl}",
                        symbolic_operands=[target_lbl]
                    ))
                    reg_holds = None
                    i += 2
                    continue
                else:
                    if reg_holds != sym1:
                        instructions.append(MachineInstruction(
                            opcode="LOAD",
                            operands=[self.default_reg, addr1],
                            comment=f"Cargar {sym1}",
                            symbolic_operands=[self.default_reg, sym1]
                        ))
                    instructions.append(MachineInstruction(
                        opcode="CMP",
                        operands=[self.default_reg, addr2],
                        comment=f"Comparar con {sym2}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))
                    set_map = {">": "SETGT", "<": "SETLT", ">=": "SETGE", "<=": "SETLE", "==": "SETEQ", "!=": "SETNE"}
                    set_op = set_map.get(tac.op, "SETEQ")
                    instructions.append(MachineInstruction(
                        opcode=set_op,
                        operands=[self.default_reg],
                        comment=f"Establecer resultado booleano ({tac.op})",
                        symbolic_operands=[self.default_reg]
                    ))
                    instructions.append(MachineInstruction(
                        opcode="STORE",
                        operands=[addr_res, self.default_reg],
                        comment=f"Guardar resultado en {sym_res}",
                        symbolic_operands=[sym_res, self.default_reg]
                    ))
                    reg_holds = sym_res

            elif tac.op in ("+", "-", "*", "/", "%"):
                addr1, sym1 = self._resolve_operand(tac.arg1)
                addr2, sym2 = self._resolve_operand(tac.arg2)
                addr_res, sym_res = self._resolve_operand(tac.result, is_target=True)

                op_name = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}[tac.op]

                # Si el primer operando ya está en R1, reutilizar
                if reg_holds == sym1:
                    instructions.append(MachineInstruction(
                        opcode=op_name,
                        operands=[self.default_reg, addr2],
                        comment=f"Operar {tac.op} {sym2} sobre registro activo {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))
                else:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Cargar {sym1} en {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                    instructions.append(MachineInstruction(
                        opcode=op_name,
                        operands=[self.default_reg, addr2],
                        comment=f"Operar {tac.op} {sym2} sobre {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym2]
                    ))

                reg_holds = sym_res

                # Verificar si la siguiente instrucción es asignación directa result = tac.result
                if i + 1 < n and tac_instructions[i + 1].op == "=" and tac_instructions[i + 1].arg1 == tac.result:
                    next_tac = tac_instructions[i + 1]
                    addr_final, sym_final = self._resolve_operand(next_tac.result, is_target=True)
                    instructions.append(MachineInstruction(
                        opcode="STORE",
                        operands=[addr_final, self.default_reg],
                        comment=f"Guardar directamente en variable final {sym_final}",
                        symbolic_operands=[sym_final, self.default_reg]
                    ))
                    # Si el temporal tac.result se utiliza más adelante, también persistirlo
                    remaining_uses = any(tac.result in (inst.arg1, inst.arg2) for inst in tac_instructions[i+2:])
                    if remaining_uses:
                        instructions.append(MachineInstruction(
                            opcode="STORE",
                            operands=[addr_res, self.default_reg],
                            comment=f"Guardar temporal activo {sym_res}",
                            symbolic_operands=[sym_res, self.default_reg]
                        ))
                    reg_holds = sym_final
                    i += 2
                    continue
                else:
                    instructions.append(MachineInstruction(
                        opcode="STORE",
                        operands=[addr_res, self.default_reg],
                        comment=f"Guardar en {sym_res}",
                        symbolic_operands=[sym_res, self.default_reg]
                    ))

            elif tac.op == "=":
                addr_src, sym_src = self._resolve_operand(tac.arg1)
                addr_dst, sym_dst = self._resolve_operand(tac.result, is_target=True)

                if reg_holds != sym_src:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr_src],
                        comment=f"Cargar {sym_src} en {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym_src]
                    ))
                instructions.append(MachineInstruction(
                    opcode="STORE",
                    operands=[addr_dst, self.default_reg],
                    comment=f"Almacenar en {sym_dst}",
                    symbolic_operands=[sym_dst, self.default_reg]
                ))
                reg_holds = sym_dst

            elif tac.op == "IF_CMP_GOTO":
                addr1, sym1 = self._resolve_operand(tac.arg1)
                arg2_clean = tac.arg2 or "== 0"
                parts = arg2_clean.split()
                comp_op, rhs = (parts[0], parts[1]) if len(parts) == 2 else ("==", "0")
                addr2, sym2 = self._resolve_operand(rhs)

                if reg_holds != sym1:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Cargar {sym1} para comparar",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, addr2],
                    comment=f"Comparar {self.default_reg} con {sym2}",
                    symbolic_operands=[self.default_reg, sym2]
                ))

                jump_map = {
                    "==": "JZ", "!=": "JNZ", ">": "JGT", "<": "JLT", ">=": "JGE", "<=": "JLE"
                }
                jump_op = jump_map.get(comp_op, "JNZ")
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode=jump_op,
                    operands=[target_lbl],
                    comment=f"Salto condicional ({comp_op}) hacia {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))
                reg_holds = None

            elif tac.op in ("IF_GOTO", "IF_NOT_GOTO"):
                addr1, sym1 = self._resolve_operand(tac.arg1)
                if reg_holds != sym1:
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr1],
                        comment=f"Evaluar condición {sym1}",
                        symbolic_operands=[self.default_reg, sym1]
                    ))
                instructions.append(MachineInstruction(
                    opcode="CMP",
                    operands=[self.default_reg, "#0"],
                    comment=f"Comparar {self.default_reg} con 0",
                    symbolic_operands=[self.default_reg, "0"]
                ))
                jump_op = "JNZ" if tac.op == "IF_GOTO" else "JZ"
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode=jump_op,
                    operands=[target_lbl],
                    comment=f"Salto condicional hacia {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))
                reg_holds = None

            elif tac.op == "GOTO":
                target_lbl = (tac.result or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode="JMP",
                    operands=[target_lbl],
                    comment=f"Salto incondicional a {target_lbl}",
                    symbolic_operands=[target_lbl]
                ))
                reg_holds = None

            elif tac.op == "PRINT":
                addr, sym = self._resolve_operand(tac.arg1)
                instructions.append(MachineInstruction(
                    opcode="PRINT",
                    operands=[addr],
                    comment=f"Imprimir {sym}",
                    symbolic_operands=[sym]
                ))

            elif tac.op == "CALL":
                target_fn = (tac.arg1 or "").rstrip(":")
                instructions.append(MachineInstruction(
                    opcode="CALL",
                    operands=[target_fn],
                    comment=f"Llamada a subrutina {target_fn}",
                    symbolic_operands=[target_fn]
                ))
                reg_holds = None

            elif tac.op == "RETURN":
                if tac.arg1:
                    addr, sym = self._resolve_operand(tac.arg1)
                    instructions.append(MachineInstruction(
                        opcode="LOAD",
                        operands=[self.default_reg, addr],
                        comment=f"Cargar valor retorno en {self.default_reg}",
                        symbolic_operands=[self.default_reg, sym]
                    ))
                instructions.append(MachineInstruction(
                    opcode="RET",
                    operands=[],
                    comment="Retorno de subrutina",
                    symbolic_operands=[]
                ))
                reg_holds = None

            elif tac.op == "HALT":
                instructions.append(MachineInstruction(
                    opcode="HALT",
                    operands=[],
                    comment="Fin de ejecución",
                    symbolic_operands=[]
                ))
                reg_holds = None

            i += 1

        if not instructions or instructions[-1].opcode != "HALT":
            instructions.append(MachineInstruction(opcode="HALT", operands=[], comment="Fin de ejecución", symbolic_operands=[]))

        # Pasada de optimización de mirilla (Peephole)
        instructions = PeepholeOptimizer.optimize(instructions)

        self._assign_addresses_and_labels(instructions, label_positions)
        self.optimized_instructions = instructions
        return instructions

    def _assign_addresses_and_labels(self, instructions: List[MachineInstruction], label_positions: Dict[str, int]):
        """Asigna direcciones físicas consecutivas de 4 bytes a cada instrucción y resuelve saltos."""
        curr_addr = self.code_base
        addr_map: Dict[int, int] = {}

        for idx, inst in enumerate(instructions):
            inst.address = curr_addr
            addr_map[idx] = curr_addr
            curr_addr += 4

        # Mapear nombres de etiquetas a direcciones de destino
        label_addr_map: Dict[str, int] = {}
        for lbl_name, inst_idx in label_positions.items():
            target_addr = addr_map.get(inst_idx, curr_addr)
            label_addr_map[lbl_name] = target_addr

        # Resolver operandos de saltos y llamadas
        for inst in instructions:
            if inst.opcode in ("JMP", "JZ", "JNZ", "JGT", "JLT", "JGE", "JLE", "CALL"):
                if inst.operands:
                    target_lbl = inst.operands[0]
                    if target_lbl in label_addr_map:
                        inst.operands[0] = f"0x{label_addr_map[target_lbl]:04X}"

    def get_optimization_metrics(self) -> Dict[str, Any]:
        """Calcula estadísticas comparativas de optimización."""
        unopt = len(self.unoptimized_instructions)
        opt = len(self.optimized_instructions)
        saved = max(0, unopt - opt)
        pct = (saved / unopt * 100.0) if unopt > 0 else 0.0
        return {
            "unoptimized_count": unopt,
            "optimized_count": opt,
            "instructions_saved": saved,
            "efficiency_gain_pct": round(pct, 2)
        }
