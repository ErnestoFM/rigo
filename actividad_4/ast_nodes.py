"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Optional

class ASTNode:
    """
    Clase base abstracta para todos los nodos del Árbol de Sintaxis Abstracta (AST).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        raise NotImplementedError


class BinaryOpNode(ASTNode):
    """
    Representa una operación binaria (aritmética, relacional o lógica).
    Ejemplos:
      - Aritmética: x + y, a * b
      - Relacional (Término Lógico): 10 > 5, 3 <= 4
      - Lógica: A && B, C || D

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, category: str, line: int, column: int):
        self.left = left
        self.operator = operator
        self.right = right
        self.category = category # 'ARITMETICA', 'RELACIONAL' (TERMINO_LOGICO), 'LOGICA'
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        
        label_map = {
            "LOGICA": f"ExpresionLogica [Op: '{self.operator}']",
            "RELACIONAL": f"TerminoLogico/Comparacion [Op: '{self.operator}']",
            "ARITMETICA": f"ExpresionAritmetica/Operacion [Op: '{self.operator}']"
        }
        label = label_map.get(self.category, f"OperacionBinaria [{self.operator}]")
        res = f"{prefix}{marker}{label} (L:{self.line}, C:{self.column})\n"

        if self.left:
            res += self.left.to_tree_str(next_prefix, False)
        if self.right:
            res += self.right.to_tree_str(next_prefix, True)

        return res


class UnaryOpNode(ASTNode):
    """
    Representa una operación unaria (negación aritmética '-' o lógica '!').

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, operator: str, operand: ASTNode, category: str, line: int, column: int):
        self.operator = operator
        self.operand = operand
        self.category = category
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}OperacionUnaria [{self.operator}] ({self.category}) (L:{self.line}, C:{self.column})\n"
        if self.operand:
            res += self.operand.to_tree_str(next_prefix, True)
        return res


class GroupedExprNode(ASTNode):
    """
    Representa una subexpresión agrupada entre paréntesis: ( expresion ).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, expression: ASTNode, line: int, column: int):
        self.expression = expression
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        res = f"{prefix}{marker}SubexpresionAgrupada '( )' (L:{self.line}, C:{self.column})\n"
        if self.expression:
            res += self.expression.to_tree_str(next_prefix, True)
        return res


class NumberNode(ASTNode):
    """
    Representa un literal numérico (entero o flotante).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, value: str, num_type: str, line: int, column: int):
        self.value = value
        self.num_type = num_type
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}Numero ({self.num_type}): {self.value} (L:{self.line}, C:{self.column})\n"


class IdentifierNode(ASTNode):
    """
    Representa un identificador de variable (factor -> IDENTIFICADOR).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
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
        return f"{prefix}{marker}Identificador: '{self.name}' (L:{self.line}, C:{self.column})\n"


class ErrorNode(ASTNode):
    """
    Nodo de recuperación de error para mantener la integridad del AST ante fallas sintácticas.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, description: str, line: int, column: int):
        self.description = description
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}[NODO ERROR SINTÁCTICO: {self.description}] (L:{self.line}, C:{self.column})\n"
