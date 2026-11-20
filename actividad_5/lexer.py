"""
================================================================================
ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL (LENGUAJE C EN PYTHON)
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
from typing import List, Tuple
from token_type import TokenType, Token


class Lexer:
    """
    Analizador Léxico especializado para la fase sintáctica de estructuras de control.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    TOKEN_SPECS: List[Tuple[TokenType, str]] = [
        # Comentarios y preprocesador
        (TokenType.COMENTARIO_BLOQUE,       r'/\*[\s\S]*?\*/'),
        (TokenType.COMENTARIO_LINEA,        r'//.*'),
        (TokenType.DIRECTIVA_PREPROCESADOR, r'#\s*(include|define|undef|ifdef|ifndef|endif)\b[^\n]*'),

        # Palabras clave de control
        (TokenType.KEYWORD_IF,              r'\bif\b'),
        (TokenType.KEYWORD_ELSE,            r'\belse\b'),
        (TokenType.KEYWORD_WHILE,           r'\bwhile\b'),
        (TokenType.KEYWORD_FOR,             r'\bfor\b'),
        (TokenType.KEYWORD_RETURN,          r'\breturn\b'),

        # Palabras clave de tipos
        (TokenType.KEYWORD_INT,             r'\bint\b'),
        (TokenType.KEYWORD_FLOAT,           r'\bfloat\b'),
        (TokenType.KEYWORD_DOUBLE,          r'\bdouble\b'),
        (TokenType.KEYWORD_CHAR,            r'\bchar\b'),
        (TokenType.KEYWORD_VOID,            r'\bvoid\b'),

        # Literales numéricos
        (TokenType.NUMERO_FLOTANTE,         r'\b\d+\.\d+([eE][+-]?\d+)?[fFlL]?\b'),
        (TokenType.NUMERO_ENTERO,           r'\b(0[xX][0-9a-fA-F]+|\d+)\b'),

        # Literales de texto
        (TokenType.LITERAL_CADENA,          r'"([^"\\]|\\.)*"'),
        (TokenType.LITERAL_CARACTER,        r"'([^'\\]|\\.)'"),

        # Operadores compuestos y relacionales
        (TokenType.INCREMENTO,              r'\+\+'),
        (TokenType.DECREMENTO,              r'--'),
        (TokenType.IGUAL_QUE,               r'=='),
        (TokenType.DISTINTO_QUE,            r'!='),
        (TokenType.MENOR_IGUAL_QUE,         r'<='),
        (TokenType.MAYOR_IGUAL_QUE,         r'>='),
        (TokenType.AND_LOGICO,              r'&&'),
        (TokenType.OR_LOGICO,               r'\|\|'),
        (TokenType.ASIGNACION_SUMA,         r'\+='),
        (TokenType.ASIGNACION_RESTA,        r'-='),

        # Operadores simples
        (TokenType.ASIGNACION,              r'='),
        (TokenType.MENOR_QUE,               r'<'),
        (TokenType.MAYOR_QUE,               r'>'),
        (TokenType.NOT_LOGICO,              r'!'),
        (TokenType.SUMA,                    r'\+'),
        (TokenType.RESTA,                   r'-'),
        (TokenType.MULTIPLICACION,          r'\*'),
        (TokenType.DIVISION,                r'/'),
        (TokenType.MODULO,                  r'%'),

        # Delimitadores
        (TokenType.PARENTESIS_IZQ,          r'\('),
        (TokenType.PARENTESIS_DER,          r'\)'),
        (TokenType.LLAVE_IZQ,               r'\{'),
        (TokenType.LLAVE_DER,               r'\}'),
        (TokenType.CORCHETE_IZQ,            r'\['),
        (TokenType.CORCHETE_DER,            r'\]'),
        (TokenType.PUNTO_Y_COMA,            r';'),
        (TokenType.COMA,                    r','),

        # Identificadores
        (TokenType.IDENTIFICADOR,           r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ]

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []
        self.line_starts = [0]
        self._compute_line_starts()
        self.compiled_specs = [(tok_type, re.compile(pat)) for tok_type, pat in self.TOKEN_SPECS]

    def _compute_line_starts(self):
        self.line_starts = [0]
        for idx, ch in enumerate(self.code):
            if ch == '\n':
                self.line_starts.append(idx + 1)

    def _get_coords(self, pos: int) -> Tuple[int, int]:
        line = 1
        for i, start in enumerate(self.line_starts):
            if pos >= start:
                line = i + 1
            else:
                break
        col = pos - self.line_starts[line - 1] + 1
        return line, col

    def tokenize(self) -> List[Token]:
        self.tokens.clear()
        pos = 0
        code_len = len(self.code)

        while pos < code_len:
            if self.code[pos].isspace():
                pos += 1
                continue

            cur_line, cur_col = self._get_coords(pos)
            matched = False

            for tok_type, regex in self.compiled_specs:
                match = regex.match(self.code, pos)
                if match:
                    val = match.group(0)
                    # Omitir comentarios de la corriente que va al parser
                    if tok_type not in (TokenType.COMENTARIO_LINEA, TokenType.COMENTARIO_BLOQUE):
                        self.tokens.append(Token(tok_type, val, cur_line, cur_col))
                    pos = match.end()
                    matched = True
                    break

            if not matched:
                # Carácter no contemplado directamente (ej. símbolo de error)
                bad_char = self.code[pos]
                # Se genera identificador o token para que el parser lo analice o capture el error
                self.tokens.append(Token(TokenType.IDENTIFICADOR, bad_char, cur_line, cur_col))
                pos += 1

        eof_line, eof_col = self._get_coords(code_len)
        self.tokens.append(Token(TokenType.EOF, "EOF", eof_line, eof_col))
        return self.tokens
