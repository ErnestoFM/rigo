"""
================================================================================
ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - VERIFICACIÓN DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Dict, Any, Optional, List, Tuple


class Symbol:
    """
    Entrada de la tabla de símbolos para almacenar variables, tipos y valores evaluados.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        name: str,
        data_type: str,
        value: Any = None,
        scope_name: str = "global",
        line: int = 1,
        column: int = 1
    ):
        self.name = name
        self.data_type = data_type
        self.value = value
        self.scope_name = scope_name
        self.line = line
        self.column = column

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identificador": self.name,
            "tipo": self.data_type,
            "valor": self.value if self.value is not None else "(no asignado)",
            "ambito": self.scope_name,
            "linea": self.line,
            "columna": self.column
        }


class SymbolTable:
    """
    Gestor de la Tabla de Símbolos para la validación de expresiones.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    def reset(self):
        self.symbols.clear()

    def insert(self, name: str, data_type: str, value: Any = None, line: int = 1, column: int = 1) -> bool:
        if name in self.symbols:
            return False
        self.symbols[name] = Symbol(name, data_type, value, "global", line, column)
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def update_value(self, name: str, value: Any) -> bool:
        sym = self.lookup(name)
        if sym:
            sym.value = value
            return True
        return False

    def to_formatted_table(self) -> str:
        if not self.symbols:
            return "Tabla de símbolos vacía."

        sep = "+" + "-" * 5 + "+" + "-" * 18 + "+" + "-" * 12 + "+" + "-" * 20 + "+" + "-" * 11 + "+"
        header = f"| {'#':<3} | {'IDENTIFICADOR':<16} | {'TIPO':<10} | {'VALOR EVALUADO':<18} | {'LÍNEA:COL':<9} |"
        rows = [sep, header, sep]

        for idx, (name, sym) in enumerate(self.symbols.items(), 1):
            val_str = str(sym.value) if sym.value is not None else "(indefinido)"
            if sym.data_type == "string" and sym.value is not None:
                val_str = f'"{sym.value}"'
            if len(val_str) > 18:
                val_str = val_str[:15] + "..."
            loc_str = f"L:{sym.line}, C:{sym.column}"
            rows.append(
                f"| {idx:<3} | {sym.name:<16} | {sym.data_type:<10} | {val_str:<18} | {loc_str:<9} |"
            )
        rows.append(sep)
        return "\n".join(rows)
