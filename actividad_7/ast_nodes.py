"""
================================================================================
ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
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
    Clase base para todos los nodos del Árbol de Sintaxis Abstracta (AST).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column
        self.inferred_type: Optional[str] = None  # Tipo inferido durante el análisis semántico

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        raise NotImplementedError


class ProgramNode(ASTNode):
    """Nodo raíz del programa C."""
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Programa ({len(self.statements)} declaraciones/sentencias)\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, stmt in enumerate(self.statements):
            last = (i == len(self.statements) - 1)
            res += stmt.to_tree_str(new_prefix, last)
        return res


class BlockNode(ASTNode):
    """Bloque de sentencias entre llaves '{' y '}'."""
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Bloque {{...}} ({len(self.statements)} sentencias)\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, stmt in enumerate(self.statements):
            last = (i == len(self.statements) - 1)
            res += stmt.to_tree_str(new_prefix, last)
        return res


class VariableDeclarationNode(ASTNode):
    """Declaración de variable: tipo nombre ('=' inicializador)? ';'"""
    def __init__(self, var_type: str, name: str, initializer: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_ann = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        init_info = " (Con inicializador)" if self.initializer else ""
        res = f"{prefix}{branch}Declaración: {self.var_type} {self.name}{init_info}{type_ann} (L:{self.line}, C:{self.column})\n"
        if self.initializer:
            new_prefix = prefix + ("    " if is_last else "│   ")
            res += self.initializer.to_tree_str(new_prefix, True)
        return res


class AssignmentNode(ASTNode):
    """Sentencia de asignación: destino '=' expresion ';'"""
    def __init__(self, target: str, expr: ASTNode, op: str = "=", line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target = target
        self.expr = expr
        self.op = op

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_ann = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        res = f"{prefix}{branch}Asignación: {self.target} {self.op}{type_ann} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(new_prefix, True)
        return res


class FunctionNode(ASTNode):
    """Definición de función: tipo_retorno nombre '(' params ')' bloque"""
    def __init__(
        self,
        return_type: str,
        name: str,
        params: List[Tuple[str, str]],  # List[(tipo, nombre)]
        body: BlockNode,
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        params_str = ", ".join(f"{ptype} {pname}" for ptype, pname in self.params) if self.params else "void"
        res = f"{prefix}{branch}Función '{self.name}' -> {self.return_type}({params_str}) (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.body.to_tree_str(new_prefix, True)
        return res


class IfNode(ASTNode):
    """Estructura condicional 'if' '(' cond ')' bloque ('else' bloque)?"""
    def __init__(self, condition: ASTNode, then_block: BlockNode, else_block: Optional[BlockNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        has_else = self.else_block is not None
        res = f"{prefix}{branch}Estructura 'if' (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += f"{new_prefix}├── Condición:\n"
        res += self.condition.to_tree_str(new_prefix + "│   ", True)
        res += f"{new_prefix}{'├── ' if has_else else '└── '}Bloque Then:\n"
        res += self.then_block.to_tree_str(new_prefix + ("│   " if has_else else "    "), True)
        if has_else and self.else_block:
            res += f"{new_prefix}└── Bloque Else:\n"
            res += self.else_block.to_tree_str(new_prefix + "    ", True)
        return res


class WhileNode(ASTNode):
    """Bucle 'while' '(' cond ')' bloque"""
    def __init__(self, condition: ASTNode, body: BlockNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Estructura 'while' (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += f"{new_prefix}├── Condición:\n"
        res += self.condition.to_tree_str(new_prefix + "│   ", True)
        res += f"{new_prefix}└── Cuerpo:\n"
        res += self.body.to_tree_str(new_prefix + "    ", True)
        return res


class ForNode(ASTNode):
    """Bucle 'for' '(' init ';' cond ';' update ')' bloque"""
    def __init__(self, init: Optional[ASTNode], condition: Optional[ASTNode], update: Optional[ASTNode], body: BlockNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Estructura 'for' (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        if self.init:
            res += f"{new_prefix}├── Init:\n" + self.init.to_tree_str(new_prefix + "│   ", True)
        if self.condition:
            res += f"{new_prefix}├── Cond:\n" + self.condition.to_tree_str(new_prefix + "│   ", True)
        if self.update:
            res += f"{new_prefix}├── Update:\n" + self.update.to_tree_str(new_prefix + "│   ", True)
        res += f"{new_prefix}└── Cuerpo:\n" + self.body.to_tree_str(new_prefix + "    ", True)
        return res


class ReturnNode(ASTNode):
    """Sentencia 'return' expr? ';'"""
    def __init__(self, value: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Sentencia 'return' (L:{self.line}, C:{self.column})\n"
        if self.value:
            new_prefix = prefix + ("    " if is_last else "│   ")
            res += self.value.to_tree_str(new_prefix, True)
        return res


class BinaryOpNode(ASTNode):
    """Operación binaria: izquierda OP derecha"""
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_ann = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        res = f"{prefix}{branch}Op Binaria '{self.op}'{type_ann} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.left.to_tree_str(new_prefix, False)
        res += self.right.to_tree_str(new_prefix, True)
        return res


class UnaryOpNode(ASTNode):
    """Operación unaria: OP operando o operando OP"""
    def __init__(self, op: str, operand: ASTNode, is_postfix: bool = False, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.operand = operand
        self.is_postfix = is_postfix

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        tipo = "Postfija" if self.is_postfix else "Prefija"
        type_ann = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        res = f"{prefix}{branch}Op Unaria {tipo} '{self.op}'{type_ann} (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.operand.to_tree_str(new_prefix, True)
        return res


class IdentifierNode(ASTNode):
    """Identificador / variable"""
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        type_ann = f" [Tipo: {self.inferred_type}]" if self.inferred_type else ""
        return f"{prefix}{branch}Identificador: {self.name}{type_ann} (L:{self.line}, C:{self.column})\n"


class LiteralNode(ASTNode):
    """Valor literal (int, float, string, char, bool)"""
    def __init__(self, value: Any, literal_type: str = "int", line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.literal_type = literal_type
        self.inferred_type = literal_type

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        return f"{prefix}{branch}Literal ({self.literal_type}): {self.value} (L:{self.line}, C:{self.column})\n"


class CallNode(ASTNode):
    """Llamada a función: nombre '(' args ')'"""
    def __init__(self, callee: str, args: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.callee = callee
        self.args = args

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        res = f"{prefix}{branch}Llamada a Función: {self.callee}() (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, arg in enumerate(self.args):
            last = (i == len(self.args) - 1)
            res += arg.to_tree_str(new_prefix, last)
        return res


class ErrorNode(ASTNode):
    """Nodo marcador de error sintáctico"""
    def __init__(self, error_message: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.error_message = error_message

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        branch = "└── " if is_last else "├── "
        return f"{prefix}{branch}❌ ErrorSintáctico: {self.error_message} (L:{self.line}, C:{self.column})\n"
