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

from typing import Optional, Dict, List, Any
from ast_nodes import (
    ASTNode,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    ParameterNode,
    VariableDeclarationNode,
    AssignmentNode,
    IfNode,
    SwitchNode,
    CaseNode,
    WhileNode,
    ForNode,
    DoWhileNode,
    ReturnNode,
    BreakNode,
    PrintNode,
    MethodCallNode,
    NewObjectNode,
    BinaryOpNode,
    UnaryOpNode,
    PostfixOpNode,
    IdentifierNode,
    LiteralNode,
    BlockNode
)
from symbol_table import SymbolTable, MethodSymbol, ClassSymbol
from error_handler import CompilerErrorHandler


class SemanticAnalyzer:
    """
    Analizador semántico integral para C.
    Verifica coherencia de tipos, concordancia de aridad en llamadas a métodos,
    existencia de clases y variables, y condiciones válidas de control de flujo.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_handler: Optional[CompilerErrorHandler] = None):
        self.error_handler = error_handler or CompilerErrorHandler()
        self.symbol_table = SymbolTable(scope_name="global")
        self.current_class: Optional[str] = None
        self.current_method: Optional[str] = None

    def analyze(self, root: ProgramNode) -> SymbolTable:
        self.symbol_table = SymbolTable(scope_name="global")

        # Fase 1: Pre-registro de clases y firmas de métodos
        self._pre_register_declarations(root)

        # Fase 2: Análisis semántico exhaustivo del AST
        for decl in root.declarations:
            self._visit_node(decl, self.symbol_table)

        return self.symbol_table

    def _pre_register_declarations(self, root: ProgramNode):
        for node in root.declarations:
            if isinstance(node, ClassDeclarationNode):
                cls_sym = self.symbol_table.insert_class(node.name)
                for member in node.members:
                    if isinstance(member, MethodDeclarationNode):
                        params = [(p.type_name, p.name) for p in member.parameters]
                        m_sym = self.symbol_table.insert_method(
                            f"{node.name}.{member.name}",
                            member.return_type,
                            params,
                            f"L_{node.name}_{member.name}",
                            class_name=node.name
                        )
                        cls_sym.methods[member.name] = m_sym
                    elif isinstance(member, VariableDeclarationNode):
                        cls_sym.fields[member.name] = member.type_name
            elif isinstance(node, MethodDeclarationNode):
                params = [(p.type_name, p.name) for p in node.parameters]
                self.symbol_table.insert_method(node.name, node.return_type, params, f"L_{node.name}")

    def _visit_node(self, node: ASTNode, current_scope: SymbolTable) -> Optional[str]:
        if isinstance(node, ClassDeclarationNode):
            old_cls = self.current_class
            self.current_class = node.name
            class_scope = SymbolTable(parent=current_scope, scope_name=f"class_{node.name}")
            for m in node.members:
                self._visit_node(m, class_scope)
            self.current_class = old_cls
            return "void"

        elif isinstance(node, MethodDeclarationNode):
            old_method = self.current_method
            self.current_method = node.name
            method_scope = SymbolTable(parent=current_scope, scope_name=f"method_{node.name}")
            for p in node.parameters:
                method_scope.insert_variable(p.name, p.type_name, is_init=True)
            for stmt in node.body:
                self._visit_node(stmt, method_scope)
            self.current_method = old_method
            return node.return_type

        elif isinstance(node, VariableDeclarationNode):
            init_type = self._visit_node(node.initializer, current_scope) if node.initializer else None
            if init_type and init_type != "error":
                # Validar compatibilidad de tipos
                if node.type_name != "any" and init_type != "any":
                    if not self._is_type_compatible(node.type_name, init_type):
                        self.error_handler.report_semantic(
                            f"Incompatibilidad de tipos en inicialización de '{node.name}'. Se esperaba '{node.type_name}' pero se obtuvo '{init_type}'.",
                            node.line, node.column,
                            suggestion=f"Asigne un valor de tipo '{node.type_name}'."
                        )
            current_scope.insert_variable(node.name, node.type_name, is_init=(node.initializer is not None))
            return node.type_name

        elif isinstance(node, AssignmentNode):
            expr_type = self._visit_node(node.expr, current_scope)
            if node.is_field and node.obj_name:
                obj_sym = current_scope.lookup_variable(node.obj_name)
                if not obj_sym:
                    self.error_handler.report_semantic(
                        f"Objeto '{node.obj_name}' no declarado.",
                        node.line, node.column
                    )
                else:
                    cls_sym = self.symbol_table.lookup_class(obj_sym.type_name)
                    if not cls_sym or node.target not in cls_sym.fields:
                        self.error_handler.report_semantic(
                            f"El atributo '{node.target}' no existe en la clase '{obj_sym.type_name}'.",
                            node.line, node.column
                        )
                return expr_type

            var_sym = current_scope.lookup_variable(node.target)
            if not var_sym:
                # Variable implícita: registrar
                current_scope.insert_variable(node.target, expr_type or "int", is_init=True)
            else:
                var_sym.is_initialized = True
                if expr_type and var_sym.type_name not in ("any", "int") and expr_type != var_sym.type_name:
                    if not self._is_type_compatible(var_sym.type_name, expr_type):
                        self.error_handler.report_semantic(
                            f"Incompatibilidad de tipos en asignación a '{node.target}'. Esperado '{var_sym.type_name}', obtenido '{expr_type}'.",
                            node.line, node.column
                        )
            return expr_type

        elif isinstance(node, IfNode):
            cond_type = self._visit_node(node.condition, current_scope)
            if cond_type == "string":
                self.error_handler.report_semantic(
                    "La condición del 'if' no puede ser una cadena de texto.",
                    node.line, node.column,
                    suggestion="Utilice una expresión relacional o booleana."
                )
            for s in node.then_block:
                self._visit_node(s, current_scope)
            if node.else_block:
                for s in node.else_block:
                    self._visit_node(s, current_scope)
            return "void"

        elif isinstance(node, SwitchNode):
            self._visit_node(node.expression, current_scope)
            for c in node.cases:
                self._visit_node(c.value, current_scope)
                for s in c.body:
                    self._visit_node(s, current_scope)
            if node.default_block:
                for s in node.default_block:
                    self._visit_node(s, current_scope)
            return "void"

        elif isinstance(node, WhileNode):
            cond_type = self._visit_node(node.condition, current_scope)
            if cond_type == "string":
                self.error_handler.report_semantic(
                    "La condición del 'while' no puede ser una cadena de texto.",
                    node.line, node.column
                )
            for s in node.body:
                self._visit_node(s, current_scope)
            return "void"

        elif isinstance(node, ForNode):
            for_scope = SymbolTable(parent=current_scope, scope_name="for_scope")
            if node.initializer:
                self._visit_node(node.initializer, for_scope)
            if node.condition:
                self._visit_node(node.condition, for_scope)
            if node.update:
                self._visit_node(node.update, for_scope)
            for s in node.body:
                self._visit_node(s, for_scope)
            return "void"

        elif isinstance(node, DoWhileNode):
            for s in node.body:
                self._visit_node(s, current_scope)
            self._visit_node(node.condition, current_scope)
            return "void"

        elif isinstance(node, MethodCallNode):
            if node.obj_name:
                obj_sym = current_scope.lookup_variable(node.obj_name)
                if not obj_sym:
                    self.error_handler.report_semantic(
                        f"El objeto '{node.obj_name}' no ha sido declarado.",
                        node.line, node.column
                    )
                    return "error"
                cls_sym = self.symbol_table.lookup_class(obj_sym.type_name)
                if not cls_sym or node.callee not in cls_sym.methods:
                    self.error_handler.report_semantic(
                        f"El método '{node.callee}' no existe en la clase '{obj_sym.type_name}'.",
                        node.line, node.column
                    )
                    return "error"
                m_sym = cls_sym.methods[node.callee]
            else:
                m_sym = self.symbol_table.lookup_method(node.callee)
                if not m_sym:
                    self.error_handler.report_semantic(
                        f"Llamada a función o método no declarado: '{node.callee}'.",
                        node.line, node.column,
                        suggestion=f"Declare la función '{node.callee}' antes de llamarla."
                    )
                    return "error"

            # Validar aridad
            if len(m_sym.parameters) != len(node.args):
                self.error_handler.report_semantic(
                    f"La función '{node.callee}' espera {len(m_sym.parameters)} argumentos pero se proporcionaron {len(node.args)}.",
                    node.line, node.column
                )
            for a in node.args:
                self._visit_node(a, current_scope)
            return m_sym.return_type

        elif isinstance(node, NewObjectNode):
            cls_sym = self.symbol_table.lookup_class(node.class_name)
            if not cls_sym:
                self.error_handler.report_semantic(
                    f"Intento de instanciar una clase no declarada: '{node.class_name}'.",
                    node.line, node.column,
                    suggestion=f"Defina la clase 'class {node.class_name} {{ ... }}'."
                )
                return "error"
            return node.class_name

        elif isinstance(node, BinaryOpNode):
            t_left = self._visit_node(node.left, current_scope)
            t_right = self._visit_node(node.right, current_scope)

            # Detectar división entre constante cero
            if node.op == "/" and isinstance(node.right, LiteralNode) and node.right.value == 0:
                self.error_handler.report_semantic(
                    "División por cero detectada en expresión.",
                    node.line, node.column
                )

            # Incompatibilidad de cadenas en operaciones aritméticas (+, -, *, /)
            if node.op in ("+", "-", "*", "/", "%"):
                if t_left == "string" or t_right == "string":
                    if node.op != "+":
                        self.error_handler.report_semantic(
                            f"Operación aritmética '{node.op}' no soportada sobre cadenas de texto.",
                            node.line, node.column
                        )
                        return "error"

            if node.op in ("==", "!=", "<", ">", "<=", ">="):
                return "bool"
            if node.op in ("&&", "||"):
                return "bool"
            if t_left == "float" or t_right == "float":
                return "float"
            return "int"

        elif isinstance(node, UnaryOpNode):
            t_expr = self._visit_node(node.expr, current_scope)
            return "bool" if node.op == "!" else t_expr

        elif isinstance(node, PostfixOpNode):
            var_sym = current_scope.lookup_variable(node.var_name)
            if not var_sym:
                current_scope.insert_variable(node.var_name, "int", is_init=True)
            return "int"

        elif isinstance(node, IdentifierNode):
            if "." in node.name:
                return "any"
            sym = current_scope.lookup_variable(node.name)
            if not sym:
                # Comprobar si existe globalmente
                sym = self.symbol_table.lookup_variable(node.name)
            return sym.type_name if sym else "int"

        elif isinstance(node, LiteralNode):
            return node.type_name

        elif isinstance(node, PrintNode):
            return self._visit_node(node.expr, current_scope)

        elif isinstance(node, ReturnNode):
            return self._visit_node(node.expr, current_scope) if node.expr else "void"

        elif isinstance(node, BlockNode):
            block_scope = SymbolTable(parent=current_scope, scope_name="block")
            for s in node.statements:
                self._visit_node(s, block_scope)
            return "void"

        return "any"

    def _is_type_compatible(self, t1: str, t2: str) -> bool:
        if t1 == t2:
            return True
        if t1 in ("int", "float") and t2 in ("int", "float"):
            return True
        if t1 == "any" or t2 == "any":
            return True
        return False
