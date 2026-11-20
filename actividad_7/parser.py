"""
================================================================================
ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Optional, Tuple
from token_type import TokenType, Token
from ast_nodes import (
    ASTNode, ProgramNode, BlockNode, VariableDeclarationNode, AssignmentNode,
    FunctionNode, IfNode, WhileNode, ForNode, ReturnNode, BinaryOpNode,
    UnaryOpNode, IdentifierNode, LiteralNode, CallNode, ErrorNode
)


class Parser:
    """
    Analizador Sintáctico Descendente Recursivo para construir el AST
    que alimentará la fase de Análisis Semántico y Verificación de Tipos.

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

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    @property
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1] if self.tokens else Token(TokenType.EOF, "", 1, 1)

    def peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1] if self.tokens else Token(TokenType.EOF, "", 1, 1)

    def is_at_end(self) -> bool:
        return self.current.type == TokenType.EOF

    def advance(self) -> Token:
        tok = self.current
        if not self.is_at_end():
            self.pos += 1
        return tok

    def check(self, tt: TokenType) -> bool:
        return self.current.type == tt

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def parse(self) -> ProgramNode:
        """Punto de entrada: genera el nodo raíz ProgramNode con todas las sentencias/declaraciones."""
        statements: List[ASTNode] = []
        start_line = self.current.line
        start_col = self.current.column

        while not self.is_at_end():
            stmt = self._top_level()
            if stmt:
                statements.append(stmt)

        return ProgramNode(statements, line=start_line, column=start_col)

    def _top_level(self) -> Optional[ASTNode]:
        # Detectar definición de función: tipo ident '(' ... ')' '{'
        if self.current.type in self.TYPE_TOKENS and self.peek(1).type == TokenType.IDENTIFICADOR and self.peek(2).type == TokenType.PARENTESIS_IZQ:
            # Buscar si termina en '{' (función)
            lookahead = 2
            p_depth = 0
            is_func = False
            while self.pos + lookahead < len(self.tokens):
                tt = self.tokens[self.pos + lookahead].type
                if tt == TokenType.PARENTESIS_IZQ:
                    p_depth += 1
                elif tt == TokenType.PARENTESIS_DER:
                    p_depth -= 1
                    if p_depth == 0:
                        next_tok = self.peek(lookahead + 1)
                        if next_tok.type == TokenType.LLAVE_IZQ:
                            is_func = True
                        break
                elif tt == TokenType.EOF:
                    break
                lookahead += 1

            if is_func:
                return self._function_definition()

        return self._statement()

    def _function_definition(self) -> FunctionNode:
        type_tok = self.advance()
        name_tok = self.advance()
        self.advance()  # consume '('

        params: List[Tuple[str, str]] = []
        if not self.check(TokenType.PARENTESIS_DER):
            while True:
                if self.current.type in self.TYPE_TOKENS:
                    ptype = self.advance().value
                    if self.check(TokenType.IDENTIFICADOR):
                        pname = self.advance().value
                        params.append((ptype, pname))
                    else:
                        params.append((ptype, "<anonimo>"))
                elif self.check(TokenType.IDENTIFICADOR):
                    pname = self.advance().value
                    params.append(("int", pname))
                else:
                    break

                if not self.match(TokenType.COMA):
                    break

        self.match(TokenType.PARENTESIS_DER)
        body = self._block()
        return FunctionNode(
            return_type=type_tok.value,
            name=name_tok.value,
            params=params,
            body=body,
            line=type_tok.line,
            column=type_tok.column
        )

    def _statement(self) -> Optional[ASTNode]:
        tok = self.current

        if tok.type in self.TYPE_TOKENS:
            return self._declaration()

        if tok.type == TokenType.KEYWORD_IF:
            return self._if_statement()

        if tok.type == TokenType.KEYWORD_WHILE:
            return self._while_statement()

        if tok.type == TokenType.KEYWORD_FOR:
            return self._for_statement()

        if tok.type == TokenType.KEYWORD_RETURN:
            return self._return_statement()

        if tok.type == TokenType.LLAVE_IZQ:
            return self._block()

        if tok.type == TokenType.PUNTO_Y_COMA:
            self.advance()
            return None

        # Asignación o llamada a función
        return self._assignment_or_expr()

    def _declaration(self) -> VariableDeclarationNode:
        type_tok = self.advance()
        name_tok = self.advance() if self.check(TokenType.IDENTIFICADOR) else Token(TokenType.IDENTIFICADOR, "<anonimo>", type_tok.line, type_tok.column)
        init_expr: Optional[ASTNode] = None

        if self.match(TokenType.ASIGNACION):
            init_expr = self._expression()

        self.match(TokenType.PUNTO_Y_COMA)
        return VariableDeclarationNode(type_tok.value, name_tok.value, init_expr, type_tok.line, type_tok.column)

    def _assignment_or_expr(self) -> ASTNode:
        if self.check(TokenType.IDENTIFICADOR) and self.peek(1).type in (
            TokenType.ASIGNACION, TokenType.ASIGNACION_SUMA, TokenType.ASIGNACION_RESTA
        ):
            target = self.advance().value
            op = self.advance().value
            expr = self._expression()
            self.match(TokenType.PUNTO_Y_COMA)
            return AssignmentNode(target, expr, op, self.current.line, self.current.column)

        expr = self._expression()
        self.match(TokenType.PUNTO_Y_COMA)
        return expr

    def _block(self) -> BlockNode:
        start_line = self.current.line
        start_col = self.current.column
        self.match(TokenType.LLAVE_IZQ)
        statements: List[ASTNode] = []

        while not self.check(TokenType.LLAVE_DER) and not self.is_at_end():
            s = self._statement()
            if s:
                statements.append(s)

        self.match(TokenType.LLAVE_DER)
        return BlockNode(statements, start_line, start_col)

    def _if_statement(self) -> IfNode:
        if_tok = self.advance()  # 'if'
        self.match(TokenType.PARENTESIS_IZQ)
        cond = self._expression()
        self.match(TokenType.PARENTESIS_DER)

        then_block = self._block() if self.check(TokenType.LLAVE_IZQ) else BlockNode([self._statement()], if_tok.line, if_tok.column)
        else_block: Optional[BlockNode] = None

        if self.match(TokenType.KEYWORD_ELSE):
            else_block = self._block() if self.check(TokenType.LLAVE_IZQ) else BlockNode([self._statement()], if_tok.line, if_tok.column)

        return IfNode(cond, then_block, else_block, if_tok.line, if_tok.column)

    def _while_statement(self) -> WhileNode:
        while_tok = self.advance()
        self.match(TokenType.PARENTESIS_IZQ)
        cond = self._expression()
        self.match(TokenType.PARENTESIS_DER)
        body = self._block() if self.check(TokenType.LLAVE_IZQ) else BlockNode([self._statement()], while_tok.line, while_tok.column)
        return WhileNode(cond, body, while_tok.line, while_tok.column)

    def _for_statement(self) -> ForNode:
        for_tok = self.advance()
        self.match(TokenType.PARENTESIS_IZQ)

        init_node: Optional[ASTNode] = None
        if self.current.type in self.TYPE_TOKENS:
            init_node = self._declaration()
        elif not self.check(TokenType.PUNTO_Y_COMA):
            init_node = self._assignment_or_expr()
        else:
            self.match(TokenType.PUNTO_Y_COMA)

        cond_node: Optional[ASTNode] = None
        if not self.check(TokenType.PUNTO_Y_COMA):
            cond_node = self._expression()
        self.match(TokenType.PUNTO_Y_COMA)

        update_node: Optional[ASTNode] = None
        if not self.check(TokenType.PARENTESIS_DER):
            if self.check(TokenType.IDENTIFICADOR) and self.peek(1).type in (TokenType.ASIGNACION, TokenType.ASIGNACION_SUMA, TokenType.ASIGNACION_RESTA):
                target = self.advance().value
                op = self.advance().value
                expr = self._expression()
                update_node = AssignmentNode(target, expr, op, for_tok.line, for_tok.column)
            else:
                update_node = self._expression()

        self.match(TokenType.PARENTESIS_DER)
        body = self._block() if self.check(TokenType.LLAVE_IZQ) else BlockNode([self._statement()], for_tok.line, for_tok.column)
        return ForNode(init_node, cond_node, update_node, body, for_tok.line, for_tok.column)

    def _return_statement(self) -> ReturnNode:
        ret_tok = self.advance()
        val: Optional[ASTNode] = None
        if not self.check(TokenType.PUNTO_Y_COMA):
            val = self._expression()
        self.match(TokenType.PUNTO_Y_COMA)
        return ReturnNode(val, ret_tok.line, ret_tok.column)

    # --------------------------------------------------------------------------
    # Expresiones
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
        while self.match(TokenType.MENOR_QUE, TokenType.MAYOR_QUE, TokenType.MENOR_IGUAL_QUE, TokenType.MAYOR_IGUAL_QUE):
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
            return UnaryOpNode(op_tok.value, operand, False, op_tok.line, op_tok.column)

        expr = self._primary()
        if self.match(TokenType.INCREMENTO, TokenType.DECREMENTO):
            op_tok = self.tokens[self.pos - 1]
            return UnaryOpNode(op_tok.value, expr, True, op_tok.line, op_tok.column)
        return expr

    def _primary(self) -> ASTNode:
        tok = self.current

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

        if self.match(TokenType.IDENTIFICADOR):
            name = self.tokens[self.pos - 1].value
            if self.match(TokenType.PARENTESIS_IZQ):
                args: List[ASTNode] = []
                if not self.check(TokenType.PARENTESIS_DER):
                    while True:
                        args.append(self._expression())
                        if not self.match(TokenType.COMA):
                            break
                self.match(TokenType.PARENTESIS_DER)
                return CallNode(name, args, tok.line, tok.column)
            return IdentifierNode(name, tok.line, tok.column)

        if self.match(TokenType.PARENTESIS_IZQ):
            expr = self._expression()
            self.match(TokenType.PARENTESIS_DER)
            return expr

        # Fallback
        self.advance()
        return ErrorNode(f"Token inesperado '{tok.value}'", tok.line, tok.column)
