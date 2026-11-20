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

from typing import List, Dict


class TACErrorItem:
    """Representa un error o validación semántica durante la generación de código intermedio."""
    def __init__(self, line: int, column: int, category: str, message: str, suggestion: str):
        self.line = line
        self.column = column
        self.category = category
        self.message = message
        self.suggestion = suggestion

    def to_diagnostic_string(self) -> str:
        return (
            f"  --> Línea {self.line}, Columna {self.column} | [{self.category}]\n"
            f"      Descripción: {self.message}\n"
            f"      Sugerencia de corrección: {self.suggestion}"
        )


class TACErrorHandler:
    """Manejador centralizado de errores para el generador de código intermedio."""
    def __init__(self):
        self.errors: List[TACErrorItem] = []

    def reset(self):
        self.errors.clear()

    def report(self, line: int, column: int, category: str, message: str, suggestion: str):
        self.errors.append(TACErrorItem(line, column, category, message, suggestion))

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def to_formatted_table(self) -> str:
        if not self.errors:
            return "✅ Ningún error detectado en la generación de código intermedio."

        sep = "+" + "-" * 5 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 32 + "+" + "-" * 42 + "+"
        header = f"| {'#':<3} | {'LÍNEA':<5} | {'COL':<4} | {'CATEGORÍA DE ERROR':<30} | {'DESCRIPCIÓN Y ACCIÓN':<40} |"
        rows = [sep, header, sep]

        for idx, err in enumerate(self.errors, 1):
            short_msg = f"{err.message}"
            if len(short_msg) > 38:
                short_msg = short_msg[:35] + "..."
            rows.append(
                f"| {idx:<3} | {err.line:<5} | {err.column:<4} | {err.category:<30} | {short_msg:<40} |"
            )
        rows.append(sep)
        return "\n".join(rows)
