"""
================================================================================
ACTIVIDAD 2: MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
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
from typing import List, Dict

class LexicalErrorCategory(Enum):
    CARACTER_NO_RECONOCIDO = "Carácter No Reconocido"
    IDENTIFICADOR_MAL_FORMADO = "Identificador Mal Formado"
    NUMERO_INCORRECTO = "Literal Numérico Incorrecto"
    CADENA_MAL_FORMADA = "Cadena de Texto Mal Formada"
    SECUENCIA_ESCAPE_INVALIDA = "Secuencia de Escape Inválida"

class LexicalError:
    def __init__(
        self, 
        category: LexicalErrorCategory, 
        lexeme: str, 
        line: int, 
        column: int, 
        description: str, 
        suggestion: str = "",
        snippet: str = ""
    ):
        self.category = category
        self.lexeme = lexeme
        self.line = line
        self.column = column
        self.description = description
        self.suggestion = suggestion
        self.snippet = snippet

    def __repr__(self):
        return f"LexicalError({self.category.value}, Lexeme:'{self.lexeme}', L:{self.line}, C:{self.column})"

    def format_detailed(self) -> str:
        res = [
            f" [!] ERROR LÉXICO: {self.category.value}",
            f"     Ubicación : Línea {self.line}, Columna {self.column}",
            f"     Lexema    : '{self.lexeme}'",
            f"     Detalle   : {self.description}",
        ]
        if self.suggestion:
            res.append(f"     Sugerencia: {self.suggestion}")
        if self.snippet:
            res.append(f"     Contexto  : {self.snippet.strip()}")
        return "\n".join(res)

class ErrorHandler:
    """
    Gestor centralizado de errores léxicos durante la fase de análisis.
    """
    def __init__(self):
        self.errors: List[LexicalError] = []

    def add_error(
        self, 
        category: LexicalErrorCategory, 
        lexeme: str, 
        line: int, 
        column: int, 
        description: str, 
        suggestion: str = "",
        snippet: str = ""
    ) -> LexicalError:
        err = LexicalError(category, lexeme, line, column, description, suggestion, snippet)
        self.errors.append(err)
        return err

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def clear(self):
        self.errors.clear()

    def get_summary(self) -> Dict[str, int]:
        summary = {cat.value: 0 for cat in LexicalErrorCategory}
        for err in self.errors:
            summary[err.category.value] += 1
        return summary

    def print_error_report(self):
        if not self.errors:
            print(" ✔ NO SE ENCONTRARON ERRORES LÉXICOS. El código cumple con las reglas del lenguaje C.\n")
            return

        print("\n" + "!" * 80)
        print(f" REPORTES DE ERRORES LÉXICOS DETECTADOS ({len(self.errors)} ERRORES)")
        print("!" * 80)
        
        divider = "+" + "-" * 6 + "+" + "-" * 6 + "+" + "-" * 28 + "+" + "-" * 18 + "+" + "-" * 35 + "+"
        header  = f"| {'#':<4} | {'LÍNEA':<4} | {'CATEGORÍA DE ERROR':<26} | {'LEXEMA':<16} | {'DESCRIPCIÓN Y SUGERENCIA':<33} |"
        
        print(divider)
        print(header)
        print(divider)

        for idx, err in enumerate(self.errors, 1):
            lex_repr = repr(err.lexeme)[1:-1] if '\n' in err.lexeme or '\t' in err.lexeme else err.lexeme
            if len(lex_repr) > 15:
                lex_repr = lex_repr[:12] + "..."
                
            desc_repr = f"{err.description}"
            if len(desc_repr) > 32:
                desc_repr = desc_repr[:29] + "..."

            print(f"| {idx:<4} | {err.line:<5} | {err.category.value:<26} | {lex_repr:<16} | {desc_repr:<33} |")

        print(divider)
        print("\n DESGLOSE ESTADÍSTICO DE ERRORES:")
        for cat, count in self.get_summary().items():
            if count > 0:
                print(f"   • {cat:<30}: {count} ocurrencia(s)")
        print("!" * 80 + "\n")
