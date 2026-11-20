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

from typing import List, Optional, Any


class ASTNode:
    """
    Nodo base del Árbol de Sintaxis Abstracta (AST) con soporte para recorrido
    y visualización jerárquica en árbol de texto.

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

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}{self.__class__.__name__}\n"


class ProgramNode(ASTNode):
    def __init__(self, declarations: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.declarations = declarations

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Programa (Nodos: {len(self.declarations)})\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, decl in enumerate(self.declarations):
            last = (i == len(self.declarations) - 1)
            res += decl.to_tree_str(child_prefix, last)
        return res


class ClassDeclarationNode(ASTNode):
    def __init__(self, name: str, members: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name
        self.members = members

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Clase '{self.name}'\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, mem in enumerate(self.members):
            last = (i == len(self.members) - 1)
            res += mem.to_tree_str(child_prefix, last)
        return res


class ParameterNode(ASTNode):
    def __init__(self, type_name: str, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.type_name = type_name
        self.name = name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}Parámetro: {self.type_name} {self.name}\n"


class MethodDeclarationNode(ASTNode):
    def __init__(self, return_type: str, name: str, parameters: List[ParameterNode], body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        params_str = ", ".join(f"{p.type_name} {p.name}" for p in self.parameters)
        res = f"{prefix}{marker}Método '{self.return_type} {self.name}({params_str})'\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, stmt in enumerate(self.body):
            last = (i == len(self.body) - 1)
            res += stmt.to_tree_str(child_prefix, last)
        return res


class VariableDeclarationNode(ASTNode):
    def __init__(self, type_name: str, name: str, initializer: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.type_name = type_name
        self.name = name
        self.initializer = initializer

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Declaración Var: {self.type_name} {self.name}\n"
        if self.initializer:
            child_prefix = prefix + ("    " if is_last else "│   ")
            res += self.initializer.to_tree_str(child_prefix, True)
        return res


class AssignmentNode(ASTNode):
    def __init__(self, target: str, expr: ASTNode, is_field: bool = False, obj_name: Optional[str] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.expr = expr
        self.is_field = is_field
        self.obj_name = obj_name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        tgt = f"{self.obj_name}.{self.target}" if self.is_field and self.obj_name else self.target
        res = f"{prefix}{marker}Asignación: {tgt} =\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(child_prefix, True)
        return res


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_block: List[ASTNode], else_block: Optional[List[ASTNode]] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Sentencia IF\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.condition.to_tree_str(child_prefix, False)
        for s in self.then_block:
            res += s.to_tree_str(child_prefix, False)
        if self.else_block:
            for s in self.else_block:
                res += s.to_tree_str(child_prefix, True)
        return res


class CaseNode(ASTNode):
    def __init__(self, value: ASTNode, body: List[ASTNode], has_break: bool = True, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.body = body
        self.has_break = has_break

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Rama CASE\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.value.to_tree_str(child_prefix, False)
        for s in self.body:
            res += s.to_tree_str(child_prefix, True)
        return res


class SwitchNode(ASTNode):
    def __init__(self, expression: ASTNode, cases: List[CaseNode], default_block: Optional[List[ASTNode]] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expression = expression
        self.cases = cases
        self.default_block = default_block

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Sentencia SWITCH\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expression.to_tree_str(child_prefix, False)
        for c in self.cases:
            res += c.to_tree_str(child_prefix, False)
        if self.default_block:
            for s in self.default_block:
                res += s.to_tree_str(child_prefix, True)
        return res


class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Bucle WHILE\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.condition.to_tree_str(child_prefix, False)
        for s in self.body:
            res += s.to_tree_str(child_prefix, True)
        return res


class ForNode(ASTNode):
    def __init__(self, initializer: Optional[ASTNode], condition: Optional[ASTNode], update: Optional[ASTNode], body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Bucle FOR\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        if self.initializer:
            res += self.initializer.to_tree_str(child_prefix, False)
        if self.condition:
            res += self.condition.to_tree_str(child_prefix, False)
        if self.update:
            res += self.update.to_tree_str(child_prefix, False)
        for s in self.body:
            res += s.to_tree_str(child_prefix, True)
        return res


class DoWhileNode(ASTNode):
    def __init__(self, body: List[ASTNode], condition: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.body = body
        self.condition = condition

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Bucle DO-WHILE\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        for s in self.body:
            res += s.to_tree_str(child_prefix, False)
        res += self.condition.to_tree_str(child_prefix, True)
        return res


class ReturnNode(ASTNode):
    def __init__(self, expr: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expr = expr

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}RETURN\n"
        if self.expr:
            child_prefix = prefix + ("    " if is_last else "│   ")
            res += self.expr.to_tree_str(child_prefix, True)
        return res


class BreakNode(ASTNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}BREAK\n"


class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expr = expr

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}PRINT\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(child_prefix, True)
        return res


class MethodCallNode(ASTNode):
    def __init__(self, callee: str, args: List[ASTNode], obj_name: Optional[str] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.callee = callee
        self.args = args
        self.obj_name = obj_name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        name = f"{self.obj_name}.{self.callee}" if self.obj_name else self.callee
        res = f"{prefix}{marker}Llamada Método: {name}()\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, a in enumerate(self.args):
            last = (i == len(self.args) - 1)
            res += a.to_tree_str(child_prefix, last)
        return res


class NewObjectNode(ASTNode):
    def __init__(self, class_name: str, args: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.class_name = class_name
        self.args = args

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}Instanciación NEW {self.class_name}()\n"


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Operación Binaria '{self.op}'\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.left.to_tree_str(child_prefix, False)
        res += self.right.to_tree_str(child_prefix, True)
        return res


class UnaryOpNode(ASTNode):
    def __init__(self, op: str, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.expr = expr

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Operación Unaria '{self.op}'\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(child_prefix, True)
        return res


class PostfixOpNode(ASTNode):
    def __init__(self, var_name: str, op: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.var_name = var_name
        self.op = op

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}Postfijo: {self.var_name}{self.op}\n"


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}Identificador: '{self.name}'\n"


class LiteralNode(ASTNode):
    def __init__(self, value: Any, type_name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.type_name = type_name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        return f"{prefix}{marker}Literal ({self.type_name}): {self.value}\n"


class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        marker = "└── " if is_last else "├── "
        res = f"{prefix}{marker}Bloque ({len(self.statements)} sentencias)\n"
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, s in enumerate(self.statements):
            last = (i == len(self.statements) - 1)
            res += s.to_tree_str(child_prefix, last)
        return res
