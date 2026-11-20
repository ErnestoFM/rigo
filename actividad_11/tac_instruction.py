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

from typing import Optional


class TACInstruction:
    """
    Representa una instrucción de Código Intermedio de Tres Direcciones (TAC).
    Soporta asignaciones, operaciones binarias/unarias, saltos condicionales,
    etiquetas, llamadas a métodos, creación de objetos y comentarios explicativos.

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
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
        self.comment = comment
        self.is_label = is_label

    def __str__(self) -> str:
        stmt = ""

        # Comentario puro
        if self.op == "COMMENT":
            stmt = f"# {self.comment}" if self.comment else ""
            return stmt

        # Etiqueta: 'L1:'
        if self.is_label or self.op == "LABEL":
            lbl_name = self.result if self.result else (self.arg1 or "L")
            if not lbl_name.endswith(":"):
                lbl_name = f"{lbl_name}:"
            stmt = f"{lbl_name:<16}"
            if self.comment:
                stmt = f"{stmt} # {self.comment}"
            return stmt

        # Salto incondicional: 'goto L2'
        if self.op == "GOTO":
            stmt = f"goto {self.result}"

        # Salto condicional simple: 'if t1 goto L1'
        elif self.op == "IF_GOTO":
            stmt = f"if {self.arg1} goto {self.result}"

        # Salto condicional negado: 'if not t3 goto L2'
        elif self.op == "IF_NOT_GOTO":
            stmt = f"if not {self.arg1} goto {self.result}"

        # Salto condicional relacional: 'if t2 == 1 goto L1'
        elif self.op == "IF_CMP_GOTO":
            stmt = f"if {self.arg1} {self.arg2} goto {self.result}"

        # Creación de objeto: 'obj = create Persona'
        elif self.op == "CREATE":
            stmt = f"{self.result} = create {self.arg1}"

        # Llamada a método: 'call L6' o 'call suma'
        elif self.op == "CALL":
            stmt = f"call {self.arg1}"

        # Retorno de valor: 'return t7' o 'return'
        elif self.op == "RETURN":
            if self.arg1:
                stmt = f"return {self.arg1}"
            else:
                stmt = "return"

        # Asignación simple: 'z = x' o 'result = return_value'
        elif self.op == "=":
            stmt = f"{self.result} = {self.arg1}"

        # Operación unaria: 't1 = -a' o 't1 = !flag'
        elif self.op in ("-u", "!", "not"):
            op_sym = "!" if self.op in ("!", "not") else "-"
            stmt = f"{self.result} = {op_sym}{self.arg1}"

        # Error / guarda de ejecución: 'error "Mensaje"'
        elif self.op == "ERROR":
            stmt = f'error "{self.arg1}"'

        # Operación binaria estándar: 't1 = a + b' o 't1 = x > y'
        else:
            stmt = f"{self.result} = {self.arg1} {self.op} {self.arg2}"

        if self.comment:
            return f"{stmt:<28} # {self.comment}"
        return stmt
