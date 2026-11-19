"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - ENTORNO DE EJECUCIÓN Y MÁQUINA VIRTUAL (VM)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Dict, List, Optional, Tuple, Any
from code_generator import MachineInstruction
from executable_format import ExecutableReader, ExecutableHeader


class VMState:
    """
    Representa una instantánea del estado de la CPU en un ciclo determinado.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, cycle: int, pc: int, instruction: str, registers: Dict[str, int], flags: Dict[str, int], output: str):
        self.cycle = cycle
        self.pc = pc
        self.instruction = instruction
        self.registers = dict(registers)
        self.flags = dict(flags)
        self.output = output

    def __str__(self) -> str:
        reg_str = " | ".join([f"{r}: {v}" for r, v in sorted(self.registers.items()) if v != 0 or r in ("R1", "R2")])
        flag_str = f"ZF={self.flags.get('ZF', 0)} SF={self.flags.get('SF', 0)}"
        return f"[Ciclo {self.cycle:03d} | PC 0x{self.pc:04X}] {self.instruction:<26} -> {reg_str} | {flag_str}"


class VirtualMachine:
    """
    Procesador Virtual RISC de 32 bits (Entorno de Ejecución).
    Implementa el ciclo Fetch-Decode-Execute para el conjunto de instrucciones
    definido por el profesor Rigoberto Cárdenas Larios.

    Componentes de Hardware Simulados:
      - Banco de 8 Registros de Propósito General (R1..R8)
      - Program Counter (PC)
      - Registro de Banderas de Estado (ZF, SF, OF)
      - Memoria RAM Segmentada (Código 0x1000, Datos 0x2000, Resultados 0x3000)
      - Unidad Aritmético-Lógica (ALU)
      - Controlador de E/S (Buffer de salida)

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, max_cycles: int = 1000):
        self.max_cycles = max_cycles
        self.registers: Dict[str, int] = {f"R{i}": 0 for i in range(1, 9)}
        self.pc: int = 0x1000
        self.flags: Dict[str, int] = {"ZF": 0, "SF": 0, "OF": 0}
        self.memory: Dict[int, int] = {}
        self.symbol_names: Dict[str, int] = {}
        self.code_instructions: Dict[int, MachineInstruction] = {}
        self.output_buffer: List[str] = []
        self.execution_history: List[VMState] = []
        self.is_halted: bool = False
        self.cycle_count: int = 0
        self.header: Optional[ExecutableHeader] = None
        self.error_message: Optional[str] = None

    def reset(self):
        """Reinicia el procesador a su estado inicial."""
        self.registers = {f"R{i}": 0 for i in range(1, 9)}
        self.pc = 0x1000
        self.flags = {"ZF": 0, "SF": 0, "OF": 0}
        self.memory.clear()
        self.symbol_names.clear()
        self.code_instructions.clear()
        self.output_buffer.clear()
        self.execution_history.clear()
        self.is_halted = False
        self.cycle_count = 0
        self.error_message = None

    def load_executable_file(self, file_path: str):
        """Carga y valida un archivo binario ejecutable en la memoria RAM de la VM."""
        self.reset()
        self.header, memory_data, instructions, symbol_names = ExecutableReader.load(file_path)

        # Cargar variables en la memoria RAM
        self.memory.update(memory_data)
        self.symbol_names = symbol_names

        # Cargar instrucciones en el segmento de código
        for inst in instructions:
            self.code_instructions[inst.address] = inst

        self.pc = self.header.entry_point

    def load_from_memory_structures(
        self,
        instructions: List[MachineInstruction],
        initial_data: Dict[int, int],
        symbol_names: Dict[str, int],
        entry_point: int = 0x1000
    ):
        """Carga directa en memoria sin necesidad de leer del disco (ideal para pruebas y GUI)."""
        self.reset()
        self.memory.update(initial_data)
        self.symbol_names = symbol_names
        for inst in instructions:
            self.code_instructions[inst.address] = inst
        self.pc = entry_point

    def _resolve_val(self, operand_str: str) -> int:
        """Resuelve el valor numérico de un operando (registro, inmediato o dirección de memoria)."""
        op = operand_str.strip()
        # Inmediato: #15 o 15
        if op.startswith("#"):
            return int(op[1:])
        # Registro: R1..R8
        if op.upper() in self.registers:
            return self.registers[op.upper()]
        # Dirección de Memoria Hexadecimal: 0x2000
        if op.startswith("0x") or op.startswith("0X"):
            addr = int(op, 16)
            return self.memory.get(addr, 0)
        # Número entero directo
        try:
            return int(op)
        except ValueError:
            # Si es nombre de símbolo
            if op in self.symbol_names:
                addr = self.symbol_names[op]
                return self.memory.get(addr, 0)
            raise ValueError(f"Operando no reconocido o variable no inicializada: '{op}'")

    def _resolve_addr(self, operand_str: str) -> int:
        """Resuelve la dirección física de memoria de destino."""
        op = operand_str.strip()
        if op.startswith("0x") or op.startswith("0X"):
            return int(op, 16)
        if op in self.symbol_names:
            return self.symbol_names[op]
        try:
            return int(op)
        except ValueError:
            raise ValueError(f"Dirección de memoria de destino inválida: '{op}'")

    def _update_flags(self, result: int):
        """Actualiza las banderas de estado del procesador (Zero Flag y Sign Flag)."""
        self.flags["ZF"] = 1 if result == 0 else 0
        self.flags["SF"] = 1 if result < 0 else 0

    def step(self) -> bool:
        """
        Ejecuta un único ciclo de instrucción (Fetch-Decode-Execute).
        Retorna True si la ejecución debe continuar, o False si terminó/hubo error.
        """
        if self.is_halted or self.error_message:
            return False

        if self.cycle_count >= self.max_cycles:
            self.error_message = f"Límite de seguridad alcanzado ({self.max_cycles} ciclos). Posible bucle infinito detectado."
            self.is_halted = True
            return False

        if self.pc not in self.code_instructions:
            self.error_message = f"Violación de segmento: Dirección de código 0x{self.pc:04X} no contiene una instrucción válida."
            self.is_halted = True
            return False

        inst = self.code_instructions[self.pc]
        current_pc = self.pc
        next_pc = current_pc + 4
        self.cycle_count += 1

        opc = inst.opcode
        ops = inst.operands

        try:
            # 1. LOAD Rd, src
            if opc == "LOAD":
                reg = ops[0].upper()
                val = self._resolve_val(ops[1])
                self.registers[reg] = val
                self._update_flags(val)

            # 2. STORE [dest_addr], Rs
            elif opc == "STORE":
                dest_addr = self._resolve_addr(ops[0])
                reg = ops[1].upper()
                val = self.registers.get(reg, 0)
                self.memory[dest_addr] = val

            # 3. ADD Rd, src
            elif opc == "ADD":
                reg = ops[0].upper()
                val = self._resolve_val(ops[1])
                self.registers[reg] += val
                self._update_flags(self.registers[reg])

            # 4. SUB Rd, src
            elif opc == "SUB":
                reg = ops[0].upper()
                val = self._resolve_val(ops[1])
                self.registers[reg] -= val
                self._update_flags(self.registers[reg])

            # 5. MUL Rd, src
            elif opc == "MUL":
                reg = ops[0].upper()
                val = self._resolve_val(ops[1])
                self.registers[reg] *= val
                self._update_flags(self.registers[reg])

            # 6. DIV Rd, src
            elif opc == "DIV":
                reg = ops[0].upper()
                val = self._resolve_val(ops[1])
                if val == 0:
                    raise ZeroDivisionError(f"Intento de división por cero en instrucción 0x{current_pc:04X}: DIV {reg}, {ops[1]}")
                self.registers[reg] //= val
                self._update_flags(self.registers[reg])

            # 7. MOD Rd, src
            elif opc == "MOD":
                reg = ops[0].upper()
                val = self._resolve_val(ops[1])
                if val == 0:
                    raise ZeroDivisionError(f"Módulo por cero en 0x{current_pc:04X}")
                self.registers[reg] %= val
                self._update_flags(self.registers[reg])

            # 8. CMP Rd, src
            elif opc == "CMP":
                val1 = self.registers.get(ops[0].upper(), 0)
                val2 = self._resolve_val(ops[1])
                diff = val1 - val2
                self._update_flags(diff)

            # 9. JMP target
            elif opc == "JMP":
                target = self._resolve_addr(ops[0])
                next_pc = target

            # 10. JZ (Jump if Zero)
            elif opc == "JZ":
                if self.flags["ZF"] == 1:
                    next_pc = self._resolve_addr(ops[0])

            # 11. JNZ (Jump if Not Zero)
            elif opc == "JNZ":
                if self.flags["ZF"] == 0:
                    next_pc = self._resolve_addr(ops[0])

            # 12. JGT (Jump if Greater Than)
            elif opc == "JGT":
                if self.flags["ZF"] == 0 and self.flags["SF"] == 0:
                    next_pc = self._resolve_addr(ops[0])

            # 13. JLT (Jump if Less Than)
            elif opc == "JLT":
                if self.flags["SF"] == 1:
                    next_pc = self._resolve_addr(ops[0])

            # 14. JGE (Jump if Greater than or Equal)
            elif opc == "JGE":
                if self.flags["SF"] == 0 or self.flags["ZF"] == 1:
                    next_pc = self._resolve_addr(ops[0])

            # 15. JLE (Jump if Less than or Equal)
            elif opc == "JLE":
                if self.flags["SF"] == 1 or self.flags["ZF"] == 1:
                    next_pc = self._resolve_addr(ops[0])

            # 16. PRINT src
            elif opc == "PRINT":
                val = self._resolve_val(ops[0])
                self.output_buffer.append(f"> {val}")

            # 15. HALT
            elif opc == "HALT":
                self.is_halted = True
                next_pc = current_pc

            else:
                raise ValueError(f"Opcode de máquina no reconocido: '{opc}'")

        except Exception as e:
            self.error_message = f"Error de ejecución en 0x{current_pc:04X} ({inst.to_memory_asm()}): {str(e)}"
            self.is_halted = True
            return False

        # Registrar historial de estado
        snapshot = VMState(
            cycle=self.cycle_count,
            pc=current_pc,
            instruction=inst.to_memory_asm(),
            registers=self.registers,
            flags=self.flags,
            output=self.output_buffer[-1] if self.output_buffer else ""
        )
        self.execution_history.append(snapshot)

        self.pc = next_pc
        return not self.is_halted

    def run(self) -> bool:
        """Ejecuta el programa completo hasta HALT o error."""
        while self.step():
            pass
        return self.error_message is None

    def dump_memory_state(self) -> str:
        """Muestra una tabla estructurada de los valores finales en memoria RAM."""
        lines = [
            "+" + "-" * 14 + "+" + "-" * 16 + "+" + "-" * 16 + "+",
            f"| {'Dirección':<12} | {'Variable / Simb':<14} | {'Valor Almacenado':<14} |",
            "+" + "-" * 14 + "+" + "-" * 16 + "+" + "-" * 16 + "+"
        ]
        # Invertir nombres para búsqueda rápida
        addr_to_name = {addr: name for name, addr in self.symbol_names.items()}
        for addr in sorted(self.memory.keys()):
            var_name = addr_to_name.get(addr, "(anónimo)")
            val = self.memory[addr]
            lines.append(f"| 0x{addr:04X}{'':<6} | {var_name:<14} | {val:<14} |")
        lines.append("+" + "-" * 14 + "+" + "-" * 16 + "+" + "-" * 16 + "+")
        return "\n".join(lines)

    def dump_registers_state(self) -> str:
        """Muestra el estado final de los registros y banderas."""
        reg_lines = [f"{r}: {v}" for r, v in sorted(self.registers.items())]
        flags_line = f"ZF: {self.flags['ZF']} | SF: {self.flags['SF']} | OF: {self.flags['OF']}"
        pc_line = f"PC Final: 0x{self.pc:04X} | Ciclos Totales: {self.cycle_count}"
        return "REGISTROS: " + " | ".join(reg_lines) + "\nBANDERAS:  " + flags_line + "\nESTADO:    " + pc_line
