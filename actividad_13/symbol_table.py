"""
================================================================================
ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL,
             MÉTODOS Y CLASES
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
from enum import Enum


class DataType(Enum):
    """
    Sistema de tipos estáticos para verificación semántica de compatibilidad.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"
    STRING = "string"
    CHAR = "char"
    VOID = "void"
    ANY = "any"
    ERROR = "error_type"
    CLASS = "class"

    @classmethod
    def from_str(cls, name: str) -> 'DataType':
        mapping = {
            'int': cls.INT,
            'float': cls.FLOAT,
            'double': cls.FLOAT,
            'boolean': cls.BOOLEAN,
            'bool': cls.BOOLEAN,
            'string': cls.STRING,
            'String': cls.STRING,
            'char': cls.CHAR,
            'void': cls.VOID,
            'any': cls.ANY
        }
        return mapping.get(name, cls.CLASS)

    def is_numeric(self) -> bool:
        return self in (DataType.INT, DataType.FLOAT)

    def is_boolean(self) -> bool:
        return self == DataType.BOOLEAN

    def can_assign_to(self, target: 'DataType') -> bool:
        """Determina compatibilidad de tipos para asignación o paso de argumentos."""
        if self == DataType.ERROR or target == DataType.ERROR:
            return True # Evita cascada de errores falsos
        if self == DataType.ANY or target == DataType.ANY:
            return True
        if self == target:
            return True
        # Coerción numérica permitida: int puede promoverse a float
        if self == DataType.INT and target == DataType.FLOAT:
            return True
        return False


class Symbol:
    """
    Entrada base para un símbolo registrado en la tabla de símbolos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, data_type: DataType, line: int = 1, column: int = 1):
        self.name = name
        self.data_type = data_type
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"Symbol({self.name}, {self.data_type.value}, L:{self.line})"


class VariableSymbol(Symbol):
    """
    Representa una variable local, parámetro o campo de clase.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, data_type: DataType, line: int = 1, column: int = 1, is_param: bool = False):
        super().__init__(name, data_type, line, column)
        self.is_param = is_param

    def __repr__(self) -> str:
        kind = "Parámetro" if self.is_param else "Variable"
        return f"{kind}({self.name}: {self.data_type.value})"


class MethodSymbol(Symbol):
    """
    Representa un método o función con su signatura completa (tipo de retorno y parámetros).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        name: str,
        return_type: DataType,
        parameters: List[Tuple[str, DataType]],
        line: int = 1,
        column: int = 1
    ):
        super().__init__(name, return_type, line, column)
        self.parameters = parameters # Lista de (nombre_param, DataType)

    @property
    def arity(self) -> int:
        return len(self.parameters)

    def format_signature(self) -> str:
        params_str = ", ".join([f"{t.value} {n}" for n, t in self.parameters])
        return f"{self.data_type.value} {self.name}({params_str})"

    def __repr__(self) -> str:
        return f"Método({self.format_signature()})"


class ClassSymbol(Symbol):
    """
    Representa una clase definida por el usuario con sus campos y métodos internos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(name, DataType.CLASS, line, column)
        self.fields: Dict[str, VariableSymbol] = {}
        self.methods: Dict[str, MethodSymbol] = {}

    def define_field(self, field: VariableSymbol):
        self.fields[field.name] = field

    def define_method(self, method: MethodSymbol):
        self.methods[method.name] = method

    def resolve_member(self, member_name: str) -> Optional[Symbol]:
        if member_name in self.fields:
            return self.fields[member_name]
        if member_name in self.methods:
            return self.methods[member_name]
        return None

    def __repr__(self) -> str:
        return f"Clase({self.name}, Campos: {len(self.fields)}, Métodos: {len(self.methods)})"


class Scope:
    """
    Ámbito léxico (Scope) jerárquico con enlace a su ámbito padre (enclosing scope).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, scope_name: str, parent: Optional['Scope'] = None):
        self.scope_name = scope_name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> bool:
        """Registra un nuevo símbolo en el ámbito actual. Retorna False si ya existe."""
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def resolve(self, name: str) -> Optional[Symbol]:
        """Busca recursivamente un símbolo desde el ámbito local hacia el global."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent is not None:
            return self.parent.resolve(name)
        return None

    def resolve_local(self, name: str) -> Optional[Symbol]:
        """Busca un símbolo únicamente dentro del ámbito local inmediato."""
        return self.symbols.get(name)

    def to_formatted_str(self, indent: int = 0) -> str:
        """Representación estructurada del ámbito y sus símbolos para diagnósticos y reportes."""
        ind = "  " * indent
        res = f"{ind}Scope '{self.scope_name}' ({len(self.symbols)} símbolos):\n"
        for name, sym in self.symbols.items():
            if isinstance(sym, MethodSymbol):
                res += f"{ind}  • [MÉTODO] {sym.format_signature()} (L:{sym.line})\n"
            elif isinstance(sym, ClassSymbol):
                res += f"{ind}  • [CLASE] {sym.name} (Campos: {len(sym.fields)}, Métodos: {len(sym.methods)})\n"
            elif isinstance(sym, VariableSymbol):
                rol = "Parámetro" if sym.is_param else "Variable"
                res += f"{ind}  • [{rol.upper()}] {sym.name} : {sym.data_type.value} (L:{sym.line})\n"
            else:
                res += f"{ind}  • {sym.name} : {sym.data_type.value}\n"
        return res
