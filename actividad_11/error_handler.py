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

from typing import List, Optional


class CompilerError:
    """
    Representa un error léxico, sintáctico o semántico detectado durante
    la fase de compilación y generación de código intermedio.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        error_type: str,
        message: str,
        line: int,
        column: int,
        suggestion: Optional[str] = None,
        offending: Optional[str] = None
    ):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.offending = offending

    def __str__(self) -> str:
        res = f"[{self.error_type}] Línea {self.line}, Columna {self.column}: {self.message}"
        if self.offending:
            res += f" (Cerca de: '{self.offending}')"
        if self.suggestion:
            res += f"\n    -> Sugerencia: {self.suggestion}"
        return res


class CompilerErrorHandler:
    """
    Gestor centralizado de errores para análisis sintáctico y semántico.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[CompilerError] = []

    def report(
        self,
        error_type: str,
        message: str,
        line: int,
        column: int,
        suggestion: Optional[str] = None,
        offending: Optional[str] = None
    ):
        self.errors.append(CompilerError(error_type, message, line, column, suggestion, offending))

    def report_syntax_error(self, message: str, line: int, column: int, suggestion: Optional[str] = None, offending: Optional[str] = None):
        self.report("Error Sintáctico", message, line, column, suggestion, offending)

    def report_semantic_error(self, message: str, line: int, column: int, suggestion: Optional[str] = None, offending: Optional[str] = None):
        self.report("Error Semántico", message, line, column, suggestion, offending)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def clear(self):
        self.errors.clear()

    def get_summary(self) -> str:
        if not self.has_errors:
            return "No se detectaron errores."
        return "\n".join(str(e) for e in self.errors)
