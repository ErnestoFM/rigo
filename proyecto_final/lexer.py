"""
================================================================================
PROYECTO FINAL: COMPILADOR INTEGRAL DE LENGUAJE C
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
from typing import List, Optional
from token_type import TokenType, Token
from error_handler import CompilerErrorHandler


class Lexer:
    """
    Analizador léxico de alta fidelidad para el compilador de C.
    Soporta palabras clave estándar, identificadores Unicode (español),
    literales numéricos (enteros, flotantes), cadenas y operadores.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    KEYWORDS = {
        "if": TokenType.KEYWORD_IF,
        "else": TokenType.KEYWORD_ELSE,
        "switch": TokenType.KEYWORD_SWITCH,
        "case": TokenType.KEYWORD_CASE,
        "default": TokenType.KEYWORD_DEFAULT,
        "break": TokenType.KEYWORD_BREAK,
        "while": TokenType.KEYWORD_WHILE,
        "for": TokenType.KEYWORD_FOR,
        "do": TokenType.KEYWORD_DO,
        "class": TokenType.KEYWORD_CLASS,
        "new": TokenType.KEYWORD_NEW,
        "return": TokenType.KEYWORD_RETURN,
        "int": TokenType.KEYWORD_INT,
        "float": TokenType.KEYWORD_FLOAT,
        "string": TokenType.KEYWORD_STRING,
        "String": TokenType.KEYWORD_STRING,
        "void": TokenType.KEYWORD_VOID,
        "bool": TokenType.KEYWORD_BOOL,
        "boolean": TokenType.KEYWORD_BOOL,
        "print": TokenType.KEYWORD_PRINT,
        "printf": TokenType.KEYWORD_PRINT,
        "true": TokenType.BOOLEANO,
        "false": TokenType.BOOLEANO,
    }

    def __init__(self, source_code: str, error_handler: Optional[CompilerErrorHandler] = None):
        self.source_code = source_code
        self.error_handler = error_handler or CompilerErrorHandler()
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        lines = self.source_code.splitlines(keepends=True)
        in_block_comment = False

        for line_idx, line_text in enumerate(lines, start=1):
            col = 1
            length = len(line_text)

            while col <= length:
                idx = col - 1
                char = line_text[idx]

                # Comentarios multilínea
                if in_block_comment:
                    end_idx = line_text.find("*/", idx)
                    if end_idx != -1:
                        in_block_comment = False
                        col = end_idx + 3
                    else:
                        break
                    continue

                # Espacios en blanco
                if char in " \t\r\n":
                    col += 1
                    continue

                # Comentario de una línea
                if line_text[idx:idx+2] == "//":
                    break

                # Inicio de comentario multilínea
                if line_text[idx:idx+2] == "/*":
                    in_block_comment = True
                    col += 2
                    continue

                # Cadenas literales: "texto"
                if char == '"':
                    m = re.match(r'"([^"\\]|\\.)*"', line_text[idx:])
                    if m:
                        val = m.group(0)
                        self.tokens.append(Token(TokenType.CADENA_TEXTO, val, line_idx, col, literal=val[1:-1]))
                        col += len(val)
                    else:
                        self.error_handler.report_lexical(
                            "Cadena literal no cerrada correctamente.",
                            line_idx, col,
                            suggestion="Agregue comillas dobles de cierre '\"'.",
                            offending=line_text[idx:].strip()
                        )
                        break
                    continue

                # Operadores de dos caracteres
                two_char = line_text[idx:idx+2]
                two_char_map = {
                    "++": TokenType.OP_INCREMENTO,
                    "--": TokenType.OP_DECREMENTO,
                    "==": TokenType.OP_IGUAL,
                    "!=": TokenType.OP_DIFERENTE,
                    "<=": TokenType.OP_MENOR_IGUAL,
                    ">=": TokenType.OP_MAYOR_IGUAL,
                    "&&": TokenType.OP_AND,
                    "||": TokenType.OP_OR,
                }
                if two_char in two_char_map:
                    self.tokens.append(Token(two_char_map[two_char], two_char, line_idx, col))
                    col += 2
                    continue

                # Números (flotantes o enteros)
                if char.isdigit():
                    m_float = re.match(r'^\d+\.\d+', line_text[idx:])
                    if m_float:
                        val = m_float.group(0)
                        self.tokens.append(Token(TokenType.NUMERO_FLOTANTE, val, line_idx, col, literal=float(val)))
                        col += len(val)
                        continue
                    m_int = re.match(r'^\d+', line_text[idx:])
                    if m_int:
                        val = m_int.group(0)
                        self.tokens.append(Token(TokenType.NUMERO_ENTERO, val, line_idx, col, literal=int(val)))
                        col += len(val)
                        continue

                # Identificadores o palabras clave (soporte de español: ñ, acentos)
                if char.isalpha() or char == '_':
                    m_id = re.match(r'^[a-zA-Z_áéíóúÁÉÍÓÚñÑüÜ][a-zA-Z0-9_áéíóúÁÉÍÓÚñÑüÜ]*', line_text[idx:])
                    if m_id:
                        val = m_id.group(0)
                        if val in self.KEYWORDS:
                            tok_type = self.KEYWORDS[val]
                            lit = True if val == "true" else (False if val == "false" else None)
                            self.tokens.append(Token(tok_type, val, line_idx, col, literal=lit))
                        else:
                            self.tokens.append(Token(TokenType.IDENTIFICADOR, val, line_idx, col))
                        col += len(val)
                        continue

                # Operadores y delimitadores de un solo carácter
                one_char_map = {
                    '=': TokenType.OP_ASIGNACION,
                    '+': TokenType.OP_SUMA,
                    '-': TokenType.OP_RESTA,
                    '*': TokenType.OP_MULTIPLICACION,
                    '/': TokenType.OP_DIVISION,
                    '%': TokenType.OP_MODULO,
                    '<': TokenType.OP_MENOR,
                    '>': TokenType.OP_MAYOR,
                    '!': TokenType.OP_NOT,
                    '(': TokenType.PARENTESIS_IZQ,
                    ')': TokenType.PARENTESIS_DER,
                    '{': TokenType.LLAVE_IZQ,
                    '}': TokenType.LLAVE_DER,
                    '[': TokenType.CORCHETE_IZQ,
                    ']': TokenType.CORCHETE_DER,
                    ';': TokenType.PUNTO_Y_COMA,
                    ',': TokenType.COMA,
                    ':': TokenType.DOS_PUNTOS,
                    '.': TokenType.PUNTO,
                }
                if char in one_char_map:
                    self.tokens.append(Token(one_char_map[char], char, line_idx, col))
                    col += 1
                    continue

                # Carácter no reconocido
                self.error_handler.report_lexical(
                    f"Carácter no reconocido: '{char}'.",
                    line_idx, col,
                    suggestion="Elimine el carácter inválido.",
                    offending=char
                )
                col += 1

        self.tokens.append(Token(TokenType.EOF, "", len(lines) + 1, 1))
        return self.tokens
