"""
================================================================================
ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL,
             MÉTODOS Y CLASES
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
from typing import Optional, Any


class TokenType(Enum):
    """
    Tipos de tokens léxicos y sintácticos para el análisis semántico de estructuras
    de control, métodos, clases y tipos de datos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Palabras clave estructurales y tipos
    KEYWORD_CLASS = "KEYWORD_CLASS"          # 'class'
    KEYWORD_INT = "KEYWORD_INT"              # 'int'
    KEYWORD_FLOAT = "KEYWORD_FLOAT"          # 'float'
    KEYWORD_VOID = "KEYWORD_VOID"            # 'void'
    KEYWORD_CHAR = "KEYWORD_CHAR"            # 'char'
    KEYWORD_BOOLEAN = "KEYWORD_BOOLEAN"      # 'boolean'
    KEYWORD_STRING = "KEYWORD_STRING"        # 'string' / 'String'
    KEYWORD_RETURN = "KEYWORD_RETURN"        # 'return'
    KEYWORD_IF = "KEYWORD_IF"                # 'if'
    KEYWORD_ELSE = "KEYWORD_ELSE"            # 'else'
    KEYWORD_WHILE = "KEYWORD_WHILE"          # 'while'
    KEYWORD_FOR = "KEYWORD_FOR"              # 'for'
    KEYWORD_FUNCTION = "KEYWORD_FUNCTION"    # 'function'
    KEYWORD_LET = "KEYWORD_LET"              # 'let'
    KEYWORD_VAR = "KEYWORD_VAR"              # 'var'
    KEYWORD_TRY = "KEYWORD_TRY"              # 'try'
    KEYWORD_CATCH = "KEYWORD_CATCH"          # 'catch'
    KEYWORD_BREAK = "KEYWORD_BREAK"          # 'break'
    KEYWORD_CONTINUE = "KEYWORD_CONTINUE"    # 'continue'

    # Identificadores y Literales
    IDENTIFICADOR = "IDENTIFICADOR"          # [a-zA-Z_][a-zA-Z0-9_]*
    NUMERO_ENTERO = "NUMERO_ENTERO"          # 123
    NUMERO_FLOTANTE = "NUMERO_FLOTANTE"      # 123.45
    LITERAL_CADENA = "LITERAL_CADENA"        # "hola mundo"
    LITERAL_CARACTER = "LITERAL_CARACTER"    # 'c'
    LITERAL_BOOLEANO = "LITERAL_BOOLEANO"    # true | false

    # Delimitadores
    LLAVE_IZQ = "LLAVE_IZQ"                  # '{'
    LLAVE_DER = "LLAVE_DER"                  # '}'
    PARENTESIS_IZQ = "PARENTESIS_IZQ"        # '('
    PARENTESIS_DER = "PARENTESIS_DER"        # ')'
    CORCHETE_IZQ = "CORCHETE_IZQ"            # '['
    CORCHETE_DER = "CORCHETE_DER"            # ']'
    PUNTO_Y_COMA = "PUNTO_Y_COMA"            # ';'
    COMA = "COMA"                            # ','
    PUNTO = "PUNTO"                          # '.'
    DOS_PUNTOS = "DOS_PUNTOS"                # ':'

    # Operadores de Asignación y Expresión
    OP_ASIGNACION = "OP_ASIGNACION"          # '='
    OP_SUMA = "OP_SUMA"                      # '+'
    OP_RESTA = "OP_RESTA"                    # '-'
    OP_MULTIPLICACION = "OP_MULT"            # '*'
    OP_DIVISION = "OP_DIV"                   # '/'
    OP_MODULO = "OP_MOD"                     # '%'
    OP_INCREMENTO = "OP_INCREMENTO"          # '++'
    OP_DECREMENTO = "OP_DECREMENTO"          # '--'

    # Operadores Relacionales
    OP_IGUAL = "OP_IGUAL"                    # '==' o '==='
    OP_DIFERENTE = "OP_DIFERENTE"            # '!=' o '!=='
    OP_MENOR = "OP_MENOR"                    # '<'
    OP_MENOR_IGUAL = "OP_MENOR_IGUAL"        # '<='
    OP_MAYOR = "OP_MAYOR"                    # '>'
    OP_MAYOR_IGUAL = "OP_MAYOR_IGUAL"        # '>='

    # Operadores Lógicos
    OP_AND = "OP_AND"                        # '&&'
    OP_OR = "OP_OR"                          # '||'
    OP_NOT = "OP_NOT"                        # '!'

    # Tokens de Control
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
    def __init__(self, type_: TokenType, value: str, line: int, column: int, literal_value: Any = None):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        self.literal_value = literal_value

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column})"

    def __str__(self) -> str:
        return f"{self.type.name}('{self.value}', L:{self.line}, C:{self.column})"
