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

import re
from typing import List, Tuple
from token_type import TokenType, Token


class Lexer:
    """
    Analizador Léxico para sentencias y expresiones de asignación en C.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    TOKEN_SPECS: List[Tuple[TokenType, str]] = [
        (TokenType.COMENTARIO_BLOQUE,   r'/\*[\s\S]*?\*/'),
        (TokenType.COMENTARIO_LINEA,    r'//.*'),
        (TokenType.KEYWORD_INT,         r'\bint\b'),
        (TokenType.KEYWORD_FLOAT,       r'\bfloat\b'),
        (TokenType.KEYWORD_DOUBLE,      r'\bdouble\b'),
        (TokenType.KEYWORD_BOOL,        r'\bbool\b'),
        (TokenType.KEYWORD_STRING,      r'\bstring\b'),
        (TokenType.KEYWORD_VOID,        r'\bvoid\b'),
        (TokenType.KEYWORD_TRUE,        r'\btrue\b'),
        (TokenType.KEYWORD_FALSE,       r'\bfalse\b'),

        (TokenType.NUMERO_FLOTANTE,     r'\b\d+\.\d+([eE][+-]?\d+)?[fFlL]?\b'),
        (TokenType.NUMERO_ENTERO,       r'\b(0[xX][0-9a-fA-F]+|\d+)\b'),
        (TokenType.LITERAL_CADENA,      r'"([^"\\]|\\.)*"'),

        (TokenType.IGUAL_QUE,           r'=='),
        (TokenType.DISTINTO_QUE,        r'!='),
        (TokenType.MENOR_IGUAL_QUE,     r'<='),
        (TokenType.MAYOR_IGUAL_QUE,     r'>='),
        (TokenType.AND_LOGICO,          r'&&'),
        (TokenType.OR_LOGICO,           r'\|\|'),
        (TokenType.NOT_LOGICO,          r'!'),

        (TokenType.ASIGNACION,          r'='),
        (TokenType.MENOR_QUE,           r'<'),
        (TokenType.MAYOR_QUE,           r'>'),
        (TokenType.SUMA,                r'\+'),
        (TokenType.RESTA,               r'-'),
        (TokenType.MULTIPLICACION,      r'\*'),
        (TokenType.DIVISION,            r'/'),
        (TokenType.MODULO,              r'%'),

        (TokenType.PARENTESIS_IZQ,      r'\('),
        (TokenType.PARENTESIS_DER,      r'\)'),
        (TokenType.PUNTO_Y_COMA,        r';'),
        (TokenType.COMA,                r','),

        (TokenType.IDENTIFICADOR,       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ]

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []
        self.line_starts = [0]
        self._compute_line_starts()

    def _compute_line_starts(self):
        for idx, char in enumerate(self.code):
            if char == '\n':
                self.line_starts.append(idx + 1)

    def _get_line_col(self, pos: int) -> Tuple[int, int]:
        low, high = 0, len(self.line_starts) - 1
        line_idx = 0
        while low <= high:
            mid = (low + high) // 2
            if self.line_starts[mid] <= pos:
                line_idx = mid
                low = mid + 1
            else:
                high = mid - 1
        line_num = line_idx + 1
        col_num = pos - self.line_starts[line_idx] + 1
        return line_num, col_num

    def tokenize(self) -> List[Token]:
        compiled = [(tt, re.compile(pat)) for tt, pat in self.TOKEN_SPECS]
        pos = 0
        n = len(self.code)

        while pos < n:
            if self.code[pos].isspace():
                pos += 1
                continue

            matched = False
            for token_type, regex in compiled:
                m = regex.match(self.code, pos)
                if m:
                    matched = True
                    text = m.group(0)
                    line, col = self._get_line_col(pos)
                    if token_type not in (TokenType.COMENTARIO_LINEA, TokenType.COMENTARIO_BLOQUE):
                        self.tokens.append(Token(token_type, text, line, col))
                    pos = m.end()
                    break

            if not matched:
                pos += 1

        f_line, f_col = self._get_line_col(n)
        self.tokens.append(Token(TokenType.EOF, "", f_line, f_col))
        return self.tokens
