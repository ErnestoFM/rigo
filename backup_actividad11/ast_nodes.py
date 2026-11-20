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

from typing import List, Optional, Any


class ASTNode:
    """
    Nodo base del Árbol de Sintaxis Abstracta (AST) con soporte para el patrón Visitor.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column

    def accept(self, visitor: Any) -> Any:
        method_name = f"visit_{self.__class__.__name__}"
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)


class ProgramNode(ASTNode):
    """Nodo raíz con declaraciones de clases, métodos, variables y sentencias."""
    def __init__(self, declarations: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.declarations = declarations


class ClassDeclarationNode(ASTNode):
    """Declaración de clase: 'class Persona { ... }'."""
    def __init__(self, name: str, members: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name
        self.members = members


class ParameterNode(ASTNode):
    """Parámetro formal de método: 'int a'."""
    def __init__(self, type_name: str, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.type_name = type_name
        self.name = name


class MethodDeclarationNode(ASTNode):
    """Declaración de método o función: 'int suma(int a, int b) { ... }'."""
    def __init__(
        self,
        return_type: str,
        name: str,
        parameters: List[ParameterNode],
        body: List[ASTNode],
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body


class VariableDeclarationNode(ASTNode):
    """Declaración de variable con o sin inicializador: 'int i = 0;'."""
    def __init__(
        self,
        type_name: str,
        name: str,
        initializer: Optional[ASTNode] = None,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.type_name = type_name
        self.name = name
        self.initializer = initializer


class AssignmentNode(ASTNode):
    """Asignación de variable o atributo: 'z = x;', 'p.edad = 10;'."""
    def __init__(
        self,
        target: str,
        expr: ASTNode,
        is_field: bool = False,
        obj_name: Optional[str] = None,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.target = target
        self.expr = expr
        self.is_field = is_field
        self.obj_name = obj_name


class IfNode(ASTNode):
    """Estructura condicional 'if (cond) { ... } else { ... }'."""
    def __init__(
        self,
        condition: ASTNode,
        then_block: List[ASTNode],
        else_block: Optional[List[ASTNode]] = None,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class CaseNode(ASTNode):
    """Rama de un switch: 'case valor: body break;'."""
    def __init__(
        self,
        value: ASTNode,
        body: List[ASTNode],
        has_break: bool = True,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.value = value
        self.body = body
        self.has_break = has_break


class SwitchNode(ASTNode):
    """Estructura de selección múltiple 'switch (n) { case ... default ... }'."""
    def __init__(
        self,
        expression: ASTNode,
        cases: List[CaseNode],
        default_block: Optional[List[ASTNode]] = None,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.expression = expression
        self.cases = cases
        self.default_block = default_block


class WhileNode(ASTNode):
    """Bucle 'while (cond) { body }'."""
    def __init__(self, condition: ASTNode, body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


class ForNode(ASTNode):
    """Bucle 'for (init; cond; update) { body }'."""
    def __init__(
        self,
        initializer: Optional[ASTNode],
        condition: Optional[ASTNode],
        update: Optional[ASTNode],
        body: List[ASTNode],
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body


class DoWhileNode(ASTNode):
    """Bucle 'do { body } while (cond);'."""
    def __init__(self, body: List[ASTNode], condition: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.body = body
        self.condition = condition


class ReturnNode(ASTNode):
    """Sentencia 'return expr;'."""
    def __init__(self, expr: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expr = expr


class BreakNode(ASTNode):
    """Sentencia 'break;'."""
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)


class MethodCallNode(ASTNode):
    """Llamada a método o función: 'suma(5, 3)' o 'p.celebrarCumpleaños()'."""
    def __init__(
        self,
        callee: str,
        args: List[ASTNode],
        obj_name: Optional[str] = None,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.callee = callee
        self.args = args
        self.obj_name = obj_name


class NewObjectNode(ASTNode):
    """Instanciación de clase: 'new Persona()'."""
    def __init__(self, class_name: str, args: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.class_name = class_name
        self.args = args


class BinaryOpNode(ASTNode):
    """Operación binaria aritmética, relacional o lógica: 'a + b', 'x > y'."""
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right


class UnaryOpNode(ASTNode):
    """Operación unaria: '-x', '!flag'."""
    def __init__(self, op: str, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.expr = expr


class PostfixOpNode(ASTNode):
    """Operación postfija: 'i++', 'count--'."""
    def __init__(self, var_name: str, op: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.var_name = var_name
        self.op = op


class IdentifierNode(ASTNode):
    """Identificador de variable o atributo: 'x', 'edad'."""
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name


class LiteralNode(ASTNode):
    """Literal numérico, cadena o booleano."""
    def __init__(self, value: Any, type_name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.type_name = type_name


class BlockNode(ASTNode):
    """Bloque de código delimitado por llaves '{ ... }'."""
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements
