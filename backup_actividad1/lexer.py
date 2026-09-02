"""
================================================================================
ACTIVIDAD 1: DEFINICIÓN DE TOKENS Y EXPRESIONES REGULARES (ANALIZADOR LÉXICO C)
MATERIA: COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import re
from typing import List
from token_type import TokenType, Token

class LexerC:
    """
    Analizador léxico para el Lenguaje C basado en Expresiones Regulares.
    """
    RULES = [
        (TokenType.COMENTARIO_BLOQUE,   r'/\*[\s\S]*?\*/'),
        (TokenType.COMENTARIO_LINEA,    r'//.*'),
        (TokenType.PALABRA_CLAVE,       r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Bool|_Complex|_Imaginary)\b'),
        (TokenType.LITERAL_FLOTANTE,    r'\b\d+\.\d+([eE][+-]?\d+)?[fFlL]?\b|\b\d+[eE][+-]?\d+[fFlL]?\b'),
        (TokenType.LITERAL_ENTERO,      r'\b(0[xX][0-9a-fA-F]+|0[0-7]+|\d+)[uUlL]*\b'),
        (TokenType.LITERAL_CADENA,      r'"([^"\\]|\\.)*"'),
        (TokenType.LITERAL_CARACTER,    r"'([^'\\]|\\.)'"),
        (TokenType.IDENTIFICADOR,       r'[a-zA-Z_][a-zA-Z0-9_]*'),
        (TokenType.OPERADOR_RELACIONAL, r'==|!=|<=|>=|<|>'),
        (TokenType.OPERADOR_LOGICO,     r'&&|\|\||!'),
        (TokenType.OPERADOR_ASIGNACION, r'\+=|-=|\*=|/=|%=|<<=|>>=|&=|\^=|\|=|='),
        (TokenType.OPERADOR_ARITMETICO, r'\+\+|--|\+|\-|\*|/|%'),
        (TokenType.OPERADOR_BIT,        r'->|<<|>>|&|\||\^|~'),
        (TokenType.DELIMITADOR,         r'\(|\)|\{|\}|\[|\]|\;|\,|\.|\:|\?'),
    ]

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []
        self.errors: List[Token] = []

    def tokenize(self) -> List[Token]:
        self.tokens = []
        self.errors = []
        
        pos = 0
        line = 1
        col = 1
        length = len(self.code)

        while pos < length:
            # Manejar saltos de línea y espacios en blanco
            char = self.code[pos]
            if char == '\n':
                line += 1
                col = 1
                pos += 1
                continue
            elif char in ' \t\r':
                if char == '\t':
                    col += 4
                else:
                    col += 1
                pos += 1
                continue

            match_found = False
            for token_type, pattern in self.RULES:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    lexeme = match.group(0)
                    
                    # Detectar errores en cadenas sin cerrar antes de crear el token
                    token = Token(token_type, lexeme, line, col)
                    self.tokens.append(token)

                    # Actualizar línea y columna si el token abarca múltiples líneas (ej. comentarios de bloque o cadenas)
                    newlines = lexeme.count('\n')
                    if newlines > 0:
                        line += newlines
                        last_line_len = len(lexeme.split('\n')[-1])
                        col = last_line_len + 1
                    else:
                        col += len(lexeme)

                    pos = match.end()
                    match_found = True
                    break

            if not match_found:
                # Comprobar si es un intento de cadena no cerrada
                if self.code[pos] == '"':
                    # Buscar el fin de línea
                    end_line = self.code.find('\n', pos)
                    if end_line == -1:
                        end_line = length
                    bad_string = self.code[pos:end_line]
                    token = Token(TokenType.ERROR_LEXICO, bad_string, line, col, "Cadena sin cerrar")
                    self.tokens.append(token)
                    self.errors.append(token)
                    pos = end_line
                    col += len(bad_string)
                else:
                    invalid_char = self.code[pos]
                    token = Token(TokenType.ERROR_LEXICO, invalid_char, line, col, f"Carácter no reconocido '{invalid_char}'")
                    self.tokens.append(token)
                    self.errors.append(token)
                    pos += 1
                    col += 1

        return self.tokens
