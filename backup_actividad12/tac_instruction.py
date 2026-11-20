"""
================================================================================
ACTIVIDAD 12: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Optional, List, Set


class TACInstruction:
    """
    Representa una instrucción de Código Intermedio de Tres Direcciones (TAC).
    Permite modelar etiquetas, asignaciones simples, operaciones binarias,
    saltos incondicionales y saltos condicionales.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        op: str,
        arg1: Optional[str] = None,
        arg2: Optional[str] = None,
        result: Optional[str] = None,
        comment: Optional[str] = None,
        is_label: bool = False
    ):
        self.op = op
        self.arg1 = str(arg1) if arg1 is not None else None
        self.arg2 = str(arg2) if arg2 is not None else None
        self.result = str(result) if result is not None else None
        self.comment = comment
        self.is_label = is_label

    def is_jump(self) -> bool:
        return self.op in ("GOTO", "IF_GOTO", "IF_NOT_GOTO", "IF_CMP_GOTO")

    def is_unconditional_jump(self) -> bool:
        return self.op == "GOTO"

    def is_conditional_jump(self) -> bool:
        return self.op in ("IF_GOTO", "IF_NOT_GOTO", "IF_CMP_GOTO")

    def is_assignment(self) -> bool:
        return self.op not in ("LABEL", "GOTO", "IF_GOTO", "IF_NOT_GOTO", "IF_CMP_GOTO", "COMMENT", "ERROR") and self.result is not None

    def get_defined_vars(self) -> Set[str]:
        """Retorna las variables escritas/definidas por esta instrucción."""
        if self.is_assignment() and self.result:
            return {self.result}
        return set()

    def get_used_vars(self) -> Set[str]:
        """Retorna las variables leídas/usadas como operandos."""
        used = set()
        for arg in (self.arg1, self.arg2):
            if arg is not None:
                # Comprobar si es un identificador de variable (no número, no cadena, no booleano)
                clean_arg = arg.strip()
                if clean_arg.startswith("==") or clean_arg.startswith("!="):
                    parts = clean_arg.split()
                    if len(parts) > 1:
                        clean_arg = parts[1]
                if clean_arg and not clean_arg.startswith('"') and not clean_arg.replace('.', '', 1).isdigit() and clean_arg not in ("true", "false", "null"):
                    if clean_arg.isidentifier():
                        used.add(clean_arg)
        return used

    def __str__(self) -> str:
        stmt = ""

        # Comentario puro
        if self.op == "COMMENT":
            return f"# {self.comment}" if self.comment else ""

        # Etiqueta
        if self.is_label or self.op == "LABEL":
            lbl = self.result or self.arg1 or "L"
            if not lbl.endswith(":"):
                lbl = f"{lbl}:"
            stmt = f"{lbl:<16}"
            if self.comment:
                stmt = f"{stmt} # {self.comment}"
            return stmt

        # Salto incondicional: 'goto L2'
        if self.op == "GOTO":
            stmt = f"goto {self.result}"

        # Salto condicional simple: 'if t1 goto L1'
        elif self.op == "IF_GOTO":
            stmt = f"if {self.arg1} goto {self.result}"

        # Salto condicional negado: 'if not t1 goto L2'
        elif self.op == "IF_NOT_GOTO":
            stmt = f"if not {self.arg1} goto {self.result}"

        # Salto condicional relacional: 'if a > 10 goto L1' o 'if t2 == 1 goto L1'
        elif self.op == "IF_CMP_GOTO":
            stmt = f"if {self.arg1} {self.arg2} goto {self.result}"

        # Asignación simple: 'result = c'
        elif self.op == "=":
            stmt = f"{self.result} = {self.arg1}"

        # Operación unaria: 't1 = -a'
        elif self.op in ("-u", "!", "not"):
            op_sym = "!" if self.op in ("!", "not") else "-"
            stmt = f"{self.result} = {op_sym}{self.arg1}"

        # Retorno
        elif self.op == "RETURN":
            stmt = f"return {self.arg1}" if self.arg1 else "return"

        # Llamada
        elif self.op == "CALL":
            stmt = f"call {self.arg1}"

        # Error
        elif self.op == "ERROR":
            stmt = f'error "{self.arg1}"'

        # Operación binaria estándar: 't1 = a + b'
        else:
            stmt = f"{self.result} = {self.arg1} {self.op} {self.arg2}"

        if self.comment:
            return f"{stmt:<28} # {self.comment}"
        return stmt
