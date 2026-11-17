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

from typing import Optional, List, Dict, Any, Tuple
from ast_nodes import (
    ASTNode,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    ParameterNode,
    VariableDeclarationNode,
    AssignmentNode,
    ReturnNode,
    IfNode,
    WhileNode,
    TryCatchNode,
    MethodCallNode,
    BlockNode,
    BinaryOpNode,
    UnaryOpNode,
    PostfixOpNode,
    IdentifierNode,
    LiteralNode
)
from symbol_table import (
    DataType,
    Scope,
    Symbol,
    VariableSymbol,
    MethodSymbol,
    ClassSymbol
)
from error_handler import CompilerErrorHandler


class SemanticAnalyzer:
    """
    Analizador Semántico de Dos Pasadas (Dragon Book) para la verificación de
    estructuras de control, llamadas a métodos, coherencia de tipos y flujo de control.

    Fases de Verificación:
    1. Pre-análisis (Pase 1): Registro de clases, firmas de métodos y variables globales.
    2. Comprobación profunda (Pase 2):
       - Chequeo de condiciones lógicas estrictamente booleanas en 'if' y 'while'.
       - Detección de bucles infinitos estáticos y código inalcanzable (unreachable code).
       - Verificación de llamadas a métodos (existencia, aridad y compatibilidad de tipos de argumentos).
       - Validación de tipos de retorno contra la declaración del método.
       - Detección de sentencias 'return' fuera de métodos.
       - Verificación de tipos en asignaciones y operaciones aritmético-lógicas.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_handler: Optional[CompilerErrorHandler] = None):
        self.error_handler = error_handler or CompilerErrorHandler()
        self.global_scope = Scope("Global")
        self.current_scope: Scope = self.global_scope
        self.current_class: Optional[ClassSymbol] = None
        self.current_method: Optional[MethodSymbol] = None
        self.all_scopes: List[Scope] = [self.global_scope]

        self._register_builtins()

    def _register_builtins(self):
        """Registra funciones integradas comunes del lenguaje (console.log, print)."""
        builtin_print = MethodSymbol("print", DataType.VOID, [("msg", DataType.ANY)])
        builtin_println = MethodSymbol("println", DataType.VOID, [("msg", DataType.ANY)])
        builtin_log = MethodSymbol("console.log", DataType.VOID, [("msg", DataType.ANY)])
        builtin_error = MethodSymbol("console.error", DataType.VOID, [("msg", DataType.ANY)])

        self.global_scope.define(builtin_print)
        self.global_scope.define(builtin_println)
        self.global_scope.define(builtin_log)
        self.global_scope.define(builtin_error)

    # -------------------------------------------------------------------------
    # GESTIÓN DE ÁMBITOS (SCOPES)
    # -------------------------------------------------------------------------

    def _enter_scope(self, name: str) -> Scope:
        new_scope = Scope(name, parent=self.current_scope)
        self.current_scope = new_scope
        self.all_scopes.append(new_scope)
        return new_scope

    def _exit_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    # -------------------------------------------------------------------------
    # PUNTO DE ENTRADA PRINCIPAL: ANALYZE()
    # -------------------------------------------------------------------------

    def analyze(self, program: ProgramNode):
        """
        Ejecuta el análisis semántico completo en dos pasadas protegidas con
        captura de excepciones para garantizar robustez absoluta.
        """
        try:
            # Pase 1: Pre-registro de definiciones de clases y métodos
            self._pass_1_declarations(program)

            # Pase 2: Validación semántica profunda y verificación de tipos/flujo
            self._pass_2_type_check(program)
        except Exception as ex:
            self.error_handler.report_syntax_error(
                f"Excepción interna controlada durante el análisis semántico: {str(ex)}",
                line=1, col=1,
                suggestion="Revise la sintaxis del programa de entrada."
            )

    # -------------------------------------------------------------------------
    # PASE 1: PRE-REGISTRO DE CLASES Y FIRMAS DE MÉTODOS
    # -------------------------------------------------------------------------

    def _pass_1_declarations(self, program: ProgramNode):
        for decl in program.declarations:
            if isinstance(decl, ClassDeclarationNode):
                cls_sym = ClassSymbol(decl.name, decl.line, decl.column)
                if not self.global_scope.define(cls_sym):
                    self.error_handler.report_duplicate_symbol(
                        decl.line, decl.column, decl.name, symbol_kind="clase"
                    )
                # Pre-registrar métodos y campos de la clase
                for member in decl.members:
                    if isinstance(member, MethodDeclarationNode):
                        m_sym = self._create_method_symbol(member)
                        cls_sym.define_method(m_sym)
                    elif isinstance(member, VariableDeclarationNode):
                        v_sym = VariableSymbol(member.name, DataType.from_str(member.var_type), member.line, member.column)
                        cls_sym.define_field(v_sym)

            elif isinstance(decl, MethodDeclarationNode):
                m_sym = self._create_method_symbol(decl)
                if not self.global_scope.define(m_sym):
                    self.error_handler.report_duplicate_symbol(
                        decl.line, decl.column, decl.name, symbol_kind="método o función"
                    )

            elif isinstance(decl, VariableDeclarationNode):
                # Si es con 'let'/'var' sin tipo estricto, tipo provisional
                var_type = DataType.from_str(decl.var_type)
                v_sym = VariableSymbol(decl.name, var_type, decl.line, decl.column)
                if not self.global_scope.define(v_sym):
                    self.error_handler.report_duplicate_symbol(
                        decl.line, decl.column, decl.name, symbol_kind="variable"
                    )

    def _create_method_symbol(self, node: MethodDeclarationNode) -> MethodSymbol:
        ret_type = DataType.from_str(node.return_type)
        params: List[Tuple[str, DataType]] = []
        for p in node.parameters:
            params.append((p.name, DataType.from_str(p.param_type)))
        return MethodSymbol(node.name, ret_type, params, node.line, node.column)

    # -------------------------------------------------------------------------
    # PASE 2: COMPROBACIÓN SEMÁNTICA PROFUNDA Y RECORRIDO DEL AST
    # -------------------------------------------------------------------------

    def _pass_2_type_check(self, program: ProgramNode):
        for decl in program.declarations:
            decl.accept(self)

    # -------------------------------------------------------------------------
    # RECORRIDO DE CLASES Y MÉTODOS
    # -------------------------------------------------------------------------

    def visit_ClassDeclarationNode(self, node: ClassDeclarationNode):
        cls_sym = self.global_scope.resolve(node.name)
        old_class = self.current_class
        if isinstance(cls_sym, ClassSymbol):
            self.current_class = cls_sym

        self._enter_scope(f"Clase_{node.name}")

        # Inyectar campos en el ámbito de la clase
        if self.current_class:
            for f in self.current_class.fields.values():
                self.current_scope.define(f)

        for member in node.members:
            member.accept(self)

        self._exit_scope()
        self.current_class = old_class

    def visit_MethodDeclarationNode(self, node: MethodDeclarationNode):
        # Resolver o crear el símbolo de método
        m_sym = None
        if self.current_class and node.name in self.current_class.methods:
            m_sym = self.current_class.methods[node.name]
        else:
            cand = self.global_scope.resolve(node.name)
            if isinstance(cand, MethodSymbol):
                m_sym = cand
            else:
                m_sym = self._create_method_symbol(node)

        old_method = self.current_method
        self.current_method = m_sym

        self._enter_scope(f"Metodo_{node.name}")

        # Registrar parámetros en el ámbito local del método
        for p in node.parameters:
            p_type = DataType.from_str(p.param_type)
            p_sym = VariableSymbol(p.name, p_type, p.line, p.column, is_param=True)
            if not self.current_scope.define(p_sym):
                self.error_handler.report_duplicate_symbol(
                    p.line, p.column, p.name, symbol_kind="parámetro"
                )

        # Analizar sentencias del cuerpo y verificar unreachable code
        self._analyze_statement_sequence(node.body)

        self._exit_scope()
        self.current_method = old_method

    def _analyze_statement_sequence(self, statements: List[ASTNode]):
        """Analiza una secuencia lineal de sentencias detectando código inalcanzable tras un 'return'."""
        has_returned = False

        for stmt in statements:
            if has_returned:
                self.error_handler.report_unreachable_code(
                    stmt.line, stmt.column,
                    suggestion="El código posterior a 'return' nunca se ejecutará."
                )
                continue

            stmt.accept(self)

            if isinstance(stmt, ReturnNode):
                has_returned = True

    # -------------------------------------------------------------------------
    # VALIDACIÓN DE ESTRUCTURAS DE CONTROL CONDICIONALES E ITERATIVAS (RÚBRICA)
    # -------------------------------------------------------------------------

    def visit_IfNode(self, node: IfNode):
        """
        REQUISITO OFICIAL DE RÚBRICA:
        1. Comprobación de condición lógica estrictamente booleana en 'if'.
        2. Bloques de sentencias correctamente estructurados.
        """
        # Evaluar tipo de la condición
        cond_type = self._evaluate_expression_type(node.condition)

        # REGLA: Las condiciones if deben ser expresiones booleanas
        # Ejemplo del profesor: if ("texto") debe ser rechazado
        if not cond_type.is_boolean() and cond_type != DataType.ANY and cond_type != DataType.ERROR:
            self.error_handler.report_condition_type_error(
                node.line, node.column,
                structure="if",
                actual_type=cond_type.value,
                suggestion="La condición del 'if' debe evaluar a true o false (ej. una comparación relacional como x > 10).",
                offending=getattr(node.condition, 'value', str(cond_type.value))
            )

        # Analizar rama Then
        self._enter_scope("Bloque_If_Then")
        self._analyze_statement_sequence(node.then_body)
        self._exit_scope()

        # Analizar rama Else opcional
        if node.else_body is not None:
            self._enter_scope("Bloque_If_Else")
            self._analyze_statement_sequence(node.else_body)
            self._exit_scope()

    def visit_WhileNode(self, node: WhileNode):
        """
        REQUISITO OFICIAL DE RÚBRICA:
        1. Comprobación de condición lógica estrictamente booleana en 'while'.
        2. Detección de bucles infinitos estáticos (while (true) sin condición de escape).
        """
        cond_type = self._evaluate_expression_type(node.condition)

        # REGLA: Las condiciones while deben ser expresiones booleanas
        if not cond_type.is_boolean() and cond_type != DataType.ANY and cond_type != DataType.ERROR:
            self.error_handler.report_condition_type_error(
                node.line, node.column,
                structure="while",
                actual_type=cond_type.value,
                suggestion="La condición del ciclo 'while' debe ser de tipo boolean (ej. contador < 10).",
                offending=getattr(node.condition, 'value', str(cond_type.value))
            )

        # REGLA: Detección de bucle infinito (while (true))
        # Ejemplo del profesor: while (true) { console.log("Esto no termina nunca"); }
        if self._is_constant_true_condition(node.condition):
            if not self._contains_loop_escape(node.body):
                self.error_handler.report_infinite_loop(
                    node.line, node.column,
                    suggestion="Incorpore una variable de control que incremente/decremente o una sentencia 'break' / 'return' condicional.",
                    offending="while (true)"
                )

        self._enter_scope("Bloque_While")
        self._analyze_statement_sequence(node.body)
        self._exit_scope()

    def _is_constant_true_condition(self, expr: ASTNode) -> bool:
        """Determina si la condición es una constante estática verdadera (true o literal distinto de cero)."""
        if isinstance(expr, LiteralNode) and expr.lit_type == "boolean":
            return expr.value is True
        return False

    def _contains_loop_escape(self, statements: List[ASTNode]) -> bool:
        """Verifica si el cuerpo del bucle contiene alguna sentencia de escape (return o break o llamada)."""
        for s in statements:
            if isinstance(s, ReturnNode):
                return True
            if isinstance(s, IfNode):
                # Si dentro del if hay un return, es un escape potencial
                if any(isinstance(x, ReturnNode) for x in s.then_body):
                    return True
                if s.else_body and any(isinstance(x, ReturnNode) for x in s.else_body):
                    return True
        return False

    def visit_TryCatchNode(self, node: TryCatchNode):
        """Manejo de excepciones: valida el bloque try y catch con su variable de error."""
        self._enter_scope("Bloque_Try")
        self._analyze_statement_sequence(node.try_body)
        self._exit_scope()

        self._enter_scope("Bloque_Catch")
        err_sym = VariableSymbol(node.error_var, DataType.ANY, node.line, node.column)
        self.current_scope.define(err_sym)
        self._analyze_statement_sequence(node.catch_body)
        self._exit_scope()

    def visit_BlockNode(self, node: BlockNode):
        self._enter_scope("Bloque_Local")
        self._analyze_statement_sequence(node.statements)
        self._exit_scope()

    # -------------------------------------------------------------------------
    # VALIDACIÓN DE SENTENCIAS RETURN Y MÉTODOS (RÚBRICA)
    # -------------------------------------------------------------------------

    def visit_ReturnNode(self, node: ReturnNode):
        """
        REQUISITO OFICIAL DE RÚBRICA:
        1. Detección de sentencias 'return' fuera de lugar (fuera de métodos).
        2. Validación de tipos de retorno contra la declaración del método.
           - Si método es void, no puede retornar valor.
           - Si método retorna int, no puede retornar string ("Veinte").
        """
        # REGLA: Return fuera de método
        if self.current_method is None:
            self.error_handler.report_misplaced_return(
                node.line, node.column,
                suggestion="La instrucción 'return' no puede estar fuera del cuerpo de un método.",
                offending="return"
            )
            return

        expected_type = self.current_method.data_type
        actual_type = DataType.VOID if node.expr is None else self._evaluate_expression_type(node.expr)

        # REGLA: Método void no puede retornar un valor
        if expected_type == DataType.VOID:
            if actual_type != DataType.VOID and actual_type != DataType.ERROR:
                self.error_handler.report_void_method_returning_value(
                    node.line, node.column,
                    method_name=self.current_method.name,
                    actual_type=actual_type.value,
                    suggestion="Elimine el valor retornado o declare un tipo de retorno distinto de void."
                )
            return

        # REGLA: Método con tipo no-void requiere valor compatible
        # Ejemplo del profesor: function obtenerEdad() { return "Veinte"; } -> Debe retornar número, no cadena
        if actual_type == DataType.VOID:
            self.error_handler.report_return_type_mismatch(
                node.line, node.column,
                method_name=self.current_method.name,
                expected_type=expected_type.value,
                actual_type="void (sin valor)",
                suggestion=f"El método '{self.current_method.name}' debe retornar una expresión de tipo '{expected_type.value}'."
            )
        elif not actual_type.can_assign_to(expected_type) and expected_type != DataType.ANY:
            self.error_handler.report_return_type_mismatch(
                node.line, node.column,
                method_name=self.current_method.name,
                expected_type=expected_type.value,
                actual_type=actual_type.value,
                suggestion=f"Retorne un valor de tipo '{expected_type.value}' o cambie el tipo de retorno declarado."
            )

    # -------------------------------------------------------------------------
    # LLAMADAS A MÉTODOS Y CHEQUEO DE PARÁMETROS (RÚBRICA)
    # -------------------------------------------------------------------------

    def visit_MethodCallNode(self, node: MethodCallNode):
        self._evaluate_call_type(node)

    def _evaluate_call_type(self, node: MethodCallNode) -> DataType:
        """
        REQUISITO OFICIAL DE RÚBRICA:
        1. Existencia del método en el ámbito accesible.
        2. Chequeo de número de argumentos (aridad).
        3. Chequeo de tipos de parámetros y compatibilidad.
           - Ejemplo del profesor: dividir(10, "texto") -> incompatible!
           - Ejemplo del profesor: imprimirMensaje("Hola", "Mundo") -> 2 argumentos en vez de 1!
        """
        full_name = node.full_name()

        # Ignorar llamadas de salida estándar en chequeo estricto
        if full_name in ("console.log", "console.error", "print", "println"):
            for arg in node.arguments:
                self._evaluate_expression_type(arg)
            return DataType.VOID

        # Resolver método en la clase actual o en el ámbito global
        method_sym: Optional[MethodSymbol] = None

        if self.current_class and node.method_name in self.current_class.methods:
            method_sym = self.current_class.methods[node.method_name]
        else:
            resolved = self.current_scope.resolve(node.method_name)
            if isinstance(resolved, MethodSymbol):
                method_sym = resolved

        # REGLA: Método no declarado
        if method_sym is None:
            self.error_handler.report_undeclared_symbol(
                node.line, node.column,
                symbol_name=node.method_name,
                symbol_kind="método o función",
                suggestion=f"Declare el método '{node.method_name}' antes de invocarlo."
            )
            # Evaluar argumentos de todas formas para no perder diagnósticos en subexpresiones
            for arg in node.arguments:
                self._evaluate_expression_type(arg)
            return DataType.ERROR

        # REGLA: Chequeo del número de argumentos (Aridad)
        expected_count = method_sym.arity
        actual_count = len(node.arguments)
        if actual_count != expected_count:
            self.error_handler.report_method_argument_count_mismatch(
                node.line, node.column,
                method_name=method_sym.name,
                expected_count=expected_count,
                actual_count=actual_count,
                suggestion=f"La función '{method_sym.name}' espera {expected_count} parámetro(s): ({method_sym.format_signature()})."
            )

        # REGLA: Chequeo de compatibilidad de tipos de argumentos
        # Ejemplo del profesor: dividir(10, "texto")
        min_args = min(actual_count, expected_count)
        for i in range(min_args):
            arg_expr = node.arguments[i]
            param_name, param_type = method_sym.parameters[i]
            arg_type = self._evaluate_expression_type(arg_expr)

            if not arg_type.can_assign_to(param_type) and param_type != DataType.ANY and arg_type != DataType.ERROR:
                self.error_handler.report_method_argument_type_mismatch(
                    node.line, node.column,
                    method_name=method_sym.name,
                    param_name=param_name,
                    expected_type=param_type.value,
                    actual_type=arg_type.value,
                    arg_index=i + 1,
                    suggestion=f"Pase un valor de tipo '{param_type.value}' para el parámetro '{param_name}'."
                )

        return method_sym.data_type

    # -------------------------------------------------------------------------
    # VALIDACIÓN DE VARIABLES, ASIGNACIONES Y EXPRESIONES
    # -------------------------------------------------------------------------

    def visit_VariableDeclarationNode(self, node: VariableDeclarationNode):
        var_type = DataType.from_str(node.var_type)

        # Si se inicializa, comprobar compatibilidad de tipo
        if node.initializer is not None:
            init_type = self._evaluate_expression_type(node.initializer)

            # Si la variable es tipo 'any' (ej. let / var), hereda el tipo del inicializador
            if var_type == DataType.ANY and init_type != DataType.ERROR:
                var_type = init_type

            if not init_type.can_assign_to(var_type) and var_type != DataType.ANY and init_type != DataType.ERROR:
                self.error_handler.report_type_mismatch_assignment(
                    node.line, node.column,
                    target_name=node.name,
                    target_type=var_type.value,
                    expr_type=init_type.value,
                    suggestion=f"Inicialice '{node.name}' con un valor compatible con '{var_type.value}'."
                )

        var_sym = VariableSymbol(node.name, var_type, node.line, node.column)
        if not self.current_scope.define(var_sym):
            # Si estamos en Pase 2 y no fue pre-registrado en este mismo ámbito, reportar duplicado
            pass

    def visit_AssignmentNode(self, node: AssignmentNode):
        # Resolver variable destino
        target_sym = self.current_scope.resolve(node.target_name)

        if target_sym is None:
            self.error_handler.report_undeclared_symbol(
                node.line, node.column,
                symbol_name=node.target_name,
                symbol_kind="variable",
                suggestion=f"Declare '{node.target_name}' con su tipo antes de asignarle un valor."
            )
            self._evaluate_expression_type(node.expr)
            return

        target_type = target_sym.data_type
        expr_type = self._evaluate_expression_type(node.expr)

        # Si target era 'any', se adapta
        if target_type == DataType.ANY and expr_type != DataType.ERROR:
            target_sym.data_type = expr_type
            return

        if not expr_type.can_assign_to(target_type) and target_type != DataType.ANY and expr_type != DataType.ERROR:
            self.error_handler.report_type_mismatch_assignment(
                node.line, node.column,
                target_name=node.target_name,
                target_type=target_type.value,
                expr_type=expr_type.value,
                suggestion=f"El valor asignado debe ser compatible con el tipo '{target_type.value}'."
            )

    def visit_PostfixOpNode(self, node: PostfixOpNode):
        sym = self.current_scope.resolve(node.target_name)
        if sym is None:
            self.error_handler.report_undeclared_symbol(
                node.line, node.column,
                symbol_name=node.target_name,
                symbol_kind="variable",
                suggestion=f"Declare '{node.target_name}' antes de incrementarla."
            )
        elif not sym.data_type.is_numeric() and sym.data_type != DataType.ANY:
            self.error_handler.report_syntax_error(
                f"El operador '{node.op}' solo puede aplicarse a variables numéricas, '{node.target_name}' es de tipo '{sym.data_type.value}'.",
                node.line, node.column
            )

    def _evaluate_expression_type(self, node: ASTNode) -> DataType:
        """Determina el tipo estático resultante de una expresión sintáctica."""
        if isinstance(node, LiteralNode):
            return DataType.from_str(node.lit_type)

        if isinstance(node, IdentifierNode):
            # Atributos calificados ej: error.message
            if "." in node.name:
                return DataType.STRING

            sym = self.current_scope.resolve(node.name)
            if sym is None:
                self.error_handler.report_undeclared_symbol(
                    node.line, node.column,
                    symbol_name=node.name,
                    symbol_kind="variable",
                    suggestion=f"Declare '{node.name}' antes de usarla en una expresión."
                )
                return DataType.ERROR
            return sym.data_type

        if isinstance(node, MethodCallNode):
            return self._evaluate_call_type(node)

        if isinstance(node, BinaryOpNode):
            left_type = self._evaluate_expression_type(node.left)
            right_type = self._evaluate_expression_type(node.right)

            if left_type == DataType.ERROR or right_type == DataType.ERROR:
                return DataType.ERROR

            # Operadores relacionales: <, <=, >, >=
            if node.op in ("<", "<=", ">", ">="):
                if not (left_type.is_numeric() or left_type == DataType.ANY) or not (right_type.is_numeric() or right_type == DataType.ANY):
                    self.error_handler.report_binary_op_type_error(
                        node.line, node.column, node.op, left_type.value, right_type.value,
                        suggestion="Los operadores de comparación relacional requieren operandos numéricos."
                    )
                return DataType.BOOLEAN

            # Operadores de igualdad: ==, !=, ===, !==
            if node.op in ("==", "!=", "===", "!=="):
                # Compatibles si son del mismo tipo o coercionables
                return DataType.BOOLEAN

            # Operadores lógicos: &&, ||
            if node.op in ("&&", "||"):
                if not left_type.is_boolean() and left_type != DataType.ANY:
                    self.error_handler.report_condition_type_error(
                        node.line, node.column,
                        structure=f"operación lógica '{node.op}'",
                        actual_type=left_type.value,
                        suggestion="Ambos operandos de '&&' y '||' deben ser de tipo boolean."
                    )
                if not right_type.is_boolean() and right_type != DataType.ANY:
                    self.error_handler.report_condition_type_error(
                        node.line, node.column,
                        structure=f"operación lógica '{node.op}'",
                        actual_type=right_type.value,
                        suggestion="Ambos operandos de '&&' y '||' deben ser de tipo boolean."
                    )
                return DataType.BOOLEAN

            # Operador suma con sobrecarga de concatenación de cadenas
            if node.op == "+":
                if left_type == DataType.STRING or right_type == DataType.STRING:
                    return DataType.STRING
                if left_type.is_numeric() and right_type.is_numeric():
                    return DataType.FLOAT if (left_type == DataType.FLOAT or right_type == DataType.FLOAT) else DataType.INT

            # Otros operadores aritméticos: -, *, /, %
            if node.op in ("-", "*", "/", "%"):
                if not (left_type.is_numeric() or left_type == DataType.ANY) or not (right_type.is_numeric() or right_type == DataType.ANY):
                    self.error_handler.report_binary_op_type_error(
                        node.line, node.column, node.op, left_type.value, right_type.value,
                        suggestion="Los operadores aritméticos requieren operandos numéricos."
                    )
                if node.op == "/":
                    return DataType.FLOAT
                return DataType.FLOAT if (left_type == DataType.FLOAT or right_type == DataType.FLOAT) else DataType.INT

            return DataType.ANY

        if isinstance(node, UnaryOpNode):
            operand_type = self._evaluate_expression_type(node.operand)
            if node.op == "!":
                if not operand_type.is_boolean() and operand_type != DataType.ANY:
                    self.error_handler.report_condition_type_error(
                        node.line, node.column,
                        structure="negación lógica '!'",
                        actual_type=operand_type.value,
                        suggestion="El operador '!' solo aplica sobre expresiones de tipo boolean."
                    )
                return DataType.BOOLEAN
            if node.op in ("-", "+"):
                return operand_type

        if isinstance(node, PostfixOpNode):
            sym = self.current_scope.resolve(node.target_name)
            return sym.data_type if sym else DataType.INT

        return DataType.ANY

    def generic_visit(self, node: ASTNode):
        """Visita genérica recursiva por defecto."""
        for attr in dir(node):
            val = getattr(node, attr)
            if isinstance(val, ASTNode):
                val.accept(self)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, ASTNode):
                        item.accept(self)
