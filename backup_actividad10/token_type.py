"""
================================================================================
ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
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


class TokenType(Enum):
    """
    Tipos de componentes léxicos para la generación de código intermedio.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Tipos de datos
    KEYWORD_INT = auto()
    KEYWORD_FLOAT = auto()
    KEYWORD_DOUBLE = auto()
    KEYWORD_BOOL = auto()
    KEYWORD_STRING = auto()
    KEYWORD_VOID = auto()

    # Literales booleanos
    KEYWORD_TRUE = auto()
    KEYWORD_FALSE = auto()

    # Identificadores y literales
    IDENTIFICADOR = auto()
    NUMERO_ENTERO = auto()
    NUMERO_FLOTANTE = auto()
    LITERAL_CADENA = auto()

    # Operadores
    ASIGNACION = auto()       # '='
    SUMA = auto()             # '+'
    RESTA = auto()            # '-'
    MULTIPLICACION = auto()   # '*'
    DIVISION = auto()         # '/'
    MODULO = auto()           # '%'

    # Relacionales
    IGUAL_QUE = auto()        # '=='
    DISTINTO_QUE = auto()     # '!='
    MENOR_QUE = auto()        # '<'
    MAYOR_QUE = auto()        # '>'
    MENOR_IGUAL_QUE = auto()  # '<='
    MAYOR_IGUAL_QUE = auto()  # '>='

    # Lógicos
    AND_LOGICO = auto()       # '&&'
    OR_LOGICO = auto()        # '||'
    NOT_LOGICO = auto()       # '!'

    # Delimitadores
    PARENTESIS_IZQ = auto()   # '('
    PARENTESIS_DER = auto()   # ')'
    PUNTO_Y_COMA = auto()     # ';'
    COMA = auto()             # ','

    # Otros
    COMENTARIO_LINEA = auto()
    COMENTARIO_BLOQUE = auto()
    EOF = auto()


class Token:
    """
    Representa un token individual.

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
