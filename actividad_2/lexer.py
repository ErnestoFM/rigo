"""
================================================================================
ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
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
from typing import List, Tuple, Optional
from token_type import TokenType, Token
from error_handler import ErrorHandler, LexicalErrorCategory


class LexerC:
    """
    Analizador Léxico (Scanner) para Lenguaje C con detección, aislamiento
    y reporte pedagógico de errores léxicos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    # 1. Reglas de detección prioritarias para patrones de ERRORES LÉXICOS ESPECÍFICOS
    ERROR_SPECS: List[Tuple[TokenType, LexicalErrorCategory, str, str, str]] = [
        # Identificador mal formado: empieza con dígitos y continúa con letras/guiones
        (
            TokenType.ERROR_IDENTIFICADOR_MAL_FORMADO,
            LexicalErrorCategory.IDENTIFICADOR_MAL_FORMADO,
            r'\b\d+[a-zA-Z_][a-zA-Z0-9_]*\b',
            "Un identificador no puede comenzar con un número en C.",
            "Renombre el identificador iniciando con una letra o guion bajo '_', ej. 'var_{lexeme}'."
        ),

        # Número flotante con múltiples puntos decimales (ej. 3.14.15)
        (
            TokenType.ERROR_NUMERO_INCORRECTO,
            LexicalErrorCategory.NUMERO_INCORRECTO,
            r'\b\d+\.\d+(\.\d+)+\b',
            "Formato de punto flotante inválido: contiene múltiples puntos decimales.",
            "Corrija la constante numérica conservando un único punto decimal."
        ),

        # Hexadecimal con dígitos inválidos fuera de A-F (ej. 0x12G4, 0x55ZZ)
        (
            TokenType.ERROR_NUMERO_INCORRECTO,
            LexicalErrorCategory.NUMERO_INCORRECTO,
            r'\b0[xX][0-9a-fA-F]*[g-zG-Z_]+[0-9a-zA-Z_]*\b',
            "Literal hexadecimal inválido: contiene caracteres fuera del rango [0-9, A-F].",
            "Utilice únicamente dígitos del 0 al 9 y letras de la A a la F en constantes 0x."
        ),

        # Exponente de coma flotante incompleto (ej. 1.5e+ sin dígitos siguientes)
        (
            TokenType.ERROR_NUMERO_INCORRECTO,
            LexicalErrorCategory.NUMERO_INCORRECTO,
            r'\b\d+(\.\d+)?[eE][+-]?(?![0-9])',
            "Literal numérico en notación científica incompleto.",
            "Agregue el valor entero del exponente después de 'e' o 'e+', ej. '1.5e+3'."
        ),
    ]

    # 2. Reglas Estándar para TOKENS VÁLIDOS del Lenguaje C
    VALID_SPECS: List[Tuple[TokenType, str]] = [
        # Comentarios
        (TokenType.COMENTARIO_BLOQUE,   r'/\*[\s\S]*?\*/'),
        (TokenType.COMENTARIO_LINEA,    r'//.*'),

        # Directivas de preprocesador de C (#include <stdio.h>, #define, etc.)
        (TokenType.DIRECTIVA_PREPROCESADOR, r'#\s*(include|define|undef|ifdef|ifndef|if|elif|else|endif|pragma|error)\b[^\n]*'),

        # Palabras clave estándar de C
        (
            TokenType.PALABRA_CLAVE,
            r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|'
            r'float|for|goto|if|inline|int|long|register|restrict|return|short|signed|'
            r'sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Bool|_Complex|_Imaginary|bool)\b'
        ),

        # Literales numéricos válidos
        (TokenType.LITERAL_FLOTANTE,    r'\b\d+\.\d+([eE][+-]?\d+)?[fFlL]?\b|\b\d+[eE][+-]?\d+[fFlL]?\b'),
        (TokenType.LITERAL_ENTERO,      r'\b(0[xX][0-9a-fA-F]+|0[0-7]+|\d+)[uUlL]*\b'),

        # Literales de texto y carácter válidos
        (TokenType.LITERAL_CADENA,      r'"([^"\\]|\\.)*"'),
        (TokenType.LITERAL_CARACTER,    r"'([^'\\]|\\.)'"),

        # Identificadores válidos
        (TokenType.IDENTIFICADOR,       r'[a-zA-Z_][a-zA-Z0-9_]*'),

        # Operadores
        (TokenType.OPERADOR_RELACIONAL, r'==|!=|<=|>=|<|>'),
        (TokenType.OPERADOR_LOGICO,     r'&&|\|\||!'),
        (TokenType.OPERADOR_ASIGNACION, r'\+=|-=|\*=|/=|%=|<<=|>>=|&=|\^=|\|=|='),
        (TokenType.OPERADOR_ARITMETICO, r'\+\+|--|\+|\-|\*|/|%'),
        (TokenType.OPERADOR_BIT,        r'->|<<|>>|&|\||\^|~'),

        # Delimitadores
        (TokenType.DELIMITADOR,         r'\(|\)|\{|\}|\[|\]|\;|\,|\.|\:|\?'),
    ]

    def __init__(self, code: str, error_handler: Optional[ErrorHandler] = None):
        self.code = code
        self.error_handler = error_handler or ErrorHandler()
        self.tokens: List[Token] = []
        self.line_start_positions = [0]
        self._compute_line_starts()

        # Precompilar regexes
        self.compiled_errors = [(t, cat, re.compile(p), msg, sug) for t, cat, p, msg, sug in self.ERROR_SPECS]
        self.compiled_valids = [(t, re.compile(p)) for t, p in self.VALID_SPECS]

    def _compute_line_starts(self):
        """Calcula los índices de inicio de cada línea para determinar columnas exactas."""
        self.line_start_positions = [0]
        for idx, char in enumerate(self.code):
            if char == '\n':
                self.line_start_positions.append(idx + 1)

    def _get_line_and_column(self, pos: int) -> Tuple[int, int]:
        """Calcula el número de línea (1-indexed) y columna (1-indexed) a partir del offset."""
        line = 1
        for i, start_pos in enumerate(self.line_start_positions):
            if pos >= start_pos:
                line = i + 1
            else:
                break
        col = pos - self.line_start_positions[line - 1] + 1
        return line, col

    def tokenize(self) -> List[Token]:
        """
        Tokeniza el código fuente completo, identificando tokens válidos y
        capturando de forma exhaustiva las 4 categorías de errores léxicos.
        """
        self.tokens.clear()
        self.error_handler.reset()
        pos = 0
        code_len = len(self.code)

        while pos < code_len:
            # 1. Ignorar espacios en blanco
            if self.code[pos].isspace():
                pos += 1
                continue

            current_line, current_col = self._get_line_and_column(pos)

            # 2. Verificar Cadenas Mal Formadas
            if self.code[pos] == '"':
                match_valid_str = re.compile(r'"([^"\\]|\\.)*"').match(self.code, pos)
                if match_valid_str:
                    lexeme = match_valid_str.group(0)
                    self.tokens.append(Token(TokenType.LITERAL_CADENA, lexeme, current_line, current_col))
                    pos = match_valid_str.end()
                    continue
                else:
                    eol_pos = self.code.find('\n', pos)
                    if eol_pos == -1:
                        eol_pos = code_len
                    bad_lexeme = self.code[pos:eol_pos]
                    err_msg = "Cadena de texto no delimitada: falta la comilla de cierre '\"' antes del fin de línea."
                    sug = "Agregue la comilla de cierre '\"' al final de la literal de cadena."

                    self.error_handler.report(
                        current_line, current_col, LexicalErrorCategory.CADENA_MAL_FORMADA, bad_lexeme, err_msg, sug
                    )
                    self.tokens.append(Token(
                        TokenType.ERROR_CADENA_MAL_FORMADA, bad_lexeme, current_line, current_col, is_error=True, error_msg=err_msg
                    ))
                    pos = eol_pos
                    continue

            # 3. Comprobar patrones prioritarios de ERRORES LÉXICOS
            error_matched = False
            for token_type, cat, regex, err_msg, sug in self.compiled_errors:
                match = regex.match(self.code, pos)
                if match:
                    lexeme = match.group(0)
                    sug_formatted = sug.replace("{lexeme}", lexeme)
                    self.error_handler.report(current_line, current_col, cat, lexeme, err_msg, sug_formatted)
                    self.tokens.append(Token(token_type, lexeme, current_line, current_col, is_error=True, error_msg=err_msg))
                    pos = match.end()
                    error_matched = True
                    break

            if error_matched:
                continue

            # 4. Comprobar TOKENS VÁLIDOS del Lenguaje C
            valid_matched = False
            for token_type, regex in self.compiled_valids:
                match = regex.match(self.code, pos)
                if match:
                    lexeme = match.group(0)
                    self.tokens.append(Token(token_type, lexeme, current_line, current_col))
                    pos = match.end()
                    valid_matched = True
                    break

            if valid_matched:
                continue

            # 5. Capturar CARÁCTER NO RECONOCIDO (Fuera del alfabeto de C)
            bad_char = self.code[pos]
            err_msg = f"El carácter '{bad_char}' no pertenece al alfabeto léxico válido del Lenguaje C."
            sug = f"Elimine el símbolo '{bad_char}' o reemplácelo por un operador o identificador válido."

            self.error_handler.report(
                current_line, current_col, LexicalErrorCategory.CARACTER_NO_RECONOCIDO, bad_char, err_msg, sug
            )
            self.tokens.append(Token(
                TokenType.ERROR_CARACTER_NO_RECONOCIDO, bad_char, current_line, current_col, is_error=True, error_msg=err_msg
            ))
            pos += 1

        # Agregar token de fin de archivo
        eof_line, eof_col = self._get_line_and_column(code_len)
        self.tokens.append(Token(TokenType.FIN_DE_ENTRADA, "EOF", eof_line, eof_col))
        return self.tokens
