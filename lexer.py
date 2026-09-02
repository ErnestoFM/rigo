"""
================================================================================
ACTIVIDAD 2: MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
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
from error_handler import ErrorHandler, LexicalErrorCategory

class LexerC:
    """
    Analizador léxico avanzado para C con manejo integral de errores léxicos.
    """
    
    # 1. Reglas de detección prioritarias para patrones de ERRORES LÉXICOS ESPECÍFICOS
    ERROR_RULES = [
        # Identificador mal formado: empieza con dígitos y continúa con letras/guiones
        (TokenType.ERROR_IDENTIFICADOR_MAL_FORMADO, LexicalErrorCategory.IDENTIFICADOR_MAL_FORMADO,
         r'\b\d+[a-zA-Z_][a-zA-Z0-9_]*\b',
         "Un identificador no puede comenzar con un número en C.",
         "Renombre la variable iniciando con una letra o guion bajo '_', ej. 'var_{lexeme}'."),

        # Número flotante con múltiples puntos flotantes (ej. 3.14.15)
        (TokenType.ERROR_NUMERO_INCORRECTO, LexicalErrorCategory.NUMERO_INCORRECTO,
         r'\b\d+\.\d+(\.\d+)+\b',
         "Formato de punto flotante inválido: contiene múltiples puntos decimales.",
         "Corrija la constante numérica conservando un único punto decimal."),

        # Hexadecimal con caracteres fuera de A-F / 0-9 (ej. 0x12G4)
        (TokenType.ERROR_NUMERO_INCORRECTO, LexicalErrorCategory.NUMERO_INCORRECTO,
         r'\b0[xX][0-9a-fA-F]*[g-zG-Z_]+[0-9a-fA-F]*\b',
         "Literal hexadecimal inválido: contiene dígitos no hexadecimales.",
         "Utilice únicamente dígitos del 0 al 9 y letras de la A a la F en constantes 0x."),

        # Exponente de coma flotante incompleto (ej. 1.2e+ sin dígitos)
        (TokenType.ERROR_NUMERO_INCORRECTO, LexicalErrorCategory.NUMERO_INCORRECTO,
         r'\b\d+(\.\d+)?[eE][+-]?(?![0-9])',
         "Literal numérico en notación científica incompleto.",
         "Agregue el valor entero del exponente después de 'e' o 'e+', ej. '1.2e+3'."),
    ]

    # 2. Reglas Estándar para TOKENS VÁLIDOS del Lenguaje C
    VALID_RULES = [
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
        self.error_handler = ErrorHandler()

    def tokenize(self) -> List[Token]:
        self.tokens = []
        self.error_handler.clear()
        
        pos = 0
        line = 1
        col = 1
        length = len(self.code)
        lines_code = self.code.splitlines()

        while pos < length:
            char = self.code[pos]
            
            # Espacios y saltos de línea
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

            snippet = lines_code[line - 1] if line <= len(lines_code) else ""
            match_found = False

            # Paso A: Comprobar patrones de Errores Estructurados Especificados
            for token_type, cat, pattern, desc, sug in self.ERROR_RULES:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    lexeme = match.group(0)
                    sug_formatted = sug.replace("{lexeme}", lexeme)
                    
                    token = Token(token_type, lexeme, line, col, desc)
                    self.tokens.append(token)
                    self.error_handler.add_error(cat, lexeme, line, col, desc, sug_formatted, snippet)
                    
                    col += len(lexeme)
                    pos = match.end()
                    match_found = True
                    break

            if match_found:
                continue

            # Paso B: Comprobar reglas para Tokens Válidos
            for token_type, pattern in self.VALID_RULES:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    lexeme = match.group(0)
                    token = Token(token_type, lexeme, line, col)
                    self.tokens.append(token)

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

            if match_found:
                continue

            # Paso C: Manejo especial para Cadenas Mal Formadas / Sin Cerrar
            if self.code[pos] == '"':
                # Buscar fin de línea o fin de archivo
                end_line = self.code.find('\n', pos)
                if end_line == -1:
                    end_line = length
                
                bad_string = self.code[pos:end_line]
                desc = "Cadena de texto no delimitada correctamente (falta comilla de cierre '\"')."
                sug = "Agregue la comilla doble de cierre '\"' al final de la cadena de texto."
                
                token = Token(TokenType.ERROR_CADENA_MAL_FORMADA, bad_string, line, col, desc)
                self.tokens.append(token)
                self.error_handler.add_error(
                    LexicalErrorCategory.CADENA_MAL_FORMADA, bad_string, line, col, desc, sug, snippet
                )
                
                pos = end_line
                col += len(bad_string)
                continue

            # Paso D: Caracteres No Reconocidos
            invalid_char = self.code[pos]
            desc = f"El carácter '{invalid_char}' no pertenece al alfabeto del lenguaje C."
            sug = f"Elimine o reemplace el símbolo '{invalid_char}' por un operador o identificador válido."
            
            token = Token(TokenType.ERROR_CARACTER_NO_RECONOCIDO, invalid_char, line, col, desc)
            self.tokens.append(token)
            self.error_handler.add_error(
                LexicalErrorCategory.CARACTER_NO_RECONOCIDO, invalid_char, line, col, desc, sug, snippet
            )
            
            pos += 1
            col += 1

        return self.tokens
