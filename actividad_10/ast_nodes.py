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

from typing import List, Optional, Any


class ASTNode:
    """Clase base para el AST de generación de código intermedio."""
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column
        self.inferred_type: Optional[str] = None


class ProgramNode(ASTNode):
    """Nodo raíz con la secuencia de sentencias del programa."""
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements


class VariableDeclarationNode(ASTNode):
    """Declaración de variable con tipo y opcional inicializador."""
    def __init__(self, var_type: str, name: str, initializer: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer


class AssignmentNode(ASTNode):
    """Sentencia de asignación: target = expr;"""
    def __init__(self, target: str, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.expr = expr


class BinaryOpNode(ASTNode):
    """Operación binaria: izquierda OP derecha."""
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right


class UnaryOpNode(ASTNode):
    """Operación unaria: OP operando."""
    def __init__(self, op: str, operand: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.operand = operand


class IdentifierNode(ASTNode):
    """Identificador o variable."""
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name


class LiteralNode(ASTNode):
    """Literal constante: entero, flotante, cadena, booleano."""
    def __init__(self, value: Any, literal_type: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.literal_type = literal_type
        self.inferred_type = literal_type
