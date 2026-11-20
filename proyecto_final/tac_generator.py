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

from typing import List, Optional, Any, Dict, Tuple
from tac_instruction import TACInstruction
from symbol_table import SymbolTable, MethodSymbol, ClassSymbol
from error_handler import CompilerErrorHandler
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


class TACGenerator:
    """
    Generador de Código Intermedio de Tres Direcciones (TAC).
    Linealiza expresiones, bucles, bifurcaciones, métodos, clases y sentencias de E/S.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_handler: Optional[CompilerErrorHandler] = None):
        self.error_handler = error_handler or CompilerErrorHandler()
        self.instructions: List[TACInstruction] = []
        self.symbol_table = SymbolTable(scope_name="global")
        self.temp_counter = 0
        self.label_counter = 0
        self.current_class: Optional[str] = None
        self.variable_types: Dict[str, str] = {}

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instr: TACInstruction):
        self.instructions.append(instr)

    def generate(self, root: ProgramNode, symbol_table: Optional[SymbolTable] = None) -> List[TACInstruction]:
        self.instructions.clear()
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table = symbol_table or SymbolTable(scope_name="global")
        self.variable_types.clear()

        self._pre_register_symbols(root)

        func_decls = [d for d in root.declarations if isinstance(d, (MethodDeclarationNode, ClassDeclarationNode))]
        main_decls = [d for d in root.declarations if not isinstance(d, (MethodDeclarationNode, ClassDeclarationNode))]

        if func_decls and main_decls:
            l_main = self.new_label()
            self.emit(TACInstruction("GOTO", result=l_main, comment="Salto al flujo principal del programa"))
            for decl in func_decls:
                self._visit_node(decl)
            self.emit(TACInstruction("LABEL", result=l_main, comment="Punto de entrada principal", is_label=True))
            for decl in main_decls:
                self._visit_node(decl)
        else:
            for decl in root.declarations:
                self._visit_node(decl)

        return self.instructions

    def _pre_register_symbols(self, root: ProgramNode):
        for node in root.declarations:
            if isinstance(node, ClassDeclarationNode):
                cls_sym = self.symbol_table.insert_class(node.name)
                for member in node.members:
                    if isinstance(member, MethodDeclarationNode):
                        lbl = self.new_label()
                        params = [(p.type_name, p.name) for p in member.parameters]
                        m_sym = MethodSymbol(member.name, member.return_type, params, lbl, class_name=node.name)
                        cls_sym.methods[member.name] = m_sym
                        self.symbol_table.methods[f"{node.name}.{member.name}"] = m_sym
                    elif isinstance(member, VariableDeclarationNode):
                        cls_sym.fields[member.name] = member.type_name
            elif isinstance(node, MethodDeclarationNode):
                lbl = self.new_label()
                params = [(p.type_name, p.name) for p in node.parameters]
                self.symbol_table.insert_method(node.name, node.return_type, params, lbl)

    def _visit_node(self, node: ASTNode) -> Optional[str]:
        if isinstance(node, ClassDeclarationNode):
            return self._visit_class_decl(node)
        elif isinstance(node, MethodDeclarationNode):
            return self._visit_method_decl(node)
        elif isinstance(node, VariableDeclarationNode):
            return self._visit_variable_decl(node)
        elif isinstance(node, AssignmentNode):
            return self._visit_assignment(node)
        elif isinstance(node, IfNode):
            return self._visit_if(node)
        elif isinstance(node, SwitchNode):
            return self._visit_switch(node)
        elif isinstance(node, WhileNode):
            return self._visit_while(node)
        elif isinstance(node, ForNode):
            return self._visit_for(node)
        elif isinstance(node, DoWhileNode):
            return self._visit_do_while(node)
        elif isinstance(node, ReturnNode):
            return self._visit_return(node)
        elif isinstance(node, BreakNode):
            return None
        elif isinstance(node, PrintNode):
            return self._visit_print(node)
        elif isinstance(node, MethodCallNode):
            return self._visit_method_call(node)
        elif isinstance(node, NewObjectNode):
            return self._visit_new_object(node)
        elif isinstance(node, BinaryOpNode):
            return self._visit_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self._visit_unary_op(node)
        elif isinstance(node, PostfixOpNode):
            return self._visit_postfix_op(node)
        elif isinstance(node, IdentifierNode):
            return node.name
        elif isinstance(node, LiteralNode):
            return self._format_literal(node.value)
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self._visit_node(stmt)
            return None
        return None

    def _format_literal(self, value: Any) -> str:
        if isinstance(value, str):
            return f'"{value}"'
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    # -------------------------------------------------------------------------
    # SENTENCIAS DE CONTROL DE FLUJO
    # -------------------------------------------------------------------------

    def _visit_if(self, node: IfNode) -> None:
        cond_temp = self._visit_node(node.condition)

        if node.else_block is not None:
            l_then = self.new_label()
            l_end = self.new_label()

            self.emit(TACInstruction("IF_GOTO", arg1=cond_temp, result=l_then, comment=f"Si {cond_temp} es verdadero, salta a {l_then}"))
            for stmt in node.else_block:
                self._visit_node(stmt)
            self.emit(TACInstruction("GOTO", result=l_end, comment=f"Fin de bloque else -> salta a {l_end}"))
            self.emit(TACInstruction("LABEL", result=l_then, comment=f"Bloque then", is_label=True))
            for stmt in node.then_block:
                self._visit_node(stmt)
            self.emit(TACInstruction("LABEL", result=l_end, comment="Fin estructura if-else", is_label=True))
        else:
            l_end = self.new_label()
            self.emit(TACInstruction("IF_NOT_GOTO", arg1=cond_temp, result=l_end, comment=f"Si no {cond_temp}, salta a {l_end}"))
            for stmt in node.then_block:
                self._visit_node(stmt)
            self.emit(TACInstruction("LABEL", result=l_end, comment="Fin estructura if", is_label=True))

    def _visit_switch(self, node: SwitchNode) -> None:
        sw_temp = self.new_temp()
        expr_val = self._visit_node(node.expression)
        self.emit(TACInstruction("=", arg1=expr_val, result=sw_temp, comment="Valor switch"))

        case_labels = [self.new_label() for _ in node.cases]
        l_default = self.new_label() if node.default_block is not None else None
        l_end = self.new_label()

        for case_node, lbl in zip(node.cases, case_labels):
            val_str = self._visit_node(case_node.value)
            self.emit(TACInstruction("IF_CMP_GOTO", arg1=sw_temp, arg2=f"== {val_str}", result=lbl, comment=f"Caso {val_str}"))

        if l_default:
            self.emit(TACInstruction("GOTO", result=l_default, comment="Salto a default"))
        else:
            self.emit(TACInstruction("GOTO", result=l_end, comment="Fin de casos switch"))

        for case_node, lbl in zip(node.cases, case_labels):
            self.emit(TACInstruction("LABEL", result=lbl, comment="Cuerpo case", is_label=True))
            for stmt in case_node.body:
                self._visit_node(stmt)
            self.emit(TACInstruction("GOTO", result=l_end, comment="Break de case"))

        if l_default and node.default_block is not None:
            self.emit(TACInstruction("LABEL", result=l_default, comment="Cuerpo default", is_label=True))
            for stmt in node.default_block:
                self._visit_node(stmt)

        self.emit(TACInstruction("LABEL", result=l_end, comment="Fin switch", is_label=True))

    def _visit_while(self, node: WhileNode) -> None:
        l_start = self.new_label()
        l_end = self.new_label()

        self.emit(TACInstruction("LABEL", result=l_start, comment="Inicio while", is_label=True))
        cond_temp = self._visit_node(node.condition)
        self.emit(TACInstruction("IF_NOT_GOTO", arg1=cond_temp, result=l_end, comment="Salida while"))
        for stmt in node.body:
            self._visit_node(stmt)

        self.emit(TACInstruction("GOTO", result=l_start, comment="Reiterar while"))
        self.emit(TACInstruction("LABEL", result=l_end, comment="Fin while", is_label=True))

    def _visit_for(self, node: ForNode) -> None:
        if node.initializer:
            if isinstance(node.initializer, VariableDeclarationNode):
                init_val = self._visit_node(node.initializer.initializer) if node.initializer.initializer else "0"
                self.emit(TACInstruction("=", arg1=init_val, result=node.initializer.name, comment="Inicialización for"))
            elif isinstance(node.initializer, AssignmentNode):
                init_val = self._visit_node(node.initializer.expr)
                self.emit(TACInstruction("=", arg1=init_val, result=node.initializer.target, comment="Inicialización for"))

        l_start = self.new_label()
        l_end = self.new_label()

        self.emit(TACInstruction("LABEL", result=l_start, comment="Inicio bucle for", is_label=True))
        if node.condition:
            cond_temp = self._visit_node(node.condition)
            self.emit(TACInstruction("IF_NOT_GOTO", arg1=cond_temp, result=l_end, comment="Salida bucle for"))

        for stmt in node.body:
            self._visit_node(stmt)

        if node.update:
            if isinstance(node.update, PostfixOpNode):
                op_sign = "+" if node.update.op == "++" else "-"
                self.emit(TACInstruction(op_sign, arg1=node.update.var_name, arg2="1", result=node.update.var_name, comment="Actualización for"))
            elif isinstance(node.update, AssignmentNode):
                val = self._visit_node(node.update.expr)
                self.emit(TACInstruction("=", arg1=val, result=node.update.target, comment="Actualización for"))

        self.emit(TACInstruction("GOTO", result=l_start, comment="Reiterar for"))
        self.emit(TACInstruction("LABEL", result=l_end, comment="Fin bucle for", is_label=True))

    def _visit_do_while(self, node: DoWhileNode) -> None:
        l_start = self.new_label()
        self.emit(TACInstruction("LABEL", result=l_start, comment="Inicio do-while", is_label=True))
        for stmt in node.body:
            self._visit_node(stmt)

        cond_temp = self._visit_node(node.condition)
        self.emit(TACInstruction("IF_GOTO", arg1=cond_temp, result=l_start, comment="Reiterar do-while si verdadero"))

    # -------------------------------------------------------------------------
    # MÉTODOS Y CLASES
    # -------------------------------------------------------------------------

    def _visit_method_decl(self, node: MethodDeclarationNode) -> None:
        key = f"{self.current_class}.{node.name}" if self.current_class else node.name
        sym = self.symbol_table.lookup_method(key) or self.symbol_table.lookup_method(node.name)
        m_lbl = sym.label if sym else self.new_label()

        self.emit(TACInstruction("COMMENT", comment=f"Definición método {node.name}"))
        self.emit(TACInstruction("LABEL", result=m_lbl, comment=f"Entrada método {node.name}", is_label=True))

        for p in node.parameters:
            self.symbol_table.insert_variable(p.name, p.type_name, is_init=True)

        for stmt in node.body:
            self._visit_node(stmt)

        if not self.instructions or self.instructions[-1].op != "RETURN":
            self.emit(TACInstruction("RETURN", comment=f"Fin de método {node.name}"))

    def _visit_method_call(self, node: MethodCallNode) -> str:
        if node.obj_name:
            obj_type = self.variable_types.get(node.obj_name)
            cls_sym = self.symbol_table.lookup_class(obj_type) if obj_type else None
            method_sym = cls_sym.methods.get(node.callee) if cls_sym else None
            m_lbl = method_sym.label if method_sym else self.new_label()

            for idx, arg in enumerate(node.args):
                arg_val = self._visit_node(arg)
                if method_sym and idx < len(method_sym.parameters):
                    target_param = method_sym.parameters[idx][1]
                    self.emit(TACInstruction("=", arg1=arg_val, result=target_param, comment=f"Parámetro {target_param}"))
                else:
                    p_temp = self.new_temp()
                    self.emit(TACInstruction("=", arg1=arg_val, result=p_temp, comment=f"Parámetro {idx+1}"))

            self.emit(TACInstruction("CALL", arg1=m_lbl, comment=f"Llamada a método {node.callee} de objeto"))
            return "return_value"

        method_sym = self.symbol_table.lookup_method(node.callee)
        m_lbl = method_sym.label if method_sym else self.new_label()

        for idx, arg in enumerate(node.args):
            arg_val = self._visit_node(arg)
            if method_sym and idx < len(method_sym.parameters):
                target_param = method_sym.parameters[idx][1]
                self.emit(TACInstruction("=", arg1=arg_val, result=target_param, comment=f"Parámetro {target_param}"))
            else:
                p_temp = self.new_temp()
                self.emit(TACInstruction("=", arg1=arg_val, result=p_temp, comment=f"Parámetro {idx+1}"))

        self.emit(TACInstruction("CALL", arg1=m_lbl, comment=f"Llamada a método {node.callee}"))
        return "return_value"

    def _visit_class_decl(self, node: ClassDeclarationNode) -> None:
        self.emit(TACInstruction("COMMENT", comment=f"Definición clase {node.name}"))
        old_class = self.current_class
        self.current_class = node.name
        for m in node.members:
            self._visit_node(m)
        self.current_class = old_class

    def _visit_new_object(self, node: NewObjectNode) -> str:
        return f"create {node.class_name}"

    def _visit_variable_decl(self, node: VariableDeclarationNode) -> None:
        self.symbol_table.insert_variable(node.name, node.type_name, is_init=(node.initializer is not None))
        self.variable_types[node.name] = node.type_name

        if node.initializer:
            if isinstance(node.initializer, NewObjectNode):
                self.emit(TACInstruction("CREATE", arg1=node.initializer.class_name, result="obj", comment=f"Creación objeto {node.name}"))
            else:
                val = self._visit_node(node.initializer)
                self.emit(TACInstruction("=", arg1=val, result=node.name))

    def _visit_assignment(self, node: AssignmentNode) -> None:
        if isinstance(node.expr, MethodCallNode):
            ret_val = self._visit_node(node.expr)
            self.emit(TACInstruction("=", arg1=ret_val, result=node.target, comment="Asignar retorno de método"))
            return
        if isinstance(node.expr, NewObjectNode):
            self.emit(TACInstruction("CREATE", arg1=node.expr.class_name, result="obj", comment=f"Creación objeto {node.target}"))
            self.variable_types[node.target] = node.expr.class_name
            return

        val = self._visit_node(node.expr)
        self.emit(TACInstruction("=", arg1=val, result=node.target, comment=f"Asigna {val} a {node.target}"))

    def _visit_return(self, node: ReturnNode) -> None:
        if node.expr:
            ret_val = self._visit_node(node.expr)
            self.emit(TACInstruction("=", arg1=ret_val, result="return_value", comment="Guardar valor de retorno"))
            self.emit(TACInstruction("RETURN", arg1="return_value", comment="Retorno de función"))
        else:
            self.emit(TACInstruction("RETURN", comment="Retorno void"))

    def _visit_print(self, node: PrintNode) -> None:
        val = self._visit_node(node.expr)
        self.emit(TACInstruction("PRINT", arg1=val, comment="Salida a consola"))

    def _visit_postfix_op(self, node: PostfixOpNode) -> str:
        op_sign = "+" if node.op == "++" else "-"
        self.emit(TACInstruction(op_sign, arg1=node.var_name, arg2="1", result=node.var_name, comment=f"Postfijo {node.var_name}"))
        return node.var_name

    def _visit_binary_op(self, node: BinaryOpNode) -> str:
        left = self._visit_node(node.left)
        right = self._visit_node(node.right)
        temp = self.new_temp()
        self.emit(TACInstruction(node.op, arg1=left, arg2=right, result=temp, comment=f"{temp} = {left} {node.op} {right}"))
        return temp

    def _visit_unary_op(self, node: UnaryOpNode) -> str:
        val = self._visit_node(node.expr)
        temp = self.new_temp()
        self.emit(TACInstruction(node.op, arg1=val, result=temp, comment=f"{temp} = {node.op}{val}"))
        return temp
