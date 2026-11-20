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

from enum import Enum
from typing import Any, Optional


class TokenType(Enum):
    """
    Tipos de tokens para el compilador completo de C.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Palabras clave de control de flujo
    KEYWORD_IF = "KEYWORD_IF"
    KEYWORD_ELSE = "KEYWORD_ELSE"
    KEYWORD_SWITCH = "KEYWORD_SWITCH"
    KEYWORD_CASE = "KEYWORD_CASE"
    KEYWORD_DEFAULT = "KEYWORD_DEFAULT"
    KEYWORD_BREAK = "KEYWORD_BREAK"
    KEYWORD_WHILE = "KEYWORD_WHILE"
    KEYWORD_FOR = "KEYWORD_FOR"
    KEYWORD_DO = "KEYWORD_DO"

    # Palabras clave estructurales y OOP
    KEYWORD_CLASS = "KEYWORD_CLASS"
    KEYWORD_NEW = "KEYWORD_NEW"
    KEYWORD_RETURN = "KEYWORD_RETURN"

    # Tipos primitivos
    KEYWORD_INT = "KEYWORD_INT"
    KEYWORD_FLOAT = "KEYWORD_FLOAT"
    KEYWORD_STRING = "KEYWORD_STRING"
    KEYWORD_VOID = "KEYWORD_VOID"
    KEYWORD_BOOL = "KEYWORD_BOOL"

    # E/S y depuración
    KEYWORD_PRINT = "KEYWORD_PRINT"

    # Identificadores y literales
    IDENTIFICADOR = "IDENTIFICADOR"
    NUMERO_ENTERO = "NUMERO_ENTERO"
    NUMERO_FLOTANTE = "NUMERO_FLOTANTE"
    CADENA_TEXTO = "CADENA_TEXTO"
    BOOLEANO = "BOOLEANO"

    # Operadores aritméticos y de asignación
    OP_ASIGNACION = "OP_ASIGNACION"        # '='
    OP_SUMA = "OP_SUMA"                    # '+'
    OP_RESTA = "OP_RESTA"                  # '-'
    OP_MULTIPLICACION = "OP_MULT"          # '*'
    OP_DIVISION = "OP_DIV"                 # '/'
    OP_MODULO = "OP_MOD"                   # '%'
    OP_INCREMENTO = "OP_INCREMENTO"        # '++'
    OP_DECREMENTO = "OP_DECREMENTO"        # '--'

    # Operadores relacionales y lógicos
    OP_IGUAL = "OP_IGUAL"                  # '=='
    OP_DIFERENTE = "OP_DIFERENTE"          # '!='
    OP_MENOR = "OP_MENOR"                  # '<'
    OP_MENOR_IGUAL = "OP_MENOR_IGUAL"      # '<='
    OP_MAYOR = "OP_MAYOR"                  # '>'
    OP_MAYOR_IGUAL = "OP_MAYOR_IGUAL"      # '>='
    OP_AND = "OP_AND"                      # '&&'
    OP_OR = "OP_OR"                        # '||'
    OP_NOT = "OP_NOT"                      # '!'

    # Delimitadores
    PARENTESIS_IZQ = "PARENTESIS_IZQ"      # '('
    PARENTESIS_DER = "PARENTESIS_DER"      # ')'
    LLAVE_IZQ = "LLAVE_IZQ"                # '{'
    LLAVE_DER = "LLAVE_DER"                # '}'
    CORCHETE_IZQ = "CORCHETE_IZQ"          # '['
    CORCHETE_DER = "CORCHETE_DER"          # ']'
    PUNTO_Y_COMA = "PUNTO_Y_COMA"          # ';'
    COMA = "COMA"                          # ','
    DOS_PUNTOS = "DOS_PUNTOS"              # ':'
    PUNTO = "PUNTO"                        # '.'

    # Control
    EOF = "EOF"
    ERROR = "ERROR"


class Token:
    """
    Representa un token léxico con metadatos de ubicación y valor tipado.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, type_: TokenType, value: str, line: int, column: int, literal: Optional[Any] = None):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        self.literal = literal

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column})"
