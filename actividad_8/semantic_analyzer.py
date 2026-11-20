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

from typing import Optional, Any
from ast_nodes import (
    ASTNode, ProgramNode, VariableDeclarationNode, AssignmentNode,
    BinaryOpNode, UnaryOpNode, CastNode, IdentifierNode, LiteralNode
)
from symbol_table import SymbolTable, Symbol
from semantic_errors import SemanticErrorHandler, SemanticErrorCategory


class SemanticAnalyzer:
    """
    Analizador Semántico especializado en la verificación de tipos de datos
    en expresiones aritméticas, lógicas, relacionales y conversiones de tipo.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    NUMERIC_TYPES = {"int", "float", "double"}

    def __init__(self, symbol_table: Optional[SymbolTable] = None, error_handler: Optional[SemanticErrorHandler] = None):
        self.symbol_table = symbol_table or SymbolTable()
        self.error_handler = error_handler or SemanticErrorHandler()

    def analyze(self, ast: ProgramNode) -> bool:
        self.symbol_table.reset()
        self.error_handler.reset()
        self.visit(ast)
        return not self.error_handler.has_errors

    def visit(self, node: Optional[ASTNode]):
        if node is None:
            return

        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        for attr in dir(node):
            val = getattr(node, attr)
            if isinstance(val, ASTNode):
                self.visit(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, ASTNode):
                        self.visit(item)

    # --------------------------------------------------------------------------
    # Visitantes de Nodos
    # --------------------------------------------------------------------------

    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VariableDeclarationNode(self, node: VariableDeclarationNode):
        init_val = None
        if node.initializer:
            init_type = self.infer_and_validate(node.initializer)
            node.initializer.inferred_type = init_type
            init_val = node.initializer.evaluated_value

            if not self.are_types_compatible(node.var_type, init_type) and init_type != "desconocido":
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.TIPO_INCOMPATIBLE_ASIGNACION,
                    message=f"Error: Tipo de dato incompatible en la inicialización de '{node.name}'. Se esperaba '{node.var_type}' pero se obtuvo '{init_type}'.",
                    suggestion=f"Asegúrese de que el valor inicial coincida con '{node.var_type}' o utilice una conversión de tipo."
                )

        node.inferred_type = node.var_type
        node.evaluated_value = init_val
        self.symbol_table.insert(node.name, node.var_type, init_val, node.line, node.column)

    def visit_AssignmentNode(self, node: AssignmentNode):
        sym = self.symbol_table.lookup(node.target)
        expr_type = self.infer_and_validate(node.expr)
        node.expr.inferred_type = expr_type
        expr_val = node.expr.evaluated_value

        if sym is None:
            self.error_handler.report(
                line=node.line,
                column=node.column,
                category=SemanticErrorCategory.IDENTIFICADOR_NO_DECLARADO,
                message=f"Error: Identificador '{node.target}' no declarado en la línea {node.line}, columna {node.column}.",
                suggestion=f"Declare la variable '{node.target}' antes de asignarle un valor."
            )
            node.inferred_type = "desconocido"
            return

        target_type = sym.data_type
        node.inferred_type = target_type
        node.evaluated_value = expr_val

        if not self.are_types_compatible(target_type, expr_type) and expr_type != "desconocido":
            self.error_handler.report(
                line=node.line,
                column=node.column,
                category=SemanticErrorCategory.TIPO_INCOMPATIBLE_ASIGNACION,
                message=f"Error: Tipo de dato incompatible en la asignación a '{node.target}'. No se puede asignar '{expr_type}' a una variable de tipo '{target_type}'.",
                suggestion=f"Convierta la expresión al tipo '{target_type}' o verifique los operandos.",
                operator=node.op
            )
        else:
            if expr_val is not None:
                self.symbol_table.update_value(node.target, expr_val)

    # --------------------------------------------------------------------------
    # Inferencia, Validación y Evaluación de Expresiones
    # --------------------------------------------------------------------------

    def are_types_compatible(self, expected: str, actual: str) -> bool:
        if expected == actual:
            return True
        if expected in ("float", "double") and actual in ("float", "double"):
            return True
        return False

    def infer_and_validate(self, expr: ASTNode) -> str:
        """Infiere el tipo de una expresión y valida todas las reglas semánticas asociadas."""
        if isinstance(expr, LiteralNode):
            expr.inferred_type = expr.literal_type
            expr.evaluated_value = expr.value
            return expr.literal_type

        if isinstance(expr, IdentifierNode):
            sym = self.symbol_table.lookup(expr.name)
            if sym is None:
                self.error_handler.report(
                    line=expr.line,
                    column=expr.column,
                    category=SemanticErrorCategory.IDENTIFICADOR_NO_DECLARADO,
                    message=f"Error: Identificador '{expr.name}' no declarado en la línea {expr.line}, columna {expr.column}.",
                    suggestion=f"Declare '{expr.name}' antes de referenciarlo en expresiones."
                )
                expr.inferred_type = "desconocido"
                return "desconocido"
            expr.inferred_type = sym.data_type
            expr.evaluated_value = sym.value
            return sym.data_type

        if isinstance(expr, CastNode):
            source_type = self.infer_and_validate(expr.expr)
            target_type = expr.target_type

            # Validar conversiones válidas (int <-> float, etc.)
            if source_type == "string" and target_type in self.NUMERIC_TYPES:
                self.error_handler.report(
                    line=expr.line,
                    column=expr.column,
                    category=SemanticErrorCategory.CONVERSION_INVALIDA,
                    message=f"Error: Conversión de tipo inválida de 'string' a '{target_type}' en la línea {expr.line}, columna {expr.column}.",
                    suggestion="No es posible convertir directamente una cadena de texto a un tipo numérico mediante static_cast."
                )
                expr.inferred_type = "desconocido"
                return "desconocido"

            expr.inferred_type = target_type
            # Evaluar conversión si el valor origen es conocido
            if expr.expr.evaluated_value is not None:
                try:
                    if target_type == "float" or target_type == "double":
                        expr.evaluated_value = float(expr.expr.evaluated_value)
                    elif target_type == "int":
                        expr.evaluated_value = int(expr.expr.evaluated_value)
                    elif target_type == "bool":
                        expr.evaluated_value = bool(expr.expr.evaluated_value)
                except Exception:
                    expr.evaluated_value = None
            return target_type

        if isinstance(expr, BinaryOpNode):
            return self._validate_binary_op(expr)

        if isinstance(expr, UnaryOpNode):
            return self._validate_unary_op(expr)

        return "desconocido"

    def _validate_binary_op(self, node: BinaryOpNode) -> str:
        left_t = self.infer_and_validate(node.left)
        right_t = self.infer_and_validate(node.right)
        op = node.op

        if left_t == "desconocido" or right_t == "desconocido":
            node.inferred_type = "desconocido"
            return "desconocido"

        # 1. Operadores Aritméticos: +, -, *, /, %
        if op in ("+", "-", "*", "/", "%"):
            # Regla: operandos deben ser numéricos
            if left_t == "string" or right_t == "string":
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.OPERACION_NO_NUMERICA,
                    message=f"Error: No se puede aplicar el operador aritmético '{op}' con una cadena de texto (operandos: '{left_t}' y '{right_t}') en la línea {node.line}, columna {node.column}.",
                    suggestion="Asegúrese de que ambos operandos sean numéricos (enteros o flotantes) y no cadenas de texto.",
                    operator=op
                )
                node.inferred_type = "desconocido"
                return "desconocido"

            if left_t == "bool" or right_t == "bool":
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.OPERACION_NO_NUMERICA,
                    message=f"Error: No se puede aplicar el operador aritmético '{op}' con un valor booleano en la línea {node.line}, columna {node.column}.",
                    suggestion="Los operadores aritméticos solo deben aplicarse a operandos numéricos.",
                    operator=op
                )
                node.inferred_type = "desconocido"
                return "desconocido"

            # Detección de división por cero
            if op in ("/", "%"):
                r_val = node.right.evaluated_value
                if r_val is not None and r_val == 0:
                    self.error_handler.report(
                        line=node.line,
                        column=node.column,
                        category=SemanticErrorCategory.DIVISION_POR_CERO,
                        message=f"Error: División por cero detectada en tiempo de compilación con el operador '{op}' en la línea {node.line}, columna {node.column}.",
                        suggestion="El denominador de una división o módulo no puede ser cero.",
                        operator=op
                    )

            # Promoción de tipo: si alguno es float, resultado es float
            res_type = "float" if (left_t in ("float", "double") or right_t in ("float", "double")) else "int"
            node.inferred_type = res_type

            # Evaluación constante si ambos valores están disponibles
            l_val = node.left.evaluated_value
            r_val = node.right.evaluated_value
            if l_val is not None and r_val is not None:
                try:
                    if op == "+": node.evaluated_value = l_val + r_val
                    elif op == "-": node.evaluated_value = l_val - r_val
                    elif op == "*": node.evaluated_value = l_val * r_val
                    elif op == "/" and r_val != 0:
                        node.evaluated_value = (l_val / r_val) if res_type == "float" else (l_val // r_val)
                    elif op == "%" and r_val != 0: node.evaluated_value = l_val % r_val
                except Exception:
                    node.evaluated_value = None

            return res_type

        # 2. Operadores Lógicos: &&, ||
        if op in ("&&", "||"):
            if left_t != "bool":
                self.error_handler.report(
                    line=node.left.line,
                    column=node.left.column,
                    category=SemanticErrorCategory.OPERANDO_LOGICO_NO_BOOLEANO,
                    message=f"Error: El operador lógico '{op}' requiere operandos booleanos. El operando izquierdo es de tipo '{left_t}' en la línea {node.line}, columna {node.column}.",
                    suggestion=f"Asegúrese de que el operando izquierdo sea de tipo booleano (bool) y no '{left_t}'.",
                    operator=op
                )
            if right_t != "bool":
                self.error_handler.report(
                    line=node.right.line,
                    column=node.right.column,
                    category=SemanticErrorCategory.OPERANDO_LOGICO_NO_BOOLEANO,
                    message=f"Error: El operador lógico '{op}' requiere operandos booleanos. El operando derecho es de tipo '{right_t}' en la línea {node.line}, columna {node.column}.",
                    suggestion=f"Asegúrese de que el operando derecho sea de tipo booleano (bool) y no '{right_t}'.",
                    operator=op
                )

            node.inferred_type = "bool"
            l_val = node.left.evaluated_value
            r_val = node.right.evaluated_value
            if l_val is not None and r_val is not None and left_t == "bool" and right_t == "bool":
                if op == "&&": node.evaluated_value = bool(l_val and r_val)
                elif op == "||": node.evaluated_value = bool(l_val or r_val)
            return "bool"

        # 3. Operadores Relacionales / Comparación: ==, !=, <, >, <=, >=
        if op in ("==", "!=", "<", ">", "<=", ">="):
            # Prohibir comparar cadenas con números
            if (left_t == "string" and right_t in self.NUMERIC_TYPES) or (right_t == "string" and left_t in self.NUMERIC_TYPES):
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.COMPARACION_INCOMPATIBLE,
                    message=f"Error: No se puede comparar una cadena con un número mediante '{op}' en la línea {node.line}, columna {node.column}.",
                    suggestion="Las comparaciones deben realizarse entre tipos compatibles (números con números, o cadenas con cadenas).",
                    operator=op
                )
            elif (left_t == "bool" and right_t in self.NUMERIC_TYPES) or (right_t == "bool" and left_t in self.NUMERIC_TYPES):
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.COMPARACION_INCOMPATIBLE,
                    message=f"Error: No se puede comparar un valor booleano con un número mediante '{op}' en la línea {node.line}, columna {node.column}.",
                    suggestion="Compare valores booleanos exclusivamente con otros valores booleanos.",
                    operator=op
                )

            node.inferred_type = "bool"
            l_val = node.left.evaluated_value
            r_val = node.right.evaluated_value
            if l_val is not None and r_val is not None:
                try:
                    if op == "==": node.evaluated_value = bool(l_val == r_val)
                    elif op == "!=": node.evaluated_value = bool(l_val != r_val)
                    elif op == "<": node.evaluated_value = bool(l_val < r_val)
                    elif op == ">": node.evaluated_value = bool(l_val > r_val)
                    elif op == "<=": node.evaluated_value = bool(l_val <= r_val)
                    elif op == ">=": node.evaluated_value = bool(l_val >= r_val)
                except Exception:
                    node.evaluated_value = None
            return "bool"

        return "desconocido"

    def _validate_unary_op(self, node: UnaryOpNode) -> str:
        op_t = self.infer_and_validate(node.operand)
        op = node.op

        if op_t == "desconocido":
            node.inferred_type = "desconocido"
            return "desconocido"

        if op == "!":
            if op_t != "bool":
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.OPERANDO_LOGICO_NO_BOOLEANO,
                    message=f"Error: El operador unario de negación lógica '!' requiere un operando booleano (recibió '{op_t}') en la línea {node.line}, columna {node.column}.",
                    suggestion="Aplique '!' únicamente sobre expresiones o variables booleanas.",
                    operator=op
                )
            node.inferred_type = "bool"
            if node.operand.evaluated_value is not None and op_t == "bool":
                node.evaluated_value = not bool(node.operand.evaluated_value)
            return "bool"

        if op in ("+", "-"):
            if op_t not in self.NUMERIC_TYPES:
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.OPERACION_NO_NUMERICA,
                    message=f"Error: El operador unario '{op}' solo puede aplicarse a operandos numéricos (recibió '{op_t}') en la línea {node.line}, columna {node.column}.",
                    suggestion="Asegúrese de que el operando sea un número entero o flotante.",
                    operator=op
                )
            node.inferred_type = op_t
            if node.operand.evaluated_value is not None and op_t in self.NUMERIC_TYPES:
                node.evaluated_value = -node.operand.evaluated_value if op == "-" else node.operand.evaluated_value
            return op_t

        node.inferred_type = op_t
        return op_t
