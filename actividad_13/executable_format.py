"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - FORMATO DE ARCHIVO EJECUTABLE (.BIN / .MVX)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import struct
import zlib
from typing import List, Dict, Tuple, Optional, Any
from code_generator import MachineInstruction
from symbol_table_mem import MemorySymbolTable, MemorySymbol


# Códigos de Operación Binarios (Opcodes de 1 byte)
OPCODE_MAP = {
    "LOAD": 0x01,
    "STORE": 0x02,
    "ADD": 0x03,
    "SUB": 0x04,
    "MUL": 0x05,
    "DIV": 0x06,
    "MOD": 0x07,
    "CMP": 0x08,
    "JMP": 0x09,
    "JZ": 0x0A,
    "JNZ": 0x0B,
    "JGT": 0x0C,
    "JLT": 0x0D,
    "JGE": 0x10,
    "JLE": 0x11,
    "PRINT": 0x0E,
    "HALT": 0x0F
}

REVERSE_OPCODE_MAP = {v: k for k, v in OPCODE_MAP.items()}


class ExecutableHeader:
    """
    Representa la cabecera estándar de 32 bytes del archivo ejecutable binario.

    Estructura de la Cabecera (32 bytes):
      - 0x00..0x03 (4B): Magic Number 'MVCO' (0x4D56434F)
      - 0x04..0x05 (2B): Versión de Formato (1)
      - 0x06..0x07 (2B): Banderas del SO (Flags)
      - 0x08..0x0B (4B): Dirección del Entry Point (0x1000)
      - 0x0C..0x0F (4B): Offset del Segmento de Código
      - 0x10..0x13 (4B): Tamaño del Segmento de Código
      - 0x14..0x17 (4B): Offset del Segmento de Datos
      - 0x18..0x1B (4B): Tamaño del Segmento de Datos
      - 0x1C..0x1F (4B): Checksum CRC32 de Verificación

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    MAGIC = b"MVCO"  # Máquina Virtual Compiladores
    HEADER_SIZE = 32

    def __init__(
        self,
        entry_point: int = 0x1000,
        code_offset: int = 32,
        code_size: int = 0,
        data_offset: int = 0,
        data_size: int = 0,
        checksum: int = 0,
        version: int = 1,
        flags: int = 0
    ):
        self.entry_point = entry_point
        self.code_offset = code_offset
        self.code_size = code_size
        self.data_offset = data_offset
        self.data_size = data_size
        self.checksum = checksum
        self.version = version
        self.flags = flags

    def pack(self) -> bytes:
        return struct.pack(
            ">4sHHIIIIII",
            self.MAGIC,
            self.version,
            self.flags,
            self.entry_point,
            self.code_offset,
            self.code_size,
            self.data_offset,
            self.data_size,
            self.checksum
        )

    @classmethod
    def unpack(cls, data: bytes) -> "ExecutableHeader":
        if len(data) < cls.HEADER_SIZE:
            raise ValueError(f"Cabecera incompleta. Se esperaban {cls.HEADER_SIZE} bytes.")
        magic, ver, flg, ep, c_off, c_sz, d_off, d_sz, chk = struct.unpack(">4sHHIIIIII", data[:cls.HEADER_SIZE])
        if magic != cls.MAGIC:
            raise ValueError(f"Firma mágica inválida '{magic}'. Archivo ejecutable no reconocido.")
        return cls(
            entry_point=ep,
            code_offset=c_off,
            code_size=c_sz,
            data_offset=d_off,
            data_size=d_sz,
            checksum=chk,
            version=ver,
            flags=flg
        )


class ExecutableBuilder:
    """
    Ensamblador y constructor de archivos ejecutables (.bin/.mvx) y archivos de
    desensamblado en código máquina (.asm).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    @staticmethod
    def build_binary(
        instructions: List[MachineInstruction],
        symbol_table: MemorySymbolTable,
        output_path: str,
        entry_point: int = 0x1000
    ) -> bytes:
        """Genera y guarda en disco el archivo ejecutable binario estructurado."""
        # 1. Empacar Segmento de Datos
        data_payload = bytearray()
        symbols_to_save = [s for s in symbol_table.symbols.values() if s.category != "TEMPORAL" or s.initial_value != 0]
        data_payload.extend(struct.pack(">I", len(symbols_to_save)))

        for sym in symbols_to_save:
            name_bytes = sym.name.encode('utf-8')
            init_val = int(sym.initial_value) if isinstance(sym.initial_value, (int, float, bool)) else 0
            # Formato de cada entrada de dato: [Addr 4B][Val 4B][NameLen 2B][NameStr]
            data_payload.extend(struct.pack(">IIH", sym.address, init_val, len(name_bytes)))
            data_payload.extend(name_bytes)

        # 2. Empacar Segmento de Código
        code_payload = bytearray()
        code_payload.extend(struct.pack(">I", len(instructions)))

        for inst in instructions:
            opcode_num = OPCODE_MAP.get(inst.opcode, 0x00)
            op_count = len(inst.operands)
            code_payload.extend(struct.pack(">IBB", inst.address, opcode_num, op_count))

            for op in inst.operands:
                op_str = str(op).strip()
                op_type = 0  # 0: Inmediato, 1: Registro, 2: Dirección Memoria, 3: Cadena
                val_int = 0

                if op_str.startswith("#"):
                    op_type = 0
                    try:
                        val_int = int(op_str[1:])
                    except ValueError:
                        val_int = 0
                elif op_str.upper().startswith("R") and len(op_str) <= 3 and op_str[1:].isdigit():
                    op_type = 1
                    val_int = int(op_str[1:])
                elif op_str.startswith("0x") or op_str.startswith("0X"):
                    op_type = 2
                    try:
                        val_int = int(op_str, 16)
                    except ValueError:
                        val_int = 0
                else:
                    try:
                        val_int = int(op_str)
                        op_type = 0
                    except ValueError:
                        # Etiqueta simbólica no resuelta o identificador
                        op_type = 3
                        val_int = 0

                code_payload.extend(struct.pack(">BI", op_type, val_int))

        # 3. Calcular offsets y Checksum
        header_size = ExecutableHeader.HEADER_SIZE
        code_offset = header_size
        code_size = len(code_payload)
        data_offset = code_offset + code_size
        data_size = len(data_payload)

        checksum = zlib.crc32(code_payload + data_payload)

        # 4. Construir Cabecera
        header = ExecutableHeader(
            entry_point=entry_point,
            code_offset=code_offset,
            code_size=code_size,
            data_offset=data_offset,
            data_size=data_size,
            checksum=checksum
        )

        full_binary = header.pack() + code_payload + data_payload

        # Guardar en archivo
        with open(output_path, "wb") as f:
            f.write(full_binary)

        return full_binary

    @staticmethod
    def generate_asm_file(
        instructions: List[MachineInstruction],
        symbol_table: MemorySymbolTable,
        output_asm_path: str,
        program_title: str = "Programa Generado"
    ):
        """Genera el archivo desensamblado legible (.asm) con cabecera y comentarios."""
        lines = [
            ";" + "=" * 80,
            f"; ARCHIVO DESENSAMBLADO EJECUTABLE: {program_title}",
            "; GENERADO POR: COMPILADOR ACTIVIDAD 13",
            "; PROFESOR: RIGOBERTO CARDENAS LARIOS",
            ";",
            "; INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):",
            "; 1. DIAZ TORRES JAZMIN MONTSERRAT",
            "; 2. FIERRO MELÉNDEZ ERNESTO HATUEY",
            "; 3. HERNANDEZ GARCIA HECTOR GABRIEL",
            "; 4. MILLAN GUERRERO OSWALDO JOSUE",
            ";" + "=" * 80,
            "",
            "; --- CABECERA DE METADATOS ---",
            "; MAGIC:        MVCO (0x4D56434F)",
            "; ENTRY POINT:  0x1000",
            "; ARCHITECTURE: 32-bit RISC Educational Processor",
            "",
            "; --- SEGMENTO DE DATOS (.DATA) ---",
        ]

        sorted_syms = sorted(symbol_table.symbols.values(), key=lambda s: s.address)
        for s in sorted_syms:
            val = s.initial_value if s.initial_value is not None else 0
            lines.append(f"{s.hex_address}:  DB  {s.name:<10} = {str(val):<6}  ; {s.category} ({s.data_type})")

        lines.extend([
            "",
            "; --- SEGMENTO DE CÓDIGO (.CODE) ---"
        ])

        for inst in instructions:
            lines.append(inst.to_memory_asm())

        lines.append("")

        with open(output_asm_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


class ExecutableReader:
    """
    Cargador del Entorno de Ejecución (Loader).
    Lee el archivo ejecutable binario, verifica la cabecera y el checksum,
    y reconstruye los segmentos de datos e instrucciones en memoria.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    @staticmethod
    def load(file_path: str) -> Tuple[ExecutableHeader, Dict[int, int], List[MachineInstruction], Dict[str, int]]:
        """
        Carga y valida un archivo binario ejecutable.
        Retorna: (Header, Memoria_Datos, Lista_Instrucciones, Tabla_Simbolos_Nombres)
        """
        with open(file_path, "rb") as f:
            raw_data = f.read()

        if len(raw_data) < ExecutableHeader.HEADER_SIZE:
            raise ValueError("El archivo binario es demasiado corto para contener una cabecera ejecutable válida.")

        header = ExecutableHeader.unpack(raw_data[:ExecutableHeader.HEADER_SIZE])

        # Extraer segmentos
        code_bytes = raw_data[header.code_offset: header.code_offset + header.code_size]
        data_bytes = raw_data[header.data_offset: header.data_offset + header.data_size]

        # Validar Checksum
        calculated_chk = zlib.crc32(code_bytes + data_bytes)
        if calculated_chk != header.checksum:
            raise ValueError(f"Error de integridad: Checksum inválido (esperado {header.checksum:#x}, calculado {calculated_chk:#x}). Archivo corrupto.")

        # Reconstruir Datos
        memory_data: Dict[int, int] = {}
        symbol_names: Dict[str, int] = {}
        d_cursor = 0
        if len(data_bytes) >= 4:
            sym_count = struct.unpack_from(">I", data_bytes, d_cursor)[0]
            d_cursor += 4
            for _ in range(sym_count):
                addr, val, name_len = struct.unpack_from(">IIH", data_bytes, d_cursor)
                d_cursor += 10
                name = data_bytes[d_cursor: d_cursor + name_len].decode('utf-8', errors='ignore')
                d_cursor += name_len
                memory_data[addr] = val
                symbol_names[name] = addr

        # Reconstruir Código
        instructions: List[MachineInstruction] = []
        c_cursor = 0
        if len(code_bytes) >= 4:
            inst_count = struct.unpack_from(">I", code_bytes, c_cursor)[0]
            c_cursor += 4

            for _ in range(inst_count):
                inst_addr, opcode_num, op_count = struct.unpack_from(">IBB", code_bytes, c_cursor)
                c_cursor += 6
                opcode_str = REVERSE_OPCODE_MAP.get(opcode_num, "UNKNOWN")

                operands: List[str] = []
                for _ in range(op_count):
                    op_type, val_int = struct.unpack_from(">BI", code_bytes, c_cursor)
                    c_cursor += 5

                    if op_type == 0:
                        operands.append(f"#{val_int}")
                    elif op_type == 1:
                        operands.append(f"R{val_int}")
                    elif op_type == 2:
                        operands.append(f"0x{val_int:04X}")
                    else:
                        operands.append(str(val_int))

                instructions.append(MachineInstruction(
                    opcode=opcode_str,
                    operands=operands,
                    address=inst_addr
                ))

        return header, memory_data, instructions, symbol_names
