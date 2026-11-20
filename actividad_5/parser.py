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

from typing import List, Optional
from token_type import TokenType, Token
from error_handler import SyntaxErrorHandler, SyntaxErrorCategory
from ast_nodes import (
    ASTNode, ProgramNode, BlockNode, IfNode, WhileNode, ForNode,
    VariableDeclarationNode, AssignmentNode, BinaryOpNode, UnaryOpNode,
    IdentifierNode, LiteralNode, FunctionNode, CallNode, ReturnNode, ErrorNode
)


class Parser:
    """
    Analizador Sintáctico Descendente Recursivo para Estructuras de Control en C.
    Valida condicionales (if/else), bucles (while, for), bloques entre llaves,
    paréntesis balanceados y componentes de control, con recuperación de errores
    (Panic Mode) y diagnósticos detallados según la rúbrica.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    TYPE_TOKENS = {
        TokenType.KEYWORD_INT,
        TokenType.KEYWORD_FLOAT,
        TokenType.KEYWORD_DOUBLE,
        TokenType.KEYWORD_CHAR,
        TokenType.KEYWORD_VOID
    }

    SYNC_TOKENS = {
        TokenType.KEYWORD_IF,
        TokenType.KEYWORD_WHILE,
        TokenType.KEYWORD_FOR,
        TokenType.KEYWORD_RETURN,
        TokenType.LLAVE_DER,
        TokenType.PUNTO_Y_COMA
    }

    def __init__(self, tokens: List[Token], error_handler: Optional[SyntaxErrorHandler] = None):
        self.tokens = tokens
        self.pos = 0
        self.error_handler = error_handler or SyntaxErrorHandler()

    @property
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1] if self.tokens else Token(TokenType.EOF, "", 1, 1)

    def peek(self, offset: int = 1) -> Token:
        target = self.pos + offset
        if target < len(self.tokens):
            return self.tokens[target]
        return self.tokens[-1] if self.tokens else Token(TokenType.EOF, "", 1, 1)

    def is_at_end(self) -> bool:
        return self.current.type == TokenType.EOF

    def advance(self) -> Token:
        tok = self.current
        if not self.is_at_end():
            self.pos += 1
        return tok

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return token_type == TokenType.EOF
        return self.current.type == token_type

    def match(self, *token_types: TokenType) -> bool:
        for tt in token_types:
            if self.check(tt):
                self.advance()
                return True
        return False

    def report_error(
        self,
        category: SyntaxErrorCategory,
        message: str,
        suggestion: str,
        structure_name: str,
        token: Optional[Token] = None
    ):
        t = token or self.current
        self.error_handler.report(
            line=t.line,
            column=t.column,
            category=category,
            message=message,
            suggestion=suggestion,
            structure_name=structure_name
        )

    def synchronize(self):
        """Recuperación ante errores sintácticos (Panic Mode) avanzando hasta un delimitador clave."""
        self.advance()
        while not self.is_at_end():
            if self.tokens[self.pos - 1].type in (TokenType.PUNTO_Y_COMA, TokenType.LLAVE_DER):
                return
            if self.current.type in self.SYNC_TOKENS or self.current.type in self.TYPE_TOKENS:
                return
            self.advance()

    # --------------------------------------------------------------------------
    # Reglas Gramaticales
    # --------------------------------------------------------------------------

    def parse(self) -> ProgramNode:
        """Punto de entrada principal: parsea una secuencia de sentencias / estructuras."""
        statements: List[ASTNode] = []
        start_line = self.current.line
        start_col = self.current.column

        while not self.is_at_end():
            stmt = self._top_level_declaration_or_statement()
            if stmt:
                statements.append(stmt)

        return ProgramNode(statements, line=start_line, column=start_col)

    def _top_level_declaration_or_statement(self) -> Optional[ASTNode]:
        """Discrimina entre definición de función o sentencia general / estructura de control."""
        # Detectar definición de función: tipo ident ( ... ) { ... }
        if self.current.type in self.TYPE_TOKENS:
            if self.peek(1).type == TokenType.IDENTIFICADOR and self.peek(2).type == TokenType.PARENTESIS_IZQ:
                # Comprobar si después de los paréntesis hay una llave '{' (función) o ';' (declaración/prototipo)
                lookahead = 2
                paren_depth = 0
                while self.pos + lookahead < len(self.tokens):
                    tt = self.tokens[self.pos + lookahead].type
                    if tt == TokenType.PARENTESIS_IZQ:
                        paren_depth += 1
                    elif tt == TokenType.PARENTESIS_DER:
                        paren_depth -= 1
                        if paren_depth == 0:
                            # Siguiente token tras ')'
                            next_tok = self.peek(lookahead + 1)
                            if next_tok.type == TokenType.LLAVE_IZQ:
                                return self._function_definition()
                            break
                    elif tt == TokenType.EOF:
                        break
                    lookahead += 1

        return self._statement()

    def _function_definition(self) -> ASTNode:
        """Parsea una función: int main(...) { ... }"""
        type_tok = self.advance()
        name_tok = self.advance()
        self.advance()  # '('

        params: List[str] = []
        if not self.check(TokenType.PARENTESIS_DER):
            while True:
                if self.current.type in self.TYPE_TOKENS:
                    ptype = self.advance().value
                    if self.check(TokenType.IDENTIFICADOR):
                        pname = self.advance().value
                        params.append(f"{ptype} {pname}")
                    else:
                        params.append(ptype)
                elif self.check(TokenType.IDENTIFICADOR):
                    params.append(self.advance().value)
                else:
                    break

                if not self.match(TokenType.COMA):
                    break

        if not self.match(TokenType.PARENTESIS_DER):
            self.report_error(
                category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                message=f"Falta paréntesis de cierre ')' en encabezado de función '{name_tok.value}'.",
                suggestion="Cierre los parámetros con ')'.",
                structure_name=f"funcion_{name_tok.value}"
            )

        body = self._block(structure_name=f"funcion_{name_tok.value}")
        return FunctionNode(
            return_type=type_tok.value,
            name=name_tok.value,
            params=params,
            body=body,
            line=type_tok.line,
            column=type_tok.column
        )

    def _statement(self) -> Optional[ASTNode]:
        """
        sentencia -> sentencia_if | sentencia_while | sentencia_for | declaracion | asignacion | retorno | bloque
        """
        tok = self.current

        if tok.type == TokenType.KEYWORD_IF:
            return self._if_statement()

        if tok.type == TokenType.KEYWORD_WHILE:
            return self._while_statement()

        if tok.type == TokenType.KEYWORD_FOR:
            return self._for_statement()

        if tok.type == TokenType.KEYWORD_RETURN:
            return self._return_statement()

        if tok.type == TokenType.LLAVE_IZQ:
            return self._block(structure_name="bloque_anonimo")

        if tok.type in self.TYPE_TOKENS:
            return self._declaration()

        if tok.type == TokenType.PUNTO_Y_COMA:
            # Sentencia vacía
            self.advance()
            return None

        # Expresión o Asignación
        return self._assignment_or_expression_statement()

    # --------------------------------------------------------------------------
    # Estructura IF / ELSE
    # --------------------------------------------------------------------------

    def _if_statement(self) -> IfNode:
        """
        sentencia_if -> 'if' '(' expresion ')' '{' bloque '}' ( 'else' '{' bloque '}' )?
        """
        if_tok = self.advance()  # consume 'if'
        line, col = if_tok.line, if_tok.column

        # 1. Paréntesis de apertura '('
        if not self.match(TokenType.PARENTESIS_IZQ):
            self.report_error(
                category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                message=f"Paréntesis de apertura '(' faltante en estructura 'if' en la línea {line}, columna {col}.",
                suggestion="Agregue '(' inmediatamente después de la palabra clave 'if'. Ejemplo: if (condicion) { ... }",
                structure_name="if",
                token=self.current
            )
            cond = ErrorNode("Falta '(' en if", line, col)
        else:
            # 2. Expresión condicional
            if self.check(TokenType.PARENTESIS_DER):
                self.report_error(
                    category=SyntaxErrorCategory.CONDICION_INVALIDA,
                    message=f"Error: Condición inválida o vacía en la estructura 'if' en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="Especifique una expresión relacional o booleana dentro de los paréntesis. Ejemplo: if (x > 0)",
                    structure_name="if"
                )
                cond = ErrorNode("Condición vacía en if", line, col)
            else:
                cond = self._expression()

            # 3. Paréntesis de cierre ')'
            if not self.match(TokenType.PARENTESIS_DER):
                self.report_error(
                    category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                    message=f"Paréntesis de cierre ')' faltante en estructura 'if' en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="Cierre la expresión condicional con ')'. Ejemplo: if (x > 0) { ... }",
                    structure_name="if",
                    token=self.current
                )

        # 4. Bloque Then obligatorio con llaves '{' ... '}'
        if not self.check(TokenType.LLAVE_IZQ):
            self.report_error(
                category=SyntaxErrorCategory.BLOQUE_SIN_LLAVES,
                message=f"Error: Bloque de sentencias faltante o sin llaves '{{' en la estructura 'if' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="La gramática exige que las sentencias del 'if' estén delimitadas por llaves obligatorias. Ejemplo: if (x > 0) { ... }",
                structure_name="if"
            )
            # Recuperar parseando una sola sentencia si es posible para no colapsar el árbol
            if not self.is_at_end() and self.current.type not in (TokenType.KEYWORD_ELSE, TokenType.LLAVE_DER):
                single_stmt = self._statement()
                then_block = BlockNode([single_stmt] if single_stmt else [], line, col)
            else:
                then_block = BlockNode([], line, col)
        else:
            then_block = self._block(structure_name="if")

        # 5. Cláusula Else opcional
        else_block: Optional[BlockNode] = None
        if self.match(TokenType.KEYWORD_ELSE):
            else_tok = self.tokens[self.pos - 1]
            if self.check(TokenType.KEYWORD_IF):
                # Soporte para else if encapsulado
                nested_if = self._if_statement()
                else_block = BlockNode([nested_if], line=nested_if.line, column=nested_if.column)
            elif not self.check(TokenType.LLAVE_IZQ):
                self.report_error(
                    category=SyntaxErrorCategory.BLOQUE_SIN_LLAVES,
                    message=f"Error: Bloque de sentencias faltante o sin llaves '{{' en la estructura 'else' en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="La cláusula 'else' debe tener un bloque delimitado por llaves obligatorias '{ ... }'.",
                    structure_name="else"
                )
                if not self.is_at_end() and self.current.type != TokenType.LLAVE_DER:
                    single_stmt = self._statement()
                    else_block = BlockNode([single_stmt] if single_stmt else [], else_tok.line, else_tok.column)
                else:
                    else_block = BlockNode([], else_tok.line, else_tok.column)
            else:
                else_block = self._block(structure_name="else")

        return IfNode(condition=cond, then_block=then_block, else_block=else_block, line=line, column=col)

    # --------------------------------------------------------------------------
    # Estructura WHILE
    # --------------------------------------------------------------------------

    def _while_statement(self) -> WhileNode:
        """
        sentencia_while -> 'while' '(' expresion ')' '{' bloque '}'
        """
        while_tok = self.advance()  # consume 'while'
        line, col = while_tok.line, while_tok.column

        # 1. Paréntesis '('
        if not self.match(TokenType.PARENTESIS_IZQ):
            self.report_error(
                category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                message=f"Paréntesis de apertura '(' faltante en estructura 'while' en la línea {line}, columna {col}.",
                suggestion="Agregue '(' inmediatamente después de 'while'. Ejemplo: while (y < 10) { ... }",
                structure_name="while",
                token=self.current
            )
            cond = ErrorNode("Falta '(' en while", line, col)
        else:
            # 2. Expresión condicional
            if self.check(TokenType.PARENTESIS_DER):
                self.report_error(
                    category=SyntaxErrorCategory.CONDICION_INVALIDA,
                    message=f"Error: Condición inválida o vacía en la estructura 'while' en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="Especifique una condición dentro de los paréntesis. Ejemplo: while (contador < 100)",
                    structure_name="while"
                )
                cond = ErrorNode("Condición vacía en while", line, col)
            else:
                cond = self._expression()

            # 3. Paréntesis ')'
            if not self.match(TokenType.PARENTESIS_DER):
                self.report_error(
                    category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                    message=f"Paréntesis de cierre ')' faltante en estructura 'while' en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="Cierre la condición del bucle con ')'. Ejemplo: while (y < 10) { ... }",
                    structure_name="while",
                    token=self.current
                )

        # 4. Bloque con llaves '{' ... '}'
        if not self.check(TokenType.LLAVE_IZQ):
            self.report_error(
                category=SyntaxErrorCategory.BLOQUE_SIN_LLAVES,
                message=f"Error: Bloque de sentencias faltante o sin llaves '{{' en la estructura 'while' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Encierre el cuerpo del bucle 'while' entre llaves '{ ... }'.",
                structure_name="while"
            )
            if not self.is_at_end() and self.current.type != TokenType.LLAVE_DER:
                single_stmt = self._statement()
                body = BlockNode([single_stmt] if single_stmt else [], line, col)
            else:
                body = BlockNode([], line, col)
        else:
            body = self._block(structure_name="while")

        return WhileNode(condition=cond, body=body, line=line, column=col)

    # --------------------------------------------------------------------------
    # Estructura FOR
    # --------------------------------------------------------------------------

    def _for_statement(self) -> ForNode:
        """
        sentencia_for -> 'for' '(' inicializacion ';' expresion ';' actualizacion ')' '{' bloque '}'
        """
        for_tok = self.advance()  # consume 'for'
        line, col = for_tok.line, for_tok.column

        # 1. Paréntesis '('
        if not self.match(TokenType.PARENTESIS_IZQ):
            self.report_error(
                category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                message=f"Paréntesis de apertura '(' faltante en estructura 'for' en la línea {line}, columna {col}.",
                suggestion="Coloque '(' inmediatamente después de 'for'. Ejemplo: for (i = 0; i < 10; i++) { ... }",
                structure_name="for",
                token=self.current
            )

        # 2. Inicialización (declaración o asignación)
        init_node: Optional[ASTNode] = None
        if self.check(TokenType.PUNTO_Y_COMA):
            self.advance()  # Inicialización vacía
        elif self.current.type in self.TYPE_TOKENS:
            # Declaración interna tipo: int i = 0;
            init_node = self._declaration()
        elif self.check(TokenType.IDENTIFICADOR):
            # Asignación tipo: i = 0;
            name_tok = self.advance()
            if self.match(TokenType.ASIGNACION):
                val_expr = self._expression()
                init_node = AssignmentNode(name_tok.value, val_expr, "=", name_tok.line, name_tok.column)
            else:
                init_node = IdentifierNode(name_tok.value, name_tok.line, name_tok.column)

            if not self.match(TokenType.PUNTO_Y_COMA):
                self.report_error(
                    category=SyntaxErrorCategory.COMPONENTE_FOR_INVALIDO,
                    message=f"Error: Componente de inicialización inválido en estructura 'for' en la línea {self.current.line}, columna {self.current.column}. Falta ';' tras inicialización.",
                    suggestion="Asegúrese de finalizar la sección de inicialización con ';'. Ejemplo: for (i = 0; ...)",
                    structure_name="for"
                )
        else:
            self.report_error(
                category=SyntaxErrorCategory.COMPONENTE_FOR_INVALIDO,
                message=f"Error: Componente inválido en la estructura 'for' (inicialización no reconocida) en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Especifique una inicialización válida como 'i = 0;' o 'int i = 0;'.",
                structure_name="for"
            )
            self.synchronize()

        # 3. Condición
        cond_node: Optional[ASTNode] = None
        if self.check(TokenType.PUNTO_Y_COMA):
            self.advance()  # Condición vacía
        elif self.check(TokenType.PARENTESIS_DER):
            self.report_error(
                category=SyntaxErrorCategory.COMPONENTE_FOR_INVALIDO,
                message=f"Error: Componente inválido en la estructura 'for' en la línea {self.current.line}, columna {self.current.column}. Faltan componentes internos.",
                suggestion="El bucle for requiere 'for (init; condicion; actualizacion)'.",
                structure_name="for"
            )
        else:
            cond_node = self._expression()
            if not self.match(TokenType.PUNTO_Y_COMA):
                self.report_error(
                    category=SyntaxErrorCategory.COMPONENTE_FOR_INVALIDO,
                    message=f"Error: Componente de condición inválido en estructura 'for' en la línea {self.current.line}, columna {self.current.column}. Falta ';' tras la condición.",
                    suggestion="Separe la condición de la actualización mediante ';'. Ejemplo: for (i = 0; i < 10; ...)",
                    structure_name="for"
                )

        # 4. Actualización
        update_node: Optional[ASTNode] = None
        if self.check(TokenType.PARENTESIS_DER):
            # Actualización vacía
            pass
        else:
            # Puede ser: i = i + 1, i++, ++i, i += 1
            if self.check(TokenType.IDENTIFICADOR) and self.peek(1).type in (TokenType.ASIGNACION, TokenType.ASIGNACION_SUMA, TokenType.ASIGNACION_RESTA):
                name_tok = self.advance()
                op_tok = self.advance()
                val_expr = self._expression()
                update_node = AssignmentNode(name_tok.value, val_expr, op_tok.value, name_tok.line, name_tok.column)
            else:
                update_node = self._expression()

        # 5. Paréntesis ')'
        if not self.match(TokenType.PARENTESIS_DER):
            self.report_error(
                category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                message=f"Paréntesis de cierre ')' faltante en estructura 'for' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Cierre los encabezados del bucle 'for' con ')'.",
                structure_name="for",
                token=self.current
            )

        # 6. Bloque '{' ... '}'
        if not self.check(TokenType.LLAVE_IZQ):
            self.report_error(
                category=SyntaxErrorCategory.BLOQUE_SIN_LLAVES,
                message=f"Error: Bloque de sentencias faltante o sin llaves '{{' en la estructura 'for' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="El cuerpo del bucle 'for' debe encerrarse entre llaves '{ ... }'.",
                structure_name="for"
            )
            if not self.is_at_end() and self.current.type != TokenType.LLAVE_DER:
                single_stmt = self._statement()
                body = BlockNode([single_stmt] if single_stmt else [], line, col)
            else:
                body = BlockNode([], line, col)
        else:
            body = self._block(structure_name="for")

        return ForNode(init=init_node, condition=cond_node, update=update_node, body=body, line=line, column=col)

    # --------------------------------------------------------------------------
    # Bloque de Sentencias '{' ... '}'
    # --------------------------------------------------------------------------

    def _block(self, structure_name: str = "bloque") -> BlockNode:
        """Parsea una secuencia de sentencias encerradas entre '{' y '}'."""
        if not self.match(TokenType.LLAVE_IZQ):
            # Error ya reportado o detectado
            tok = self.current
            self.report_error(
                category=SyntaxErrorCategory.BLOQUE_SIN_LLAVES,
                message=f"Llave de apertura '{{' faltante en {structure_name} en la línea {tok.line}, columna {tok.column}.",
                suggestion="Abra el bloque con '{'.",
                structure_name=structure_name
            )
            return BlockNode([], tok.line, tok.column)

        open_tok = self.tokens[self.pos - 1]
        statements: List[ASTNode] = []

        while not self.check(TokenType.LLAVE_DER) and not self.is_at_end():
            stmt = self._statement()
            if stmt:
                statements.append(stmt)

        if not self.match(TokenType.LLAVE_DER):
            self.report_error(
                category=SyntaxErrorCategory.LLAVE_FALTANTE,
                message=f"Error: Llave de cierre '}}' faltante en bloque de estructura '{structure_name}' en la línea {self.current.line}, columna {self.current.column}. (Bloque iniciado en línea {open_tok.line}, col {open_tok.column}).",
                suggestion="Agregue '}' para cerrar el bloque de sentencias.",
                structure_name=structure_name
            )

        return BlockNode(statements, line=open_tok.line, column=open_tok.column)

    # --------------------------------------------------------------------------
    # Declaraciones y Asignaciones
    # --------------------------------------------------------------------------

    def _declaration(self) -> VariableDeclarationNode:
        """tipo nombre ('=' expresion)? ';'"""
        type_tok = self.advance()
        if not self.check(TokenType.IDENTIFICADOR):
            self.report_error(
                category=SyntaxErrorCategory.ERROR_SINTACTICO_GENERAL,
                message=f"Se esperaba un identificador tras el tipo '{type_tok.value}' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Indique el nombre de la variable. Ejemplo: int contador = 0;",
                structure_name="declaracion"
            )
            return VariableDeclarationNode(type_tok.value, "<anonimo>", None, type_tok.line, type_tok.column)

        name_tok = self.advance()
        initializer: Optional[ASTNode] = None

        if self.match(TokenType.ASIGNACION):
            initializer = self._expression()

        if not self.match(TokenType.PUNTO_Y_COMA):
            self.report_error(
                category=SyntaxErrorCategory.PUNTO_Y_COMA_FALTANTE,
                message=f"Punto y coma ';' faltante tras la declaración de '{name_tok.value}' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Termine la sentencia de declaración con ';'.",
                structure_name="declaracion"
            )

        return VariableDeclarationNode(type_tok.value, name_tok.value, initializer, type_tok.line, type_tok.column)

    def _assignment_or_expression_statement(self) -> ASTNode:
        """Asignación o sentencia de expresión evaluada con ';'"""
        start_tok = self.current

        # Checar asignación simple o con operador compuesto: x = expr;, x += expr;
        if self.check(TokenType.IDENTIFICADOR) and self.peek(1).type in (
            TokenType.ASIGNACION, TokenType.ASIGNACION_SUMA, TokenType.ASIGNACION_RESTA
        ):
            target_tok = self.advance()
            op_tok = self.advance()
            expr = self._expression()

            if not self.match(TokenType.PUNTO_Y_COMA):
                self.report_error(
                    category=SyntaxErrorCategory.PUNTO_Y_COMA_FALTANTE,
                    message=f"Punto y coma ';' faltante tras la asignación a '{target_tok.value}' en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="Finalice la asignación con ';'.",
                    structure_name="asignacion"
                )

            return AssignmentNode(target_tok.value, expr, op_tok.value, target_tok.line, target_tok.column)

        # Expresión simple terminada en ';'
        expr = self._expression()
        if not self.match(TokenType.PUNTO_Y_COMA):
            self.report_error(
                category=SyntaxErrorCategory.PUNTO_Y_COMA_FALTANTE,
                message=f"Punto y coma ';' faltante tras la expresión en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Agregue ';' al final de la sentencia.",
                structure_name="sentencia_expresion"
            )

        return expr

    def _return_statement(self) -> ReturnNode:
        """'return' expresion? ';'"""
        ret_tok = self.advance()
        val_expr: Optional[ASTNode] = None

        if not self.check(TokenType.PUNTO_Y_COMA):
            val_expr = self._expression()

        if not self.match(TokenType.PUNTO_Y_COMA):
            self.report_error(
                category=SyntaxErrorCategory.PUNTO_Y_COMA_FALTANTE,
                message=f"Punto y coma ';' faltante tras sentencia 'return' en la línea {self.current.line}, columna {self.current.column}.",
                suggestion="Finalice la instrucción 'return' con ';'.",
                structure_name="return"
            )

        return ReturnNode(val_expr, ret_tok.line, ret_tok.column)

    # --------------------------------------------------------------------------
    # Expresiones con Precedencia de Operadores
    # --------------------------------------------------------------------------

    def _expression(self) -> ASTNode:
        return self._logical_or()

    def _logical_or(self) -> ASTNode:
        expr = self._logical_and()
        while self.match(TokenType.OR_LOGICO):
            op = self.tokens[self.pos - 1].value
            right = self._logical_and()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _logical_and(self) -> ASTNode:
        expr = self._equality()
        while self.match(TokenType.AND_LOGICO):
            op = self.tokens[self.pos - 1].value
            right = self._equality()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _equality(self) -> ASTNode:
        expr = self._relational()
        while self.match(TokenType.IGUAL_QUE, TokenType.DISTINTO_QUE):
            op = self.tokens[self.pos - 1].value
            right = self._relational()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _relational(self) -> ASTNode:
        expr = self._additive()
        while self.match(
            TokenType.MENOR_QUE, TokenType.MAYOR_QUE,
            TokenType.MENOR_IGUAL_QUE, TokenType.MAYOR_IGUAL_QUE
        ):
            op = self.tokens[self.pos - 1].value
            right = self._additive()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _additive(self) -> ASTNode:
        expr = self._multiplicative()
        while self.match(TokenType.SUMA, TokenType.RESTA):
            op = self.tokens[self.pos - 1].value
            right = self._multiplicative()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _multiplicative(self) -> ASTNode:
        expr = self._unary()
        while self.match(TokenType.MULTIPLICACION, TokenType.DIVISION, TokenType.MODULO):
            op = self.tokens[self.pos - 1].value
            right = self._unary()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _unary(self) -> ASTNode:
        if self.match(TokenType.NOT_LOGICO, TokenType.RESTA, TokenType.SUMA, TokenType.INCREMENTO, TokenType.DECREMENTO):
            op_tok = self.tokens[self.pos - 1]
            operand = self._unary()
            return UnaryOpNode(op_tok.value, operand, is_postfix=False, line=op_tok.line, column=op_tok.column)
        return self._postfix()

    def _postfix(self) -> ASTNode:
        expr = self._primary()
        if self.match(TokenType.INCREMENTO, TokenType.DECREMENTO):
            op_tok = self.tokens[self.pos - 1]
            return UnaryOpNode(op_tok.value, expr, is_postfix=True, line=op_tok.line, column=op_tok.column)
        return expr

    def _primary(self) -> ASTNode:
        tok = self.current

        # Literales numéricos
        if self.match(TokenType.NUMERO_ENTERO):
            val = int(self.tokens[self.pos - 1].value, 0)
            return LiteralNode(val, "int", tok.line, tok.column)

        if self.match(TokenType.NUMERO_FLOTANTE):
            val = float(self.tokens[self.pos - 1].value.rstrip('fFlL'))
            return LiteralNode(val, "float", tok.line, tok.column)

        if self.match(TokenType.LITERAL_CADENA):
            val = self.tokens[self.pos - 1].value[1:-1]
            return LiteralNode(val, "string", tok.line, tok.column)

        if self.match(TokenType.LITERAL_CARACTER):
            val = self.tokens[self.pos - 1].value[1:-1]
            return LiteralNode(val, "char", tok.line, tok.column)

        # Identificador o llamada a función
        if self.match(TokenType.IDENTIFICADOR):
            name = self.tokens[self.pos - 1].value
            if self.match(TokenType.PARENTESIS_IZQ):
                # Llamada a función: printf(...)
                args: List[ASTNode] = []
                if not self.check(TokenType.PARENTESIS_DER):
                    while True:
                        args.append(self._expression())
                        if not self.match(TokenType.COMA):
                            break
                if not self.match(TokenType.PARENTESIS_DER):
                    self.report_error(
                        category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                        message=f"Falta ')' en llamada a función '{name}' en la línea {self.current.line}, columna {self.current.column}.",
                        suggestion="Cierre los argumentos con ')'.",
                        structure_name="llamada_funcion"
                    )
                return CallNode(name, args, tok.line, tok.column)
            return IdentifierNode(name, tok.line, tok.column)

        # Expresión agrupada: ( expr )
        if self.match(TokenType.PARENTESIS_IZQ):
            expr = self._expression()
            if not self.match(TokenType.PARENTESIS_DER):
                self.report_error(
                    category=SyntaxErrorCategory.PARENTESIS_DESBALANCEADOS,
                    message=f"Paréntesis de cierre ')' desbalanceado o faltante en expresión en la línea {self.current.line}, columna {self.current.column}.",
                    suggestion="Cierre la expresión con ')'.",
                    structure_name="expresion"
                )
            return expr

        # Si llegamos aquí sin coincidir, error de sintaxis en expresión
        self.report_error(
            category=SyntaxErrorCategory.ERROR_SINTACTICO_GENERAL,
            message=f"Token inesperado '{tok.value}' en la línea {tok.line}, columna {tok.column}.",
            suggestion="Verifique que la sintaxis de la expresión u operando sea válida.",
            structure_name="expresion",
            token=tok
        )
        self.advance()
        return ErrorNode(f"Token inesperado '{tok.value}'", tok.line, tok.column)
