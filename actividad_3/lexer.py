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

import re
from typing import List
from token_type import TokenType, Token

class Lexer:
    """
    Analizador léxico que convierte el código fuente en un flujo de tokens
    con seguimiento estricto de número de línea y columna.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    
    TIPOS_VALIDOS = {
        'entero', 'flotante', 'booleano', 'cadena',
        'int', 'float', 'bool', 'char', 'string'
    }
    
    PALABRAS_CONSTANTE = {'constante', 'const'}
    
    BOOLEANOS = {'verdadero', 'falso', 'true', 'false'}

    def __init__(self, source_code: str):
        self.source = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < self.length:
            return self.source[idx]
        return '\0'

    def _advance(self) -> str:
        char = self._peek()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def _skip_whitespace_and_comments(self):
        while self.pos < self.length:
            char = self._peek()
            
            # Espacios en blanco
            if char in ' \t\r\n':
                self._advance()
                continue
                
            # Comentario de una línea //
            if char == '/' and self._peek(1) == '/':
                while self.pos < self.length and self._peek() != '\n':
                    self._advance()
                continue
                
            # Comentario multilínea /* ... */
            if char == '/' and self._peek(1) == '*':
                self._advance() # /
                self._advance() # *
                while self.pos < self.length:
                    if self._peek() == '*' and self._peek(1) == '/':
                        self._advance()
                        self._advance()
                        break
                    self._advance()
                continue
                
            break

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        
        while self.pos < self.length:
            self._skip_whitespace_and_comments()
            if self.pos >= self.length:
                break

            start_line = self.line
            start_col = self.column
            char = self._peek()

            # Cadenas de texto ("..." o '...')
            if char in ('"', "'"):
                quote = self._advance()
                val = ""
                while self.pos < self.length and self._peek() != quote:
                    if self._peek() == '\n':
                        break
                    val += self._advance()
                if self.pos < self.length and self._peek() == quote:
                    self._advance() # Cierre
                tokens.append(Token(TokenType.LITERAL_CADENA, val, start_line, start_col))
                continue

            # Números e Identificadores que inician con dígitos (ej: 123x, 8promedio)
            if char.isdigit():
                num_str = ""
                has_dot = False
                while self.pos < self.length:
                    c = self._peek()
                    if c.isdigit():
                        num_str += self._advance()
                    elif c == '.' and not has_dot and self._peek(1).isdigit():
                        has_dot = True
                        num_str += self._advance()
                    else:
                        break
                
                # Si inmediatamente sigue una letra o guión bajo, es un identificador inválido!
                if self.pos < self.length and (self._peek().isalpha() or self._peek() == '_'):
                    while self.pos < self.length and (self._peek().isalnum() or self._peek() == '_'):
                        num_str += self._advance()
                    tokens.append(Token(TokenType.IDENTIFICADOR_INVALIDO, num_str, start_line, start_col))
                else:
                    tok_type = TokenType.LITERAL_FLOTANTE if has_dot else TokenType.LITERAL_ENTERO
                    tokens.append(Token(tok_type, num_str, start_line, start_col))
                continue

            # Identificadores válidos y palabras clave (inician con letra o _)
            if char.isalpha() or char == '_':
                ident = ""
                while self.pos < self.length and (self._peek().isalnum() or self._peek() == '_'):
                    ident += self._advance()
                
                # Clasificar
                if ident.lower() in self.TIPOS_VALIDOS:
                    tokens.append(Token(TokenType.TIPO, ident, start_line, start_col))
                elif ident.lower() in self.PALABRAS_CONSTANTE:
                    tokens.append(Token(TokenType.CONSTANTE, ident, start_line, start_col))
                elif ident.lower() in self.BOOLEANOS:
                    tokens.append(Token(TokenType.LITERAL_BOOLEANO, ident, start_line, start_col))
                elif ident.lower() == 'and':
                    tokens.append(Token(TokenType.OP_Y, ident, start_line, start_col))
                elif ident.lower() == 'or':
                    tokens.append(Token(TokenType.OP_O, ident, start_line, start_col))
                elif ident.lower() == 'not':
                    tokens.append(Token(TokenType.OP_NO, ident, start_line, start_col))
                else:
                    tokens.append(Token(TokenType.IDENTIFICADOR, ident, start_line, start_col))
                continue

            # Operadores de dos caracteres
            two_chars = self._peek() + self._peek(1)
            if two_chars == '==':
                self._advance(); self._advance()
                tokens.append(Token(TokenType.OP_IGUAL, '==', start_line, start_col))
                continue
            elif two_chars == '!=':
                self._advance(); self._advance()
                tokens.append(Token(TokenType.OP_DISTINTO, '!=', start_line, start_col))
                continue
            elif two_chars == '<=':
                self._advance(); self._advance()
                tokens.append(Token(TokenType.OP_MENOR_IGUAL, '<=', start_line, start_col))
                continue
            elif two_chars == '>=':
                self._advance(); self._advance()
                tokens.append(Token(TokenType.OP_MAYOR_IGUAL, '>=', start_line, start_col))
                continue
            elif two_chars == '&&':
                self._advance(); self._advance()
                tokens.append(Token(TokenType.OP_Y, '&&', start_line, start_col))
                continue
            elif two_chars == '||':
                self._advance(); self._advance()
                tokens.append(Token(TokenType.OP_O, '||', start_line, start_col))
                continue

            # Operadores y signos de un solo carácter
            c = self._advance()
            if c == '=':
                tokens.append(Token(TokenType.ASIGNACION, '=', start_line, start_col))
            elif c == ';':
                tokens.append(Token(TokenType.PUNTO_Y_COMA, ';', start_line, start_col))
            elif c == ',':
                tokens.append(Token(TokenType.COMA, ',', start_line, start_col))
            elif c == '(':
                tokens.append(Token(TokenType.PARENTESIS_IZQ, '(', start_line, start_col))
            elif c == ')':
                tokens.append(Token(TokenType.PARENTESIS_DER, ')', start_line, start_col))
            elif c == '+':
                tokens.append(Token(TokenType.OP_SUMA, '+', start_line, start_col))
            elif c == '-':
                tokens.append(Token(TokenType.OP_RESTA, '-', start_line, start_col))
            elif c == '*':
                tokens.append(Token(TokenType.OP_MULT, '*', start_line, start_col))
            elif c == '/':
                tokens.append(Token(TokenType.OP_DIV, '/', start_line, start_col))
            elif c == '%':
                tokens.append(Token(TokenType.OP_MOD, '%', start_line, start_col))
            elif c == '<':
                tokens.append(Token(TokenType.OP_MENOR, '<', start_line, start_col))
            elif c == '>':
                tokens.append(Token(TokenType.OP_MAYOR, '>', start_line, start_col))
            elif c == '!':
                tokens.append(Token(TokenType.OP_NO, '!', start_line, start_col))
            else:
                tokens.append(Token(TokenType.DESCONOCIDO, c, start_line, start_col))

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens
