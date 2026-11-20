"""
================================================================================
ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL (LENGUAJE C EN PYTHON)
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


class SyntaxErrorCategory(Enum):
    """
    Categorías de errores sintácticos específicos para estructuras de control
    (if, while, for) conforme a los requerimientos de la rúbrica oficial.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    PARENTESIS_DESBALANCEADOS = "Paréntesis Faltantes o Desbalanceados"
    CONDICION_INVALIDA = "Condición Inválida en Estructura de Control"
    BLOQUE_SIN_LLAVES = "Bloque de Sentencias Faltante o Sin Llaves"
    LLAVE_FALTANTE = "Llave de Cierre Faltante en Bloque"
    COMPONENTE_FOR_INVALIDO = "Componente Inválido en Estructura 'for'"
    PUNTO_Y_COMA_FALTANTE = "Punto y Coma Faltante en Sentencia"
    ERROR_SINTACTICO_GENERAL = "Error Sintáctico General"


class SyntaxErrorItem:
    """
    Representa un error sintáctico detectado durante el análisis descendente recursivo.

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
        category: SyntaxErrorCategory,
        message: str,
        suggestion: str,
        structure_name: str = "general"
    ):
        self.line = line
        self.column = column
        self.category = category
        self.message = message
        self.suggestion = suggestion
        self.structure_name = structure_name

    def __repr__(self) -> str:
        return f"[L:{self.line}, C:{self.column}] {self.category.value} ({self.structure_name}): {self.message}"

    def to_diagnostic_string(self) -> str:
        return (
            f"  --> Línea {self.line}, Columna {self.column} | [{self.category.value}]\n"
            f"      Estructura: '{self.structure_name}'\n"
            f"      Descripción: {self.message}\n"
            f"      Sugerencia de corrección: {self.suggestion}"
        )


class SyntaxErrorHandler:
    """
    Manejador centralizado de errores sintácticos para estructuras de control.
    Almacena incidencias y produce tablas formateadas comprensibles a simple vista.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[SyntaxErrorItem] = []

    def reset(self):
        self.errors.clear()

    def report(
        self,
        line: int,
        column: int,
        category: SyntaxErrorCategory,
        message: str,
        suggestion: str,
        structure_name: str = "general"
    ) -> SyntaxErrorItem:
        err = SyntaxErrorItem(line, column, category, message, suggestion, structure_name)
        self.errors.append(err)
        return err

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def total_errors(self) -> int:
        return len(self.errors)

    def count_by_category(self) -> Dict[str, int]:
        counts = {cat.value: 0 for cat in SyntaxErrorCategory}
        for err in self.errors:
            counts[err.category.value] += 1
        return counts

    def to_formatted_table(self) -> str:
        if not self.errors:
            return "✅ Ningún error sintáctico detectado. Estructuras de control construidas correctamente."

        sep = "+" + "-" * 5 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 15 + "+" + "-" * 38 + "+" + "-" * 42 + "+"
        header = f"| {'#':<3} | {'LÍNEA':<5} | {'COL':<4} | {'ESTRUCTURA':<13} | {'CATEGORÍA DE ERROR':<36} | {'DESCRIPCIÓN Y SUGERENCIA':<40} |"
        rows = [sep, header, sep]

        for idx, err in enumerate(self.errors, 1):
            short_msg = f"{err.message} Sugerencia: {err.suggestion}"
            if len(short_msg) > 38:
                short_msg = short_msg[:35] + "..."
            rows.append(
                f"| {idx:<3} | {err.line:<5} | {err.column:<4} | {err.structure_name:<13} | {err.category.value:<36} | {short_msg:<40} |"
            )
        rows.append(sep)

        breakdown = self.count_by_category()
        rows.append("\n  DESGLOSE ESTADÍSTICO DE ERRORES SINTÁCTICOS:")
        for cat, cnt in breakdown.items():
            if cnt > 0:
                rows.append(f"   • {cat:<36}: {cnt} ocurrencia(s)")

        return "\n".join(rows)
