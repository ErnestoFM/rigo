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

from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    """
    Definición de tipos de tokens para el analizador léxico de C,
    incluyendo categorías estándar y tokens de errores léxicos específicos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Tokens Válidos de C
    DIRECTIVA_PREPROCESADOR = auto()  # #include, #define, #ifdef, etc.
    PALABRA_CLAVE = auto()            # int, float, if, else, while, return, etc.
    IDENTIFICADOR = auto()            # [a-zA-Z_][a-zA-Z0-9_]*
    LITERAL_ENTERO = auto()           # 123, 0x1A, 077
    LITERAL_FLOTANTE = auto()         # 3.14, 1.5e-3, 9.5f
    LITERAL_CADENA = auto()           # "hola mundo\n"
    LITERAL_CARACTER = auto()         # 'c', '\n'
    OPERADOR_ARITMETICO = auto()      # +, -, *, /, %, ++, --
    OPERADOR_RELACIONAL = auto()      # ==, !=, <, >, <=, >=
    OPERADOR_LOGICO = auto()          # &&, ||, !
    OPERADOR_ASIGNACION = auto()      # =, +=, -=, *=, /=, %=
    OPERADOR_BIT = auto()             # &, |, ^, ~, <<, >>, ->
    DELIMITADOR = auto()              # (, ), {, }, [, ], ;, ,, .
    COMENTARIO_LINEA = auto()         # // comentario
    COMENTARIO_BLOQUE = auto()        # /* bloque */
    FIN_DE_ENTRADA = auto()           # EOF

    # Tokens Específicos de Error Léxico (Rúbrica Actividad 2)
    ERROR_CARACTER_NO_RECONOCIDO = auto()       # @, $, #, ~, ¿, ñ
    ERROR_IDENTIFICADOR_MAL_FORMADO = auto()    # 123contador, 8promedio
    ERROR_NUMERO_INCORRECTO = auto()            # 3.14.15, 0x12G4, 1.5e+
    ERROR_CADENA_MAL_FORMADA = auto()           # "cadena sin comilla de cierre


class Token:
    """
    Representa un componente léxico individual con su valor, posición
    y metadata contextual para diagnósticos precisos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, type_: TokenType, value: str, line: int, column: int, is_error: bool = False, error_msg: Optional[str] = None):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        self.is_error = is_error
        self.error_msg = error_msg

    def __repr__(self) -> str:
        err_flag = " [ERROR]" if self.is_error else ""
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column}{err_flag})"

    @property
    def category_name(self) -> str:
        """Nombre legible de la categoría del token para visualización en tablas y reportes."""
        names = {
            TokenType.DIRECTIVA_PREPROCESADOR: "Directiva de Preprocesador",
            TokenType.PALABRA_CLAVE: "Palabra Clave (C)",
            TokenType.IDENTIFICADOR: "Identificador",
            TokenType.LITERAL_ENTERO: "Literal Entero",
            TokenType.LITERAL_FLOTANTE: "Literal Flotante",
            TokenType.LITERAL_CADENA: "Literal Cadena de Texto",
            TokenType.LITERAL_CARACTER: "Literal Carácter",
            TokenType.OPERADOR_ARITMETICO: "Operador Aritmético",
            TokenType.OPERADOR_RELACIONAL: "Operador Relacional",
            TokenType.OPERADOR_LOGICO: "Operador Lógico",
            TokenType.OPERADOR_ASIGNACION: "Operador de Asignación",
            TokenType.OPERADOR_BIT: "Operador a Nivel de Bits",
            TokenType.DELIMITADOR: "Delimitador / Símbolo",
            TokenType.COMENTARIO_LINEA: "Comentario de Línea",
            TokenType.COMENTARIO_BLOQUE: "Comentario de Bloque",
            TokenType.FIN_DE_ENTRADA: "Fin de Archivo (EOF)",
            TokenType.ERROR_CARACTER_NO_RECONOCIDO: "❌ Error: Carácter No Reconocido",
            TokenType.ERROR_IDENTIFICADOR_MAL_FORMADO: "❌ Error: Identificador Mal Formado",
            TokenType.ERROR_NUMERO_INCORRECTO: "❌ Error: Literal Numérico Incorrecto",
            TokenType.ERROR_CADENA_MAL_FORMADA: "❌ Error: Cadena Mal Formada"
        }
        return names.get(self.type, self.type.name)
