"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List

class SyntaxErrorItem:
    """
    Representa un error sintáctico con su ubicación y descripción estandarizada.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, message: str, line: int, column: int, category: str = "ERROR SINTÁCTICO", suggestion: str = "", offending_token: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.category = category
        self.suggestion = suggestion
        self.offending_token = offending_token

    def __str__(self) -> str:
        base = f"Error: {self.message} en la línea {self.line}, columna {self.column}."
        if self.suggestion:
            base += f" {self.suggestion}"
        return base


class SyntaxErrorHandler:
    """
    Manejador centralizado de errores sintácticos.
    Garantiza el cumplimiento exacto del formato solicitado en la rúbrica oficial.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[SyntaxErrorItem] = []

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def add_error(self, message: str, line: int, column: int, category: str = "ERROR SINTÁCTICO", suggestion: str = "", offending_token: str = ""):
        error = SyntaxErrorItem(message, line, column, category, suggestion, offending_token)
        self.errors.append(error)

    # -------------------------------------------------------------------------
    # MÉTODOS ESTANDARIZADOS CONFORME A LA RÚBRICA OFICIAL DEL PROFESOR
    # -------------------------------------------------------------------------

    def report_operator_without_term(self, op: str, line: int, column: int, suggestion: str = ""):
        """
        Regla específica requerida:
        'Error: Operador sin término en la línea X, columna Y.'
        """
        msg = "Operador sin término"
        sugg = suggestion or f"El operador '{op}' carece de un operando o factor válido posterior."
        self.add_error(msg, line, column, category="OPERADOR_SIN_TERMINO", suggestion=sugg, offending_token=op)

    def report_invalid_comparison(self, line: int, column: int, op: str = "", suggestion: str = ""):
        """
        Regla específica requerida:
        'Error: Comparación inválida en la línea X, columna Y.'
        """
        msg = "Comparación inválida"
        sugg = suggestion or f"La comparación con '{op}' requiere una expresión aritmética válida en ambos lados."
        self.add_error(msg, line, column, category="COMPARACION_INVALIDA", suggestion=sugg, offending_token=op)

    def report_unbalanced_parentheses(self, line: int, column: int, suggestion: str = "", paren: str = "("):
        """
        Regla específica requerida:
        'Error: Paréntesis desbalanceados en la línea X, columna Y.'
        """
        msg = "Paréntesis desbalanceados"
        sugg = suggestion or "Asegúrese de cerrar y emparejar correctamente todos los paréntesis abiertos."
        self.add_error(msg, line, column, category="PARENTESIS_DESBALANCEADOS", suggestion=sugg, offending_token=paren)

    def report_incomplete_logical_expression(self, op: str, line: int, column: int, suggestion: str = ""):
        """
        Reporta operadores lógicos incompletos o sin término.
        """
        msg = "Expresión lógica incompleta o malformada"
        sugg = suggestion or f"El operador lógico '{op}' requiere términos lógicos válidos en ambos extremos."
        self.add_error(msg, line, column, category="LOGICA_INCOMPLETA", suggestion=sugg, offending_token=op)

    def report_missing_operator(self, line: int, column: int, token_val: str, suggestion: str = ""):
        """
        Reporta falta de operador entre dos términos adyacentes (e.g. 'a + b c').
        """
        msg = f"Falta operador entre términos antes de '{token_val}'"
        sugg = suggestion or "Inserte un operador aritmético o relacional entre los operandos."
        self.add_error(msg, line, column, category="FALTA_OPERADOR", suggestion=sugg, offending_token=token_val)

    def report_general_syntax_error(self, expected: str, found: str, line: int, column: int):
        msg = f"Se esperaba {expected} pero se encontró '{found}'"
        sugg = f"Verifique la estructura de la expresión cerca de la columna {column}."
        self.add_error(msg, line, column, category="SINTAXIS_GENERAL", suggestion=sugg, offending_token=found)

    def print_error_report(self):
        """Imprime una tabla elegante y estructurada con todos los errores detectados."""
        if not self.errors:
            print("  ✔ No se registraron errores sintácticos.")
            return

        print("\n  ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("  ║                      TABLA DE DIAGNÓSTICO DE ERRORES SINTÁCTICOS                              ║")
        print("  ╠═════╦════════╦════════╦═════════════════════════════════╦═════════════════════════════════════╣")
        print("  ║  #  ║ LÍNEA  ║  COL.  ║ MENSAJE ESTÁNDAR DE ERROR       ║ SUGERENCIA PEDAGÓGICA               ║")
        print("  ╠═════╬════════╬════════╬═════════════════════════════════╬═════════════════════════════════════╣")
        for i, err in enumerate(self.errors, 1):
            std_msg = f"Error: {err.message}"
            print(f"  ║ {i:3d} ║  {err.line:4d}  ║  {err.column:4d}  ║ {std_msg[:31]:<31} ║ {err.suggestion[:35]:<35} ║")
        print("  ╚═════╩════════╩════════╩═════════════════════════════════╩═════════════════════════════════════╝")
        
        print("\n  [DETALLE PRECISO DE CADA ERROR]:")
        for i, err in enumerate(self.errors, 1):
            print(f"   [{i}] {err}")
