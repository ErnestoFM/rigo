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

from typing import List, Optional
from token_type import TokenType, Token
from ast_nodes import (
    ASTNode, ProgramNode, VariableDeclarationNode, AssignmentNode,
    BinaryOpNode, UnaryOpNode, IdentifierNode, LiteralNode
)


class Parser:
    """
    Analizador Sintáctico Descendente Recursivo para expresiones,
    declaraciones y asignaciones destinadas a la generación de código intermedio.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    TYPE_TOKENS = {
        TokenType.KEYWORD_INT: "int",
        TokenType.KEYWORD_FLOAT: "float",
        TokenType.KEYWORD_DOUBLE: "double",
        TokenType.KEYWORD_BOOL: "bool",
        TokenType.KEYWORD_STRING: "string",
        TokenType.KEYWORD_VOID: "void"
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
        statements: List[ASTNode] = []
        start_line = self.current.line
        start_col = self.current.column

        while not self.is_at_end():
            stmts = self._statement()
            if stmts:
                statements.extend(stmts)

        return ProgramNode(statements, start_line, start_col)

    def _statement(self) -> List[ASTNode]:
        tok = self.current

        # Declaración de variables tipo: int a = 10, b = 5;
        if tok.type in self.TYPE_TOKENS:
            return self._declaration()

        if tok.type == TokenType.PUNTO_Y_COMA:
            self.advance()
            return []

        # Asignación clásica: x = expr;
        if self.check(TokenType.IDENTIFICADOR) and self.peek(1).type == TokenType.ASIGNACION:
            target_tok = self.advance()  # ident
            self.advance()               # '='
            expr = self._expression()
            self.match(TokenType.PUNTO_Y_COMA)
            return [AssignmentNode(target_tok.value, expr, target_tok.line, target_tok.column)]

        # Expresión simple
        expr = self._expression()
        self.match(TokenType.PUNTO_Y_COMA)
        return [expr]

    def _declaration(self) -> List[ASTNode]:
        type_tok = self.advance()
        var_type = self.TYPE_TOKENS[type_tok.type]
        declarations: List[ASTNode] = []

        while True:
            if not self.check(TokenType.IDENTIFICADOR):
                break
            name_tok = self.advance()
            init_expr: Optional[ASTNode] = None

            if self.match(TokenType.ASIGNACION):
                init_expr = self._expression()

            decl = VariableDeclarationNode(var_type, name_tok.value, init_expr, name_tok.line, name_tok.column)
            declarations.append(decl)

            if not self.match(TokenType.COMA):
                break

        self.match(TokenType.PUNTO_Y_COMA)
        return declarations

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
        if self.match(TokenType.NOT_LOGICO, TokenType.RESTA, TokenType.SUMA):
            op_tok = self.tokens[self.pos - 1]
            operand = self._unary()
            return UnaryOpNode(op_tok.value, operand, op_tok.line, op_tok.column)
        return self._primary()

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

        if self.match(TokenType.KEYWORD_TRUE):
            return LiteralNode(True, "bool", tok.line, tok.column)

        if self.match(TokenType.KEYWORD_FALSE):
            return LiteralNode(False, "bool", tok.line, tok.column)

        if self.match(TokenType.IDENTIFICADOR):
            return IdentifierNode(self.tokens[self.pos - 1].value, tok.line, tok.column)

        if self.match(TokenType.PARENTESIS_IZQ):
            expr = self._expression()
            self.match(TokenType.PARENTESIS_DER)
            return expr

        # Fallback
        self.advance()
        return LiteralNode(0, "int", tok.line, tok.column)
