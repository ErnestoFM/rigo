"""
================================================================================
ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
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
    Categorías de errores semánticos conforme a la rúbrica oficial de la Actividad 7.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    IDENTIFICADOR_NO_DECLARADO = "Identificador No Declarado"
    TIPO_INCOMPATIBLE_ASIGNACION = "Tipo Incompatible en Asignación"
    VARIABLE_YA_DECLARADA = "Redeclaración de Identificador en Mismo Ámbito"
    TIPO_INCOMPATIBLE_EXPRESION = "Tipo Incompatible en Operación / Expresión"
    AMBITO_INVALIDO = "Acceso a Identificador Fuera de su Ámbito"
    ERROR_SEMANTICO_GENERAL = "Error Semántico General"


class SemanticErrorItem:
    """
    Representa una inconsistencia semántica detectada durante el recorrido del AST.

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
        identifier: str = "",
        scope_name: str = "global"
    ):
        self.line = line
        self.column = column
        self.category = category
        self.message = message
        self.suggestion = suggestion
        self.identifier = identifier
        self.scope_name = scope_name

    def to_diagnostic_string(self) -> str:
        ident_info = f" | Identificador: '{self.identifier}'" if self.identifier else ""
        return (
            f"  --> Línea {self.line}, Columna {self.column} | [{self.category.value}]{ident_info}\n"
            f"      Ámbito: '{self.scope_name}'\n"
            f"      Descripción: {self.message}\n"
            f"      Sugerencia de corrección: {self.suggestion}"
        )

    def __repr__(self) -> str:
        return f"[L:{self.line}, C:{self.column}] {self.category.value}: {self.message}"


class SemanticErrorHandler:
    """
    Manejador centralizado de errores semánticos para la verificación de tipos
    y control de ámbitos en la tabla de símbolos.

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
        identifier: str = "",
        scope_name: str = "global"
    ) -> SemanticErrorItem:
        err = SemanticErrorItem(line, column, category, message, suggestion, identifier, scope_name)
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
            return "✅ Ningún error semántico detectado. Tipos y ámbitos plenamente válidos."

        sep = "+" + "-" * 5 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 15 + "+" + "-" * 38 + "+" + "-" * 42 + "+"
        header = f"| {'#':<3} | {'LÍNEA':<5} | {'COL':<4} | {'ÁMBITO':<13} | {'CATEGORÍA DE ERROR':<36} | {'DESCRIPCIÓN Y SUGERENCIA':<40} |"
        rows = [sep, header, sep]

        for idx, err in enumerate(self.errors, 1):
            short_msg = f"{err.message} Sugerencia: {err.suggestion}"
            if len(short_msg) > 38:
                short_msg = short_msg[:35] + "..."
            rows.append(
                f"| {idx:<3} | {err.line:<5} | {err.column:<4} | {err.scope_name:<13} | {err.category.value:<36} | {short_msg:<40} |"
            )
        rows.append(sep)

        breakdown = self.count_by_category()
        rows.append("\n  DESGLOSE ESTADÍSTICO DE ERRORES SEMÁNTICOS:")
        for cat, cnt in breakdown.items():
            if cnt > 0:
                rows.append(f"   • {cat:<40}: {cnt} ocurrencia(s)")

        return "\n".join(rows)
