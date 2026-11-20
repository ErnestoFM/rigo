"""
================================================================================
ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
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
from ast_nodes import (
    ASTNode, ProgramNode, VariableDeclarationNode, AssignmentNode,
    BinaryOpNode, UnaryOpNode, IdentifierNode, LiteralNode
)
from tac_instruction import TACInstruction
from symbol_table import SymbolTable
from error_handler import TACErrorHandler


class TACGenerator:
    """
    Generador de Código Intermedio de Tres Direcciones (Three-Address Code).
    Transforma asignaciones, constantes y expresiones en instrucciones lineales
    con etiquetas temporales (t1, t2, ...) y validaciones semánticas integradas.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    OP_DESCRIPTIONS = {
        "+": "suma",
        "-": "resta",
        "*": "multiplicación",
        "/": "división",
        "%": "módulo",
        "==": "comparación de igualdad",
        "!=": "comparación de desigualdad",
        "<": "comparación menor que",
        ">": "comparación mayor que",
        "<=": "comparación menor o igual que",
        ">=": "comparación mayor o igual que",
        "&&": "operación lógica AND",
        "||": "operación lógica OR",
        "!": "negación lógica"
    }

    def __init__(self, symbol_table: Optional[SymbolTable] = None, error_handler: Optional[TACErrorHandler] = None):
        self.symbol_table = symbol_table or SymbolTable()
        self.error_handler = error_handler or TACErrorHandler()
        self.instructions: List[TACInstruction] = []
        self.temp_count = 0

    def reset(self):
        self.instructions.clear()
        self.temp_count = 0
        self.symbol_table.reset()
        self.error_handler.reset()

    def new_temp(self) -> str:
        self.temp_count += 1
        return f"t{self.temp_count}"

    def emit(self, result: str, op: str, arg1: str, arg2: Optional[str] = None, comment: str = ""):
        inst = TACInstruction(result, op, arg1, arg2, comment=comment)
        self.instructions.append(inst)

    def emit_guard(self, guard_text: str, comment: str = ""):
        inst = TACInstruction(result="", op="GUARD", arg1="", arg2=None, comment=comment, is_guard=True, guard_text=guard_text)
        self.instructions.append(inst)

    def generate(self, ast: ProgramNode) -> List[TACInstruction]:
        self.reset()
        for stmt in ast.statements:
            self._gen_statement(stmt)
        return self.instructions

    def _gen_statement(self, stmt: ASTNode):
        if isinstance(stmt, VariableDeclarationNode):
            self.symbol_table.set_type(stmt.name, stmt.var_type)
            if stmt.initializer:
                self._gen_assignment_core(stmt.name, stmt.initializer, stmt.line, stmt.column)

        elif isinstance(stmt, AssignmentNode):
            self._gen_assignment_core(stmt.target, stmt.expr, stmt.line, stmt.column)

    def _gen_assignment_core(self, target: str, expr: ASTNode, line: int = 1, col: int = 1):
        target_type = self.symbol_table.get_type(target)

        # Regla 1 de la Rúbrica: Si es una constante literal directa:
        # t1 = 5       # t1 es una etiqueta temporal que representa la constante 5
        # x = t1       # Asigna el valor de t1 a x
        if isinstance(expr, LiteralNode):
            val_str = f'"{expr.value}"' if expr.literal_type == "string" else str(expr.value)

            # Validar compatibilidad si la variable destino tiene tipo definido
            if target_type == "int" and expr.literal_type == "string":
                self.emit_guard(f'if type({target}) != integer or type("{expr.value}") != integer then error "Type mismatch"', comment="Valida tipos")
                self.error_handler.report(
                    line, col, "Discrepancia de Tipos",
                    f"No se puede asignar una constante de tipo '{expr.literal_type}' a la variable entera '{target}'.",
                    "Asegúrese de que el tipo de la constante coincida con el tipo de la variable."
                )
                return

            t = self.new_temp()
            self.emit(t, "=", val_str, comment=f"{t} es una etiqueta temporal que representa la constante {val_str}")
            self.emit(target, "=", t, comment=f"Asigna el valor de {t} a {target}")
            self.symbol_table.set_type(target, expr.literal_type, expr.value)
            return

        # Para expresiones complejas o binarias
        res_temp = self._gen_expr(expr)
        if res_temp is not None:
            self.emit(target, "=", res_temp, comment=f"Asigna el valor de {res_temp} a {target}")

    def _gen_expr(self, expr: ASTNode) -> Optional[str]:
        if isinstance(expr, LiteralNode):
            val_str = f'"{expr.value}"' if expr.literal_type == "string" else str(expr.value)
            t = self.new_temp()
            self.emit(t, "=", val_str, comment=f"{t} es una etiqueta temporal que representa la constante {val_str}")
            return t

        if isinstance(expr, IdentifierNode):
            return expr.name

        if isinstance(expr, UnaryOpNode):
            operand_temp = self._gen_expr(expr.operand)
            if operand_temp is None:
                return None
            t = self.new_temp()
            op_desc = self.OP_DESCRIPTIONS.get(expr.op, "operación unaria")
            self.emit(t, expr.op, operand_temp, None, comment=f"{t} es una etiqueta temporal para la {op_desc} de {operand_temp}")
            return t

        if isinstance(expr, BinaryOpNode):
            return self._gen_binary_expr(expr)

        return None

    def _gen_binary_expr(self, node: BinaryOpNode) -> Optional[str]:
        op = node.op

        # 1. Validación de División por Cero (Ejemplo Rúbrica)
        if op in ("/", "%"):
            # Si el divisor es un literal 0:
            if isinstance(node.right, LiteralNode) and node.right.value == 0:
                self.emit_guard('if 0 == 0 then error "Division by zero"', comment="Valida que no se realice división por cero")
                self.error_handler.report(
                    node.line, node.column, "División por Cero",
                    f"Error: División por cero en tiempo de compilación detectada con operador '{op}'.",
                    "El denominador no puede ser cero."
                )
                return None
            # Si el divisor es una variable:
            elif isinstance(node.right, IdentifierNode):
                self.emit_guard(f'if {node.right.name} == 0 then error "Division by zero"', comment="Valida que no se realice división por cero")

        # 2. Validación de Incompatibilidad de Tipos (Ejemplo Rúbrica: total = a + "string")
        left_is_str = isinstance(node.left, LiteralNode) and node.left.literal_type == "string"
        right_is_str = isinstance(node.right, LiteralNode) and node.right.literal_type == "string"

        left_name = getattr(node.left, "name", "a")
        right_name = getattr(node.right, "name", "b")

        left_type = "string" if left_is_str else self.symbol_table.get_type(left_name)
        right_type = "string" if right_is_str else self.symbol_table.get_type(right_name)

        if op in ("+", "-", "*", "/", "%"):
            if left_is_str or right_is_str or (left_type == "string" and right_type != "string") or (right_type == "string" and left_type != "string"):
                arg1_disp = f'"{node.left.value}"' if left_is_str else left_name
                arg2_disp = f'"{node.right.value}"' if right_is_str else right_name
                self.emit_guard(
                    f'if type({arg1_disp}) != integer or type({arg2_disp}) != integer then error "Type mismatch"',
                    comment="Valida tipos"
                )
                self.error_handler.report(
                    node.line, node.column, "Incompatibilidad de Tipos",
                    f"Operación inválida entre tipo '{left_type}' y '{right_type}'.",
                    "Asegúrese de operar sobre el mismo tipo de dato numérico."
                )
                return None

        # 3. Validación de Operandos Lógicos No Booleanos
        if op in ("&&", "||"):
            if left_is_str or right_is_str:
                self.emit_guard(
                    f'if type({left_name}) != boolean or type({right_name}) != boolean then error "Type mismatch"',
                    comment="Valida operandos booleanos"
                )
                self.error_handler.report(
                    node.line, node.column, "Operando Lógico Inválido",
                    f"El operador lógico '{op}' requiere operandos de tipo booleano.",
                    "No mezcle cadenas con expresiones booleanas."
                )
                return None

        # Generar código intermedio recursivo
        arg1 = self._gen_expr(node.left)
        arg2 = self._gen_expr(node.right)

        if arg1 is None or arg2 is None:
            return None

        t = self.new_temp()
        desc = self.OP_DESCRIPTIONS.get(op, "operación")
        if op in ("<", ">", "<=", ">=", "==", "!="):
            comment = f"{t} es una etiqueta temporal para la comparación {arg1} {op} {arg2}"
        elif op in ("&&", "||"):
            comment = f"{t} es una etiqueta temporal para la operación lógica {desc} entre {arg1} y {arg2}"
        else:
            comment = f"{t} es una etiqueta temporal que representa la {desc} de {arg1} y {arg2}"

        self.emit(t, op, arg1, arg2, comment=comment)
        return t

    def to_formatted_tac_string(self) -> str:
        if not self.instructions:
            return "# No se generaron instrucciones de código intermedio."
        return "\n".join(inst.to_code_str() for inst in self.instructions)
