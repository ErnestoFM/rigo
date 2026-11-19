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

from typing import List
from token_type import TokenType, Token


class Lexer:
    """
    Analizador Léxico (Scanner) para definiciones de métodos, clases y sentencias.
    Convierte el flujo de caracteres en tokens precisos con control de línea y columna.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    KEYWORDS = {
        "class": TokenType.KEYWORD_CLASS,
        "int": TokenType.KEYWORD_INT,
        "float": TokenType.KEYWORD_FLOAT,
        "void": TokenType.KEYWORD_VOID,
        "char": TokenType.KEYWORD_CHAR,
        "boolean": TokenType.KEYWORD_BOOLEAN,
        "return": TokenType.KEYWORD_RETURN,
        "if": TokenType.KEYWORD_IF,
        "else": TokenType.KEYWORD_ELSE,
        "while": TokenType.KEYWORD_WHILE,
        "for": TokenType.KEYWORD_FOR,
        "true": TokenType.LITERAL_BOOLEANO,
        "false": TokenType.LITERAL_BOOLEANO
    }

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

            # 1. Espacios en blanco y saltos de línea
            if ch in (' ', '\t', '\r', '\n'):
                self._advance()
                continue

            # 2. Comentarios de línea (// o #)
            if ch == '/' and self._peek(1) == '/':
                while self._peek() not in ('\n', '\0'):
                    self._advance()
                continue

            if ch == '#':
                while self._peek() not in ('\n', '\0'):
                    self._advance()
                continue

            # 3. Comentarios multilínea (/* ... */)
            if ch == '/' and self._peek(1) == '*':
                self._advance() # Consume '/'
                self._advance() # Consume '*'
                while self.pos < self.length:
                    if self._peek() == '*' and self._peek(1) == '/':
                        self._advance() # Consume '*'
                        self._advance() # Consume '/'
                        break
                    self._advance()
                continue

            start_col = self.column
            start_line = self.line

            # 4. Números enteros y flotantes
            if ch.isdigit():
                tokens.append(self._read_number(start_line, start_col))
                continue

            # 5. Cadenas de texto entre comillas dobles
            if ch == '"':
                tokens.append(self._read_string(start_line, start_col))
                continue

            # 6. Caracteres entre comillas simples
            if ch == "'":
                tokens.append(self._read_char(start_line, start_col))
                continue

            # 7. Identificadores y palabras clave
            if ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier(start_line, start_col))
                continue

            # 8. Operadores de comparación y asignación
            if ch == '=':
                self._advance()
                if self._match('='):
                    tokens.append(Token(TokenType.OP_IGUAL, "==", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.OP_ASIGNACION, "=", start_line, start_col))
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
                    tokens.append(Token(TokenType.DESCONOCIDO, "&", start_line, start_col))
                continue

            if ch == '|':
                self._advance()
                if self._match('|'):
                    tokens.append(Token(TokenType.OP_OR, "||", start_line, start_col))
                else:
                    tokens.append(Token(TokenType.DESCONOCIDO, "|", start_line, start_col))
                continue

            # 9. Operadores aritméticos de 1 carácter
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

            # 10. Delimitadores
            if ch == '{':
                self._advance()
                tokens.append(Token(TokenType.LLAVE_IZQ, "{", start_line, start_col))
                continue

            if ch == '}':
                self._advance()
                tokens.append(Token(TokenType.LLAVE_DER, "}", start_line, start_col))
                continue

            if ch == '(':
                self._advance()
                tokens.append(Token(TokenType.PARENTESIS_IZQ, "(", start_line, start_col))
                continue

            if ch == ')':
                self._advance()
                tokens.append(Token(TokenType.PARENTESIS_DER, ")", start_line, start_col))
                continue

            if ch == '[':
                self._advance()
                tokens.append(Token(TokenType.CORCHETE_IZQ, "[", start_line, start_col))
                continue

            if ch == ']':
                self._advance()
                tokens.append(Token(TokenType.CORCHETE_DER, "]", start_line, start_col))
                continue

            if ch == ';':
                self._advance()
                tokens.append(Token(TokenType.PUNTO_Y_COMA, ";", start_line, start_col))
                continue

            if ch == ',':
                self._advance()
                tokens.append(Token(TokenType.COMA, ",", start_line, start_col))
                continue

            if ch == '.':
                self._advance()
                tokens.append(Token(TokenType.PUNTO, ".", start_line, start_col))
                continue

            # Carácter no reconocido
            bad_ch = self._advance()
            tokens.append(Token(TokenType.DESCONOCIDO, bad_ch, start_line, start_col))

        tokens.append(Token(TokenType.EOF, "<EOF>", self.line, self.column))
        return tokens

    def _read_number(self, line: int, col: int) -> Token:
        num_str = ""
        is_float = False

        while self._peek().isdigit():
            num_str += self._advance()

        if self._peek() == '.' and self._peek(1).isdigit():
            is_float = True
            num_str += self._advance() # consume '.'
            while self._peek().isdigit():
                num_str += self._advance()

        tipo = TokenType.NUMERO_FLOTANTE if is_float else TokenType.NUMERO_ENTERO
        return Token(tipo, num_str, line, col)

    def _read_identifier(self, line: int, col: int) -> Token:
        ident_str = ""
        while self._peek().isalnum() or self._peek() == '_':
            ident_str += self._advance()

        tipo = self.KEYWORDS.get(ident_str, TokenType.IDENTIFICADOR)
        return Token(tipo, ident_str, line, col)

    def _read_string(self, line: int, col: int) -> Token:
        self._advance() # consume '"'
        val = ""
        while self.pos < self.length and self._peek() != '"' and self._peek() != '\n':
            if self._peek() == '\\' and self._peek(1) != '\0':
                self._advance()
                val += self._advance()
            else:
                val += self._advance()

        if self._peek() == '"':
            self._advance()
            return Token(TokenType.LITERAL_CADENA, f'"{val}"', line, col)
        return Token(TokenType.DESCONOCIDO, f'"{val}', line, col)

    def _read_char(self, line: int, col: int) -> Token:
        self._advance() # consume "'"
        val = ""
        while self.pos < self.length and self._peek() != "'" and self._peek() != '\n':
            if self._peek() == '\\' and self._peek(1) != '\0':
                self._advance()
                val += self._advance()
            else:
                val += self._advance()

        if self._peek() == "'":
            self._advance()
            return Token(TokenType.LITERAL_CARACTER, f"'{val}'", line, col)
        return Token(TokenType.DESCONOCIDO, f"'{val}", line, col)
