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

from typing import List, Optional


class CompilerError:
    """
    Representa un error diagnosticado en alguna de las fases del compilador.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        phase: str,
        message: str,
        line: int = 1,
        column: int = 1,
        suggestion: Optional[str] = None,
        offending: Optional[str] = None
    ):
        self.phase = phase
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.offending = offending

    def __str__(self) -> str:
        res = f"[{self.phase}] Línea {self.line}, Columna {self.column}: {self.message}"
        if self.offending:
            res += f" (Cerca de: '{self.offending}')"
        if self.suggestion:
            res += f"\n    -> Sugerencia: {self.suggestion}"
        return res


class CompilerErrorHandler:
    """
    Gestor centralizado de diagnósticos y bitácora de optimizaciones para el compilador.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[CompilerError] = []
        self.optimization_logs: List[str] = []

    def report(
        self,
        phase: str,
        message: str,
        line: int = 1,
        column: int = 1,
        suggestion: Optional[str] = None,
        offending: Optional[str] = None
    ):
        self.errors.append(CompilerError(phase, message, line, column, suggestion, offending))

    def report_lexical(self, message: str, line: int, column: int, suggestion: Optional[str] = None, offending: Optional[str] = None):
        self.report("Error Léxico", message, line, column, suggestion, offending)

    def report_syntax(self, message: str, line: int, column: int, suggestion: Optional[str] = None, offending: Optional[str] = None):
        self.report("Error Sintáctico", message, line, column, suggestion, offending)

    def report_semantic(self, message: str, line: int, column: int, suggestion: Optional[str] = None, offending: Optional[str] = None):
        self.report("Error Semántico", message, line, column, suggestion, offending)

    def log_optimization(self, message: str):
        self.optimization_logs.append(message)

    def has_errors_method(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_errors(self) -> List[CompilerError]:
        return list(self.errors)

    def clear(self):
        self.errors.clear()
        self.optimization_logs.clear()

    def get_summary(self) -> str:
        if not self.has_errors:
            return "Compilación completada sin errores."
        return "\n".join(str(e) for e in self.errors)
