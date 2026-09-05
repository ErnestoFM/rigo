"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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

class TokenType(Enum):
    """
    Tipos de tokens léxicos y sintácticos para expresiones aritméticas y lógicas.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Identificadores y Literales Numéricos
    IDENTIFICADOR = "IDENTIFICADOR"
    NUMERO_ENTERO = "NUMERO_ENTERO"
    NUMERO_FLOTANTE = "NUMERO_FLOTANTE"

    # Operadores Aritméticos
    OP_SUMA = "OP_SUMA"                 # +
    OP_RESTA = "OP_RESTA"               # -
    OP_MULTIPLICACION = "OP_MULT"       # *
    OP_DIVISION = "OP_DIV"             # /
    OP_MODULO = "OP_MOD"               # %
    OP_POTENCIA = "OP_POTENCIA"         # ^ o **

    # Operadores Relacionales (Comparación)
    OP_IGUAL = "OP_IGUAL"               # ==
    OP_DIFERENTE = "OP_DIFERENTE"       # !=
    OP_MENOR = "OP_MENOR"               # <
    OP_MENOR_IGUAL = "OP_MENOR_IGUAL"   # <=
    OP_MAYOR = "OP_MAYOR"               # >
    OP_MAYOR_IGUAL = "OP_MAYOR_IGUAL"   # >=

    # Operadores Lógicos
    OP_AND = "OP_AND"                   # &&, and
    OP_OR = "OP_OR"                     # ||, or
    OP_NOT = "OP_NOT"                   # !, not

    # Delimitadores de Agrupación
    PARENTESIS_IZQ = "PARENTESIS_IZQ"   # (
    PARENTESIS_DER = "PARENTESIS_DER"   # )

    # Control de Flujo y Especiales
    EOF = "FIN_DE_ENTRADA"
    DESCONOCIDO = "TOKEN_DESCONOCIDO"


class Token:
    """
    Representa un token léxico con su tipo, lexema y posición (línea y columna).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def is_arithmetic_op(self) -> bool:
        """Indica si el token es un operador aritmético."""
        return self.type in (
            TokenType.OP_SUMA,
            TokenType.OP_RESTA,
            TokenType.OP_MULTIPLICACION,
            TokenType.OP_DIVISION,
            TokenType.OP_MODULO,
            TokenType.OP_POTENCIA
        )

    def is_relational_op(self) -> bool:
        """Indica si el token es un operador relacional de comparación."""
        return self.type in (
            TokenType.OP_IGUAL,
            TokenType.OP_DIFERENTE,
            TokenType.OP_MENOR,
            TokenType.OP_MENOR_IGUAL,
            TokenType.OP_MAYOR,
            TokenType.OP_MAYOR_IGUAL
        )

    def is_logical_op(self) -> bool:
        """Indica si el token es un operador lógico binario (&&, ||)."""
        return self.type in (TokenType.OP_AND, TokenType.OP_OR)

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column})"

    def __str__(self) -> str:
        return f"[{self.type.name} '{self.value}' (L:{self.line}, C:{self.column})]"
