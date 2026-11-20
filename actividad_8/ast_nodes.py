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

from typing import List, Optional, Any


class ASTNode:
    """
    Clase base para los nodos del Árbol de Sintaxis Abstracta (AST)
    con soporte para tipo inferido y valor constante evaluado.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column
        self.inferred_type: Optional[str] = None
        self.evaluated_value: Optional[Any] = None

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        raise NotImplementedError


class ProgramNode(ASTNode):
    """Nodo raíz del programa."""
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Programa ({len(self.statements)} declaraciones/expresiones)\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, stmt in enumerate(self.statements):
            last = (i == len(self.statements) - 1)
            res += stmt.to_tree_str(new_prefix, last)
        return res


class VariableDeclarationNode(ASTNode):
    """Declaración de variable con tipo y opcional inicializador."""
    def __init__(self, var_type: str, name: str, initializer: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_str = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        val_str = f" [Valor: {self.evaluated_value}]" if self.evaluated_value is not None else ""
        res = f"{prefix}{branch}Declaración: {self.var_type} {self.name}{type_str}{val_str} (L:{self.line}, C:{self.column})\n"
        if self.initializer:
            new_prefix = prefix + ("    " if is_last else "│   ")
            res += self.initializer.to_tree_str(new_prefix, True)
        return res


class AssignmentNode(ASTNode):
    """Sentencia de asignación: target = expr;"""
    def __init__(self, target: str, expr: ASTNode, op: str = "=", line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.expr = expr
        self.op = op

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_str = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        val_str = f" [Valor: {self.evaluated_value}]" if self.evaluated_value is not None else ""
        res = f"{prefix}{branch}Asignación: {self.target} {self.op}{type_str}{val_str} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(new_prefix, True)
        return res


class BinaryOpNode(ASTNode):
    """Operación binaria: aritmética (+, -, *, /, %), relacional (==, <, >) o lógica (&&, ||)."""
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_str = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        val_str = f" [Evaluado: {self.evaluated_value}]" if self.evaluated_value is not None else ""
        res = f"{prefix}{branch}Op Binaria '{self.op}'{type_str}{val_str} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.left.to_tree_str(new_prefix, False)
        res += self.right.to_tree_str(new_prefix, True)
        return res


class UnaryOpNode(ASTNode):
    """Operación unaria: !, -, +."""
    def __init__(self, op: str, operand: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.operand = operand

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_str = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        val_str = f" [Evaluado: {self.evaluated_value}]" if self.evaluated_value is not None else ""
        res = f"{prefix}{branch}Op Unaria '{self.op}'{type_str}{val_str} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.operand.to_tree_str(new_prefix, True)
        return res


class CastNode(ASTNode):
    """Conversión de tipo explícita: static_cast<type>(expr) o (type)expr."""
    def __init__(self, target_type: str, expr: ASTNode, is_static_cast: bool = False, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target_type = target_type
        self.expr = expr
        self.is_static_cast = is_static_cast
        self.inferred_type = target_type

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        cast_kind = "static_cast" if self.is_static_cast else "cast_c"
        val_str = f" [Evaluado: {self.evaluated_value}]" if self.evaluated_value is not None else ""
        res = f"{prefix}{branch}Conversión {cast_kind}<{self.target_type}>{val_str} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(new_prefix, True)
        return res


class IdentifierNode(ASTNode):
    """Identificador / variable referenciada."""
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_str = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        val_str = f" [Valor: {self.evaluated_value}]" if self.evaluated_value is not None else ""
        return f"{prefix}{branch}Identificador: {self.name}{type_str}{val_str} (L:{self.line}, C:{self.column})\n"


class LiteralNode(ASTNode):
    """Literal de cualquier tipo: int, float, string, bool, char."""
    def __init__(self, value: Any, literal_type: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.literal_type = literal_type
        self.inferred_type = literal_type
        self.evaluated_value = value

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        val_repr = f'"{self.value}"' if self.literal_type == "string" else str(self.value)
        return f"{prefix}{branch}Literal ({self.literal_type}): {val_repr} (L:{self.line}, C:{self.column})\n"
