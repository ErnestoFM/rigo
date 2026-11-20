"""
================================================================================
ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from enum import Enum
from typing import List, Dict, Any, Optional


class LexicalErrorCategory(Enum):
    """
    Categorías formales de errores léxicos requeridas por la rúbrica oficial.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    CARACTER_NO_RECONOCIDO = "Carácter No Reconocido"
    IDENTIFICADOR_MAL_FORMADO = "Identificador Mal Formado"
    NUMERO_INCORRECTO = "Literal Numérico Incorrecto"
    CADENA_MAL_FORMADA = "Cadena de Texto Mal Formada"


class LexicalError:
    """
    Estructura informativa detallada de un error léxico detectado.
    Contiene la ubicación exacta (línea y columna), la categoría, el lexema defectuoso,
    la descripción del problema y una sugerencia pedagógica de corrección.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        line: int,
        column: int,
        category: LexicalErrorCategory,
        lexeme: str,
        message: str,
        suggestion: str
    ):
        self.line = line
        self.column = column
        self.category = category
        self.lexeme = lexeme
        self.message = message
        self.suggestion = suggestion

    def __repr__(self) -> str:
        return f"[L:{self.line}, C:{self.column}] {self.category.value}: '{self.lexeme}' - {self.message}"

    def to_diagnostic_string(self) -> str:
        """Formato claro para diagnósticos."""
        return (
            f"  --> Línea {self.line}, Columna {self.column} | [{self.category.value}]\n"
            f"      Lexema defectuoso: '{self.lexeme}'\n"
            f"      Descripción: {self.message}\n"
            f"      Sugerencia de corrección: {self.suggestion}"
        )


class ErrorHandler:
    """
    Manejador centralizado de errores léxicos. Almacena, clasifica
    y genera reportes y tablas comprensibles a simple vista.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[LexicalError] = []

    def reset(self):
        """Limpia los errores registrados."""
        self.errors.clear()

    def report(
        self,
        line: int,
        column: int,
        category: LexicalErrorCategory,
        lexeme: str,
        message: str,
        suggestion: str
    ) -> LexicalError:
        """Registra un nuevo error léxico en el manejador."""
        err = LexicalError(line, column, category, lexeme, message, suggestion)
        self.errors.append(err)
        return err

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def total_errors(self) -> int:
        return len(self.errors)

    def count_by_category(self) -> Dict[str, int]:
        """Devuelve un desglose estadístico de errores por categoría."""
        counts = {cat.value: 0 for cat in LexicalErrorCategory}
        for err in self.errors:
            counts[err.category.value] += 1
        return counts

    def to_formatted_table(self) -> str:
        """Genera una tabla ASCII estructurada de errores para la salida en consola."""
        if not self.errors:
            return "✅ Ningún error léxico detectado. El código fuente cumple con el alfabeto y reglas de C."

        sep = "+" + "-" * 6 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 30 + "+" + "-" * 20 + "+" + "-" * 42 + "+"
        header = f"| {'#':<4} | {'LÍNEA':<5} | {'COL':<5} | {'CATEGORÍA DE ERROR':<28} | {'LEXEMA':<18} | {'DESCRIPCIÓN Y SUGERENCIA':<40} |"
        rows = [sep, header, sep]

        for idx, err in enumerate(self.errors, 1):
            short_lex = err.lexeme if len(err.lexeme) <= 16 else err.lexeme[:13] + "..."
            desc_sug = f"{err.message} Sugerencia: {err.suggestion}"
            short_desc = desc_sug if len(desc_sug) <= 38 else desc_sug[:35] + "..."
            rows.append(
                f"| {idx:<4} | {err.line:<5} | {err.column:<5} | {err.category.value:<28} | {short_lex:<18} | {short_desc:<40} |"
            )
        rows.append(sep)

        # Resumen estadístico
        breakdown = self.count_by_category()
        rows.append("\n  DESGLOSE ESTADÍSTICO DE ERRORES:")
        for cat, count in breakdown.items():
            if count > 0:
                rows.append(f"   • {cat:<28}: {count} ocurrencia(s)")

        return "\n".join(rows)
