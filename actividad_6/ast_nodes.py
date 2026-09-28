"""
================================================================================
ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES
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
    Nodo base del Árbol de Sintaxis Abstracta (AST).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}{self.__class__.__name__}\n"


class ProgramNode(ASTNode):
    """
    Nodo raíz que representa un archivo fuente con clases o declaraciones.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, declarations: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.declarations = declarations

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Programa (Declaraciones: {len(self.declarations)})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, decl in enumerate(self.declarations):
            last = (i == len(self.declarations) - 1)
            res += decl.to_tree_str(new_prefix, last)
        return res


class ClassDeclarationNode(ASTNode):
    """
    Representa una declaración de clase: 'class' identificador '{' cuerpo_clase '}'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, members: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name
        self.members = members

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Clase '{self.name}' (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        if not self.members:
            res += f"{new_prefix}└── (Cuerpo vacío)\n"
        else:
            for i, member in enumerate(self.members):
                last = (i == len(self.members) - 1)
                res += member.to_tree_str(new_prefix, last)
        return res


class ParameterNode(ASTNode):
    """
    Representa un parámetro formal: tipo identificador.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, param_type: str, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.param_type = param_type
        self.name = name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}Parámetro: {self.param_type} {self.name}\n"


class MethodDeclarationNode(ASTNode):
    """
    Representa la declaración de un método: tipo identificador '(' parametros ')' '{' cuerpo_metodo '}'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, return_type: str, name: str, parameters: List[ParameterNode], body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Método: {self.return_type} {self.name}() (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Parámetros
        has_body = len(self.body) > 0
        if not self.parameters:
            res += f"{new_prefix}{'├── ' if has_body else '└── '}Parámetros: (Ninguno)\n"
        else:
            res += f"{new_prefix}{'├── ' if has_body else '└── '}Parámetros ({len(self.parameters)}):\n"
            p_prefix = new_prefix + ("│   " if has_body else "    ")
            for i, p in enumerate(self.parameters):
                last_p = (i == len(self.parameters) - 1)
                res += p.to_tree_str(p_prefix, last_p)

        # Cuerpo del método
        if not self.body:
            res += f"{new_prefix}└── Cuerpo: (Vacío)\n"
        else:
            res += f"{new_prefix}└── Cuerpo ({len(self.body)} sentencias):\n"
            b_prefix = new_prefix + "    "
            for i, stmt in enumerate(self.body):
                last_b = (i == len(self.body) - 1)
                res += stmt.to_tree_str(b_prefix, last_b)

        return res


class VariableDeclarationNode(ASTNode):
    """
    Representa una declaración de variable o campo: tipo identificador ('=' expresion)? ';'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, var_type: str, name: str, initializer: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        init_str = " (Con inicializador)" if self.initializer else ""
        res = f"{prefix}{'└── ' if is_last else '├── '}Variable: {self.var_type} {self.name}{init_str} (L:{self.line}, C:{self.column})\n"
        if self.initializer:
            new_prefix = prefix + ("    " if is_last else "│   ")
            res += self.initializer.to_tree_str(new_prefix, True)
        return res


class AssignmentNode(ASTNode):
    """
    Representa una sentencia de asignación: identificador '=' expresion ';'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, target_name: str, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target_name = target_name
        self.expr = expr

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Asignación: {self.target_name} =\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(new_prefix, True)
        return res


class ReturnNode(ASTNode):
    """
    Representa una sentencia de retorno: 'return' (expresion)? ';'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, expr: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expr = expr

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        if self.expr:
            res = f"{prefix}{'└── ' if is_last else '├── '}Retorno: return (Con valor)\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            res += self.expr.to_tree_str(new_prefix, True)
            return res
        return f"{prefix}{'└── ' if is_last else '├── '}Retorno: return (void)\n"


class IfNode(ASTNode):
    """
    Representa una estructura condicional: 'if' '(' condicion ')' cuerpo ('else' cuerpo)?.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Sentencia IF (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += f"{new_prefix}├── Condición:\n"
        res += self.condition.to_tree_str(new_prefix + "│   ", True)

        has_else = self.else_body is not None
        res += f"{new_prefix}{'├── ' if has_else else '└── '}Bloque Then ({len(self.then_body)} sentencias):\n"
        then_prefix = new_prefix + ("│   " if has_else else "    ")
        for i, stmt in enumerate(self.then_body):
            res += stmt.to_tree_str(then_prefix, i == len(self.then_body) - 1)

        if has_else and self.else_body is not None:
            res += f"{new_prefix}└── Bloque Else ({len(self.else_body)} sentencias):\n"
            for i, stmt in enumerate(self.else_body):
                res += stmt.to_tree_str(new_prefix + "    ", i == len(self.else_body) - 1)
        return res


class WhileNode(ASTNode):
    """
    Representa un ciclo while: 'while' '(' condicion ')' cuerpo.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, condition: ASTNode, body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Ciclo WHILE (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += f"{new_prefix}├── Condición:\n"
        res += self.condition.to_tree_str(new_prefix + "│   ", True)
        res += f"{new_prefix}└── Cuerpo ({len(self.body)} sentencias):\n"
        for i, stmt in enumerate(self.body):
            res += stmt.to_tree_str(new_prefix + "    ", i == len(self.body) - 1)
        return res


class MethodCallNode(ASTNode):
    """
    Representa una llamada a método o función: identificador '(' argumentos ')'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, method_name: str, arguments: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.method_name = method_name
        self.arguments = arguments

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}LlamadaMétodo: {self.method_name}() (Args: {len(self.arguments)})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, arg in enumerate(self.arguments):
            res += arg.to_tree_str(new_prefix, i == len(self.arguments) - 1)
        return res


class BinaryOpNode(ASTNode):
    """
    Operación binaria (aritmética, relacional o lógica).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}OpBinaria: '{self.op}'\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.left.to_tree_str(new_prefix, False)
        res += self.right.to_tree_str(new_prefix, True)
        return res


class UnaryOpNode(ASTNode):
    """
    Operación unaria ('-', '+', '!').

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, op: str, operand: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.op = op
        self.operand = operand

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}OpUnaria: '{self.op}'\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.operand.to_tree_str(new_prefix, True)
        return res


class IdentifierNode(ASTNode):
    """
    Nodo de identificador / variable.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}ID: {self.name}\n"


class LiteralNode(ASTNode):
    """
    Nodo de valor literal (entero, flotante, cadena, booleano, carácter).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, value: Any, lit_type: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.value = value
        self.lit_type = lit_type

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}Literal ({self.lit_type}): {self.value}\n"


class BlockNode(ASTNode):
    """
    Representa un bloque de sentencias delimitado por llaves '{' ... '}'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Bloque (Sentencias: {len(self.statements)})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, stmt in enumerate(self.statements):
            res += stmt.to_tree_str(new_prefix, i == len(self.statements) - 1)
        return res

