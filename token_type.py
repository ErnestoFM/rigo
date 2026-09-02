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

class TokenType(Enum):
    PALABRA_CLAVE = "Palabra Clave"
    IDENTIFICADOR = "Identificador"
    LITERAL_ENTERO = "Literal Entero"
    LITERAL_FLOTANTE = "Literal Flotante"
    LITERAL_CADENA = "Literal Cadena"
    LITERAL_CARACTER = "Literal Carácter"
    OPERADOR_ARITMETICO = "Operador Aritmético"
    OPERADOR_RELACIONAL = "Operador Relacional"
    OPERADOR_LOGICO = "Operador Lógico"
    OPERADOR_ASIGNACION = "Operador Asignación"
    OPERADOR_BIT = "Operador de Bits"
    DELIMITADOR = "Delimitador / Símbolo"
    COMENTARIO_LINEA = "Comentario de Línea"
    COMENTARIO_BLOQUE = "Comentario de Bloque"
    
    # Subtipos específicos de Error Léxico (Actividad 2)
    ERROR_CARACTER_NO_RECONOCIDO = "Error: Carácter No Reconocido"
    ERROR_IDENTIFICADOR_MAL_FORMADO = "Error: Identificador Mal Formado"
    ERROR_NUMERO_INCORRECTO = "Error: Literal Numérico Incorrecto"
    ERROR_CADENA_MAL_FORMADA = "Error: Cadena Mal Formada"

class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int, description: str = ""):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        self.description = description

    @property
    def is_error(self) -> bool:
        return self.type.name.startswith("ERROR_")

    def __repr__(self):
        return f"Token({self.type.value}, '{self.value}', L:{self.line}, C:{self.column})"
