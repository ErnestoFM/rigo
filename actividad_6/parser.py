"""
================================================================================
ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES
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
from error_handler import SyntaxErrorHandler
from ast_nodes import (
    ASTNode,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    ParameterNode,
    VariableDeclarationNode,
    AssignmentNode,
    ReturnNode,
    IfNode,
    WhileNode,
    MethodCallNode,
    BlockNode,
    BinaryOpNode,
    UnaryOpNode,
    IdentifierNode,
    LiteralNode
)


class Parser:
    """
    Analizador Sintáctico Descendente Recursivo para definición de métodos y clases.
    Construye el AST completo y gestiona la captura y reporte de errores sintácticos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, tokens: List[Token], error_handler: Optional[SyntaxErrorHandler] = None):
        self.tokens = tokens
        self.error_handler = error_handler or SyntaxErrorHandler()
        self.pos = 0

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DE NAVEGACIÓN Y CONSUMO DE TOKENS
    # -------------------------------------------------------------------------

    def _current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def _peek_token(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def _is_at_end(self) -> bool:
        return self._current_token().type == TokenType.EOF

    def _advance(self) -> Token:
        token = self._current_token()
        if not self._is_at_end():
            self.pos += 1
        return token

    def _check(self, type_: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._current_token().type == type_

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, type_: TokenType, error_message: str) -> Optional[Token]:
        if self._check(type_):
            return self._advance()
        tok = self._current_token()
        self.error_handler.add_error(error_message, tok.line, tok.column, offending_token=tok.value)
        return None

    # -------------------------------------------------------------------------
    # PUNTO DE ENTRADA PRINCIPAL: PARSE()
    # -------------------------------------------------------------------------

    def parse(self) -> ProgramNode:
        """
        Inicia el análisis sintáctico del programa.
        Gramática:
        programa -> ( clase | declaracion_metodo | declaracion_variable )*
        """
        declarations: List[ASTNode] = []

        while not self._is_at_end():
            start_tok = self._current_token()

            if self._check(TokenType.KEYWORD_CLASS):
                cls_node = self._parse_class_declaration()
                if cls_node:
                    declarations.append(cls_node)
            elif self._is_type_specifier(start_tok):
                # Permite métodos o variables declarados a nivel superior
                member = self._parse_method_or_variable()
                if member:
                    declarations.append(member)
            else:
                tok = self._advance()
                self.error_handler.report_invalid_class_body(
                    tok.line, tok.column,
                    suggestion=f"Se esperaba 'class' o una definición válida, pero se encontró '{tok.value}'.",
                    offending=tok.value
                )
                self._synchronize()

        return ProgramNode(declarations, 1, 1)

    # -------------------------------------------------------------------------
    # REGLA: CLASE -> 'class' identificador '{' cuerpo_clase '}'
    # -------------------------------------------------------------------------

    def _parse_class_declaration(self) -> Optional[ClassDeclarationNode]:
        class_kw = self._advance() # Consume 'class'
        name_tok = self._current_token()

        if name_tok.type != TokenType.IDENTIFICADOR:
            self.error_handler.report_missing_class_name(
                name_tok.line, name_tok.column,
                suggestion=f"Se esperaba el identificador de la clase después de 'class', se encontró '{name_tok.value}'.",
                offending=name_tok.value
            )
            class_name = "<ClaseInvalida>"
            if not self._check(TokenType.LLAVE_IZQ) and not self._is_at_end():
                self._advance()
        else:
            class_name = name_tok.value
            self._advance()

        # Verificar apertura de cuerpo '{'
        if not self._check(TokenType.LLAVE_IZQ):
            tok = self._current_token()
            self.error_handler.report_invalid_class_body(
                tok.line, tok.column,
                suggestion="Se esperaba '{' para iniciar el cuerpo de la clase.",
                offending=tok.value
            )
            # Intentar sincronizar hasta '{' o siguiente declaración
            while not self._check(TokenType.LLAVE_IZQ) and not self._check(TokenType.KEYWORD_CLASS) and not self._is_at_end():
                self._advance()
            if not self._check(TokenType.LLAVE_IZQ):
                return None

        self._advance() # Consume '{'

        # cuerpo_clase -> ( declaracion_metodo | declaracion_variable )*
        members: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            member = self._parse_class_member()
            if member:
                members.append(member)

        if not self._check(TokenType.LLAVE_DER):
            last_tok = self._current_token()
            self.error_handler.report_unbalanced_braces(
                last_tok.line, last_tok.column,
                suggestion=f"Falta '}}' de cierre para el cuerpo de la clase '{class_name}'.",
                offending=last_tok.value
            )
        else:
            self._advance() # Consume '}'

        return ClassDeclarationNode(class_name, members, class_kw.line, class_kw.column)

    def _parse_class_member(self) -> Optional[ASTNode]:
        """
        Analiza un miembro dentro de la clase (método o variable).
        Identifica tipos de retorno inválidos, llaves extras o sentencias fuera de lugar.
        """
        tok = self._current_token()

        # Caso: punto y coma suelto
        if tok.type == TokenType.PUNTO_Y_COMA:
            self._advance()
            return None

        # Si inicia con un tipo válido:
        if self._is_type_specifier(tok):
            return self._parse_method_or_variable()

        # Detección específica de error: Tipo de retorno inválido
        # e.g. "123 miMetodo(int a)" o "miMetodo(int a)"
        next_tok = self._peek_token(1)
        if tok.type == TokenType.IDENTIFICADOR and next_tok.type == TokenType.PARENTESIS_IZQ:
            # Caso como "miMetodo(int a)" sin tipo de retorno o constructor
            self.error_handler.report_invalid_return_type(
                tok.line, tok.column,
                suggestion=f"El método '{tok.value}' carece de tipo de retorno explícito (e.g. 'void', 'int').",
                offending=tok.value
            )
            # Lo interpretamos como método con tipo de retorno implícito para seguir
            return self._parse_method_declaration("void")

        # Otro token inválido como número o símbolo
        self.error_handler.report_invalid_return_type(
            tok.line, tok.column,
            suggestion=f"Se encontró '{tok.value}' en lugar de un tipo de retorno válido ('int', 'float', 'void', etc.).",
            offending=tok.value
        )
        self._synchronize_member()
        return None

    def _parse_method_or_variable(self) -> Optional[ASTNode]:
        """
        Determina si una declaración iniciada con un tipo es un método o una variable:
        tipo identificador '(' ... -> método
        tipo identificador '{' ... -> método al que le faltan paréntesis (caso inválido del profe)
        tipo identificador ';' ... -> variable
        tipo identificador '=' ... -> variable con asignación
        """
        type_tok = self._advance() # Consume tipo
        type_name = type_tok.value

        name_tok = self._current_token()
        if name_tok.type != TokenType.IDENTIFICADOR:
            # Error: falta identificador
            if name_tok.type == TokenType.PUNTO_Y_COMA:
                self.error_handler.report_invalid_parameter(
                    name_tok.line, name_tok.column,
                    suggestion=f"Se declaró el tipo '{type_name}' pero falta el nombre del identificador.",
                    offending=name_tok.value
                )
                self._advance()
                return None
            else:
                self.error_handler.report_invalid_return_type(
                    type_tok.line, type_tok.column,
                    suggestion=f"Se esperaba un nombre de método o variable después de '{type_name}', pero se encontró '{name_tok.value}'.",
                    offending=name_tok.value
                )
                self._synchronize_member()
                return None

        member_name = name_tok.value
        self._advance() # Consume identificador

        # 1. Caso de Método estándar: seguido de '('
        if self._check(TokenType.PARENTESIS_IZQ):
            return self._finish_method_declaration(type_name, member_name, type_tok.line, type_tok.column)

        # 2. Caso oficial del profesor: "void otroMetodo { // Faltan paréntesis"
        if self._check(TokenType.LLAVE_IZQ):
            curr = self._current_token()
            self.error_handler.report_missing_parenthesis(
                curr.line, curr.column,
                suggestion=f"En el método '{member_name}', se omitieron los paréntesis '()' de los parámetros.",
                offending=curr.value
            )
            # Continuamos parseando el cuerpo del método
            return self._parse_method_body_block(type_name, member_name, [], type_tok.line, type_tok.column)

        # 3. Caso de Variable: seguido de '=' o ';' o ','
        if self._check(TokenType.PUNTO_Y_COMA) or self._check(TokenType.OP_ASIGNACION):
            initializer = None
            if self._match(TokenType.OP_ASIGNACION):
                initializer = self._parse_expression()

            if not self._check(TokenType.PUNTO_Y_COMA):
                tok = self._current_token()
                self.error_handler.report_missing_semicolon(
                    tok.line, tok.column,
                    suggestion=f"Falta ';' al final de la declaración de '{member_name}'.",
                    offending=tok.value
                )
            else:
                self._advance() # Consume ';'

            return VariableDeclarationNode(type_name, member_name, initializer, type_tok.line, type_tok.column)

        # Caso inválido no previsto
        tok = self._current_token()
        self.error_handler.report_invalid_class_body(
            tok.line, tok.column,
            suggestion=f"Sintaxis inesperada después de '{type_name} {member_name}': '{tok.value}'.",
            offending=tok.value
        )
        self._synchronize_member()
        return None

    # -------------------------------------------------------------------------
    # REGLA: DECLARACION_METODO -> tipo identificador '(' parametros ')' '{' cuerpo_metodo '}'
    # -------------------------------------------------------------------------

    def _finish_method_declaration(self, return_type: str, name: str, line: int, col: int) -> MethodDeclarationNode:
        self._advance() # Consume '('

        # parametros -> ( parametro ( ',' parametro )* )?
        parameters: List[ParameterNode] = []
        if not self._check(TokenType.PARENTESIS_DER):
            parameters = self._parse_parameters()

        if not self._check(TokenType.PARENTESIS_DER):
            curr = self._current_token()
            self.error_handler.report_missing_parenthesis(
                curr.line, curr.column,
                suggestion=f"Falta ')' de cierre en la lista de parámetros del método '{name}'.",
                offending=curr.value
            )
            # Si encontramos '{', avanzamos a parsear el cuerpo
            if not self._check(TokenType.LLAVE_IZQ) and not self._is_at_end():
                self._advance()
        else:
            self._advance() # Consume ')'

        return self._parse_method_body_block(return_type, name, parameters, line, col)

    def _parse_method_body_block(self, return_type: str, name: str, parameters: List[ParameterNode], line: int, col: int) -> MethodDeclarationNode:
        if not self._check(TokenType.LLAVE_IZQ):
            tok = self._current_token()
            self.error_handler.report_invalid_class_body(
                tok.line, tok.column,
                suggestion=f"Falta '{{' para iniciar el cuerpo del método '{name}'.",
                offending=tok.value
            )
            return MethodDeclarationNode(return_type, name, parameters, [], line, col)

        self._advance() # Consume '{'

        # cuerpo_metodo -> ( sentencia )*
        body_statements: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body_statements.append(stmt)

        if not self._check(TokenType.LLAVE_DER):
            tok = self._current_token()
            self.error_handler.report_unbalanced_braces(
                tok.line, tok.column,
                suggestion=f"Falta '}}' de cierre para el cuerpo del método '{name}'.",
                offending=tok.value
            )
        else:
            self._advance() # Consume '}'

        return MethodDeclarationNode(return_type, name, parameters, body_statements, line, col)

    # -------------------------------------------------------------------------
    # REGLA: PARAMETROS -> ( parametro ( ',' parametro )* )?
    # REGLA: PARAMETRO -> tipo identificador
    # -------------------------------------------------------------------------

    def _parse_parameters(self) -> List[ParameterNode]:
        params: List[ParameterNode] = []

        while not self._check(TokenType.PARENTESIS_DER) and not self._is_at_end():
            param = self._parse_single_parameter()
            if param:
                params.append(param)

            # Caso normal: coma separadora
            if self._match(TokenType.COMA):
                # Verificar si es una coma colgante al final: (int a, )
                if self._check(TokenType.PARENTESIS_DER):
                    curr = self._current_token()
                    self.error_handler.report_invalid_parameter(
                        curr.line, curr.column,
                        suggestion="Coma sobrante al final de la lista de parámetros sin parámetro posterior.",
                        offending=curr.value
                    )
                    break
                continue

            # Si ya se cierra el paréntesis: terminar
            if self._check(TokenType.PARENTESIS_DER) or self._check(TokenType.LLAVE_IZQ):
                break

            # CASO OFICIAL DEL PROFESOR: "int miMetodo(int a float b)"
            # Falta coma entre parámetros: el siguiente token es otro tipo válido
            curr = self._current_token()
            if self._is_type_specifier(curr):
                self.error_handler.report_missing_comma_parameters(
                    curr.line, curr.column,
                    suggestion=f"Falta coma ',' antes del parámetro '{curr.value}'.",
                    offending=curr.value
                )
                continue # Continúa para parsear el siguiente parámetro

            # Cualquier otro token no esperado en los parámetros
            self.error_handler.report_invalid_parameter(
                curr.line, curr.column,
                suggestion=f"Símbolo inesperado '{curr.value}' dentro de la lista de parámetros.",
                offending=curr.value
            )
            self._advance()

        return params

    def _parse_single_parameter(self) -> Optional[ParameterNode]:
        tok = self._current_token()

        if not self._is_type_specifier(tok):
            self.error_handler.report_invalid_parameter(
                tok.line, tok.column,
                suggestion=f"Se esperaba un tipo de parámetro ('int', 'float', etc.), pero se encontró '{tok.value}'.",
                offending=tok.value
            )
            self._advance()
            return None

        param_type = tok.value
        self._advance() # Consume tipo

        name_tok = self._current_token()
        if name_tok.type != TokenType.IDENTIFICADOR:
            # Caso como: "void procesar(int)" -> falta nombre de variable
            self.error_handler.report_invalid_parameter(
                name_tok.line, name_tok.column,
                suggestion=f"Falta el identificador del parámetro para el tipo '{param_type}'.",
                offending=name_tok.value
            )
            return ParameterNode(param_type, "<param_invalido>", tok.line, tok.column)

        param_name = name_tok.value
        self._advance() # Consume nombre

        return ParameterNode(param_type, param_name, tok.line, tok.column)

    # -------------------------------------------------------------------------
    # REGLA: CUERPO_METODO -> ( SENTENCIA )*
    # -------------------------------------------------------------------------

    def _parse_statement(self) -> Optional[ASTNode]:
        tok = self._current_token()

        # 1. Punto y coma suelto
        if tok.type == TokenType.PUNTO_Y_COMA:
            self._advance()
            return None

        # 2. Bloque anidado '{' ... '}'
        if tok.type == TokenType.LLAVE_IZQ:
            return self._parse_block()

        # 3. Retorno: 'return' expr? ';'
        if tok.type == TokenType.KEYWORD_RETURN:
            return self._parse_return_statement()

        # 4. Condicional IF: 'if' '(' cond ')' stmt ('else' stmt)?
        if tok.type == TokenType.KEYWORD_IF:
            return self._parse_if_statement()

        # 5. Ciclo WHILE: 'while' '(' cond ')' stmt
        if tok.type == TokenType.KEYWORD_WHILE:
            return self._parse_while_statement()

        # 6. Declaración de variable local: tipo id ('=' expr)? ';'
        if self._is_type_specifier(tok):
            return self._parse_variable_declaration()

        # 7. Asignación o Llamada a Método iniciada con un identificador
        if tok.type == TokenType.IDENTIFICADOR:
            next_tok = self._peek_token(1)
            if next_tok.type == TokenType.OP_ASIGNACION:
                return self._parse_assignment_statement()
            elif next_tok.type == TokenType.PARENTESIS_IZQ:
                return self._parse_call_statement()

        # Sentencia no válida
        self.error_handler.report_invalid_statement(
            tok.line, tok.column,
            suggestion=f"La sentencia que inicia con '{tok.value}' no es válida en el cuerpo del método.",
            offending=tok.value
        )
        self._synchronize_statement()
        return None

    def _parse_block(self) -> BlockNode:
        lbrace = self._advance() # Consume '{'
        statements: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            s = self._parse_statement()
            if s:
                statements.append(s)

        if not self._check(TokenType.LLAVE_DER):
            curr = self._current_token()
            self.error_handler.report_unbalanced_braces(
                curr.line, curr.column,
                suggestion="Falta '}' de cierre para el bloque.",
                offending=curr.value
            )
        else:
            self._advance()

        return BlockNode(statements, lbrace.line, lbrace.column)

    def _parse_return_statement(self) -> ReturnNode:
        ret_tok = self._advance() # Consume 'return'
        expr = None
        if not self._check(TokenType.PUNTO_Y_COMA):
            expr = self._parse_expression()

        if not self._check(TokenType.PUNTO_Y_COMA):
            curr = self._current_token()
            self.error_handler.report_missing_semicolon(
                curr.line, curr.column,
                suggestion="Falta ';' al final de la sentencia return.",
                offending=curr.value
            )
        else:
            self._advance()

        return ReturnNode(expr, ret_tok.line, ret_tok.column)

    def _parse_if_statement(self) -> IfNode:
        if_tok = self._advance() # Consume 'if'
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' después de 'if'")
        condition = self._parse_expression()
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' después de la condición del 'if'")

        then_branch: List[ASTNode] = []
        if self._check(TokenType.LLAVE_IZQ):
            then_branch = self._parse_block().statements
        else:
            s = self._parse_statement()
            if s:
                then_branch.append(s)

        else_branch = None
        if self._match(TokenType.KEYWORD_ELSE):
            else_branch = []
            if self._check(TokenType.LLAVE_IZQ):
                else_branch = self._parse_block().statements
            else:
                s = self._parse_statement()
                if s:
                    else_branch.append(s)

        return IfNode(condition, then_branch, else_branch, if_tok.line, if_tok.column)

    def _parse_while_statement(self) -> WhileNode:
        w_tok = self._advance() # Consume 'while'
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' después de 'while'")
        condition = self._parse_expression()
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' después de la condición del 'while'")

        body: List[ASTNode] = []
        if self._check(TokenType.LLAVE_IZQ):
            body = self._parse_block().statements
        else:
            s = self._parse_statement()
            if s:
                body.append(s)

        return WhileNode(condition, body, w_tok.line, w_tok.column)

    def _parse_variable_declaration(self) -> Optional[VariableDeclarationNode]:
        type_tok = self._advance()
        name_tok = self._current_token()
        if name_tok.type != TokenType.IDENTIFICADOR:
            self.error_handler.report_invalid_statement(
                name_tok.line, name_tok.column,
                suggestion=f"Se esperaba identificador después del tipo '{type_tok.value}', pero se encontró '{name_tok.value}'.",
                offending=name_tok.value
            )
            self._synchronize_statement()
            return None

        var_name = name_tok.value
        self._advance()

        initializer = None
        if self._match(TokenType.OP_ASIGNACION):
            initializer = self._parse_expression()

        if not self._check(TokenType.PUNTO_Y_COMA):
            curr = self._current_token()
            self.error_handler.report_missing_semicolon(
                curr.line, curr.column,
                suggestion=f"Falta ';' al final de la declaración de la variable '{var_name}'.",
                offending=curr.value
            )
        else:
            self._advance()

        return VariableDeclarationNode(type_tok.value, var_name, initializer, type_tok.line, type_tok.column)

    def _parse_assignment_statement(self) -> AssignmentNode:
        id_tok = self._advance() # Consume identificador
        self._advance() # Consume '='
        expr = self._parse_expression()

        if not self._check(TokenType.PUNTO_Y_COMA):
            curr = self._current_token()
            self.error_handler.report_missing_semicolon(
                curr.line, curr.column,
                suggestion=f"Falta ';' al final de la asignación a '{id_tok.value}'.",
                offending=curr.value
            )
        else:
            self._advance()

        return AssignmentNode(id_tok.value, expr, id_tok.line, id_tok.column)

    def _parse_call_statement(self) -> MethodCallNode:
        id_tok = self._advance() # Consume identificador
        self._advance() # Consume '('

        args: List[ASTNode] = []
        if not self._check(TokenType.PARENTESIS_DER):
            while True:
                args.append(self._parse_expression())
                if not self._match(TokenType.COMA):
                    break

        self._consume(TokenType.PARENTESIS_DER, f"Falta ')' al llamar al método '{id_tok.value}'")

        if not self._check(TokenType.PUNTO_Y_COMA):
            curr = self._current_token()
            self.error_handler.report_missing_semicolon(
                curr.line, curr.column,
                suggestion=f"Falta ';' al final de la llamada al método '{id_tok.value}'.",
                offending=curr.value
            )
        else:
            self._advance()

        return MethodCallNode(id_tok.value, args, id_tok.line, id_tok.column)

    # -------------------------------------------------------------------------
    # EXPRESIONES SINTÁCTICAS (ARITMÉTICAS, RELACIONALES Y LÓGICAS)
    # -------------------------------------------------------------------------

    def _parse_expression(self) -> ASTNode:
        return self._parse_logical_or()

    def _parse_logical_or(self) -> ASTNode:
        expr = self._parse_logical_and()
        while self._check(TokenType.OP_OR):
            op_tok = self._advance()
            right = self._parse_logical_and()
            expr = BinaryOpNode(expr, op_tok.value, right, op_tok.line, op_tok.column)
        return expr

    def _parse_logical_and(self) -> ASTNode:
        expr = self._parse_equality()
        while self._check(TokenType.OP_AND):
            op_tok = self._advance()
            right = self._parse_equality()
            expr = BinaryOpNode(expr, op_tok.value, right, op_tok.line, op_tok.column)
        return expr

    def _parse_equality(self) -> ASTNode:
        expr = self._parse_relational()
        while self._check(TokenType.OP_IGUAL) or self._check(TokenType.OP_DIFERENTE):
            op_tok = self._advance()
            right = self._parse_relational()
            expr = BinaryOpNode(expr, op_tok.value, right, op_tok.line, op_tok.column)
        return expr

    def _parse_relational(self) -> ASTNode:
        expr = self._parse_additive()
        while self._check(TokenType.OP_MENOR) or self._check(TokenType.OP_MENOR_IGUAL) or \
              self._check(TokenType.OP_MAYOR) or self._check(TokenType.OP_MAYOR_IGUAL):
            op_tok = self._advance()
            right = self._parse_additive()
            expr = BinaryOpNode(expr, op_tok.value, right, op_tok.line, op_tok.column)
        return expr

    def _parse_additive(self) -> ASTNode:
        expr = self._parse_multiplicative()
        while self._check(TokenType.OP_SUMA) or self._check(TokenType.OP_RESTA):
            op_tok = self._advance()
            right = self._parse_multiplicative()
            expr = BinaryOpNode(expr, op_tok.value, right, op_tok.line, op_tok.column)
        return expr

    def _parse_multiplicative(self) -> ASTNode:
        expr = self._parse_unary()
        while self._check(TokenType.OP_MULTIPLICACION) or self._check(TokenType.OP_DIVISION) or self._check(TokenType.OP_MODULO):
            op_tok = self._advance()
            right = self._parse_unary()
            expr = BinaryOpNode(expr, op_tok.value, right, op_tok.line, op_tok.column)
        return expr

    def _parse_unary(self) -> ASTNode:
        if self._check(TokenType.OP_NOT) or self._check(TokenType.OP_RESTA) or self._check(TokenType.OP_SUMA):
            op_tok = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(op_tok.value, operand, op_tok.line, op_tok.column)
        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        tok = self._current_token()

        if tok.type in (TokenType.NUMERO_ENTERO, TokenType.NUMERO_FLOTANTE):
            self._advance()
            return LiteralNode(tok.value, tok.type.name, tok.line, tok.column)

        if tok.type in (TokenType.LITERAL_CADENA, TokenType.LITERAL_CARACTER, TokenType.LITERAL_BOOLEANO):
            self._advance()
            return LiteralNode(tok.value, tok.type.name, tok.line, tok.column)

        if tok.type == TokenType.IDENTIFICADOR:
            self._advance()
            if self._match(TokenType.PARENTESIS_IZQ):
                # Llamada como expresión f(x)
                args = []
                if not self._check(TokenType.PARENTESIS_DER):
                    while True:
                        args.append(self._parse_expression())
                        if not self._match(TokenType.COMA):
                            break
                self._consume(TokenType.PARENTESIS_DER, f"Falta ')' en llamada a '{tok.value}'")
                return MethodCallNode(tok.value, args, tok.line, tok.column)
            return IdentifierNode(tok.value, tok.line, tok.column)

        if self._match(TokenType.PARENTESIS_IZQ):
            expr = self._parse_expression()
            self._consume(TokenType.PARENTESIS_DER, "Falta ')' de cierre en la subexpresión")
            return expr

        # Fallback para token inesperado en expresión
        self.error_handler.report_invalid_statement(
            tok.line, tok.column,
            suggestion=f"Expresión inesperada o término faltante cerca de '{tok.value}'.",
            offending=tok.value
        )
        self._advance()
        return LiteralNode("<error>", "ERROR", tok.line, tok.column)

    # -------------------------------------------------------------------------
    # RECUPERACIÓN DE ERRORES Y MÉTODOS DE APOYO
    # -------------------------------------------------------------------------

    def _is_type_specifier(self, token: Token) -> bool:
        """Determina si el token es un tipo válido."""
        return token.is_type_specifier()

    def _synchronize(self):
        """Avanza tokens hasta encontrar un límite seguro de declaración."""
        self._advance()
        while not self._is_at_end():
            if self._current_token().type == TokenType.KEYWORD_CLASS:
                return
            if self._current_token().type == TokenType.LLAVE_DER:
                self._advance()
                return
            self._advance()

    def _synchronize_member(self):
        """Avanza tokens hasta el siguiente miembro de clase o cierre."""
        while not self._is_at_end():
            if self._current_token().type in (TokenType.PUNTO_Y_COMA, TokenType.LLAVE_DER):
                self._advance()
                return
            if self._is_type_specifier(self._current_token()) or self._current_token().type == TokenType.KEYWORD_CLASS:
                return
            self._advance()

    def _synchronize_statement(self):
        """Avanza tokens hasta el final de la sentencia."""
        while not self._is_at_end():
            if self._current_token().type in (TokenType.PUNTO_Y_COMA, TokenType.LLAVE_DER):
                self._advance()
                return
            self._advance()
