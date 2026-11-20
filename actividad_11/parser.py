"""
================================================================================
ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Optional, Any
from token_type import TokenType, Token
from error_handler import CompilerErrorHandler
from ast_nodes import (
    ASTNode,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    ParameterNode,
    VariableDeclarationNode,
    AssignmentNode,
    IfNode,
    SwitchNode,
    CaseNode,
    WhileNode,
    ForNode,
    DoWhileNode,
    ReturnNode,
    BreakNode,
    MethodCallNode,
    NewObjectNode,
    BinaryOpNode,
    UnaryOpNode,
    PostfixOpNode,
    IdentifierNode,
    LiteralNode,
    BlockNode
)


class Parser:
    """
    Analizador Sintáctico Descendente Recursivo para estructuras de control de flujo,
    bucles, switch-case, métodos y clases.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    TYPE_KEYWORDS = {
        TokenType.KEYWORD_INT,
        TokenType.KEYWORD_FLOAT,
        TokenType.KEYWORD_STRING,
        TokenType.KEYWORD_VOID,
        TokenType.KEYWORD_BOOL
    }

    def __init__(self, tokens: List[Token], error_handler: Optional[CompilerErrorHandler] = None):
        self.tokens = tokens
        self.error_handler = error_handler or CompilerErrorHandler()
        self.pos = 0

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES
    # -------------------------------------------------------------------------

    def _curr(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def _peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def _is_at_end(self) -> bool:
        return self._curr().type == TokenType.EOF

    def _advance(self) -> Token:
        tok = self._curr()
        if not self._is_at_end():
            self.pos += 1
        return tok

    def _check(self, type_: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._curr().type == type_

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, type_: TokenType, err_msg: str, suggestion: Optional[str] = None) -> Token:
        if self._check(type_):
            return self._advance()
        tok = self._curr()
        self.error_handler.report_syntax_error(err_msg, tok.line, tok.column, suggestion, offending=tok.value)
        return tok

    # -------------------------------------------------------------------------
    # PUNTO DE ENTRADA: PARSE()
    # -------------------------------------------------------------------------

    def parse(self) -> ProgramNode:
        declarations: List[ASTNode] = []
        while not self._is_at_end():
            node = self._parse_top_level_or_statement()
            if node:
                declarations.append(node)
            else:
                self._advance()
        return ProgramNode(declarations, 1, 1)

    def _parse_top_level_or_statement(self) -> Optional[ASTNode]:
        tok = self._curr()

        if tok.type == TokenType.PUNTO_Y_COMA:
            self._advance()
            return None

        # Definición de clase
        if tok.type == TokenType.KEYWORD_CLASS:
            return self._parse_class_declaration()

        # Estructura IF
        if tok.type == TokenType.KEYWORD_IF:
            return self._parse_if_statement()

        # Estructura SWITCH
        if tok.type == TokenType.KEYWORD_SWITCH:
            return self._parse_switch_statement()

        # Bucle WHILE
        if tok.type == TokenType.KEYWORD_WHILE:
            return self._parse_while_statement()

        # Bucle FOR
        if tok.type == TokenType.KEYWORD_FOR:
            return self._parse_for_statement()

        # Bucle DO-WHILE
        if tok.type == TokenType.KEYWORD_DO:
            return self._parse_do_while_statement()

        # Sentencia RETURN
        if tok.type == TokenType.KEYWORD_RETURN:
            return self._parse_return_statement()

        # Sentencia BREAK
        if tok.type == TokenType.KEYWORD_BREAK:
            b_tok = self._advance()
            self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' después de 'break'.")
            return BreakNode(b_tok.line, b_tok.column)

        # Bloque {...}
        if tok.type == TokenType.LLAVE_IZQ:
            return self._parse_block()

        # Tipo primitivo: int, float, void, string, bool
        if tok.type in self.TYPE_KEYWORDS:
            # Puede ser método 'int suma(...)' o variable 'int a = 5;'
            if self._peek(1).type == TokenType.IDENTIFICADOR and self._peek(2).type == TokenType.PARENTESIS_IZQ:
                return self._parse_method_declaration()
            return self._parse_variable_declaration()

        # Identificador al inicio: puede ser tipo de clase (Persona p = new Persona()),
        # llamada a método, asignación o llamada a objeto (p.celebrarCumpleaños())
        if tok.type == TokenType.IDENTIFICADOR:
            next1 = self._peek(1)
            # Caso 'Persona p = ...' o 'Persona p;'
            if next1.type == TokenType.IDENTIFICADOR:
                return self._parse_custom_type_variable_declaration()

            # Caso 'p.celebrarCumpleaños();' o 'p.edad = 10;'
            if next1.type == TokenType.PUNTO:
                return self._parse_dot_expression_statement()

            # Caso llamada a función directa: 'suma(5, 3);'
            if next1.type == TokenType.PARENTESIS_IZQ:
                call_node = self._parse_method_call()
                self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' después de la llamada a función.")
                return call_node

            # Caso incremento/decremento: 'i++;'
            if next1.type in (TokenType.OP_INCREMENTO, TokenType.OP_DECREMENTO):
                id_tok = self._advance()
                op_tok = self._advance()
                self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' después de la operación postfija.")
                return PostfixOpNode(id_tok.value, op_tok.value, id_tok.line, id_tok.column)

            # Caso asignación simple: 'z = x;'
            if next1.type == TokenType.OP_ASIGNACION:
                return self._parse_assignment_statement()

        # Expresión genérica evaluada como sentencia
        expr = self._parse_expression()
        self._match(TokenType.PUNTO_Y_COMA)
        return expr

    # -------------------------------------------------------------------------
    # CLASES Y MÉTODOS
    # -------------------------------------------------------------------------

    def _parse_class_declaration(self) -> ClassDeclarationNode:
        cls_tok = self._advance() # Consume 'class'
        name_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre de la clase tras 'class'.")
        self._consume(TokenType.LLAVE_IZQ, "Se esperaba '{' para iniciar el cuerpo de la clase.")

        members: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            mem = self._parse_class_member()
            if mem:
                members.append(mem)
            else:
                self._advance()

        self._consume(TokenType.LLAVE_DER, f"Se esperaba '}}' para cerrar la clase '{name_tok.value}'.")
        return ClassDeclarationNode(name_tok.value, members, cls_tok.line, cls_tok.column)

    def _parse_class_member(self) -> Optional[ASTNode]:
        tok = self._curr()
        if tok.type in self.TYPE_KEYWORDS or tok.type == TokenType.IDENTIFICADOR:
            if self._peek(1).type == TokenType.IDENTIFICADOR and self._peek(2).type == TokenType.PARENTESIS_IZQ:
                return self._parse_method_declaration()
            return self._parse_variable_declaration()
        return None

    def _parse_method_declaration(self) -> MethodDeclarationNode:
        ret_type_tok = self._advance()
        name_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre del método.")
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' tras el nombre del método.")

        parameters: List[ParameterNode] = []
        if not self._check(TokenType.PARENTESIS_DER):
            while True:
                p_type = self._advance()
                p_name = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre del parámetro.")
                parameters.append(ParameterNode(p_type.value, p_name.value, p_type.line, p_type.column))
                if not self._match(TokenType.COMA):
                    break

        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras la lista de parámetros.")
        self._consume(TokenType.LLAVE_IZQ, f"Se esperaba '{{' para el cuerpo del método '{name_tok.value}'.")

        body: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            stmt = self._parse_top_level_or_statement()
            if stmt:
                body.append(stmt)

        self._consume(TokenType.LLAVE_DER, f"Se esperaba '}}' para cerrar el cuerpo del método '{name_tok.value}'.")
        return MethodDeclarationNode(ret_type_tok.value, name_tok.value, parameters, body, ret_type_tok.line, ret_type_tok.column)

    def _parse_variable_declaration(self) -> VariableDeclarationNode:
        type_tok = self._advance()
        name_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre de la variable.")
        init_expr = None
        if self._match(TokenType.OP_ASIGNACION):
            init_expr = self._parse_expression()
        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' al final de la declaración de variable.")
        return VariableDeclarationNode(type_tok.value, name_tok.value, init_expr, type_tok.line, type_tok.column)

    def _parse_custom_type_variable_declaration(self) -> VariableDeclarationNode:
        type_tok = self._advance() # Tipo de clase (ej. Persona)
        name_tok = self._advance() # Nombre de variable (ej. p)
        init_expr = None
        if self._match(TokenType.OP_ASIGNACION):
            init_expr = self._parse_expression()
        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras la instanciación/declaración de variable.")
        return VariableDeclarationNode(type_tok.value, name_tok.value, init_expr, type_tok.line, type_tok.column)

    def _parse_dot_expression_statement(self) -> ASTNode:
        obj_tok = self._advance() # ej. 'p'
        self._advance() # Consume '.'
        member_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre del miembro tras '.'.")

        # Llamada a método de objeto: 'p.celebrarCumpleaños();'
        if self._check(TokenType.PARENTESIS_IZQ):
            self._advance()
            args: List[ASTNode] = []
            if not self._check(TokenType.PARENTESIS_DER):
                while True:
                    args.append(self._parse_expression())
                    if not self._match(TokenType.COMA):
                        break
            self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras los argumentos del método.")
            self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras la invocación del método.")
            return MethodCallNode(member_tok.value, args, obj_name=obj_tok.value, line=obj_tok.line, column=obj_tok.column)

        # Asignación a atributo de objeto: 'p.edad = 10;'
        if self._match(TokenType.OP_ASIGNACION):
            expr = self._parse_expression()
            self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras la asignación al atributo.")
            return AssignmentNode(member_tok.value, expr, is_field=True, obj_name=obj_tok.value, line=obj_tok.line, column=obj_tok.column)

        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras la sentencia.")
        return IdentifierNode(f"{obj_tok.value}.{member_tok.value}", obj_tok.line, obj_tok.column)

    def _parse_assignment_statement(self) -> AssignmentNode:
        id_tok = self._advance() # Consume ID
        self._advance() # Consume '='
        expr = self._parse_expression()
        self._consume(TokenType.PUNTO_Y_COMA, f"Se esperaba ';' tras la asignación a '{id_tok.value}'.")
        return AssignmentNode(id_tok.value, expr, line=id_tok.line, column=id_tok.column)

    def _parse_return_statement(self) -> ReturnNode:
        ret_tok = self._advance()
        expr = None
        if not self._check(TokenType.PUNTO_Y_COMA):
            expr = self._parse_expression()
        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras 'return'.")
        return ReturnNode(expr, ret_tok.line, ret_tok.column)

    # -------------------------------------------------------------------------
    # ESTRUCTURAS DE CONTROL DE FLUJO
    # -------------------------------------------------------------------------

    def _parse_if_statement(self) -> IfNode:
        if_tok = self._advance() # Consume 'if'
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' para la condición del 'if'.")
        cond = self._parse_expression()
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' para cerrar la condición del 'if'.")

        then_block = self._parse_statement_or_block()
        else_block = None
        if self._match(TokenType.KEYWORD_ELSE):
            else_block = self._parse_statement_or_block()

        return IfNode(cond, then_block, else_block, if_tok.line, if_tok.column)

    def _parse_switch_statement(self) -> SwitchNode:
        sw_tok = self._advance() # Consume 'switch'
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' tras 'switch'.")
        expr = self._parse_expression()
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras la expresión del 'switch'.")
        self._consume(TokenType.LLAVE_IZQ, "Se esperaba '{' para iniciar el cuerpo del 'switch'.")

        cases: List[CaseNode] = []
        default_block: Optional[List[ASTNode]] = None

        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            if self._match(TokenType.KEYWORD_CASE):
                case_val = self._parse_expression()
                self._consume(TokenType.DOS_PUNTOS, "Se esperaba ':' tras el valor del case.")
                case_body: List[ASTNode] = []
                has_break = False
                while not self._check(TokenType.KEYWORD_CASE) and not self._check(TokenType.KEYWORD_DEFAULT) and not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
                    if self._check(TokenType.KEYWORD_BREAK):
                        self._advance()
                        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras 'break'.")
                        has_break = True
                        break
                    stmt = self._parse_top_level_or_statement()
                    if stmt:
                        case_body.append(stmt)
                cases.append(CaseNode(case_val, case_body, has_break, case_val.line, case_val.column))
            elif self._match(TokenType.KEYWORD_DEFAULT):
                self._consume(TokenType.DOS_PUNTOS, "Se esperaba ':' tras 'default'.")
                def_body: List[ASTNode] = []
                while not self._check(TokenType.KEYWORD_CASE) and not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
                    if self._check(TokenType.KEYWORD_BREAK):
                        self._advance()
                        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras 'break'.")
                        break
                    stmt = self._parse_top_level_or_statement()
                    if stmt:
                        def_body.append(stmt)
                default_block = def_body
            else:
                self._advance()

        self._consume(TokenType.LLAVE_DER, "Se esperaba '}' para cerrar el 'switch'.")
        return SwitchNode(expr, cases, default_block, sw_tok.line, sw_tok.column)

    def _parse_while_statement(self) -> WhileNode:
        wh_tok = self._advance()
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' para la condición del 'while'.")
        cond = self._parse_expression()
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras la condición del 'while'.")
        body = self._parse_statement_or_block()
        return WhileNode(cond, body, wh_tok.line, wh_tok.column)

    def _parse_for_statement(self) -> ForNode:
        for_tok = self._advance()
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' para el bucle 'for'.")

        # Inicialización: 'int i = 0;' o 'i = 0;' o ';'
        init = None
        if not self._check(TokenType.PUNTO_Y_COMA):
            if self._curr().type in self.TYPE_KEYWORDS:
                type_tok = self._advance()
                name_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre de variable en for.")
                self._consume(TokenType.OP_ASIGNACION, "Se esperaba '=' en inicialización de for.")
                val_expr = self._parse_expression()
                init = VariableDeclarationNode(type_tok.value, name_tok.value, val_expr, type_tok.line, type_tok.column)
            elif self._curr().type == TokenType.IDENTIFICADOR and self._peek(1).type == TokenType.OP_ASIGNACION:
                name_tok = self._advance()
                self._advance() # Consume '='
                val_expr = self._parse_expression()
                init = AssignmentNode(name_tok.value, val_expr, line=name_tok.line, column=name_tok.column)
        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras la inicialización del 'for'.")

        # Condición: 'i < 5;'
        cond = None
        if not self._check(TokenType.PUNTO_Y_COMA):
            cond = self._parse_expression()
        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' tras la condición del 'for'.")

        # Actualización: 'i++' o 'i = i + 1'
        update = None
        if not self._check(TokenType.PARENTESIS_DER):
            if self._curr().type == TokenType.IDENTIFICADOR and self._peek(1).type in (TokenType.OP_INCREMENTO, TokenType.OP_DECREMENTO):
                id_tok = self._advance()
                op_tok = self._advance()
                update = PostfixOpNode(id_tok.value, op_tok.value, id_tok.line, id_tok.column)
            elif self._curr().type == TokenType.IDENTIFICADOR and self._peek(1).type == TokenType.OP_ASIGNACION:
                name_tok = self._advance()
                self._advance()
                val_expr = self._parse_expression()
                update = AssignmentNode(name_tok.value, val_expr, line=name_tok.line, column=name_tok.column)
            else:
                update = self._parse_expression()

        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras las cláusulas del 'for'.")
        body = self._parse_statement_or_block()
        return ForNode(init, cond, update, body, for_tok.line, for_tok.column)

    def _parse_do_while_statement(self) -> DoWhileNode:
        do_tok = self._advance() # Consume 'do'
        body = self._parse_statement_or_block()
        self._consume(TokenType.KEYWORD_WHILE, "Se esperaba 'while' tras el cuerpo del 'do'.")
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' para la condición del 'do-while'.")
        cond = self._parse_expression()
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras la condición del 'do-while'.")
        self._consume(TokenType.PUNTO_Y_COMA, "Se esperaba ';' al final del 'do-while'.")
        return DoWhileNode(body, cond, do_tok.line, do_tok.column)

    def _parse_block(self) -> BlockNode:
        lbrace = self._consume(TokenType.LLAVE_IZQ, "Se esperaba '{'.")
        stmts: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            s = self._parse_top_level_or_statement()
            if s:
                stmts.append(s)
        self._consume(TokenType.LLAVE_DER, "Se esperaba '}'.")
        return BlockNode(stmts, lbrace.line, lbrace.column)

    def _parse_statement_or_block(self) -> List[ASTNode]:
        if self._check(TokenType.LLAVE_IZQ):
            block = self._parse_block()
            return block.statements
        stmt = self._parse_top_level_or_statement()
        return [stmt] if stmt else []

    # -------------------------------------------------------------------------
    # EXPRESIONES
    # -------------------------------------------------------------------------

    def _parse_expression(self) -> ASTNode:
        return self._parse_logical_or()

    def _parse_logical_or(self) -> ASTNode:
        expr = self._parse_logical_and()
        while self._match(TokenType.OP_OR):
            op = "||"
            right = self._parse_logical_and()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_logical_and(self) -> ASTNode:
        expr = self._parse_equality()
        while self._match(TokenType.OP_AND):
            op = "&&"
            right = self._parse_equality()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_equality(self) -> ASTNode:
        expr = self._parse_relational()
        while self._check(TokenType.OP_IGUAL) or self._check(TokenType.OP_DIFERENTE):
            op_tok = self._advance()
            right = self._parse_relational()
            expr = BinaryOpNode(expr, op_tok.value, right, expr.line, expr.column)
        return expr

    def _parse_relational(self) -> ASTNode:
        expr = self._parse_additive()
        while self._check(TokenType.OP_MENOR) or self._check(TokenType.OP_MENOR_IGUAL) or \
              self._check(TokenType.OP_MAYOR) or self._check(TokenType.OP_MAYOR_IGUAL):
            op_tok = self._advance()
            right = self._parse_additive()
            expr = BinaryOpNode(expr, op_tok.value, right, expr.line, expr.column)
        return expr

    def _parse_additive(self) -> ASTNode:
        expr = self._parse_multiplicative()
        while self._check(TokenType.OP_SUMA) or self._check(TokenType.OP_RESTA):
            op_tok = self._advance()
            right = self._parse_multiplicative()
            expr = BinaryOpNode(expr, op_tok.value, right, expr.line, expr.column)
        return expr

    def _parse_multiplicative(self) -> ASTNode:
        expr = self._parse_unary()
        while self._check(TokenType.OP_MULTIPLICACION) or self._check(TokenType.OP_DIVISION) or self._check(TokenType.OP_MODULO):
            op_tok = self._advance()
            right = self._parse_unary()
            expr = BinaryOpNode(expr, op_tok.value, right, expr.line, expr.column)
        return expr

    def _parse_unary(self) -> ASTNode:
        if self._check(TokenType.OP_RESTA) or self._check(TokenType.OP_NOT):
            op_tok = self._advance()
            right = self._parse_unary()
            return UnaryOpNode(op_tok.value, right, op_tok.line, op_tok.column)
        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        tok = self._curr()

        # Instanciación 'new Clase()'
        if tok.type == TokenType.KEYWORD_NEW:
            new_tok = self._advance()
            cls_name_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre de la clase tras 'new'.")
            self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' tras el nombre de la clase.")
            args: List[ASTNode] = []
            if not self._check(TokenType.PARENTESIS_DER):
                while True:
                    args.append(self._parse_expression())
                    if not self._match(TokenType.COMA):
                        break
            self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' para cerrar los argumentos del constructor.")
            return NewObjectNode(cls_name_tok.value, args, new_tok.line, new_tok.column)

        # Literales simples
        if tok.type == TokenType.NUMERO_ENTERO:
            self._advance()
            return LiteralNode(tok.literal, "int", tok.line, tok.column)

        if tok.type == TokenType.NUMERO_FLOTANTE:
            self._advance()
            return LiteralNode(tok.literal, "float", tok.line, tok.column)

        if tok.type == TokenType.CADENA_TEXTO:
            self._advance()
            return LiteralNode(tok.literal, "string", tok.line, tok.column)

        if tok.type == TokenType.BOOLEANO:
            self._advance()
            return LiteralNode(tok.literal, "bool", tok.line, tok.column)

        # Identificador o llamada
        if tok.type == TokenType.IDENTIFICADOR:
            next1 = self._peek(1)
            # Llamada a método 'suma(5, 3)'
            if next1.type == TokenType.PARENTESIS_IZQ:
                return self._parse_method_call()
            # Acceso a atributo de objeto 'p.edad'
            if next1.type == TokenType.PUNTO:
                obj_tok = self._advance()
                self._advance() # '.'
                mem_tok = self._consume(TokenType.IDENTIFICADOR, "Se esperaba el nombre del atributo tras '.'.")
                return IdentifierNode(f"{obj_tok.value}.{mem_tok.value}", obj_tok.line, obj_tok.column)
            # Operación postfija 'i++'
            if next1.type in (TokenType.OP_INCREMENTO, TokenType.OP_DECREMENTO):
                id_tok = self._advance()
                op_tok = self._advance()
                return PostfixOpNode(id_tok.value, op_tok.value, id_tok.line, id_tok.column)

            self._advance()
            return IdentifierNode(tok.value, tok.line, tok.column)

        # Paréntesis agrupados: '( expr )'
        if tok.type == TokenType.PARENTESIS_IZQ:
            self._advance()
            expr = self._parse_expression()
            self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras la expresión.")
            return expr

        self.error_handler.report_syntax_error(
            f"Expresión inesperada o inválida: '{tok.value}'.",
            tok.line, tok.column,
            offending=tok.value
        )
        self._advance()
        return LiteralNode(0, "int", tok.line, tok.column)

    def _parse_method_call(self) -> MethodCallNode:
        name_tok = self._advance() # Consume callee name
        self._consume(TokenType.PARENTESIS_IZQ, "Se esperaba '(' en la llamada a método.")
        args: List[ASTNode] = []
        if not self._check(TokenType.PARENTESIS_DER):
            while True:
                args.append(self._parse_expression())
                if not self._match(TokenType.COMA):
                    break
        self._consume(TokenType.PARENTESIS_DER, "Se esperaba ')' tras los argumentos de la llamada.")
        return MethodCallNode(name_tok.value, args, None, name_tok.line, name_tok.column)
