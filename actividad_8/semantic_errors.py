"""
================================================================================
ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - VERIFICACIÓN DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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
from typing import List, Dict, Optional


class SemanticErrorCategory(Enum):
    """
    Categorías de errores semánticos para validación de expresiones
    aritméticas, lógicas y conversiones de tipo según la rúbrica oficial.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    OPERACION_NO_NUMERICA = "Operación Aritmética con Tipo No Numérico"
    OPERANDO_LOGICO_NO_BOOLEANO = "Operador Lógico con Operando No Booleano"
    COMPARACION_INCOMPATIBLE = "Comparación entre Tipos Incompatibles"
    DIVISION_POR_CERO = "División por Cero en Tiempo de Compilación"
    TIPO_INCOMPATIBLE_ASIGNACION = "Tipo Incompatible en Asignación"
    CONVERSION_INVALIDA = "Conversión de Tipo Inválida"
    IDENTIFICADOR_NO_DECLARADO = "Identificador No Declarado"


class SemanticErrorItem:
    """
    Representa un error semántico individual detectado durante la validación de expresiones.

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
        category: SemanticErrorCategory,
        message: str,
        suggestion: str,
        operator: str = ""
    ):
        self.line = line
        self.column = column
        self.category = category
        self.message = message
        self.suggestion = suggestion
        self.operator = operator

    def to_diagnostic_string(self) -> str:
        op_info = f" | Operador: '{self.operator}'" if self.operator else ""
        return (
            f"  --> Línea {self.line}, Columna {self.column} | [{self.category.value}]{op_info}\n"
            f"      Descripción: {self.message}\n"
            f"      Sugerencia de corrección: {self.suggestion}"
        )

    def __repr__(self) -> str:
        return f"[L:{self.line}, C:{self.column}] {self.category.value}: {self.message}"


class SemanticErrorHandler:
    """
    Manejador centralizado de errores semánticos para expresiones.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[SemanticErrorItem] = []

    def reset(self):
        self.errors.clear()

    def report(
        self,
        line: int,
        column: int,
        category: SemanticErrorCategory,
        message: str,
        suggestion: str,
        operator: str = ""
    ) -> SemanticErrorItem:
        err = SemanticErrorItem(line, column, category, message, suggestion, operator)
        self.errors.append(err)
        return err

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def total_errors(self) -> int:
        return len(self.errors)

    def count_by_category(self) -> Dict[str, int]:
        counts = {cat.value: 0 for cat in SemanticErrorCategory}
        for err in self.errors:
            counts[err.category.value] += 1
        return counts

    def to_formatted_table(self) -> str:
        if not self.errors:
            return "✅ Ningún error semántico detectado en expresiones. Todos los tipos y operadores son válidos y consistentes."

        sep = "+" + "-" * 5 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 10 + "+" + "-" * 42 + "+" + "-" * 42 + "+"
        header = f"| {'#':<3} | {'LÍNEA':<5} | {'COL':<4} | {'OPERADOR':<8} | {'CATEGORÍA DE ERROR':<40} | {'DESCRIPCIÓN Y SUGERENCIA':<40} |"
        rows = [sep, header, sep]

        for idx, err in enumerate(self.errors, 1):
            short_msg = f"{err.message} Sugerencia: {err.suggestion}"
            if len(short_msg) > 38:
                short_msg = short_msg[:35] + "..."
            op_disp = err.operator if err.operator else "(N/A)"
            rows.append(
                f"| {idx:<3} | {err.line:<5} | {err.column:<4} | {op_disp:<8} | {err.category.value:<40} | {short_msg:<40} |"
            )
        rows.append(sep)

        breakdown = self.count_by_category()
        rows.append("\n  DESGLOSE ESTADÍSTICO DE ERRORES EN EXPRESIONES:")
        for cat, cnt in breakdown.items():
            if cnt > 0:
                rows.append(f"   • {cat:<42}: {cnt} ocurrencia(s)")

        return "\n".join(rows)
