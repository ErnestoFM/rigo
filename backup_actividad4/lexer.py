"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List
from token_type import TokenType, Token

class Lexer:
    """
    Analizador Léxico (Scanner) para expresiones aritméticas y lógicas.
    Convierte el flujo de caracteres en tokens precisos con control de línea y columna.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
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
        ch = self._peek()
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def tokenize(self) -> List[Token]:
        """Procesa toda la entrada y retorna la lista de tokens finalizada en EOF."""
        tokens: List[Token] = []

        while self.pos < self.length:
            ch = self._peek()

            # 1. Ignorar espacios en blanco y saltos de línea
            if ch in (' ', '\t', '\r', '\n'):
                self._advance()
                continue

            # 2. Ignorar comentarios de una línea (// o #)
            if ch == '/' and self._peek(1) == '/':
                while self._peek() not in ('\n', '\0'):
                    self._advance()
                continue
            if ch == '#':
                while self._peek() not in ('\n', '\0'):
                    self._advance()
                continue

            start_col = self.column
            start_line = self.line

            # 3. Números (Enteros o Flotantes)
            if ch.isdigit():
                tokens.append(self._read_number(start_line, start_col))
                continue

            # 4. Identificadores y palabras clave
            if ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier(start_line, start_col))
                continue

            # 5. Operadores de dos caracteres y relacionales
            if ch == '=':
                self._advance()
                if self._match('='):
                    tokens.append(Token(TokenType.OP_IGUAL, "==", start_line, start_col))
                else:
                    # En expresiones puras, un '=' solitario se marca como operador o desconocido
                    tokens.append(Token(TokenType.DESCONOCIDO, "=", start_line, start_col))
                continue

            if ch == '!':
                self._advance()
                if self._match('='):
                    tokens.append(Token(TokenType.OP_DIFERENTE, "!=", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_NOT, "!", start_line, start_col))
                continue

            if ch == '<':
                self._advance()
                if self._match('='):
                    tokens.append(Token(TokenType.OP_MENOR_IGUAL, "<=", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_MENOR, "<", start_line, start_col))
                continue

            if ch == '>':
                self._advance()
                if self._match('='):
                    tokens.append(Token(TokenType.OP_MAYOR_IGUAL, ">=", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_MAYOR, ">", start_line, start_col))
                continue

            if ch == '&':
                self._advance()
                if self._match('&'):
                    tokens.append(Token(TokenType.OP_AND, "&&", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_AND, "&", start_line, start_col))
                continue

            if ch == '|':
                self._advance()
                if self._match('|'):
                    tokens.append(Token(TokenType.OP_OR, "||", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_OR, "|", start_line, start_col))
                continue

            # 6. Operadores aritméticos de un carácter
            if ch == '+':
                self._advance()
                tokens.append(Token(TokenType.OP_SUMA, "+", start_line, start_col))
                continue

            if ch == '-':
                self._advance()
                tokens.append(Token(TokenType.OP_RESTA, "-", start_line, start_col))
                continue

            if ch == '*':
                self._advance()
                if self._match('*'):
                    tokens.append(Token(TokenType.OP_POTENCIA, "**", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_MULTIPLICACION, "*", start_line, start_col))
                continue

            if ch == '/':
                self._advance()
                tokens.append(Token(TokenType.OP_DIVISION, "/", start_line, start_col))
                continue

            if ch == '%':
                self._advance()
                tokens.append(Token(TokenType.OP_MODULO, "%", start_line, start_col))
                continue

            if ch == '^':
                self._advance()
                tokens.append(Token(TokenType.OP_POTENCIA, "^", start_line, start_col))
                continue

            # 7. Delimitadores
            if ch == '(':
                self._advance()
                tokens.append(Token(TokenType.PARENTESIS_IZQ, "(", start_line, start_col))
                continue

            if ch == ')':
                self._advance()
                tokens.append(Token(TokenType.PARENTESIS_DER, ")", start_line, start_col))
                continue

            # 8. Token Desconocido
            self._advance()
            tokens.append(Token(TokenType.DESCONOCIDO, ch, start_line, start_col))

        tokens.append(Token(TokenType.EOF, "<EOF>", self.line, self.column))
        return tokens

    def _read_number(self, start_line: int, start_col: int) -> Token:
        num_str = ""
        is_float = False

        while self._peek().isdigit():
            num_str += self._advance()

        if self._peek() == '.' and self._peek(1).isdigit():
            is_float = True
            num_str += self._advance() # consume '.'
            while self._peek().isdigit():
                num_str += self._advance()

        type_ = TokenType.NUMERO_FLOTANTE if is_float else TokenType.NUMERO_ENTERO
        return Token(type_, num_str, start_line, start_col)

    def _read_identifier(self, start_line: int, start_col: int) -> Token:
        ident_str = ""
        while self._peek().isalnum() or self._peek() == '_':
            ident_str += self._advance()

        lower = ident_str.lower()
        if lower == 'and':
            return Token(TokenType.OP_AND, ident_str, start_line, start_col)
        elif lower == 'or':
            return Token(TokenType.OP_OR, ident_str, start_line, start_col)
        elif lower == 'not':
            return Token(TokenType.OP_NOT, ident_str, start_line, start_col)

        return Token(TokenType.IDENTIFICADOR, ident_str, start_line, start_col)
