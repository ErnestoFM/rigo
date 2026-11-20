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
    Generador de Código Intermedio de Tres Direcciones (TAC) enfocado en
    estructuras de control de flujo (if/else, switch-case), bucles (while, for, do-while),
    métodos (definición y llamadas con paso de parámetros y retornos) y
    clases (definición, instanciación de objetos e invocación de métodos de instancia).

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
        self.variable_types: Dict[str, str] = {}  # var_name -> tipo (ej. p -> Persona)

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instr: TACInstruction):
        self.instructions.append(instr)

    def generate(self, root: ProgramNode) -> List[TACInstruction]:
        self.instructions.clear()
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table = SymbolTable(scope_name="global")
        self.variable_types.clear()

        # Primer pase: registrar clases y firmas de métodos globales y de clases
        self._pre_register_symbols(root)

        # Segundo pase: generación de código intermedio
        for decl in root.declarations:
            self._visit_node(decl)

        return self.instructions

    # -------------------------------------------------------------------------
    # PRE-REGISTRO DE SÍMBOLOS (MÉTODOS Y CLASES)
    # -------------------------------------------------------------------------

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
                        # También disponible en symbol_table
                        self.symbol_table.methods[f"{node.name}.{member.name}"] = m_sym
                    elif isinstance(member, VariableDeclarationNode):
                        cls_sym.fields[member.name] = member.type_name
            elif isinstance(node, MethodDeclarationNode):
                lbl = self.new_label()
                params = [(p.type_name, p.name) for p in node.parameters]
                self.symbol_table.insert_method(node.name, node.return_type, params, lbl)

    # -------------------------------------------------------------------------
    # DESPACHO DE NODOS (VISITOR)
    # -------------------------------------------------------------------------

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
            return self._visit_break(node)
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
    # 1. ESTRUCTURAS CONDICIONALES: IF / ELSE Y SWITCH
    # -------------------------------------------------------------------------

    def _visit_if(self, node: IfNode) -> None:
        # Validación semántica: la condición no debe ser una cadena pura
        if isinstance(node.condition, LiteralNode) and node.condition.type_name == "string":
            self.error_handler.report_semantic_error(
                f"La condición del 'if' no puede ser una cadena literal (tipo inválido '{node.condition.value}').",
                node.line, node.column,
                suggestion="Utilice una expresión relacional o booleana (ej. 'x > y')."
            )
            self.emit(TACInstruction("ERROR", arg1="Tipo incompatible en condición de if"))
            return

        # Generar TAC para la condición
        cond_temp = self._visit_node(node.condition)

        # Caso con bloque 'else' (Ejemplo exacto de la rúbrica):
        # t1 = x > y      # t1 es una etiqueta temporal para la comparación x > y
        # if t1 goto L1   # Si t1 es verdadero, salta a la etiqueta L1
        # z = y           # Si t1 es falso, asigna y a z
        # goto L2         # Salta a la etiqueta L2 después del bloque else
        # L1:             # Etiqueta L1 para el bloque if
        # z = x           # Asigna x a z
        # L2:             # Etiqueta L2 marca el final de la estructura condicional
        if node.else_block is not None:
            l_then = self.new_label()
            l_end = self.new_label()

            self.emit(TACInstruction(
                "IF_GOTO",
                arg1=cond_temp,
                result=l_then,
                comment=f"Si {cond_temp} es verdadero, salta a la etiqueta {l_then}"
            ))

            # Bloque else
            for stmt in node.else_block:
                self._visit_node(stmt)

            self.emit(TACInstruction(
                "GOTO",
                result=l_end,
                comment=f"Salta a la etiqueta {l_end} después del bloque else"
            ))

            # Etiqueta L1 para el bloque if
            self.emit(TACInstruction(
                "LABEL",
                result=l_then,
                comment=f"Etiqueta {l_then} para el bloque if",
                is_label=True
            ))

            # Bloque then
            for stmt in node.then_block:
                self._visit_node(stmt)

            # Etiqueta L2 marca el final
            self.emit(TACInstruction(
                "LABEL",
                result=l_end,
                comment=f"Etiqueta {l_end} marca el final de la estructura condicional",
                is_label=True
            ))
        else:
            # Caso if simple sin else:
            # if not t1 goto Lend
            # [then block]
            # Lend:
            l_end = self.new_label()
            self.emit(TACInstruction(
                "IF_NOT_GOTO",
                arg1=cond_temp,
                result=l_end,
                comment=f"Si {cond_temp} es falso, salta a la etiqueta {l_end}"
            ))
            for stmt in node.then_block:
                self._visit_node(stmt)
            self.emit(TACInstruction(
                "LABEL",
                result=l_end,
                comment=f"Etiqueta {l_end} marca el final de la estructura condicional",
                is_label=True
            ))

    def _visit_switch(self, node: SwitchNode) -> None:
        # Ejemplo exacto de la rúbrica:
        # t2 = n         # t2 es una etiqueta temporal para el valor de n
        # if t2 == 1 goto L1  # Si t2 es 1, salta a la etiqueta L1
        # if t2 == 2 goto L2  # Si t2 es 2, salta a la etiqueta L2
        # goto L3         # Si t2 no es ni 1 ni 2, salta a la etiqueta L3
        # L1:              # Etiqueta L1 para el caso 1
        # result = "Uno"
        # goto L4          # Salta a la etiqueta L4 después de manejar el caso 1
        # L2:              # Etiqueta L2 para el caso 2
        # result = "Dos"
        # goto L4          # Salta a la etiqueta L4 después de manejar el caso 2
        # L3:              # Etiqueta L3 para el caso default
        # result = "Otro"
        # L4:              # Etiqueta L4 marca el final de la estructura switch

        switch_temp = self.new_temp()
        expr_val = self._visit_node(node.expression)
        self.emit(TACInstruction(
            "=",
            arg1=expr_val,
            result=switch_temp,
            comment=f"{switch_temp} es una etiqueta temporal para el valor de {expr_val}"
        ))

        # Asignar etiquetas para cada caso, default y final
        case_labels = [self.new_label() for _ in node.cases]
        l_default = self.new_label() if node.default_block is not None else None
        l_end = self.new_label()

        # Emitir comparaciones de saltos
        for case_node, lbl in zip(node.cases, case_labels):
            val_str = self._visit_node(case_node.value)
            self.emit(TACInstruction(
                "IF_CMP_GOTO",
                arg1=switch_temp,
                arg2=f"== {val_str}",
                result=lbl,
                comment=f"Si {switch_temp} es {val_str}, salta a la etiqueta {lbl}"
            ))

        # Salto a default o fin
        if l_default:
            self.emit(TACInstruction(
                "GOTO",
                result=l_default,
                comment=f"Si {switch_temp} no coincide con ningún caso, salta a la etiqueta {l_default}"
            ))
        else:
            self.emit(TACInstruction(
                "GOTO",
                result=l_end,
                comment=f"Salta al final {l_end} si ningún caso coincide"
            ))

        # Emitir cuerpos de los casos
        for idx, (case_node, lbl) in enumerate(zip(node.cases, case_labels), start=1):
            val_str = self._visit_node(case_node.value)
            self.emit(TACInstruction(
                "LABEL",
                result=lbl,
                comment=f"Etiqueta {lbl} para el caso {val_str}",
                is_label=True
            ))
            for stmt in case_node.body:
                self._visit_node(stmt)
            self.emit(TACInstruction(
                "GOTO",
                result=l_end,
                comment=f"Salta a la etiqueta {l_end} después de manejar el caso {val_str}"
            ))

        # Emitir caso default
        if l_default and node.default_block is not None:
            self.emit(TACInstruction(
                "LABEL",
                result=l_default,
                comment=f"Etiqueta {l_default} para el caso default",
                is_label=True
            ))
            for stmt in node.default_block:
                self._visit_node(stmt)

        # Etiqueta final
        self.emit(TACInstruction(
            "LABEL",
            result=l_end,
            comment=f"Etiqueta {l_end} marca el final de la estructura switch",
            is_label=True
        ))

    # -------------------------------------------------------------------------
    # 2. GENERACIÓN DE CÓDIGO INTERMEDIO PARA BUCLES: WHILE, FOR, DO-WHILE
    # -------------------------------------------------------------------------

    def _visit_while(self, node: WhileNode) -> None:
        # Validación semántica
        if isinstance(node.condition, LiteralNode) and node.condition.type_name == "string":
            self.error_handler.report_semantic_error(
                f"La condición del bucle 'while' no puede ser una cadena ('{node.condition.value}').",
                node.line, node.column,
                suggestion="Utilice una expresión relacional o booleana."
            )
            self.emit(TACInstruction("ERROR", arg1="Tipo incompatible en condición de while"))
            return

        # Ejemplo exacto de la rúbrica:
        # L1:            # Etiqueta L1 marca el inicio del bucle
        # t3 = i < 10    # t3 es una etiqueta temporal para la condición i < 10
        # if not t3 goto L2  # Si t3 es falso, salta a la etiqueta L2 (fin del bucle)
        # i = i + 1      # Incrementa i
        # goto L1        # Salta de vuelta al inicio del bucle
        # L2:            # Etiqueta L2 marca el final del bucle
        l_start = self.new_label()
        l_end = self.new_label()

        self.emit(TACInstruction(
            "LABEL",
            result=l_start,
            comment=f"Etiqueta {l_start} marca el inicio del bucle",
            is_label=True
        ))

        cond_temp = self._visit_node(node.condition)

        self.emit(TACInstruction(
            "IF_NOT_GOTO",
            arg1=cond_temp,
            result=l_end,
            comment=f"Si {cond_temp} es falso, salta a la etiqueta {l_end} (fin del bucle)"
        ))

        for stmt in node.body:
            self._visit_node(stmt)

        self.emit(TACInstruction(
            "GOTO",
            result=l_start,
            comment=f"Salta de vuelta al inicio del bucle {l_start}"
        ))

        self.emit(TACInstruction(
            "LABEL",
            result=l_end,
            comment=f"Etiqueta {l_end} marca el final del bucle",
            is_label=True
        ))

    def _visit_for(self, node: ForNode) -> None:
        # Ejemplo exacto de la rúbrica:
        # i = 0          # Inicialización
        # L3:            # Etiqueta L3 marca el inicio del bucle
        # t4 = i < 5     # t4 es una etiqueta temporal para la condición i < 5
        # if not t4 goto L4  # Si t4 es falso, salta a la etiqueta L4 (fin del bucle)
        # t5 = sum + i   # t5 es una etiqueta temporal para la suma de sum e i
        # sum = t5       # Asigna el valor de t5 a sum
        # i = i + 1      # Incrementa i
        # goto L3        # Salta de vuelta al inicio del bucle
        # L4:            # Etiqueta L4 marca el final del bucle

        # Inicialización
        if node.initializer:
            if isinstance(node.initializer, VariableDeclarationNode):
                init_val = self._visit_node(node.initializer.initializer) if node.initializer.initializer else "0"
                self.emit(TACInstruction("=", arg1=init_val, result=node.initializer.name, comment="Inicialización"))
            elif isinstance(node.initializer, AssignmentNode):
                init_val = self._visit_node(node.initializer.expr)
                self.emit(TACInstruction("=", arg1=init_val, result=node.initializer.target, comment="Inicialización"))

        l_start = self.new_label()
        l_end = self.new_label()

        self.emit(TACInstruction(
            "LABEL",
            result=l_start,
            comment=f"Etiqueta {l_start} marca el inicio del bucle",
            is_label=True
        ))

        if node.condition:
            cond_temp = self._visit_node(node.condition)
            self.emit(TACInstruction(
                "IF_NOT_GOTO",
                arg1=cond_temp,
                result=l_end,
                comment=f"Si {cond_temp} es falso, salta a la etiqueta {l_end} (fin del bucle)"
            ))

        for stmt in node.body:
            self._visit_node(stmt)

        # Actualización
        if node.update:
            if isinstance(node.update, PostfixOpNode):
                # i++ -> i = i + 1
                op_sign = "+" if node.update.op == "++" else "-"
                action_name = "Incrementa" if node.update.op == "++" else "Decrementa"
                self.emit(TACInstruction(
                    op_sign,
                    arg1=node.update.var_name,
                    arg2="1",
                    result=node.update.var_name,
                    comment=f"{action_name} {node.update.var_name}"
                ))
            elif isinstance(node.update, AssignmentNode):
                val = self._visit_node(node.update.expr)
                self.emit(TACInstruction("=", arg1=val, result=node.update.target, comment="Actualización del contador"))

        self.emit(TACInstruction(
            "GOTO",
            result=l_start,
            comment=f"Salta de vuelta al inicio del bucle {l_start}"
        ))

        self.emit(TACInstruction(
            "LABEL",
            result=l_end,
            comment=f"Etiqueta {l_end} marca el final del bucle",
            is_label=True
        ))

    def _visit_do_while(self, node: DoWhileNode) -> None:
        # Ejemplo exacto de la rúbrica:
        # L5:            # Etiqueta L5 marca el inicio del bucle
        # count = count + 1  # Incrementa count
        # t6 = count < 10    # t6 es una etiqueta temporal para la condición count < 10
        # if t6 goto L5      # Si t6 es verdadero, salta de vuelta al inicio del bucle
        l_start = self.new_label()

        self.emit(TACInstruction(
            "LABEL",
            result=l_start,
            comment=f"Etiqueta {l_start} marca el inicio del bucle",
            is_label=True
        ))

        for stmt in node.body:
            self._visit_node(stmt)

        cond_temp = self._visit_node(node.condition)

        self.emit(TACInstruction(
            "IF_GOTO",
            arg1=cond_temp,
            result=l_start,
            comment=f"Si {cond_temp} es verdadero, salta de vuelta al inicio del bucle {l_start}"
        ))

    # -------------------------------------------------------------------------
    # 3. GENERACIÓN DE CÓDIGO INTERMEDIO PARA MÉTODOS
    # -------------------------------------------------------------------------

    def _visit_method_decl(self, node: MethodDeclarationNode) -> None:
        # Ejemplo exacto de la rúbrica:
        # # Definición del método suma
        # L6:            # Etiqueta L6 marca el inicio del método suma
        # t7 = a + b     # t7 es una etiqueta temporal para la suma de a y b
        # return t7      # Retorna el valor de t7

        key = f"{self.current_class}.{node.name}" if self.current_class else node.name
        sym = self.symbol_table.lookup_method(key) or self.symbol_table.lookup_method(node.name)
        m_lbl = sym.label if sym else self.new_label()

        self.emit(TACInstruction("COMMENT", comment=f"Definición del método {node.name}"))
        self.emit(TACInstruction(
            "LABEL",
            result=m_lbl,
            comment=f"Etiqueta {m_lbl} marca el inicio del método {node.name}",
            is_label=True
        ))

        # Registrar parámetros en el ámbito local
        for p in node.parameters:
            self.symbol_table.insert_variable(p.name, p.type_name)

        for stmt in node.body:
            self._visit_node(stmt)

    def _visit_method_call(self, node: MethodCallNode) -> str:
        # Ejemplo exacto de la rúbrica:
        # result = suma(5, 3);
        # t8 = 5         # t8 es una etiqueta temporal para el primer parámetro
        # t9 = 3         # t9 es una etiqueta temporal para el segundo parámetro
        # call L6        # Llama al método definido en la etiqueta L6
        # result = return_value  # Asigna el valor retornado por el método a result

        # Caso llamada sobre objeto: p.celebrarCumpleaños()
        if node.obj_name:
            obj_type = self.variable_types.get(node.obj_name)
            if not obj_type:
                # Comprobar si existe la clase
                self.error_handler.report_semantic_error(
                    f"El objeto '{node.obj_name}' no ha sido declarado o inicializado.",
                    node.line, node.column,
                    suggestion=f"Declare e instancie el objeto antes de invocar métodos (ej. 'MiClase {node.obj_name} = new MiClase();')."
                )
                self.emit(TACInstruction("ERROR", arg1=f"Objeto no declarado '{node.obj_name}'"))
                return "error"

            cls_sym = self.symbol_table.lookup_class(obj_type)
            if not cls_sym or node.callee not in cls_sym.methods:
                self.error_handler.report_semantic_error(
                    f"La clase '{obj_type}' no define ningún método llamado '{node.callee}'.",
                    node.line, node.column,
                    suggestion=f"Verifique la definición de la clase '{obj_type}' o el nombre del método '{node.callee}'."
                )
                self.emit(TACInstruction("ERROR", arg1=f"Método '{node.callee}' no existe en la clase '{obj_type}'"))
                return "error"

            method_sym = cls_sym.methods[node.callee]
            m_lbl = method_sym.label

            # Generar temporales para parámetros
            arg_temps = []
            ordinal_names = ["primer", "segundo", "tercer", "cuarto", "quinto"]
            for idx, arg in enumerate(node.args):
                p_temp = self.new_temp()
                arg_val = self._visit_node(arg)
                ord_name = ordinal_names[idx] if idx < len(ordinal_names) else f"{idx+1}º"
                self.emit(TACInstruction(
                    "=",
                    arg1=arg_val,
                    result=p_temp,
                    comment=f"{p_temp} es una etiqueta temporal para el {ord_name} parámetro"
                ))
                arg_temps.append(p_temp)

            self.emit(TACInstruction(
                "CALL",
                arg1=m_lbl,
                comment=f"Llama al método {node.callee} del objeto {node.obj_name}"
            ))
            return "return_value"

        # Caso función global
        method_sym = self.symbol_table.lookup_method(node.callee)
        if not method_sym:
            self.error_handler.report_semantic_error(
                f"Llamada a método o función no declarada '{node.callee}'.",
                node.line, node.column,
                suggestion=f"Defina la función '{node.callee}' antes de invocarla."
            )
            self.emit(TACInstruction("ERROR", arg1=f"Llamada a método no declarado '{node.callee}'"))
            return "error"

        # Verificación de aridad (número de argumentos)
        expected_params = len(method_sym.parameters)
        provided_args = len(node.args)
        if expected_params != provided_args:
            self.error_handler.report_semantic_error(
                f"La función '{node.callee}' espera {expected_params} argumentos pero se proporcionaron {provided_args}.",
                node.line, node.column,
                suggestion=f"Ajuste los argumentos para cumplir con la firma: '{node.callee}({', '.join(t + ' ' + n for t, n in method_sym.parameters)})'."
            )
            self.emit(TACInstruction("ERROR", arg1=f"Aridad incorrecta en llamada a '{node.callee}'"))
            return "error"

        # Generar temporales para cada argumento
        ordinal_names = ["primer", "segundo", "tercer", "cuarto", "quinto"]
        for idx, arg in enumerate(node.args):
            p_temp = self.new_temp()
            arg_val = self._visit_node(arg)
            ord_name = ordinal_names[idx] if idx < len(ordinal_names) else f"{idx+1}º"
            self.emit(TACInstruction(
                "=",
                arg1=arg_val,
                result=p_temp,
                comment=f"{p_temp} es una etiqueta temporal para el {ord_name} parámetro"
            ))

        self.emit(TACInstruction(
            "CALL",
            arg1=method_sym.label,
            comment=f"Llama al método definido en la etiqueta {method_sym.label}"
        ))

        return "return_value"

    # -------------------------------------------------------------------------
    # 4. GENERACIÓN DE CÓDIGO INTERMEDIO PARA CLASES Y OBJETOS
    # -------------------------------------------------------------------------

    def _visit_class_decl(self, node: ClassDeclarationNode) -> None:
        # Ejemplo exacto de la rúbrica:
        # # Definición de la clase Persona
        # # (omitiendo detalles de manejo interno de objetos para simplicidad)
        # L7:            # Etiqueta L7 marca el inicio del método celebrarCumpleaños
        # t10 = edad + 1 # t10 es una etiqueta temporal para la nueva edad
        # edad = t10     # Actualiza la edad
        self.emit(TACInstruction("COMMENT", comment=f"Definición de la clase {node.name}"))
        self.emit(TACInstruction("COMMENT", comment="(omitiendo detalles de manejo interno de objetos para simplicidad)"))

        old_class = self.current_class
        self.current_class = node.name

        for member in node.members:
            self._visit_node(member)

        self.current_class = old_class

    def _visit_new_object(self, node: NewObjectNode) -> str:
        # Validación semántica: ¿existe la clase?
        cls_sym = self.symbol_table.lookup_class(node.class_name)
        if not cls_sym:
            self.error_handler.report_semantic_error(
                f"Intento de instanciar una clase no declarada: '{node.class_name}'.",
                node.line, node.column,
                suggestion=f"Declare la clase 'class {node.class_name} {{ ... }}' antes de instanciarla."
            )
            self.emit(TACInstruction("ERROR", arg1=f"Clase no declarada '{node.class_name}'"))
            return "null"

        return f"create {node.class_name}"

    # -------------------------------------------------------------------------
    # SENTENCIAS COMUNES (ASIGNACIÓN, RETORNO, VARIABLES)
    # -------------------------------------------------------------------------

    def _visit_variable_decl(self, node: VariableDeclarationNode) -> None:
        self.symbol_table.insert_variable(node.name, node.type_name)
        self.variable_types[node.name] = node.type_name

        if node.initializer:
            if isinstance(node.initializer, NewObjectNode):
                # Ejemplo exacto de la rúbrica:
                # Persona p = new Persona();
                # obj = create Persona  # Representa la creación del objeto p
                self.emit(TACInstruction("COMMENT", comment=f"Creación del objeto {node.initializer.class_name}"))
                create_expr = self._visit_node(node.initializer)
                if create_expr != "null":
                    cls_name = node.initializer.class_name
                    self.emit(TACInstruction(
                        "CREATE",
                        arg1=cls_name,
                        result="obj",
                        comment=f"Representa la creación del objeto {node.name}"
                    ))
            else:
                val = self._visit_node(node.initializer)
                self.emit(TACInstruction("=", arg1=val, result=node.name))

    def _visit_assignment(self, node: AssignmentNode) -> None:
        if isinstance(node.expr, MethodCallNode):
            # Invocación de método que asigna a variable:
            # result = suma(5, 3)
            # call L6
            # result = return_value
            ret_val = self._visit_node(node.expr)
            if ret_val != "error":
                self.emit(TACInstruction(
                    "=",
                    arg1=ret_val,
                    result=node.target,
                    comment=f"Asigna el valor retornado por el método a {node.target}"
                ))
            return

        if isinstance(node.expr, NewObjectNode):
            # Creación de objeto asignado: obj = create Persona
            self.emit(TACInstruction("COMMENT", comment=f"Creación del objeto {node.expr.class_name}"))
            self.emit(TACInstruction(
                "CREATE",
                arg1=node.expr.class_name,
                result="obj",
                comment=f"Representa la creación del objeto {node.target}"
            ))
            self.variable_types[node.target] = node.expr.class_name
            return

        # Asignación estándar o con expresión
        val = self._visit_node(node.expr)
        self.emit(TACInstruction("=", arg1=val, result=node.target, comment=f"Asigna {val} a {node.target}"))

    def _visit_return(self, node: ReturnNode) -> None:
        ret_val = self._visit_node(node.expr) if node.expr else None
        comment = f"Retorna el valor de {ret_val}" if ret_val else "Retorna del método"
        self.emit(TACInstruction("RETURN", arg1=ret_val, comment=comment))

    def _visit_break(self, node: BreakNode) -> None:
        # break se maneja directamente en bucles o switches
        pass

    def _visit_postfix_op(self, node: PostfixOpNode) -> str:
        # count = count + 1  # Incrementa count
        op_sign = "+" if node.op == "++" else "-"
        action = "Incrementa" if node.op == "++" else "Decrementa"
        self.emit(TACInstruction(
            op_sign,
            arg1=node.var_name,
            arg2="1",
            result=node.var_name,
            comment=f"{action} {node.var_name}"
        ))
        return node.var_name

    def _visit_binary_op(self, node: BinaryOpNode) -> str:
        left_val = self._visit_node(node.left)
        right_val = self._visit_node(node.right)
        temp = self.new_temp()

        # Generar comentario descriptivo según el tipo de operador
        comment = None
        if node.op in (">", "<", ">=", "<=", "==", "!="):
            comment = f"{temp} es una etiqueta temporal para la condición {left_val} {node.op} {right_val}"
        elif node.op in ("&&", "||"):
            comment = f"{temp} es una etiqueta temporal para la operación lógica {left_val} {node.op} {right_val}"
        elif node.op in ("+", "-", "*", "/"):
            op_names = {"+": "suma", "-": "resta", "*": "multiplicación", "/": "división"}
            op_name = op_names.get(node.op, "operación")
            comment = f"{temp} es una etiqueta temporal para la {op_name} de {left_val} y {right_val}"

        self.emit(TACInstruction(
            node.op,
            arg1=left_val,
            arg2=right_val,
            result=temp,
            comment=comment
        ))
        return temp

    def _visit_unary_op(self, node: UnaryOpNode) -> str:
        val = self._visit_node(node.expr)
        temp = self.new_temp()
        self.emit(TACInstruction(
            node.op,
            arg1=val,
            result=temp,
            comment=f"{temp} es una etiqueta temporal para la operación unaria {node.op}{val}"
        ))
        return temp
