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

from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    """
    Tipos de tokens para el analizador sintáctico de estructuras de control
    (if, else, while, for), expresiones, declaraciones y asignaciones en C.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Palabras clave estructurales
    KEYWORD_IF = auto()         # 'if'
    KEYWORD_ELSE = auto()       # 'else'
    KEYWORD_WHILE = auto()      # 'while'
    KEYWORD_FOR = auto()        # 'for'
    KEYWORD_RETURN = auto()     # 'return'

    # Palabras clave de tipos de datos en C
    KEYWORD_INT = auto()        # 'int'
    KEYWORD_FLOAT = auto()      # 'float'
    KEYWORD_DOUBLE = auto()     # 'double'
    KEYWORD_CHAR = auto()       # 'char'
    KEYWORD_VOID = auto()       # 'void'

    # Identificadores y Literales
    IDENTIFICADOR = auto()      # [a-zA-Z_][a-zA-Z0-9_]*
    NUMERO_ENTERO = auto()      # 123
    NUMERO_FLOTANTE = auto()    # 123.45
    LITERAL_CADENA = auto()     # "hola"
    LITERAL_CARACTER = auto()   # 'c'

    # Delimitadores
    PARENTESIS_IZQ = auto()     # '('
    PARENTESIS_DER = auto()     # ')'
    LLAVE_IZQ = auto()          # '{'
    LLAVE_DER = auto()          # '}'
    CORCHETE_IZQ = auto()       # '['
    CORCHETE_DER = auto()       # ']'
    PUNTO_Y_COMA = auto()       # ';'
    COMA = auto()               # ','

    # Operadores de Asignación
    ASIGNACION = auto()         # '='
    ASIGNACION_SUMA = auto()    # '+='
    ASIGNACION_RESTA = auto()   # '-='

    # Operadores Aritméticos
    SUMA = auto()               # '+'
    RESTA = auto()              # '-'
    MULTIPLICACION = auto()     # '*'
    DIVISION = auto()           # '/'
    MODULO = auto()             # '%'
    INCREMENTO = auto()         # '++'
    DECREMENTO = auto()         # '--'

    # Operadores Relacionales
    IGUAL_QUE = auto()          # '=='
    DISTINTO_QUE = auto()       # '!='
    MENOR_QUE = auto()          # '<'
    MAYOR_QUE = auto()          # '>'
    MENOR_IGUAL_QUE = auto()    # '<='
    MAYOR_IGUAL_QUE = auto()    # '>='

    # Operadores Lógicos
    AND_LOGICO = auto()         # '&&'
    OR_LOGICO = auto()          # '||'
    NOT_LOGICO = auto()         # '!'

    # Otros
    DIRECTIVA_PREPROCESADOR = auto()  # #include <stdio.h>
    COMENTARIO_LINEA = auto()         # // ...
    COMENTARIO_BLOQUE = auto()        # /* ... */
    EOF = auto()                      # Fin de Entrada


class Token:
    """
    Representa un componente léxico individual con su valor textual y ubicación.

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

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column})"
