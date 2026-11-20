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

from typing import List, Optional


class OptimizationLog:
    """
    Registro descriptivo de una optimización aplicada sobre el código intermedio.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, rule_name: str, detail: str, original_code: Optional[str] = None):
        self.rule_name = rule_name
        self.detail = detail
        self.original_code = original_code

    def __str__(self) -> str:
        res = f"[{self.rule_name}] {self.detail}"
        if self.original_code:
            res += f" -> Eliminado/Transformado: '{self.original_code}'"
        return res


class CompilerError:
    """
    Representa un error sintáctico o semántico detectado en el código intermedio.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_type: str, message: str, line: int = 1, suggestion: Optional[str] = None):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.suggestion = suggestion

    def __str__(self) -> str:
        res = f"[{self.error_type}] Línea {self.line}: {self.message}"
        if self.suggestion:
            res += f"\n    -> Sugerencia: {self.suggestion}"
        return res


class CompilerErrorHandler:
    """
    Gestor centralizado de errores y bitácora de optimizaciones.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[CompilerError] = []
        self.optimizations: List[OptimizationLog] = []

    def report_error(self, error_type: str, message: str, line: int = 1, suggestion: Optional[str] = None):
        self.errors.append(CompilerError(error_type, message, line, suggestion))

    def log_optimization(self, rule_name: str, detail: str, original_code: Optional[str] = None):
        self.optimizations.append(OptimizationLog(rule_name, detail, original_code))

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def clear(self):
        self.errors.clear()
        self.optimizations.clear()
