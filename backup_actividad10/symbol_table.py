"""
================================================================================
ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Dict, Any, Optional


class Symbol:
    """Almacena el identificador, su tipo conocido y valor opcional."""
    def __init__(self, name: str, data_type: str = "int", value: Any = None):
        self.name = name
        self.data_type = data_type
        self.value = value


class SymbolTable:
    """Tabla de símbolos para rastreo de tipos y variables en el código intermedio."""
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    def reset(self):
        self.symbols.clear()

    def set_type(self, name: str, data_type: str, value: Any = None):
        self.symbols[name] = Symbol(name, data_type, value)

    def get_type(self, name: str) -> str:
        sym = self.symbols.get(name)
        return sym.data_type if sym else "int"

    def get_value(self, name: str) -> Optional[Any]:
        sym = self.symbols.get(name)
        return sym.value if sym else None
