"""
================================================================================
ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES
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
from typing import Optional


class TokenType(Enum):
    """
    Tipos de tokens léxicos y sintácticos para la definición de clases y métodos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Palabras clave estructurales y tipos
    KEYWORD_CLASS = "KEYWORD_CLASS"        # 'class'
    KEYWORD_INT = "KEYWORD_INT"            # 'int'
    KEYWORD_FLOAT = "KEYWORD_FLOAT"        # 'float'
    KEYWORD_VOID = "KEYWORD_VOID"          # 'void'
    KEYWORD_CHAR = "KEYWORD_CHAR"          # 'char'
    KEYWORD_BOOLEAN = "KEYWORD_BOOLEAN"    # 'boolean'
    KEYWORD_RETURN = "KEYWORD_RETURN"      # 'return'
    KEYWORD_IF = "KEYWORD_IF"              # 'if'
    KEYWORD_ELSE = "KEYWORD_ELSE"          # 'else'
    KEYWORD_WHILE = "KEYWORD_WHILE"        # 'while'
    KEYWORD_FOR = "KEYWORD_FOR"            # 'for'

    # Identificadores y Literales
    IDENTIFICADOR = "IDENTIFICADOR"        # [a-zA-Z_][a-zA-Z0-9_]*
    NUMERO_ENTERO = "NUMERO_ENTERO"        # 123
    NUMERO_FLOTANTE = "NUMERO_FLOTANTE"    # 123.45
    LITERAL_CADENA = "LITERAL_CADENA"      # "hola"
    LITERAL_CARACTER = "LITERAL_CARACTER"  # 'c'
    LITERAL_BOOLEANO = "LITERAL_BOOLEANO"  # true | false

    # Delimitadores
    LLAVE_IZQ = "LLAVE_IZQ"                # '{'
    LLAVE_DER = "LLAVE_DER"                # '}'
    PARENTESIS_IZQ = "PARENTESIS_IZQ"      # '('
    PARENTESIS_DER = "PARENTESIS_DER"      # ')'
    CORCHETE_IZQ = "CORCHETE_IZQ"          # '['
    CORCHETE_DER = "CORCHETE_DER"          # ']'
    PUNTO_Y_COMA = "PUNTO_Y_COMA"          # ';'
    COMA = "COMA"                          # ','
    PUNTO = "PUNTO"                        # '.'

    # Operadores de Asignación y Expresión
    OP_ASIGNACION = "OP_ASIGNACION"        # '='
    OP_SUMA = "OP_SUMA"                    # '+'
    OP_RESTA = "OP_RESTA"                  # '-'
    OP_MULTIPLICACION = "OP_MULT"          # '*'
    OP_DIVISION = "OP_DIV"                 # '/'
    OP_MODULO = "OP_MOD"                   # '%'

    # Operadores Relacionales
    OP_IGUAL = "OP_IGUAL"                  # '=='
    OP_DIFERENTE = "OP_DIFERENTE"          # '!='
    OP_MENOR = "OP_MENOR"                  # '<'
    OP_MENOR_IGUAL = "OP_MENOR_IGUAL"      # '<='
    OP_MAYOR = "OP_MAYOR"                  # '>'
    OP_MAYOR_IGUAL = "OP_MAYOR_IGUAL"      # '>='

    # Operadores Lógicos
    OP_AND = "OP_AND"                      # '&&'
    OP_OR = "OP_OR"                        # '||'
    OP_NOT = "OP_NOT"                      # '!'

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
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def is_type_specifier(self) -> bool:
        """
        Determina si el token corresponde a un tipo permitido por la gramática:
        tipo -> 'int' | 'float' | 'void' | 'char' | 'boolean' | identificador
        """
        return self.type in (
            TokenType.KEYWORD_INT,
            TokenType.KEYWORD_FLOAT,
            TokenType.KEYWORD_VOID,
            TokenType.KEYWORD_CHAR,
            TokenType.KEYWORD_BOOLEAN,
            TokenType.IDENTIFICADOR
        )

    def is_primitive_type(self) -> bool:
        """Indica si es un tipo primitivo nativo."""
        return self.type in (
            TokenType.KEYWORD_INT,
            TokenType.KEYWORD_FLOAT,
            TokenType.KEYWORD_VOID,
            TokenType.KEYWORD_CHAR,
            TokenType.KEYWORD_BOOLEAN
        )

    def is_arithmetic_op(self) -> bool:
        return self.type in (
            TokenType.OP_SUMA,
            TokenType.OP_RESTA,
            TokenType.OP_MULTIPLICACION,
            TokenType.OP_DIVISION,
            TokenType.OP_MODULO
        )

    def is_relational_op(self) -> bool:
        return self.type in (
            TokenType.OP_IGUAL,
            TokenType.OP_DIFERENTE,
            TokenType.OP_MENOR,
            TokenType.OP_MENOR_IGUAL,
            TokenType.OP_MAYOR,
            TokenType.OP_MAYOR_IGUAL
        )

    def is_logical_op(self) -> bool:
        return self.type in (
            TokenType.OP_AND,
            TokenType.OP_OR
        )

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column})"
