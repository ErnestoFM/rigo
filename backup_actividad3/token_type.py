"""
================================================================================
ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES
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
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    # Palabras reservadas para tipos de datos
    TIPO = "TIPO_DATO"
    
    # Declaración de constantes
    CONSTANTE = "PALABRA_CONSTANTE"
    
    # Identificadores
    IDENTIFICADOR = "IDENTIFICADOR"
    IDENTIFICADOR_INVALIDO = "IDENTIFICADOR_INVALIDO"
    
    # Literales
    LITERAL_ENTERO = "LITERAL_ENTERO"
    LITERAL_FLOTANTE = "LITERAL_FLOTANTE"
    LITERAL_CADENA = "LITERAL_CADENA"
    LITERAL_BOOLEANO = "LITERAL_BOOLEANO"
    
    # Operador de asignación
    ASIGNACION = "OPERADOR_ASIGNACION"       # =
    
    # Operadores aritméticos
    OP_SUMA = "OPERADOR_SUMA"                 # +
    OP_RESTA = "OPERADOR_RESTA"               # -
    OP_MULT = "OPERADOR_MULTIPLICACION"       # *
    OP_DIV = "OPERADOR_DIVISION"             # /
    OP_MOD = "OPERADOR_MODULO"               # %
    
    # Operadores relacionales y lógicos
    OP_IGUAL = "OPERADOR_IGUALDAD"           # ==
    OP_DISTINTO = "OPERADOR_DISTINTO"         # !=
    OP_MENOR = "OPERADOR_MENOR"               # <
    OP_MENOR_IGUAL = "OPERADOR_MENOR_IGUAL"   # <=
    OP_MAYOR = "OPERADOR_MAYOR"               # >
    OP_MAYOR_IGUAL = "OPERADOR_MAYOR_IGUAL"   # >=
    OP_Y = "OPERADOR_CONJUNCION"             # &&, y, and
    OP_O = "OPERADOR_DISYUNCION"             # ||, o, or
    OP_NO = "OPERADOR_NEGACION"               # !, no, not
    
    # Delimitadores y puntuación
    PUNTO_Y_COMA = "PUNTO_Y_COMA"             # ;
    COMA = "COMA"                             # ,
    PARENTESIS_IZQ = "PARENTESIS_IZQ"         # (
    PARENTESIS_DER = "PARENTESIS_DER"         # )
    
    # Especiales
    EOF = "FIN_DE_ENTRADA"
    DESCONOCIDO = "TOKEN_DESCONOCIDO"

class Token:
    """
    Integrantes:
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

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', L:{self.line}, C:{self.column})"
