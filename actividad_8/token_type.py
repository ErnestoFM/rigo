"""
================================================================================
ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - VERIFICACIÓN DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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
    Tipos de tokens para expresiones aritméticas, lógicas y relacionales en C.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Palabras clave de tipos de datos
    KEYWORD_INT = auto()         # 'int'
    KEYWORD_FLOAT = auto()       # 'float'
    KEYWORD_DOUBLE = auto()      # 'double'
    KEYWORD_CHAR = auto()        # 'char'
    KEYWORD_BOOL = auto()        # 'bool'
    KEYWORD_STRING = auto()      # 'string'
    KEYWORD_VOID = auto()        # 'void'

    # Literales booleanos
    KEYWORD_TRUE = auto()        # 'true'
    KEYWORD_FALSE = auto()       # 'false'

    # Palabra clave de conversión
    KEYWORD_STATIC_CAST = auto() # 'static_cast'

    # Palabras clave de control
    KEYWORD_IF = auto()          # 'if'
    KEYWORD_ELSE = auto()        # 'else'
    KEYWORD_WHILE = auto()       # 'while'
    KEYWORD_FOR = auto()         # 'for'
    KEYWORD_RETURN = auto()      # 'return'

    # Literales e Identificadores
    IDENTIFICADOR = auto()       # edad, nombre
    NUMERO_ENTERO = auto()       # 10, 25
    NUMERO_FLOTANTE = auto()     # 3.14, 2.5
    LITERAL_CADENA = auto()      # "Juan", "Hola"
    LITERAL_CARACTER = auto()    # 'A'

    # Operadores Aritméticos
    SUMA = auto()                # '+'
    RESTA = auto()               # '-'
    MULTIPLICACION = auto()      # '*'
    DIVISION = auto()            # '/'
    MODULO = auto()              # '%'

    # Operadores Relacionales / Comparación
    IGUAL_QUE = auto()           # '=='
    DISTINTO_QUE = auto()        # '!='
    MENOR_QUE = auto()           # '<'
    MAYOR_QUE = auto()           # '>'
    MENOR_IGUAL_QUE = auto()     # '<='
    MAYOR_IGUAL_QUE = auto()     # '>='

    # Operadores Lógicos
    AND_LOGICO = auto()          # '&&'
    OR_LOGICO = auto()           # '||'
    NOT_LOGICO = auto()          # '!'

    # Operadores de Asignación
    ASIGNACION = auto()          # '='
    ASIGNACION_SUMA = auto()     # '+='
    ASIGNACION_RESTA = auto()    # '-='

    # Delimitadores
    PARENTESIS_IZQ = auto()      # '('
    PARENTESIS_DER = auto()      # ')'
    LLAVE_IZQ = auto()           # '{'
    LLAVE_DER = auto()           # '}'
    CORCHETE_IZQ = auto()        # '['
    CORCHETE_DER = auto()        # ']'
    PUNTO_Y_COMA = auto()        # ';'
    COMA = auto()                # ','

    # Otros
    DIRECTIVA_PREPROCESADOR = auto()
    COMENTARIO_LINEA = auto()
    COMENTARIO_BLOQUE = auto()
    EOF = auto()


class Token:
    """
    Representa un componente léxico con su lexema y ubicación exacta.

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
