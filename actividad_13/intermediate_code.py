"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - CÓDIGO INTERMEDIO (TAC / CUÁDRUPLOS)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Optional, Tuple, Dict, Any
import re
from ast_nodes import (
    ASTNode,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    VariableDeclarationNode,
    AssignmentNode,
    ReturnNode,
    IfNode,
    WhileNode,
    BinaryOpNode,
    UnaryOpNode,
    IdentifierNode,
    LiteralNode,
    MethodCallNode,
    BlockNode
)


class Quadruple:
    """
    Representa una instrucción de código de tres direcciones (TAC) estructurada
    como cuádruplo: (Operador, Argumento 1, Argumento 2, Resultado).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None, result: Optional[str] = None):
        self.op = op
        self.arg1 = str(arg1) if arg1 is not None else None
        self.arg2 = str(arg2) if arg2 is not None else None
        self.result = str(result) if result is not None else None

    def __str__(self) -> str:
        if self.op == "LABEL":
            return f"{self.result}:"
        elif self.op == "GOTO":
            return f"goto {self.result}"
        elif self.op in ("IF_GOTO", "IF_TRUE_GOTO"):
            return f"if {self.arg1} goto {self.result}"
        elif self.op == "IF_FALSE_GOTO":
            return f"ifFalse {self.arg1} goto {self.result}"
        elif self.op.startswith("IF_"):
            # Condiciones como IF_GT, IF_LT, IF_EQ
            rel_map = {"IF_GT": ">", "IF_LT": "<", "IF_GE": ">=", "IF_LE": "<=", "IF_EQ": "==", "IF_NE": "!="}
            symbol = rel_map.get(self.op, self.op)
            return f"if {self.arg1} {symbol} {self.arg2} goto {self.result}"
        elif self.op == "=":
            return f"{self.result} = {self.arg1}"
        elif self.op == "PRINT":
            return f"print {self.arg1}"
        elif self.op == "HALT":
            return "halt"
        elif self.arg2 is not None:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.arg1 is not None:
            return f"{self.result} = {self.op} {self.arg1}"
        else:
            return f"{self.op} {self.result or ''}".strip()

    def to_tuple_str(self) -> str:
        return f"({self.op}, {self.arg1 or '-'}, {self.arg2 or '-'}, {self.result or '-'})"


class TACGenerator:
    """
    Generador de Código Intermedio de Tres Direcciones (TAC).
    Soporta generación desde el AST del compilador y también análisis
    directo de cadenas TAC (enfoque híbrido).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.quadruples: List[Quadruple] = []
        self.temp_counter: int = 1
        self.label_counter: int = 1
        self.variables_declared: Dict[str, Any] = {}

    def new_temp(self) -> str:
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def new_label(self) -> str:
        label_name = f"L{self.label_counter}"
        self.label_counter += 1
        return label_name

    def emit(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None, result: Optional[str] = None) -> Quadruple:
        quad = Quadruple(op, arg1, arg2, result)
        self.quadruples.append(quad)
        return quad

    def generate_from_ast(self, node: ASTNode) -> List[Quadruple]:
        """Recorre el AST y genera la lista de cuádruplos TAC."""
        self.quadruples = []
        self.temp_counter = 1
        self.label_counter = 1
        self.variables_declared = {}
        self._visit(node)
        return self.quadruples

    def _visit(self, node: ASTNode) -> Optional[str]:
        if node is None:
            return None

        if isinstance(node, ProgramNode):
            for decl in node.declarations:
                self._visit(decl)
            return None

        elif isinstance(node, ClassDeclarationNode):
            for member in node.members:
                self._visit(member)
            return None

        elif isinstance(node, MethodDeclarationNode):
            self.emit("LABEL", result=f"func_{node.name}")
            if node.body:
                self._visit(node.body)
            return None

        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self._visit(stmt)
            return None

        elif isinstance(node, VariableDeclarationNode):
            var_name = node.name
            init_val = None
            if hasattr(node, "initializer") and node.initializer:
                init_val = self._visit(node.initializer)
                self.emit("=", arg1=init_val, result=var_name)
            elif hasattr(node, "initial_value") and node.initial_value:
                init_val = self._visit(node.initial_value)
                self.emit("=", arg1=init_val, result=var_name)
            var_type = getattr(node, "var_type", getattr(node, "data_type", "int"))
            self.variables_declared[var_name] = var_type
            return var_name

        elif isinstance(node, AssignmentNode):
            val = self._visit(getattr(node, "expr", getattr(node, "value", None)))
            target = getattr(node, "target_name", getattr(node, "target", None))
            self.emit("=", arg1=val, result=target)
            return target

        elif isinstance(node, BinaryOpNode):
            left_val = self._visit(node.left)
            right_val = self._visit(node.right)
            temp = self.new_temp()
            bin_op = getattr(node, "op", getattr(node, "operator", "+"))
            self.emit(bin_op, arg1=left_val, arg2=right_val, result=temp)
            return temp

        elif isinstance(node, UnaryOpNode):
            operand_val = self._visit(node.operand)
            temp = self.new_temp()
            un_op = getattr(node, "op", getattr(node, "operator", "-"))
            self.emit(un_op, arg1=operand_val, result=temp)
            return temp

        elif isinstance(node, IdentifierNode):
            return node.name

        elif isinstance(node, LiteralNode):
            return str(node.value)

        elif isinstance(node, IfNode):
            lbl_true = self.new_label()
            lbl_false = self.new_label()
            has_else = (hasattr(node, "else_body") and node.else_body) or (hasattr(node, "else_block") and node.else_block)
            lbl_end = self.new_label() if has_else else lbl_false

            # Evaluar condición relacional o simple
            cond_op = getattr(node.condition, "op", getattr(node.condition, "operator", None)) if isinstance(node.condition, BinaryOpNode) else None
            if cond_op in (">", "<", ">=", "<=", "==", "!="):
                l_val = self._visit(node.condition.left)
                r_val = self._visit(node.condition.right)
                rel_map = {">": "IF_GT", "<": "IF_LT", ">=": "IF_GE", "<=": "IF_LE", "==": "IF_EQ", "!=": "IF_NE"}
                self.emit(rel_map[cond_op], arg1=l_val, arg2=r_val, result=lbl_true)
            else:
                cond_val = self._visit(node.condition)
                self.emit("IF_GOTO", arg1=cond_val, result=lbl_true)

            self.emit("GOTO", result=lbl_false)

            # Bloque Then
            self.emit("LABEL", result=lbl_true)
            then_stmts = getattr(node, "then_body", getattr(node, "then_block", []))
            if isinstance(then_stmts, list):
                for s in then_stmts:
                    self._visit(s)
            else:
                self._visit(then_stmts)

            if has_else:
                self.emit("GOTO", result=lbl_end)
                self.emit("LABEL", result=lbl_false)
                else_stmts = getattr(node, "else_body", getattr(node, "else_block", []))
                if isinstance(else_stmts, list):
                    for s in else_stmts:
                        self._visit(s)
                else:
                    self._visit(else_stmts)
                self.emit("LABEL", result=lbl_end)
            else:
                self.emit("LABEL", result=lbl_false)
            return None

        elif isinstance(node, WhileNode):
            lbl_start = self.new_label()
            lbl_body = self.new_label()
            lbl_end = self.new_label()

            self.emit("LABEL", result=lbl_start)

            cond_op = getattr(node.condition, "op", getattr(node.condition, "operator", None)) if isinstance(node.condition, BinaryOpNode) else None
            if cond_op in (">", "<", ">=", "<=", "==", "!="):
                l_val = self._visit(node.condition.left)
                r_val = self._visit(node.condition.right)
                rel_map = {">": "IF_GT", "<": "IF_LT", ">=": "IF_GE", "<=": "IF_LE", "==": "IF_EQ", "!=": "IF_NE"}
                self.emit(rel_map[cond_op], arg1=l_val, arg2=r_val, result=lbl_body)
            else:
                cond_val = self._visit(node.condition)
                self.emit("IF_GOTO", arg1=cond_val, result=lbl_body)

            self.emit("GOTO", result=lbl_end)

            self.emit("LABEL", result=lbl_body)
            body_stmts = getattr(node, "body", [])
            if isinstance(body_stmts, list):
                for s in body_stmts:
                    self._visit(s)
            else:
                self._visit(body_stmts)

            self.emit("GOTO", result=lbl_start)
            self.emit("LABEL", result=lbl_end)
            return None

        elif isinstance(node, MethodCallNode):
            full_fn_name = node.full_name() if hasattr(node, "full_name") else getattr(node, "name", "")
            # Soporte para console.log o print
            if full_fn_name in ("console.log", "print") or getattr(node, "method_name", "") in ("log", "print"):
                for arg in node.arguments:
                    arg_val = self._visit(arg)
                    self.emit("PRINT", arg1=arg_val)
            else:
                for arg in node.arguments:
                    arg_val = self._visit(arg)
                    self.emit("PARAM", arg1=arg_val)
                temp = self.new_temp()
                self.emit("CALL", arg1=full_fn_name, arg2=str(len(node.arguments)), result=temp)
                return temp
            return None

        elif isinstance(node, ReturnNode):
            ret_val = self._visit(node.expression) if node.expression else None
            self.emit("RETURN", arg1=ret_val)
            return None

        return None

    def parse_tac_text(self, text: str) -> List[Quadruple]:
        """
        Analizador directo de código intermedio textual. Permite procesar
        ejemplos como:
            t1 = a + b
            t2 = t1 * c
            result = t2
            L1:
            goto L2
        """
        self.quadruples = []
        lines = [line.strip() for line in text.strip().split("\n") if line.strip() and not line.strip().startswith("#")]

        for line in lines:
            # Etiqueta: L1:
            if line.endswith(":"):
                lbl = line[:-1].strip()
                self.emit("LABEL", result=lbl)
                continue

            # print x
            if line.startswith("print "):
                val = line[6:].strip()
                self.emit("PRINT", arg1=val)
                continue

            # goto L1
            if line.startswith("goto "):
                lbl = line[5:].strip()
                self.emit("GOTO", result=lbl)
                continue

            # if condition goto L1
            match_if = re.match(r"^if\s+([a-zA-Z0-9_]+)\s*(==|!=|<=|>=|<|>)\s*([a-zA-Z0-9_]+)\s+goto\s+([a-zA-Z0-9_]+)$", line)
            if match_if:
                arg1, rel_op, arg2, target = match_if.groups()
                op_map = {">": "IF_GT", "<": "IF_LT", ">=": "IF_GE", "<=": "IF_LE", "==": "IF_EQ", "!=": "IF_NE"}
                self.emit(op_map.get(rel_op, "IF_GOTO"), arg1=arg1, arg2=arg2, result=target)
                continue

            match_if_simple = re.match(r"^if\s+([a-zA-Z0-9_]+)\s+goto\s+([a-zA-Z0-9_]+)$", line)
            if match_if_simple:
                arg1, target = match_if_simple.groups()
                self.emit("IF_GOTO", arg1=arg1, result=target)
                continue

            # Asignaciones: result = arg1 op arg2 O result = arg1
            if "=" in line:
                target, expr = [part.strip() for part in line.split("=", 1)]

                # Operación binaria: a + b, t1 * c
                match_bin = re.match(r"^([a-zA-Z0-9_\.\"]+)\s*([\+\-\*/%])\s*([a-zA-Z0-9_\.\"]+)$", expr)
                if match_bin:
                    arg1, op, arg2 = match_bin.groups()
                    self.emit(op, arg1=arg1, arg2=arg2, result=target)
                else:
                    # Asignación simple: result = t2
                    self.emit("=", arg1=expr, result=target)
                continue

        return self.quadruples

    def get_tac_text(self) -> str:
        """Devuelve el código de tres direcciones en formato de texto estándar."""
        return "\n".join([str(q) for q in self.quadruples])

    def get_quadruples_summary(self) -> str:
        """Devuelve una tabla formateada con los cuádruplos generados."""
        encabezado = f"{'Índice':<8} | {'Operador':<12} | {'Argumento 1':<14} | {'Argumento 2':<14} | {'Resultado':<14}"
        separador = "-" * len(encabezado)
        filas = [encabezado, separador]
        for idx, q in enumerate(self.quadruples, 1):
            filas.append(f"{idx:<8} | {q.op:<12} | {str(q.arg1 or '-'):<14} | {str(q.arg2 or '-'):<14} | {str(q.result or '-'):<14}")
        return "\n".join(filas)
