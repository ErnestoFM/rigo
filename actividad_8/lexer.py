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

import re
from typing import List, Tuple
from token_type import TokenType, Token


class Lexer:
    """
    Analizador Léxico especializado para la validación de expresiones
    aritméticas, lógicas, relacionales y conversiones de tipo en C.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    TOKEN_SPECS: List[Tuple[TokenType, str]] = [
        # Comentarios y directivas
        (TokenType.COMENTARIO_BLOQUE,       r'/\*[\s\S]*?\*/'),
        (TokenType.COMENTARIO_LINEA,        r'//.*'),
        (TokenType.DIRECTIVA_PREPROCESADOR, r'#\s*(include|define|undef|ifdef|ifndef|endif)\b[^\n]*'),

        # Conversión de tipo
        (TokenType.KEYWORD_STATIC_CAST,     r'\bstatic_cast\b'),

        # Palabras clave de tipos
        (TokenType.KEYWORD_INT,             r'\bint\b'),
        (TokenType.KEYWORD_FLOAT,           r'\bfloat\b'),
        (TokenType.KEYWORD_DOUBLE,          r'\bdouble\b'),
        (TokenType.KEYWORD_CHAR,            r'\bchar\b'),
        (TokenType.KEYWORD_BOOL,            r'\bbool\b'),
        (TokenType.KEYWORD_STRING,          r'\bstring\b'),
        (TokenType.KEYWORD_VOID,            r'\bvoid\b'),

        # Literales booleanos
        (TokenType.KEYWORD_TRUE,            r'\btrue\b'),
        (TokenType.KEYWORD_FALSE,           r'\bfalse\b'),

        # Palabras clave de control
        (TokenType.KEYWORD_IF,              r'\bif\b'),
        (TokenType.KEYWORD_ELSE,            r'\belse\b'),
        (TokenType.KEYWORD_WHILE,           r'\bwhile\b'),
        (TokenType.KEYWORD_FOR,             r'\bfor\b'),
        (TokenType.KEYWORD_RETURN,          r'\breturn\b'),

        # Literales numéricos
        (TokenType.NUMERO_FLOTANTE,         r'\b\d+\.\d+([eE][+-]?\d+)?[fFlL]?\b'),
        (TokenType.NUMERO_ENTERO,           r'\b(0[xX][0-9a-fA-F]+|\d+)\b'),

        # Literales de texto y carácter
        (TokenType.LITERAL_CADENA,          r'"([^"\\]|\\.)*"'),
        (TokenType.LITERAL_CARACTER,        r"'([^'\\]|\\.)'"),

        # Operadores compuestos relacionales y lógicos
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

    def _compute_line_starts(self):
        for idx, char in enumerate(self.code):
            if char == '\n':
                self.line_starts.append(idx + 1)

    def _get_line_col(self, pos: int) -> Tuple[int, int]:
        low = 0
        high = len(self.line_starts) - 1
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

                    if token_type not in (
                        TokenType.COMENTARIO_LINEA,
                        TokenType.COMENTARIO_BLOQUE,
                        TokenType.DIRECTIVA_PREPROCESADOR
                    ):
                        self.tokens.append(Token(token_type, text, line, col))

                    pos = m.end()
                    break

            if not matched:
                pos += 1

        f_line, f_col = self._get_line_col(n)
        self.tokens.append(Token(TokenType.EOF, "", f_line, f_col))
        return self.tokens
