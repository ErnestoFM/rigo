"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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
    ASTNode, BinaryOpNode, UnaryOpNode, NumberNode, IdentifierNode,
    GroupedExprNode, ErrorNode
)
from error_handler import SyntaxErrorHandler

class Parser:
    """
    Analizador Sintáctico Descendente Recursivo (Recursive Descent Parser)
    para Expresiones Aritméticas y Lógicas conforme a la gramática formal:

      expresion            -> expresion_logica | expresion_aritmetica
      expresion_logica     -> termino_logico (( '&&' | '||' ) termino_logico)*
      termino_logico       -> expresion_aritmetica ( '==' | '!=' | '>' | '<' | '>=' | '<=' ) expresion_aritmetica
                            | expresion_aritmetica
      expresion_aritmetica -> termino (( '+' | '-' ) termino)*
      termino              -> factor (( '*' | '/' | '%' | '^' ) factor)*
      factor               -> IDENTIFICADOR | NUMERO | '(' expresion ')'

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, tokens: List[Token], error_handler: Optional[SyntaxErrorHandler] = None):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler or SyntaxErrorHandler()
        self.open_paren_stack: List[Token] = []

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DE NAVEGACIÓN DE TOKENS
    # -------------------------------------------------------------------------

    def _peek(self, offset: int = 0) -> Token:
        idx = self.current + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1] # Retorna EOF

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

    # -------------------------------------------------------------------------
    # PUNTO DE ENTRADA PRINCIPAL: PARSE
    # -------------------------------------------------------------------------

    def parse(self) -> ASTNode:
        """
        Inicia el análisis sintáctico de la expresión completa.
        Verifica que no queden tokens residuales tras la expresión.
        """
        if self._is_at_end():
            self.error_handler.add_error("Entrada vacía", 1, 1, suggestion="Ingrese una expresión para analizar.")
            return ErrorNode("Entrada vacía", 1, 1)

        # Verificar si inicia erróneamente con un operador binario o relacional
        first = self._peek()
        if first.type in (TokenType.OP_MULTIPLICACION, TokenType.OP_DIVISION, TokenType.OP_MODULO, TokenType.OP_POTENCIA):
            self.error_handler.report_operator_without_term(
                first.value, first.line, first.column,
                suggestion=f"El operador '{first.value}' no puede iniciar una expresión sin un término previo."
            )
            self._advance()
        elif first.type in (TokenType.OP_AND, TokenType.OP_OR):
            self.error_handler.report_incomplete_logical_expression(
                first.value, first.line, first.column,
                suggestion=f"La expresión no puede comenzar con el operador lógico '{first.value}'."
            )
            self._advance()
        elif first.is_relational_op():
            self.error_handler.report_invalid_comparison(
                first.line, first.column, op=first.value,
                suggestion=f"No puede iniciar una comparación con '{first.value}' sin una expresión aritmética izquierda."
            )
            self._advance()

        root = self._expresion()

        # Verificar tokens sobrantes tras finalizar el análisis sintáctico
        while not self._is_at_end():
            tok = self._peek()
            if tok.type == TokenType.PARENTESIS_DER:
                self.error_handler.report_unbalanced_parentheses(
                    tok.line, tok.column,
                    suggestion="Paréntesis de cierre ')' sobrante o sin apertura previa.",
                    paren=")"
                )
                self._advance()
            elif tok.type in (TokenType.IDENTIFICADOR, TokenType.NUMERO_ENTERO, TokenType.NUMERO_FLOTANTE):
                self.error_handler.report_missing_operator(
                    tok.line, tok.column, tok.value,
                    suggestion=f"Falta un operador aritmético o relacional antes de '{tok.value}'."
                )
                self._advance()
            elif tok.is_arithmetic_op():
                self.error_handler.report_operator_without_term(
                    tok.value, tok.line, tok.column,
                    suggestion=f"El operador '{tok.value}' se encuentra al final sin término posterior."
                )
                self._advance()
            elif tok.is_relational_op():
                self.error_handler.report_invalid_comparison(
                    tok.line, tok.column, op=tok.value,
                    suggestion=f"El operador de comparación '{tok.value}' se encuentra incompleto."
                )
                self._advance()
            elif tok.is_logical_op():
                self.error_handler.report_incomplete_logical_expression(
                    tok.value, tok.line, tok.column,
                    suggestion=f"El operador lógico '{tok.value}' carece de término posterior."
                )
                self._advance()
            else:
                self.error_handler.report_general_syntax_error(
                    "fin de expresión", tok.value, tok.line, tok.column
                )
                self._advance()

        return root

    # -------------------------------------------------------------------------
    # JERARQUÍA DE REGLAS SINTÁCTICAS (GRAMÁTICA DEL PROFESOR)
    # -------------------------------------------------------------------------

    def _expresion(self) -> ASTNode:
        """
        expresion -> expresion_logica | expresion_aritmetica
        Regla superior de disyunción lógica ('||', 'or').
        """
        return self._expresion_logica_or()

    def _expresion_logica_or(self) -> ASTNode:
        """
        expresion_logica_or -> expresion_logica_and ( ( '||' | 'or' ) expresion_logica_and )*
        """
        node = self._expresion_logica_and()

        while self._match(TokenType.OP_OR):
            op = self._previous()
            if self._is_at_end() or self._peek().type == TokenType.PARENTESIS_DER:
                self.error_handler.report_incomplete_logical_expression(
                    op.value, op.line, op.column,
                    suggestion=f"Falta el término lógico derecho tras el operador '{op.value}'."
                )
                right = ErrorNode("Término lógico faltante", op.line, op.column + len(op.value))
            elif self._peek().type in (TokenType.OP_OR, TokenType.OP_AND):
                next_op = self._advance()
                self.error_handler.report_incomplete_logical_expression(
                    op.value, op.line, op.column,
                    suggestion=f"Operadores lógicos consecutivos '{op.value}' y '{next_op.value}' inválidos."
                )
                right = self._expresion_logica_and()
            else:
                right = self._expresion_logica_and()

            node = BinaryOpNode(node, op.value, right, "LOGICA", op.line, op.column)

        return node

    def _expresion_logica_and(self) -> ASTNode:
        """
        expresion_logica_and -> termino_logico ( ( '&&' | 'and' ) termino_logico )*
        """
        node = self._termino_logico()

        while self._match(TokenType.OP_AND):
            op = self._previous()
            if self._is_at_end() or self._peek().type == TokenType.PARENTESIS_DER:
                self.error_handler.report_incomplete_logical_expression(
                    op.value, op.line, op.column,
                    suggestion=f"Falta el término lógico derecho tras el operador '{op.value}'."
                )
                right = ErrorNode("Término lógico faltante", op.line, op.column + len(op.value))
            elif self._peek().type in (TokenType.OP_AND, TokenType.OP_OR):
                next_op = self._advance()
                self.error_handler.report_incomplete_logical_expression(
                    op.value, op.line, op.column,
                    suggestion=f"Operadores lógicos consecutivos '{op.value}' y '{next_op.value}' inválidos."
                )
                right = self._termino_logico()
            else:
                right = self._termino_logico()

            node = BinaryOpNode(node, op.value, right, "LOGICA", op.line, op.column)

        return node

    def _termino_logico(self) -> ASTNode:
        """
        termino_logico -> expresion_aritmetica ( ( '==' | '!=' | '>' | '<' | '>=' | '<=' ) expresion_aritmetica )?
                        | '!' termino_logico
        """
        if self._match(TokenType.OP_NOT):
            op = self._previous()
            operand = self._termino_logico()
            return UnaryOpNode(op.value, operand, "LOGICA", op.line, op.column)

        # Analizar primer lado: expresión aritmética
        left = self._expresion_aritmetica()

        # Verificar si sigue un operador de comparación relacional
        if self._peek().is_relational_op():
            op = self._advance()
            
            # Verificar si falta la expresión derecha o si hay otro operador
            if self._is_at_end() or self._peek().type == TokenType.PARENTESIS_DER:
                self.error_handler.report_invalid_comparison(
                    op.line, op.column, op=op.value,
                    suggestion=f"Comparación incompleta: falta la expresión aritmética derecha tras '{op.value}'."
                )
                right = ErrorNode("Expresión aritmética derecha faltante", op.line, op.column + len(op.value))
            elif self._peek().is_relational_op():
                next_op = self._advance()
                self.error_handler.report_invalid_comparison(
                    op.line, op.column, op=f"{op.value} {next_op.value}",
                    suggestion=f"Operadores de comparación consecutivos '{op.value}' y '{next_op.value}' inválidos."
                )
                right = self._expresion_aritmetica()
            elif self._peek().is_logical_op():
                next_op = self._peek()
                self.error_handler.report_invalid_comparison(
                    op.line, op.column, op=op.value,
                    suggestion=f"Comparación sin expresión aritmética válida antes de '{next_op.value}'."
                )
                right = ErrorNode("Expresión faltante en comparación", op.line, op.column)
            else:
                right = self._expresion_aritmetica()

            return BinaryOpNode(left, op.value, right, "RELACIONAL", op.line, op.column)

        return left

    def _expresion_aritmetica(self) -> ASTNode:
        """
        expresion_aritmetica -> termino (( '+' | '-' ) termino)*
        """
        node = self._termino()

        while self._match(TokenType.OP_SUMA, TokenType.OP_RESTA):
            op = self._previous()

            # Caso de prueba específico: x + * y  o  x +
            if self._peek().type in (TokenType.OP_MULTIPLICACION, TokenType.OP_DIVISION, TokenType.OP_MODULO, TokenType.OP_POTENCIA):
                next_tok = self._advance()
                self.error_handler.report_operator_without_term(
                    op.value, op.line, op.column,
                    suggestion=f"Operador '{op.value}' sin término: no puede ir seguido del operador '{next_tok.value}'."
                )
                right = self._termino()
            elif self._is_at_end() or self._peek().type == TokenType.PARENTESIS_DER:
                self.error_handler.report_operator_without_term(
                    op.value, op.line, op.column,
                    suggestion=f"El operador '{op.value}' carece de término a la derecha."
                )
                right = ErrorNode("Término faltante", op.line, op.column + 1)
            else:
                right = self._termino()

            node = BinaryOpNode(node, op.value, right, "ARITMETICA", op.line, op.column)

        return node

    def _termino(self) -> ASTNode:
        """
        termino -> factor (( '*' | '/' | '%' | '^' ) factor)*
        """
        node = self._factor()

        while self._match(TokenType.OP_MULTIPLICACION, TokenType.OP_DIVISION, TokenType.OP_MODULO, TokenType.OP_POTENCIA):
            op = self._previous()

            if self._peek().is_arithmetic_op():
                next_tok = self._advance()
                self.error_handler.report_operator_without_term(
                    op.value, op.line, op.column,
                    suggestion=f"Operador '{op.value}' sin término: no puede ir seguido directamente de '{next_tok.value}'."
                )
                right = self._factor()
            elif self._is_at_end() or self._peek().type == TokenType.PARENTESIS_DER:
                self.error_handler.report_operator_without_term(
                    op.value, op.line, op.column,
                    suggestion=f"El operador '{op.value}' no tiene un factor o término derecho válido."
                )
                right = ErrorNode("Factor faltante", op.line, op.column + 1)
            else:
                right = self._factor()

            node = BinaryOpNode(node, op.value, right, "ARITMETICA", op.line, op.column)

        return node

    def _factor(self) -> ASTNode:
        """
        factor -> IDENTIFICADOR
                | NUMERO
                | '(' expresion ')'
                | '-' factor
                | '+' factor
        """
        # 1. Operador unario aritmético (+ o -)
        if self._match(TokenType.OP_RESTA, TokenType.OP_SUMA):
            op = self._previous()
            operand = self._factor()
            return UnaryOpNode(op.value, operand, "ARITMETICA", op.line, op.column)

        # 2. Literales Numéricos (Entero o Flotante)
        if self._match(TokenType.NUMERO_ENTERO):
            tok = self._previous()
            return NumberNode(tok.value, "entero", tok.line, tok.column)

        if self._match(TokenType.NUMERO_FLOTANTE):
            tok = self._previous()
            return NumberNode(tok.value, "flotante", tok.line, tok.column)

        # 3. Identificador
        if self._match(TokenType.IDENTIFICADOR):
            tok = self._previous()
            return IdentifierNode(tok.value, tok.line, tok.column)

        # 4. Agrupación entre paréntesis '(' expresion ')'
        if self._match(TokenType.PARENTESIS_IZQ):
            open_tok = self._previous()
            self.open_paren_stack.append(open_tok)

            # Caso especial: () paréntesis vacíos
            if self._check(TokenType.PARENTESIS_DER):
                self._advance()
                self.open_paren_stack.pop()
                self.error_handler.report_operator_without_term(
                    "( )", open_tok.line, open_tok.column,
                    suggestion="Paréntesis vacíos: se esperaba una expresión aritmética o lógica en su interior."
                )
                return ErrorNode("Expresión vacía en paréntesis", open_tok.line, open_tok.column)

            expr = self._expresion()

            if self._match(TokenType.PARENTESIS_DER):
                self.open_paren_stack.pop()
                return GroupedExprNode(expr, open_tok.line, open_tok.column)
            else:
                # Regla específica: Paréntesis desbalanceados
                self.error_handler.report_unbalanced_parentheses(
                    open_tok.line, open_tok.column,
                    suggestion=f"Falta el paréntesis de cierre ')' correspondiente abierto en la columna {open_tok.column}."
                )
                return GroupedExprNode(expr, open_tok.line, open_tok.column)

        # 5. Manejo de errores en factores no reconocidos o inesperados
        cur = self._peek()

        if cur.is_arithmetic_op():
            # Ejemplo: operador doble consecutivo no atrapado previamente
            self._advance()
            self.error_handler.report_operator_without_term(
                cur.value, cur.line, cur.column,
                suggestion=f"Operador inesperado '{cur.value}' sin factor previo válido."
            )
            return ErrorNode(f"Operador inesperado {cur.value}", cur.line, cur.column)

        if cur.is_relational_op():
            self._advance()
            self.error_handler.report_invalid_comparison(
                cur.line, cur.column, op=cur.value,
                suggestion=f"Operador relacional inesperado '{cur.value}' sin término aritmético válido."
            )
            return ErrorNode(f"Comparación inválida {cur.value}", cur.line, cur.column)

        if cur.type == TokenType.PARENTESIS_DER:
            # Paréntesis de cierre no esperado aquí
            return ErrorNode("Paréntesis de cierre inesperado", cur.line, cur.column)

        if self._is_at_end():
            prev = self._previous()
            self.error_handler.report_operator_without_term(
                prev.value, prev.line, prev.column,
                suggestion="La expresión termina de forma abrupta sin completar el factor requerido."
            )
            return ErrorNode("Fin inesperado de expresión", prev.line, prev.column)

        # Token desconocido o no válido
        self._advance()
        self.error_handler.report_general_syntax_error(
            "identificador, número o '('", cur.value, cur.line, cur.column
        )
        return ErrorNode(f"Token no válido '{cur.value}'", cur.line, cur.column)
