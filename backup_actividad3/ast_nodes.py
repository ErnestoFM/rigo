"""
================================================================================
ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Optional

class ASTNode:
    """
    Clase base para todos los nodos del Árbol de Sintaxis Abstracta (AST).
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        raise NotImplementedError

class ProgramNode(ASTNode):
    """
    Nodo raíz del programa que contiene la lista de declaraciones y sentencias.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}└── ProgramNode\n"
        child_prefix = prefix + "    "
        for i, stmt in enumerate(self.statements):
            last_child = (i == len(self.statements) - 1)
            marker = "└── " if last_child else "├── "
            next_prefix = child_prefix + ("    " if last_child else "│   ")
            if hasattr(stmt, 'to_tree_str'):
                node_str = stmt.to_tree_str(child_prefix, last_child)
                res += node_str
            else:
                res += f"{child_prefix}{marker}{stmt}\n"
        return res

class VarDeclarationNode(ASTNode):
    """
    Representa la declaración de una variable:
    Ejemplo: entero x;  o  flotante y = 3.14;
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, tipo: str, name: str, initial_value: Optional[ASTNode], line: int, column: int):
        self.tipo = tipo
        self.name = name
        self.initial_value = initial_value
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}VarDeclarationNode: tipo='{self.tipo}', id='{self.name}' (L:{self.line}, C:{self.column})\n"
        if self.initial_value:
            res += self.initial_value.to_tree_str(next_prefix, True)
        return res

class ConstDeclarationNode(ASTNode):
    """
    Representa la declaración de una constante:
    Ejemplo: constante entero MAX = 100;
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, tipo: str, name: str, initial_value: ASTNode, line: int, column: int):
        self.tipo = tipo
        self.name = name
        self.initial_value = initial_value
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}ConstDeclarationNode: tipo='{self.tipo}', id='{self.name}' [CONSTANTE] (L:{self.line}, C:{self.column})\n"
        if self.initial_value:
            res += self.initial_value.to_tree_str(next_prefix, True)
        return res

class AssignmentNode(ASTNode):
    """
    Representa una sentencia de asignación / uso de variable:
    Ejemplo: x = y + 10;
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, expression: ASTNode, line: int, column: int):
        self.name = name
        self.expression = expression
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}AssignmentNode: target='{self.name}' (L:{self.line}, C:{self.column})\n"
        if self.expression:
            res += self.expression.to_tree_str(next_prefix, True)
        return res

class BinaryOpNode(ASTNode):
    """
    Representa una operación binaria (aritmética, relacional o lógica):
    Ejemplo: a + b, x > 10, activo && visible
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int, column: int):
        self.left = left
        self.op = op
        self.right = right
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}BinaryOpNode: op='{self.op}'\n"
        res += self.left.to_tree_str(next_prefix, False)
        res += self.right.to_tree_str(next_prefix, True)
        return res

class UnaryOpNode(ASTNode):
    """
    Representa una operación unaria:
    Ejemplo: -x, !activo
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, op: str, operand: ASTNode, line: int, column: int):
        self.op = op
        self.operand = operand
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}UnaryOpNode: op='{self.op}'\n"
        res += self.operand.to_tree_str(next_prefix, True)
        return res

class LiteralNode(ASTNode):
    """
    Representa un valor literal (número entero, flotante, cadena o booleano):
    Ejemplo: 42, 3.1416, "hola", verdadero
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, value: str, literal_type: str, line: int, column: int):
        self.value = value
        self.literal_type = literal_type
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}LiteralNode: valor={repr(self.value)}, tipo={self.literal_type} (L:{self.line}, C:{self.column})\n"

class IdentifierNode(ASTNode):
    """
    Representa una referencia a un identificador en una expresión.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, line: int, column: int):
        self.name = name
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}IdentifierNode: '{self.name}' (L:{self.line}, C:{self.column})\n"
