"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - ASIGNACIÓN DE DIRECCIONES Y TABLA DE SÍMBOLOS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Dict, Optional, List, Any


class MemorySymbol:
    """
    Representa un símbolo con su dirección de memoria física asignada,
    tipo de dato, valor inicial y tamaño en bytes.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        name: str,
        address: int,
        data_type: str = "int",
        initial_value: Any = 0,
        size_bytes: int = 4,
        category: str = "VARIABLE"
    ):
        self.name = name
        self.address = address
        self.data_type = data_type
        self.initial_value = initial_value
        self.size_bytes = size_bytes
        self.category = category  # VARIABLE, TEMPORAL, RESULT, LABEL

    @property
    def hex_address(self) -> str:
        return f"0x{self.address:04X}"

    def __str__(self) -> str:
        return f"| {self.name:<10} | {self.hex_address:<10} | {self.data_type:<8} | {str(self.initial_value):<14} | {self.category:<10} |"


class MemorySymbolTable:
    """
    Tabla de símbolos especializada en la gestión y asignación de direcciones
    de memoria física para variables, temporales, resultados y etiquetas.

    Segmentos de Memoria:
      - 0x1000 - 0x1FFF: Segmento de Código (Instrucciones de Máquina)
      - 0x2000 - 0x2FFF: Segmento de Datos (Variables de Entrada y Constantes)
      - 0x3000 - 0x3FFF: Segmento de Resultados (Variables de Destino y Salida)

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        code_base: int = 0x1000,
        data_base: int = 0x2000,
        result_base: int = 0x3000
    ):
        self.code_base = code_base
        self.data_base = data_base
        self.result_base = result_base

        self.current_data_addr = data_base
        self.current_result_addr = result_base
        self.symbols: Dict[str, MemorySymbol] = {}
        self.labels: Dict[str, int] = {}  # Nombre de etiqueta -> dirección hex (0x1000, etc.)

    def reset(self):
        """Reinicia la asignación de memoria."""
        self.current_data_addr = self.data_base
        self.current_result_addr = self.result_base
        self.symbols.clear()
        self.labels.clear()

    def allocate_variable(
        self,
        name: str,
        data_type: str = "int",
        initial_value: Any = 0,
        is_result: bool = False
    ) -> MemorySymbol:
        """Asigna una dirección de memoria de 4 bytes a una variable."""
        if name in self.symbols:
            return self.symbols[name]

        if is_result or name.lower().startswith("result") or name.lower().startswith("res"):
            addr = self.current_result_addr
            self.current_result_addr += 4
            category = "RESULTADO"
        elif name.startswith("t") and name[1:].isdigit():
            addr = self.current_data_addr
            self.current_data_addr += 4
            category = "TEMPORAL"
        else:
            addr = self.current_data_addr
            self.current_data_addr += 4
            category = "VARIABLE"

        sym = MemorySymbol(
            name=name,
            address=addr,
            data_type=data_type,
            initial_value=initial_value,
            size_bytes=4,
            category=category
        )
        self.symbols[name] = sym
        return sym

    def register_label(self, label_name: str, code_address: int):
        """Registra la dirección en el segmento de código (0x1000...) para una etiqueta."""
        self.labels[label_name] = code_address

    def get_address(self, name: str) -> Optional[int]:
        """Obtiene la dirección numérica de una variable o etiqueta."""
        if name in self.symbols:
            return self.symbols[name].address
        if name in self.labels:
            return self.labels[name]
        return None

    def get_hex_address(self, name: str) -> Optional[str]:
        """Obtiene la dirección en formato hexadecimal (ej. 0x2000)."""
        addr = self.get_address(name)
        if addr is not None:
            return f"0x{addr:04X}"
        return None

    def get_symbol_by_address(self, address: int) -> Optional[MemorySymbol]:
        """Busca un símbolo por su dirección física de memoria."""
        for sym in self.symbols.values():
            if sym.address == address:
                return sym
        return None

    def to_markdown_table(self) -> str:
        """Genera la tabla de símbolos exacta requerida por la rúbrica."""
        lineas = [
            "| Símbolo    | Dirección  | Tipo     | Valor Inicial   | Categoría   |",
            "|:-----------|:-----------|:---------|:----------------|:------------|"
        ]
        # Ordenar por dirección
        sorted_syms = sorted(self.symbols.values(), key=lambda s: s.address)
        for s in sorted_syms:
            lineas.append(f"| {s.name:<10} | {s.hex_address:<10} | {s.data_type:<8} | {str(s.initial_value):<15} | {s.category:<11} |")
        return "\n".join(lineas)

    def to_formatted_str(self) -> str:
        """Representación textual clara para consola."""
        sep = "+" + "-" * 14 + "+" + "-" * 13 + "+" + "-" * 10 + "+" + "-" * 17 + "+" + "-" * 13 + "+"
        header = f"| {'Símbolo':<12} | {'Dirección':<11} | {'Tipo':<8} | {'Valor Inicial':<15} | {'Categoría':<11} |"
        rows = [sep, header, sep]
        sorted_syms = sorted(self.symbols.values(), key=lambda s: s.address)
        for s in sorted_syms:
            rows.append(f"| {s.name:<12} | {s.hex_address:<11} | {s.data_type:<8} | {str(s.initial_value):<15} | {s.category:<11} |")
        rows.append(sep)
        return "\n".join(rows)

