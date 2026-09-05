"""
================================================================================
ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES
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
    ASTNode, ProgramNode, VarDeclarationNode, ConstDeclarationNode,
    AssignmentNode, BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode
)
from error_handler import SyntaxErrorHandler

class Parser:
    """
    Analizador Sintáctico Descendente Recursivo (Recursive Descent Parser)
    para declaraciones y uso de variables y constantes.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    KNOWN_INVALID_TYPES = {
        'decimal', 'doble', 'double', 'caracter', 'char', 'texto', 'string',
        'real', 'int', 'float', 'bool', 'flotando', 'entera', 'boleano'
    }

    def __init__(self, tokens: List[Token], error_handler: Optional[SyntaxErrorHandler] = None):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler or SyntaxErrorHandler()

    def _peek(self, offset: int = 0) -> Token:
        idx = self.current + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1] # EOF

    def _previous(self) -> Token:
        if self.current > 0:
            return self.tokens[self.current - 1]
        return self.tokens[0]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _match(self, *token_types: TokenType) -> bool:
        for t in token_types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _synchronize(self):
        """Modo Pánico (Panic Mode): Sincronización tras encontrar un error sintáctico."""
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.PUNTO_Y_COMA:
                return
            
            # Siguiente inicio de declaración o sentencia
            if self._peek().type in (TokenType.TIPO, TokenType.CONSTANTE):
                return
            self._advance()

    def parse(self) -> ProgramNode:
        """Punto de entrada: analiza el flujo de tokens y genera el AST."""
        statements: List[ASTNode] = []
        while not self._is_at_end():
            stmt = self._declaration_or_statement()
            if stmt is not None:
                if isinstance(stmt, list):
                    statements.extend(stmt)
                else:
                    statements.append(stmt)
        return ProgramNode(statements)

    def _declaration_or_statement(self):
        try:
            # 1. Declaración de constante: 'constante' | 'const'
            if self._check(TokenType.CONSTANTE):
                return self._const_declaration()

            # 2. Declaración de variable con tipo válido: 'entero', 'flotante', etc.
            if self._check(TokenType.TIPO):
                return self._var_declaration()

            # 3. Caso especial de error: Uso de tipo no válido como palabra inicial (ej: "doble x;" o "flotando y;")
            if self._check(TokenType.IDENTIFICADOR):
                token = self._peek()
                # Si el siguiente token parece un identificador o identificador inválido, es un tipo inválido
                next_tok = self._peek(1)
                if next_tok.type in (TokenType.IDENTIFICADOR, TokenType.IDENTIFICADOR_INVALIDO, TokenType.LITERAL_ENTERO) or token.value.lower() in self.KNOWN_INVALID_TYPES:
                    self.error_handler.report_invalid_type(token.value, token.line, token.column)
                    self._synchronize()
                    return None

                # 4. Sentencia de Asignación / Uso de variable: id = expresion ;
                return self._assignment_statement()

            # 5. Si encontramos un identificador inválido o número iniciando una sentencia
            if self._check(TokenType.IDENTIFICADOR_INVALIDO) or self._check(TokenType.LITERAL_ENTERO):
                tok = self._peek()
                self.error_handler.report_invalid_identifier(tok.value, tok.line, tok.column)
                self._synchronize()
                return None

            # Token inesperado
            tok = self._advance()
            self.error_handler.report_general_syntax_error("declaración o sentencia válida", tok.value, tok.line, tok.column)
            self._synchronize()
            return None

        except Exception as e:
            self._synchronize()
            return None

    def _var_declaration(self) -> Optional[List[VarDeclarationNode]]:
        """
        declaracion_variable -> tipo IDENTIFICADOR ( '=' expresion )? ( ',' IDENTIFICADOR ( '=' expresion )? )* ';'
        """
        tipo_token = self._advance()
        tipo_name = tipo_token.value
        nodes: List[VarDeclarationNode] = []

        while True:
            # Validar identificador
            if self._check(TokenType.IDENTIFICADOR_INVALIDO):
                inv_tok = self._advance()
                self.error_handler.report_invalid_identifier(inv_tok.value, inv_tok.line, inv_tok.column)
                self._synchronize()
                return None
            elif self._check(TokenType.LITERAL_ENTERO) or self._check(TokenType.LITERAL_FLOTANTE):
                inv_tok = self._advance()
                self.error_handler.report_invalid_identifier(inv_tok.value, inv_tok.line, inv_tok.column)
                self._synchronize()
                return None
            elif not self._check(TokenType.IDENTIFICADOR):
                tok = self._peek()
                self.error_handler.add_error(
                    f"Se esperaba un identificador válido tras el tipo '{tipo_name}'",
                    tok.line, tok.column,
                    "Un identificador debe comenzar con una letra o guion bajo.",
                    tok.value
                )
                self._synchronize()
                return None

            id_token = self._advance()
            var_name = id_token.value
            init_val: Optional[ASTNode] = None

            # Inicialización opcional (= expresion)
            if self._match(TokenType.ASIGNACION):
                init_val = self._expression()

            nodes.append(VarDeclarationNode(tipo_name, var_name, init_val, id_token.line, id_token.column))

            if self._match(TokenType.COMA):
                continue
            else:
                break

        # Verificar ';' obligatorio al final
        if not self._match(TokenType.PUNTO_Y_COMA):
            prev = self._previous()
            self.error_handler.report_missing_semicolon(prev.line, prev.column + len(prev.value))
            # No avanzamos bruscamente si el siguiente ya es otra línea
            if self._peek().type != TokenType.PUNTO_Y_COMA:
                pass
            else:
                self._advance()

        return nodes

    def _const_declaration(self) -> Optional[List[ConstDeclarationNode]]:
        """
        declaracion_constante -> ( 'constante' | 'const' ) tipo IDENTIFICADOR '=' expresion ( ',' IDENTIFICADOR '=' expresion )* ';'
        """
        const_kw = self._advance() # 'constante' / 'const'
        
        # Validar tipo
        if not self._check(TokenType.TIPO):
            tok = self._peek()
            self.error_handler.report_invalid_type(tok.value, tok.line, tok.column)
            self._synchronize()
            return None
        
        tipo_token = self._advance()
        tipo_name = tipo_token.value
        nodes: List[ConstDeclarationNode] = []

        while True:
            # Validar identificador
            if self._check(TokenType.IDENTIFICADOR_INVALIDO) or self._check(TokenType.LITERAL_ENTERO):
                inv_tok = self._advance()
                self.error_handler.report_invalid_identifier(inv_tok.value, inv_tok.line, inv_tok.column)
                self._synchronize()
                return None
            elif not self._check(TokenType.IDENTIFICADOR):
                tok = self._peek()
                self.error_handler.add_error(
                    f"Se esperaba un identificador para la constante tras el tipo '{tipo_name}'",
                    tok.line, tok.column,
                    "Especifique un nombre de constante válido.",
                    tok.value
                )
                self._synchronize()
                return None

            id_token = self._advance()
            const_name = id_token.value

            # Para constantes, la inicialización con '=' es OBLIGATORIA
            if not self._match(TokenType.ASIGNACION):
                self.error_handler.report_uninitialized_constant(const_name, id_token.line, id_token.column)
                self._synchronize()
                return None

            init_val = self._expression()
            nodes.append(ConstDeclarationNode(tipo_name, const_name, init_val, id_token.line, id_token.column))

            if self._match(TokenType.COMA):
                continue
            else:
                break

        # Verificar ';' obligatorio al final
        if not self._match(TokenType.PUNTO_Y_COMA):
            prev = self._previous()
            self.error_handler.report_missing_semicolon(prev.line, prev.column + len(prev.value))
            if self._peek().type == TokenType.PUNTO_Y_COMA:
                self._advance()

        return nodes

    def _assignment_statement(self) -> Optional[AssignmentNode]:
        """
        sentencia_asignacion -> IDENTIFICADOR '=' expresion ';'
        """
        id_token = self._advance()
        target_name = id_token.value

        if not self._match(TokenType.ASIGNACION):
            tok = self._peek()
            self.error_handler.report_general_syntax_error("'=' en la sentencia de asignación", tok.value, tok.line, tok.column)
            self._synchronize()
            return None

        expr = self._expression()

        # Verificar ';'
        if not self._match(TokenType.PUNTO_Y_COMA):
            prev = self._previous()
            self.error_handler.report_missing_semicolon(prev.line, prev.column + len(prev.value))
            if self._peek().type == TokenType.PUNTO_Y_COMA:
                self._advance()

        return AssignmentNode(target_name, expr, id_token.line, id_token.column)

    # ------------------ Jerarquía de Expresiones ------------------

    def _expression(self) -> ASTNode:
        return self._logic_or()

    def _logic_or(self) -> ASTNode:
        expr = self._logic_and()
        while self._match(TokenType.OP_O):
            op = self._previous()
            right = self._logic_and()
            expr = BinaryOpNode(expr, op.value, right, op.line, op.column)
        return expr

    def _logic_and(self) -> ASTNode:
        expr = self._equality()
        while self._match(TokenType.OP_Y):
            op = self._previous()
            right = self._equality()
            expr = BinaryOpNode(expr, op.value, right, op.line, op.column)
        return expr

    def _equality(self) -> ASTNode:
        expr = self._relational()
        while self._match(TokenType.OP_IGUAL, TokenType.OP_DISTINTO):
            op = self._previous()
            right = self._relational()
            expr = BinaryOpNode(expr, op.value, right, op.line, op.column)
        return expr

    def _relational(self) -> ASTNode:
        expr = self._additive()
        while self._match(TokenType.OP_MENOR, TokenType.OP_MENOR_IGUAL, TokenType.OP_MAYOR, TokenType.OP_MAYOR_IGUAL):
            op = self._previous()
            right = self._additive()
            expr = BinaryOpNode(expr, op.value, right, op.line, op.column)
        return expr

    def _additive(self) -> ASTNode:
        expr = self._multiplicative()
        while self._match(TokenType.OP_SUMA, TokenType.OP_RESTA):
            op = self._previous()
            right = self._multiplicative()
            expr = BinaryOpNode(expr, op.value, right, op.line, op.column)
        return expr

    def _multiplicative(self) -> ASTNode:
        expr = self._unary()
        while self._match(TokenType.OP_MULT, TokenType.OP_DIV, TokenType.OP_MOD):
            op = self._previous()
            right = self._unary()
            expr = BinaryOpNode(expr, op.value, right, op.line, op.column)
        return expr

    def _unary(self) -> ASTNode:
        if self._match(TokenType.OP_NO, TokenType.OP_RESTA, TokenType.OP_SUMA):
            op = self._previous()
            operand = self._unary()
            return UnaryOpNode(op.value, operand, op.line, op.column)
        return self._primary()

    def _primary(self) -> ASTNode:
        tok = self._peek()

        if self._match(TokenType.LITERAL_ENTERO):
            return LiteralNode(tok.value, "entero", tok.line, tok.column)
        
        if self._match(TokenType.LITERAL_FLOTANTE):
            return LiteralNode(tok.value, "flotante", tok.line, tok.column)

        if self._match(TokenType.LITERAL_CADENA):
            return LiteralNode(tok.value, "cadena", tok.line, tok.column)

        if self._match(TokenType.LITERAL_BOOLEANO):
            return LiteralNode(tok.value, "booleano", tok.line, tok.column)

        if self._match(TokenType.IDENTIFICADOR):
            return IdentifierNode(tok.value, tok.line, tok.column)

        if self._match(TokenType.PARENTESIS_IZQ):
            expr = self._expression()
            if not self._match(TokenType.PARENTESIS_DER):
                cur = self._peek()
                self.error_handler.add_error(
                    "Se esperaba ')' de cierre en la expresión",
                    cur.line, cur.column,
                    "Asegúrese de emparejar todos los paréntesis abiertos.",
                    ")"
                )
            return expr

        # Si llegamos aquí y hay un token inválido o vacío
        self._advance()
        self.error_handler.add_error(
            f"Expresión incompleta o token inesperado '{tok.value}'",
            tok.line, tok.column,
            "Verifique la sintaxis del operando o valor asignado.",
            tok.value
        )
        return LiteralNode("ERROR", "error", tok.line, tok.column)
