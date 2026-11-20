"""
================================================================================
ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO
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


class MethodSymbol:
    """
    Información asociada a un método o función en la tabla de símbolos.

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
        parameters: List[Tuple[str, str]], # (tipo, nombre)
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
    Información asociada a una clase y sus miembros.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str):
        self.name = name
        self.fields: Dict[str, str] = {}  # nombre_campo -> tipo
        self.methods: Dict[str, MethodSymbol] = {}


class SymbolTable:
    """
    Tabla de símbolos con soporte para jerarquía de ámbitos, registro de tipos,
    variables, métodos y clases.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, parent: Optional['SymbolTable'] = None, scope_name: str = "global"):
        self.parent = parent
        self.scope_name = scope_name
        self.symbols: Dict[str, Dict[str, Any]] = {}
        self.methods: Dict[str, MethodSymbol] = {}
        self.classes: Dict[str, ClassSymbol] = {}

    def insert_variable(self, name: str, type_name: str, value: Any = None) -> bool:
        if name in self.symbols:
            return False
        self.symbols[name] = {
            "type": type_name,
            "value": value,
            "scope": self.scope_name
        }
        return True

    def lookup_variable(self, name: str) -> Optional[Dict[str, Any]]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup_variable(name)
        return None

    def insert_method(
        self,
        name: str,
        return_type: str,
        params: List[Tuple[str, str]],
        label: str,
        class_name: Optional[str] = None
    ) -> bool:
        if name in self.methods and class_name is None:
            return False
        sym = MethodSymbol(name, return_type, params, label, class_name)
        self.methods[name] = sym
        return True

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
