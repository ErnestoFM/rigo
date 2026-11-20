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

from typing import Optional


class TACInstruction:
    """
    Representa una instrucción de Código Intermedio de Tres Direcciones (TAC)
    conforme a los ejemplos y formato de la rúbrica oficial.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        result: str,
        op: str,
        arg1: str,
        arg2: Optional[str] = None,
        comment: str = "",
        is_guard: bool = False,
        guard_text: str = ""
    ):
        self.result = result
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.comment = comment
        self.is_guard = is_guard
        self.guard_text = guard_text

    def to_code_str(self) -> str:
        if self.is_guard:
            cmt = f" # {self.comment}" if self.comment else ""
            return f"{self.guard_text}{cmt}"

        if self.op == "=":
            # Asignación simple: x = t1 o t1 = 5
            expr_str = f"{self.result} = {self.arg1}"
        elif self.arg2 is not None:
            # Operación binaria: t3 = x + y
            expr_str = f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        else:
            # Operación unaria: t1 = -x
            expr_str = f"{self.result} = {self.op}{self.arg1}"

        if self.comment:
            return f"{expr_str:<20} # {self.comment}"
        return expr_str

    def __repr__(self) -> str:
        return self.to_code_str()
