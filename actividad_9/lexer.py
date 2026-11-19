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

from typing import List, Optional
from token_type import TokenType, Token
from error_handler import CompilerErrorHandler, ErrorPhase


class Lexer:
    """
    Analizador Léxico (Scanner) para el compilador de métodos, clases y estructuras de control.
    Convierte el código fuente en un flujo ordenado de tokens etiquetados con línea y columna.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    KEYWORDS = {
        'class': TokenType.KEYWORD_CLASS,
        'int': TokenType.KEYWORD_INT,
        'float': TokenType.KEYWORD_FLOAT,
        'void': TokenType.KEYWORD_VOID,
        'char': TokenType.KEYWORD_CHAR,
        'boolean': TokenType.KEYWORD_BOOLEAN,
        'bool': TokenType.KEYWORD_BOOLEAN,
        'string': TokenType.KEYWORD_STRING,
        'String': TokenType.KEYWORD_STRING,
        'return': TokenType.KEYWORD_RETURN,
        'if': TokenType.KEYWORD_IF,
        'else': TokenType.KEYWORD_ELSE,
        'while': TokenType.KEYWORD_WHILE,
        'for': TokenType.KEYWORD_FOR,
        'function': TokenType.KEYWORD_FUNCTION,
        'let': TokenType.KEYWORD_LET,
        'var': TokenType.KEYWORD_VAR,
        'try': TokenType.KEYWORD_TRY,
        'catch': TokenType.KEYWORD_CATCH,
        'break': TokenType.KEYWORD_BREAK,
        'continue': TokenType.KEYWORD_CONTINUE,
        'true': TokenType.LITERAL_BOOLEANO,
        'false': TokenType.LITERAL_BOOLEANO,
    }

    def __init__(self, source_code: str, error_handler: Optional[CompilerErrorHandler] = None):
        self.source = source_code
        self.error_handler = error_handler or CompilerErrorHandler()
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.token_start_column = 1

    def tokenize(self) -> List[Token]:
        """Procesa todo el código fuente y genera la lista de tokens terminada en EOF."""
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1

        while not self._is_at_end():
            self.start = self.current
            self.token_start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        self.column += 1
        return c

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _add_token(self, type_: TokenType, literal_val=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, self.line, self.token_start_column, literal_val))

    def _scan_token(self):
        c = self._advance()

        # Espacios en blanco
        if c in [' ', '\r', '\t']:
            return

        if c == '\n':
            self.line += 1
            self.column = 1
            return

        # Comentarios tipo Python '#' (utilizados por el profesor en las instrucciones)
        if c == '#':
            while self._peek() != '\n' and not self._is_at_end():
                self._advance()
            return

        # Delimitadores y Operadores de un caracter o compuestos
        if c == '(':
            self._add_token(TokenType.PARENTESIS_IZQ)
        elif c == ')':
            self._add_token(TokenType.PARENTESIS_DER)
        elif c == '{':
            self._add_token(TokenType.LLAVE_IZQ)
        elif c == '}':
            self._add_token(TokenType.LLAVE_DER)
        elif c == '[':
            self._add_token(TokenType.CORCHETE_IZQ)
        elif c == ']':
            self._add_token(TokenType.CORCHETE_DER)
        elif c == ',':
            self._add_token(TokenType.COMA)
        elif c == '.':
            self._add_token(TokenType.PUNTO)
        elif c == ';':
            self._add_token(TokenType.PUNTO_Y_COMA)
        elif c == ':':
            self._add_token(TokenType.DOS_PUNTOS)
        elif c == '+':
            if self._match('+'):
                self._add_token(TokenType.OP_INCREMENTO)
            else:
                self._add_token(TokenType.OP_SUMA)
        elif c == '-':
            if self._match('-'):
                self._add_token(TokenType.OP_DECREMENTO)
            else:
                self._add_token(TokenType.OP_RESTA)
        elif c == '*':
            self._add_token(TokenType.OP_MULTIPLICACION)
        elif c == '%':
            self._add_token(TokenType.OP_MODULO)
        elif c == '/':
            if self._match('/'):
                # Comentario de una línea //
                while self._peek() != '\n' and not self._is_at_end():
                    self._advance()
            elif self._match('*'):
                # Comentario multilínea /* ... */
                self._multi_line_comment()
            else:
                self._add_token(TokenType.OP_DIVISION)
        elif c == '!':
            if self._match('='):
                if self._match('='): # !==
                    pass
                self._add_token(TokenType.OP_DIFERENTE)
            else:
                self._add_token(TokenType.OP_NOT)
        elif c == '=':
            if self._match('='):
                if self._match('='): # ===
                    pass
                self._add_token(TokenType.OP_IGUAL)
            else:
                self._add_token(TokenType.OP_ASIGNACION)
        elif c == '<':
            self._add_token(TokenType.OP_MENOR_IGUAL if self._match('=') else TokenType.OP_MENOR)
        elif c == '>':
            self._add_token(TokenType.OP_MAYOR_IGUAL if self._match('=') else TokenType.OP_MAYOR)
        elif c == '&':
            if self._match('&'):
                self._add_token(TokenType.OP_AND)
            else:
                self._report_lexical_error(f"Operador '&' no reconocido, ¿quiso escribir '&&'?")
        elif c == '|':
            if self._match('|'):
                self._add_token(TokenType.OP_OR)
            else:
                self._report_lexical_error(f"Operador '|' no reconocido, ¿quiso escribir '||'?")
        elif c == '"':
            self._string()
        elif c == "'":
            self._char()
        else:
            if c.isdigit():
                self._number()
            elif c.isalpha() or c == '_':
                self._identifier()
            else:
                self._report_lexical_error(f"Carácter desconocido o no admitido: '{c}'")

    def _multi_line_comment(self):
        start_line = self.line
        start_col = self.token_start_column
        while not self._is_at_end():
            if self._peek() == '*' and self._peek_next() == '/':
                self._advance() # consume '*'
                self._advance() # consume '/'
                return
            if self._peek() == '\n':
                self.line += 1
                self.column = 0
            self._advance()

        self.error_handler.add_error(
            phase=ErrorPhase.LEXICA,
            category="COMENTARIO_NO_CERRADO",
            message="Comentario multilínea '/*' no cerrado al final del archivo.",
            line=start_line,
            column=start_col,
            suggestion="Cierre el comentario con '*/'."
        )

    def _string(self):
        start_col = self.token_start_column
        val_chars = []
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                self.line += 1
                self.column = 0
            val_chars.append(self._advance())

        if self._is_at_end():
            self.error_handler.add_error(
                phase=ErrorPhase.LEXICA,
                category="CADENA_NO_CERRADA",
                message="Literal de cadena no cerrado con comillas dobles '\"'.",
                line=self.line,
                column=start_col,
                suggestion="Agregue las comillas dobles de cierre '\"'."
            )
            return

        self._advance() # Consume '"' de cierre
        cadena = "".join(val_chars)
        self.tokens.append(Token(TokenType.LITERAL_CADENA, f'"{cadena}"', self.line, start_col, literal_value=cadena))

    def _char(self):
        start_col = self.token_start_column
        c_val = ""
        if not self._is_at_end() and self._peek() != "'":
            c_val = self._advance()

        if self._match("'"):
            self.tokens.append(Token(TokenType.LITERAL_CARACTER, f"'{c_val}'", self.line, start_col, literal_value=c_val))
        else:
            self.error_handler.add_error(
                phase=ErrorPhase.LEXICA,
                category="CARACTER_NO_CERRADO",
                message="Literal de carácter no cerrado con comilla simple.",
                line=self.line,
                column=start_col,
                suggestion="Cierre el literal de carácter con comilla simple '\''."
            )

    def _number(self):
        start_col = self.token_start_column
        is_float = False

        while self._peek().isdigit():
            self._advance()

        # Parte decimal opcional
        if self._peek() == '.' and self._peek_next().isdigit():
            is_float = True
            self._advance() # Consume '.'
            while self._peek().isdigit():
                self._advance()

        text = self.source[self.start:self.current]
        if is_float:
            self.tokens.append(Token(TokenType.NUMERO_FLOTANTE, text, self.line, start_col, literal_value=float(text)))
        else:
            self.tokens.append(Token(TokenType.NUMERO_ENTERO, text, self.line, start_col, literal_value=int(text)))

    def _identifier(self):
        start_col = self.token_start_column
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()

        text = self.source[self.start:self.current]
        type_ = self.KEYWORDS.get(text, TokenType.IDENTIFICADOR)

        lit_val = None
        if type_ == TokenType.LITERAL_BOOLEANO:
            lit_val = (text == 'true')

        self.tokens.append(Token(type_, text, self.line, start_col, literal_value=lit_val))

    def _report_lexical_error(self, message: str):
        self.error_handler.add_error(
            phase=ErrorPhase.LEXICA,
            category="CARACTER_INVALIDO",
            message=message,
            line=self.line,
            column=self.token_start_column,
            offending_text=self.source[self.start:self.current]
        )
