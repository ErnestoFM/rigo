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

from typing import List, Optional, Any


class ASTNode:
    """
    Nodo base del Árbol de Sintaxis Abstracta (AST) con soporte para patrón Visitor.

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
        """Patrón Visitor para recorridos de análisis semántico y generación de código."""
        method_name = f"visit_{self.__class__.__name__}"
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}{self.__class__.__name__}\n"


class ProgramNode(ASTNode):
    """
    Nodo raíz que representa un programa con clases, funciones y sentencias.

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
        res = f"{prefix}{'└── ' if is_last else '├── '}Programa (Declaraciones/Sentencias: {len(self.declarations)})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, decl in enumerate(self.declarations):
            last = (i == len(self.declarations) - 1)
            res += decl.to_tree_str(new_prefix, last)
        return res


class ClassDeclarationNode(ASTNode):
    """
    Declaración formal de una clase: 'class' identificador '{' miembros '}'.

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
    Parámetro formal de un método: tipo identificador.

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
    Declaración de un método o función: tipo_retorno identificador '(' parámetros ')' bloque.

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

        has_body = len(self.body) > 0
        if not self.parameters:
            res += f"{new_prefix}{'├── ' if has_body else '└── '}Parámetros: (Ninguno)\n"
        else:
            res += f"{new_prefix}{'├── ' if has_body else '└── '}Parámetros ({len(self.parameters)}):\n"
            p_prefix = new_prefix + ("│   " if has_body else "    ")
            for i, p in enumerate(self.parameters):
                last_p = (i == len(self.parameters) - 1)
                res += p.to_tree_str(p_prefix, last_p)

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
    Declaración de una variable: tipo identificador ('=' expresión)? ';'.

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
    Sentencia de asignación: identificador '=' expresión ';'.

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
        res = f"{prefix}{'└── ' if is_last else '├── '}Asignación: {self.target_name} = (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.expr.to_tree_str(new_prefix, True)
        return res


class ReturnNode(ASTNode):
    """
    Sentencia de retorno: 'return' expresión? ';'.

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
            res = f"{prefix}{'└── ' if is_last else '├── '}Retorno: return (Con valor) (L:{self.line}, C:{self.column})\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            res += self.expr.to_tree_str(new_prefix, True)
            return res
        return f"{prefix}{'└── ' if is_last else '├── '}Retorno: return (void) (L:{self.line}, C:{self.column})\n"


class IfNode(ASTNode):
    """
    Estructura condicional: 'if' '(' condición ')' cuerpo_then ('else' cuerpo_else)?.

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
        res = f"{prefix}{'└── ' if is_last else '├── '}Estructura IF (L:{self.line}, C:{self.column})\n"
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
    Estructura iterativa: 'while' '(' condición ')' cuerpo.

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
        res = f"{prefix}{'└── ' if is_last else '├── '}Estructura WHILE (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += f"{new_prefix}├── Condición:\n"
        res += self.condition.to_tree_str(new_prefix + "│   ", True)
        res += f"{new_prefix}└── Cuerpo ({len(self.body)} sentencias):\n"
        for i, stmt in enumerate(self.body):
            res += stmt.to_tree_str(new_prefix + "    ", i == len(self.body) - 1)
        return res


class TryCatchNode(ASTNode):
    """
    Estructura de manejo de excepciones: 'try' bloque 'catch' '(' error_var ')' bloque.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, try_body: List[ASTNode], error_var: str, catch_body: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.try_body = try_body
        self.error_var = error_var
        self.catch_body = catch_body

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}Estructura TRY-CATCH (L:{self.line}, C:{self.column})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += f"{new_prefix}├── Bloque Try ({len(self.try_body)} sentencias):\n"
        for i, stmt in enumerate(self.try_body):
            res += stmt.to_tree_str(new_prefix + "│   ", i == len(self.try_body) - 1)
        res += f"{new_prefix}└── Bloque Catch (Variable: '{self.error_var}', {len(self.catch_body)} sentencias):\n"
        for i, stmt in enumerate(self.catch_body):
            res += stmt.to_tree_str(new_prefix + "    ", i == len(self.catch_body) - 1)
        return res


class MethodCallNode(ASTNode):
    """
    Llamada a método o función: identificador '(' argumentos ')'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, method_name: str, arguments: List[ASTNode], target_object: Optional[str] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.method_name = method_name
        self.arguments = arguments
        self.target_object = target_object

    def full_name(self) -> str:
        if self.target_object:
            return f"{self.target_object}.{self.method_name}"
        return self.method_name

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        res = f"{prefix}{'└── ' if is_last else '├── '}LlamadaMétodo: {self.full_name()}() (Args: {len(self.arguments)}) (L:{self.line})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, arg in enumerate(self.arguments):
            res += arg.to_tree_str(new_prefix, i == len(self.arguments) - 1)
        return res


class BlockNode(ASTNode):
    """
    Bloque de sentencias delimitado por llaves: '{' sentencias '}'.

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


class BinaryOpNode(ASTNode):
    """
    Operación binaria (aritmética, relacional o lógica): izquierda OP derecha.

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
        res = f"{prefix}{'└── ' if is_last else '├── '}OpBinaria: '{self.op}' (L:{self.line})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.left.to_tree_str(new_prefix, False)
        res += self.right.to_tree_str(new_prefix, True)
        return res


class UnaryOpNode(ASTNode):
    """
    Operación unaria ('-', '+', '!'): OP operando.

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
        res = f"{prefix}{'└── ' if is_last else '├── '}OpUnaria: '{self.op}' (L:{self.line})\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        res += self.operand.to_tree_str(new_prefix, True)
        return res


class PostfixOpNode(ASTNode):
    """
    Operación postfija de incremento o decremento: identificador '++' | '--'.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, target_name: str, op: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.target_name = target_name
        self.op = op

    def to_tree_str(self, prefix: str = "", is_last: bool = True) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}OpPostfija: {self.target_name}{self.op} (L:{self.line})\n"


class IdentifierNode(ASTNode):
    """
    Identificador de variable o atributo: nombre.

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
        return f"{prefix}{'└── ' if is_last else '├── '}Identificador: '{self.name}' (L:{self.line})\n"


class LiteralNode(ASTNode):
    """
    Literal constante de tipo entero, flotante, booleano, cadena o carácter.

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
        return f"{prefix}{'└── ' if is_last else '├── '}Literal [{self.lit_type}]: {repr(self.value)} (L:{self.line})\n"
