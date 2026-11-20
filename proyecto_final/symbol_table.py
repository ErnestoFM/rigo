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

from typing import Dict, Any, Optional, List, Tuple


class Symbol:
    """
    Símbolo individual que representa una variable o constante en memoria.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        name: str,
        type_name: str,
        scope: str = "global",
        address: Optional[int] = None,
        value: Any = None,
        is_initialized: bool = False
    ):
        self.name = name
        self.type_name = type_name
        self.scope = scope
        self.address = address
        self.value = value
        self.is_initialized = is_initialized

    def __str__(self) -> str:
        addr_str = f"0x{self.address:04X}" if self.address is not None else "N/A"
        return f"Symbol({self.name:<12} | Tipo: {self.type_name:<8} | Ámbito: {self.scope:<8} | Dir: {addr_str} | Init: {self.is_initialized})"


class MethodSymbol:
    """
    Información de firma de método o función.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        name: str,
        return_type: str,
        parameters: List[Tuple[str, str]],
        label: str,
        class_name: Optional[str] = None
    ):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.label = label
        self.class_name = class_name


class ClassSymbol:
    """
    Información de estructura y miembros de clase.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str):
        self.name = name
        self.fields: Dict[str, str] = {}
        self.methods: Dict[str, MethodSymbol] = {}


class SymbolTable:
    """
    Tabla de símbolos con gestión de ámbitos jerárquicos y asignación de direcciones
    de memoria física para la arquitectura de máquina virtual (segmento de datos 0x2000).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, parent: Optional['SymbolTable'] = None, scope_name: str = "global"):
        self.parent = parent
        self.scope_name = scope_name
        self.symbols: Dict[str, Symbol] = {}
        self.methods: Dict[str, MethodSymbol] = {}
        self.classes: Dict[str, ClassSymbol] = {}
        self.next_memory_address = 0x2000 if parent is None else parent.next_memory_address

    def allocate_memory(self, size: int = 4) -> int:
        if self.parent:
            return self.parent.allocate_memory(size)
        addr = self.next_memory_address
        self.next_memory_address += size
        return addr

    def insert_variable(self, name: str, type_name: str, value: Any = None, is_init: bool = False) -> Symbol:
        if name in self.symbols:
            sym = self.symbols[name]
            if value is not None:
                sym.value = value
                sym.is_initialized = True
            return sym

        addr = self.allocate_memory(4)
        sym = Symbol(name, type_name, self.scope_name, addr, value, is_init)
        self.symbols[name] = sym
        return sym

    def lookup_variable(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup_variable(name)
        return None

    def insert_method(self, name: str, return_type: str, params: List[Tuple[str, str]], label: str, class_name: Optional[str] = None) -> MethodSymbol:
        sym = MethodSymbol(name, return_type, params, label, class_name)
        self.methods[name] = sym
        return sym

    def lookup_method(self, name: str) -> Optional[MethodSymbol]:
        if name in self.methods:
            return self.methods[name]
        if self.parent:
            return self.parent.lookup_method(name)
        return None

    def insert_class(self, name: str) -> ClassSymbol:
        if name not in self.classes:
            self.classes[name] = ClassSymbol(name)
        return self.classes[name]

    def lookup_class(self, name: str) -> Optional[ClassSymbol]:
        if name in self.classes:
            return self.classes[name]
        if self.parent:
            return self.parent.lookup_class(name)
        return None

    def get_all_symbols(self) -> List[Symbol]:
        res = list(self.symbols.values())
        if self.parent:
            res.extend(self.parent.get_all_symbols())
        return res
