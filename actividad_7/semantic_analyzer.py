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

from typing import Optional, Any
from ast_nodes import (
    ASTNode, ProgramNode, BlockNode, VariableDeclarationNode, AssignmentNode,
    FunctionNode, IfNode, WhileNode, ForNode, ReturnNode, BinaryOpNode,
    UnaryOpNode, IdentifierNode, LiteralNode, CallNode, ErrorNode
)
from symbol_table import SymbolTable, Symbol
from semantic_errors import SemanticErrorHandler, SemanticErrorCategory


class SemanticAnalyzer:
    """
    Analizador Semántico para C.
    Verifica la coherencia de tipos de datos en declaraciones y asignaciones,
    administra la tabla de símbolos jerárquica con ámbitos (global y locales),
    y detecta identificadores no declarados o redeclarados en el mismo ámbito.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, symbol_table: Optional[SymbolTable] = None, error_handler: Optional[SemanticErrorHandler] = None):
        self.symbol_table = symbol_table or SymbolTable()
        self.error_handler = error_handler or SemanticErrorHandler()
        self.current_function_return_type: Optional[str] = None

    def analyze(self, ast: ProgramNode) -> bool:
        """
        Ejecuta el análisis semántico sobre el AST completo.
        Retorna True si no se hallaron inconsistencias semánticas, False en caso contrario.
        """
        self.symbol_table.reset()
        self.error_handler.reset()
        self.visit(ast)
        return not self.error_handler.has_errors

    def visit(self, node: Optional[ASTNode]):
        """Despachador dinámico de nodos AST."""
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
        """
        Maneja declaraciones de variables:
        - Inserción en la tabla de símbolos.
        - Detección de colisión (redeclaración en el mismo ámbito).
        - Verificación de tipos en la inicialización (si existe).
        """
        # 1. Verificar si ya fue declarada en el ámbito actual
        existing = self.symbol_table.current_scope.lookup_current(node.name)
        if existing:
            self.error_handler.report(
                line=node.line,
                column=node.column,
                category=SemanticErrorCategory.VARIABLE_YA_DECLARADA,
                message=f"Error: El identificador '{node.name}' ya fue declarado previamente en el ámbito '{self.symbol_table.current_scope.name}' (línea {existing.line}).",
                suggestion=f"Utilice un nombre distinto o evite redeclarar '{node.name}' en el mismo bloque.",
                identifier=node.name,
                scope_name=self.symbol_table.current_scope.name
            )
            return

        # 2. Evaluar inicializador si está presente
        init_val = None
        if node.initializer:
            init_type = self.infer_type(node.initializer)
            node.initializer.inferred_type = init_type

            if not self.are_types_compatible(node.var_type, init_type) and init_type != "desconocido":
                self.error_handler.report(
                    line=node.line,
                    column=node.column,
                    category=SemanticErrorCategory.TIPO_INCOMPATIBLE_ASIGNACION,
                    message=f"Error: Tipo de dato incompatible en la inicialización de '{node.name}' en la línea {node.line}, columna {node.column}. Se esperaba '{node.var_type}' pero se obtuvo '{init_type}'.",
                    suggestion=f"Asigne una expresión de tipo '{node.var_type}' o realice una conversión explícita.",
                    identifier=node.name,
                    scope_name=self.symbol_table.current_scope.name
                )
            init_val = self.evaluate_const_expr(node.initializer)

        # 3. Registrar en la tabla de símbolos mediante la función inserten_simbolo
        success, sym = self.symbol_table.inserten_simbolo(
            identificador=node.name,
            tipo_de_dato=node.var_type,
            alcance=self.symbol_table.current_scope.scope_type,
            valor=init_val,
            linea=node.line,
            columna=node.column
        )
        node.inferred_type = node.var_type

    def visit_FunctionNode(self, node: FunctionNode):
        """
        Maneja definiciones de funciones:
        - Registro del prototipo de función en el ámbito padre (usualmente global).
        - Creación de un nuevo ámbito local con el nombre de la función.
        - Inserción de los parámetros formales en el nuevo ámbito.
        - Análisis de las sentencias del cuerpo.
        """
        # Registrar función en el ámbito actual
        success, sym = self.symbol_table.inserten_simbolo(
            identificador=node.name,
            tipo_de_dato=node.return_type,
            alcance=self.symbol_table.current_scope.scope_type,
            valor=f"func_{node.name}",
            linea=node.line,
            columna=node.column,
            is_function=True,
            params=node.params
        )

        prev_func_ret = self.current_function_return_type
        self.current_function_return_type = node.return_type

        # Entrar al nuevo ámbito local de la función
        self.symbol_table.enter_scope(name=node.name, scope_type="local")

        # Insertar parámetros como variables locales del ámbito
        for ptype, pname in node.params:
            self.symbol_table.inserten_simbolo(
                identificador=pname,
                tipo_de_dato=ptype,
                alcance="local",
                valor="(parametro)",
                linea=node.line,
                columna=node.column
            )

        # Analizar el cuerpo de la función
        self.visit(node.body)

        # Salir del ámbito local
        self.symbol_table.exit_scope()
        self.current_function_return_type = prev_func_ret

    def visit_BlockNode(self, node: BlockNode):
        """Visita las sentencias contenidas en un bloque de llaves."""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_AssignmentNode(self, node: AssignmentNode):
        """
        Maneja asignaciones de variables (target = expr):
        - Búsqueda del identificador con busquen_simbolo (ámbito local -> global).
        - Si no existe: reporta 'Identificador No Declarado'.
        - Verificación estricta de compatibilidad de tipos entre destino y expresión.
        - Actualización del valor en la tabla de símbolos si es constante evaluable.
        """
        # 1. Búsqueda en la tabla de símbolos
        symbol = self.symbol_table.busquen_simbolo(node.target)
        expr_type = self.infer_type(node.expr)
        node.expr.inferred_type = expr_type

        if symbol is None:
            self.error_handler.report(
                line=node.line,
                column=node.column,
                category=SemanticErrorCategory.IDENTIFICADOR_NO_DECLARADO,
                message=f"Error: Identificador '{node.target}' no declarado en la línea {node.line}, columna {node.column}.",
                suggestion=f"Declare la variable '{node.target}' antes de asignarle un valor (ejemplo: int {node.target};).",
                identifier=node.target,
                scope_name=self.symbol_table.current_scope.name
            )
            node.inferred_type = "desconocido"
            return

        # 2. Verificación de compatibilidad de tipos
        target_type = symbol.data_type
        node.inferred_type = target_type

        if not self.are_types_compatible(target_type, expr_type) and expr_type != "desconocido":
            self.error_handler.report(
                line=node.line,
                column=node.column,
                category=SemanticErrorCategory.TIPO_INCOMPATIBLE_ASIGNACION,
                message=f"Error: Tipo de dato incompatible en la asignación a '{node.target}' en la línea {node.line}, columna {node.column}. Se esperaba '{target_type}' pero se obtuvo '{expr_type}'.",
                suggestion=f"No es posible asignar un valor de tipo '{expr_type}' a una variable de tipo '{target_type}'.",
                identifier=node.target,
                scope_name=self.symbol_table.current_scope.name
            )
        else:
            # 3. Actualizar valor si es evaluable
            val = self.evaluate_const_expr(node.expr)
            if val is not None:
                self.symbol_table.update_symbol_value(node.target, val)

    def visit_IfNode(self, node: IfNode):
        cond_type = self.infer_type(node.condition)
        node.condition.inferred_type = cond_type
        self.visit(node.then_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_WhileNode(self, node: WhileNode):
        cond_type = self.infer_type(node.condition)
        node.condition.inferred_type = cond_type
        self.visit(node.body)

    def visit_ForNode(self, node: ForNode):
        if node.init:
            self.visit(node.init)
        if node.condition:
            self.infer_type(node.condition)
        if node.update:
            self.visit(node.update)
        self.visit(node.body)

    def visit_ReturnNode(self, node: ReturnNode):
        if node.value:
            ret_type = self.infer_type(node.value)
            node.value.inferred_type = ret_type
            if self.current_function_return_type:
                if not self.are_types_compatible(self.current_function_return_type, ret_type) and ret_type != "desconocido":
                    self.error_handler.report(
                        line=node.line,
                        column=node.column,
                        category=SemanticErrorCategory.TIPO_INCOMPATIBLE_ASIGNACION,
                        message=f"Error: Tipo de retorno incompatible en la línea {node.line}, columna {node.column}. La función espera '{self.current_function_return_type}' pero retorna '{ret_type}'.",
                        suggestion=f"Retorne una expresión compatible con '{self.current_function_return_type}'.",
                        scope_name=self.symbol_table.current_scope.name
                    )

    # --------------------------------------------------------------------------
    # Inferencia y Comprobación de Tipos
    # --------------------------------------------------------------------------

    def are_types_compatible(self, expected: str, actual: str) -> bool:
        """
        Regla estricta de compatibilidad de tipos exigida en la rúbrica oficial:
        - int x; float y = 3.5; x = y; -> Error: Asignación de float a int
        - float b; b = a; -> Error: Asignación de int a float
        Por tanto, se requiere equivalencia de tipo estricta para evitar coerción silenciosa.
        """
        if expected == actual:
            return True
        if expected in ("double", "float") and actual in ("double", "float"):
            return True
        return False

    def infer_type(self, expr: ASTNode) -> str:
        """Determina el tipo resultante de una expresión sintáctica."""
        if isinstance(expr, LiteralNode):
            expr.inferred_type = expr.literal_type
            return expr.literal_type

        if isinstance(expr, IdentifierNode):
            sym = self.symbol_table.busquen_simbolo(expr.name)
            if sym is None:
                self.error_handler.report(
                    line=expr.line,
                    column=expr.column,
                    category=SemanticErrorCategory.IDENTIFICADOR_NO_DECLARADO,
                    message=f"Error: Identificador '{expr.name}' no declarado en la línea {expr.line}, columna {expr.column}.",
                    suggestion=f"Declare la variable '{expr.name}' antes de utilizarla en expresiones.",
                    identifier=expr.name,
                    scope_name=self.symbol_table.current_scope.name
                )
                expr.inferred_type = "desconocido"
                return "desconocido"
            expr.inferred_type = sym.data_type
            return sym.data_type

        if isinstance(expr, BinaryOpNode):
            left_t = self.infer_type(expr.left)
            right_t = self.infer_type(expr.right)

            if left_t == "desconocido" or right_t == "desconocido":
                expr.inferred_type = "desconocido"
                return "desconocido"

            # Operadores relacionales / lógicos: generan int (booleano en C)
            if expr.op in ("<", ">", "<=", ">=", "==", "!=", "&&", "||"):
                if not self.are_types_compatible(left_t, right_t):
                    self.error_handler.report(
                        line=expr.line,
                        column=expr.column,
                        category=SemanticErrorCategory.TIPO_INCOMPATIBLE_EXPRESION,
                        message=f"Error: Comparación entre tipos incompatibles ('{left_t}' y '{right_t}') con operador '{expr.op}' en la línea {expr.line}, columna {expr.column}.",
                        suggestion="Compare variables del mismo tipo numérico o realice conversión explícita.",
                        scope_name=self.symbol_table.current_scope.name
                    )
                expr.inferred_type = "int"
                return "int"

            # Operadores aritméticos (+, -, *, /, %)
            if not self.are_types_compatible(left_t, right_t):
                self.error_handler.report(
                    line=expr.line,
                    column=expr.column,
                    category=SemanticErrorCategory.TIPO_INCOMPATIBLE_EXPRESION,
                    message=f"Error: Operación aritmética incompatible entre tipos '{left_t}' y '{right_t}' con operador '{expr.op}' en la línea {expr.line}, columna {expr.column}.",
                    suggestion="Ambos operandos deben ser del mismo tipo para asegurar operaciones válidas.",
                    scope_name=self.symbol_table.current_scope.name
                )
                expr.inferred_type = "desconocido"
                return "desconocido"

            expr.inferred_type = left_t
            return left_t

        if isinstance(expr, UnaryOpNode):
            op_t = self.infer_type(expr.operand)
            expr.inferred_type = op_t
            return op_t

        if isinstance(expr, CallNode):
            sym = self.symbol_table.busquen_simbolo(expr.callee)
            if sym is None:
                self.error_handler.report(
                    line=expr.line,
                    column=expr.column,
                    category=SemanticErrorCategory.IDENTIFICADOR_NO_DECLARADO,
                    message=f"Error: Función '{expr.callee}' no declarada en la línea {expr.line}, columna {expr.column}.",
                    suggestion=f"Declare o defina la función '{expr.callee}' antes de llamarla.",
                    identifier=expr.callee,
                    scope_name=self.symbol_table.current_scope.name
                )
                expr.inferred_type = "desconocido"
                return "desconocido"
            for arg in expr.args:
                self.infer_type(arg)
            expr.inferred_type = sym.data_type
            return sym.data_type

        return "desconocido"

    def evaluate_const_expr(self, expr: ASTNode) -> Any:
        """Evalúa expresiones aritméticas constantes simples para poblar la tabla de símbolos."""
        if isinstance(expr, LiteralNode):
            return expr.value
        if isinstance(expr, IdentifierNode):
            sym = self.symbol_table.busquen_simbolo(expr.name)
            return sym.value if sym else None
        if isinstance(expr, BinaryOpNode):
            l_val = self.evaluate_const_expr(expr.left)
            r_val = self.evaluate_const_expr(expr.right)
            if l_val is not None and r_val is not None:
                try:
                    if expr.op == "+": return l_val + r_val
                    if expr.op == "-": return l_val - r_val
                    if expr.op == "*": return l_val * r_val
                    if expr.op == "/" and r_val != 0: return l_val / r_val
                    if expr.op == "%" and r_val != 0: return l_val % r_val
                except Exception:
                    return None
        return None
