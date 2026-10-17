"""
================================================================================
ACTIVIDAD 9: ANÁLISIS SEMÁNTICO Y VERIFICACIÓN DE ESTRUCTURAS DE CONTROL,
             MÉTODOS Y CLASES
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
from error_handler import CompilerErrorHandler
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
    TryCatchNode,
    MethodCallNode,
    BlockNode,
    BinaryOpNode,
    UnaryOpNode,
    PostfixOpNode,
    IdentifierNode,
    LiteralNode
)


class Parser:
    """
    Analizador Sintáctico Descendente Recursivo para estructuras de control,
    métodos, clases y expresiones. Construye el AST garantizando la validación
    estructural y detección de errores de llaves, delimitadores y sintaxis.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    TYPE_KEYWORDS = {
        TokenType.KEYWORD_INT,
        TokenType.KEYWORD_FLOAT,
        TokenType.KEYWORD_VOID,
        TokenType.KEYWORD_CHAR,
        TokenType.KEYWORD_BOOLEAN,
        TokenType.KEYWORD_STRING
    }

    def __init__(self, tokens: List[Token], error_handler: Optional[CompilerErrorHandler] = None):
        self.tokens = tokens
        self.error_handler = error_handler or CompilerErrorHandler()
        self.pos = 0

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DE NAVEGACIÓN
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

    def _is_type_specifier(self, token: Token) -> bool:
        return token.type in self.TYPE_KEYWORDS

    # -------------------------------------------------------------------------
    # PUNTO DE ENTRADA PRINCIPAL: PARSE()
    # -------------------------------------------------------------------------

    def parse(self) -> ProgramNode:
        """
        Inicia el análisis sintáctico del programa completo.
        Gramática:
        programa -> ( clase | declaracion_metodo | declaracion_variable | sentencia )*
        """
        declarations: List[ASTNode] = []

        while not self._is_at_end():
            start_tok = self._current_token()

            # 1. Declaración de clase
            if self._check(TokenType.KEYWORD_CLASS):
                cls_node = self._parse_class_declaration()
                if cls_node:
                    declarations.append(cls_node)

            # 2. Declaración con 'function'
            elif self._check(TokenType.KEYWORD_FUNCTION):
                fn_node = self._parse_function_keyword_declaration()
                if fn_node:
                    declarations.append(fn_node)

            # 3. Declaración con 'let' o 'var'
            elif self._check(TokenType.KEYWORD_LET) or self._check(TokenType.KEYWORD_VAR):
                let_node = self._parse_let_var_declaration()
                if let_node:
                    declarations.append(let_node)

            # 4. Declaración formal iniciada por tipo ('int', 'float', etc.)
            elif self._is_type_specifier(start_tok):
                member = self._parse_method_or_variable()
                if member:
                    declarations.append(member)

            # 5. Sentencias sueltas o estructuras de control a nivel superior
            elif self._check(TokenType.KEYWORD_IF) or \
                 self._check(TokenType.KEYWORD_WHILE) or \
                 self._check(TokenType.KEYWORD_TRY) or \
                 self._check(TokenType.KEYWORD_RETURN) or \
                 self._check(TokenType.IDENTIFICADOR) or \
                 self._check(TokenType.LLAVE_IZQ):
                stmt = self._parse_statement()
                if stmt:
                    declarations.append(stmt)
            else:
                tok = self._advance()
                self.error_handler.report_syntax_error(
                    f"Símbolo inesperado '{tok.value}' a nivel superior.",
                    tok.line, tok.column,
                    suggestion="Verifique la estructura o declaración.",
                    offending=tok.value
                )
                self._synchronize()

        return ProgramNode(declarations, 1, 1)

    # -------------------------------------------------------------------------
    # DECLARACIÓN DE CLASE
    # -------------------------------------------------------------------------

    def _parse_class_declaration(self) -> Optional[ClassDeclarationNode]:
        class_kw = self._advance() # Consume 'class'
        name_tok = self._current_token()

        if name_tok.type != TokenType.IDENTIFICADOR:
            self.error_handler.report_syntax_error(
                f"Se esperaba el identificador de la clase después de 'class', pero se encontró '{name_tok.value}'.",
                name_tok.line, name_tok.column,
                suggestion="Proporcione un nombre válido para la clase (ej. 'class MiClase').",
                offending=name_tok.value
            )
            class_name = "<ClaseInvalida>"
        else:
            class_name = name_tok.value
            self._advance()

        if not self._check(TokenType.LLAVE_IZQ):
            tok = self._current_token()
            self.error_handler.report_syntax_error(
                f"Falta '{{' para iniciar el cuerpo de la clase '{class_name}'.",
                tok.line, tok.column,
                suggestion="Abra el cuerpo de la clase con '{'.",
                offending=tok.value
            )
            return ClassDeclarationNode(class_name, [], class_kw.line, class_kw.column)

        self._advance() # Consume '{'

        members: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            curr = self._current_token()
            if self._is_type_specifier(curr):
                member = self._parse_method_or_variable()
                if member:
                    members.append(member)
            elif curr.type == TokenType.KEYWORD_FUNCTION:
                fn = self._parse_function_keyword_declaration()
                if fn:
                    members.append(fn)
            else:
                # Intenta parsear como sentencia en clase o reporta
                stmt = self._parse_statement()
                if stmt:
                    members.append(stmt)

        if not self._check(TokenType.LLAVE_DER):
            curr = self._current_token()
            self.error_handler.report_missing_brace(
                curr.line, curr.column,
                structure=f"class {class_name}",
                suggestion=f"Cierre el cuerpo de la clase '{class_name}' con '}}'.",
                offending=curr.value
            )
        else:
            self._advance() # Consume '}'

        return ClassDeclarationNode(class_name, members, class_kw.line, class_kw.column)

    # -------------------------------------------------------------------------
    # DECLARACIÓN DE MÉTODO O VARIABLE CON TIPO ESPECIFICADO
    # -------------------------------------------------------------------------

    def _parse_method_or_variable(self) -> Optional[ASTNode]:
        type_tok = self._advance() # Consume tipo
        type_name = type_tok.value

        name_tok = self._current_token()
        if name_tok.type != TokenType.IDENTIFICADOR:
            self.error_handler.report_syntax_error(
                f"Se esperaba un identificador tras el tipo '{type_name}', pero se encontró '{name_tok.value}'.",
                name_tok.line, name_tok.column,
                suggestion=f"Especifique el nombre de la variable o método (ej. '{type_name} miMetodo').",
                offending=name_tok.value
            )
            self._advance()
            return None

        member_name = name_tok.value
        self._advance() # Consume nombre

        # Si viene '(', es una definición de método
        if self._check(TokenType.PARENTESIS_IZQ):
            return self._finish_method_declaration(type_name, member_name, type_tok.line, type_tok.column)

        # Si viene directamente '{', faltaron paréntesis en el método
        if self._check(TokenType.LLAVE_IZQ):
            curr = self._current_token()
            self.error_handler.report_missing_parenthesis(
                curr.line, curr.column,
                element=f"método '{member_name}'",
                suggestion=f"En el método '{member_name}', se omitieron los paréntesis '()' de los parámetros.",
                offending=curr.value
            )
            return self._parse_method_body_block(type_name, member_name, [], type_tok.line, type_tok.column)

        # Declaración de variable: opcionalmente inicializada
        initializer = None
        if self._match(TokenType.OP_ASIGNACION):
            initializer = self._parse_expression()

        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()
        else:
            tok = self._current_token()
            self.error_handler.report_syntax_error(
                f"Falta ';' al final de la declaración de la variable '{member_name}'.",
                tok.line, tok.column,
                suggestion="Agregue ';' para finalizar la sentencia.",
                offending=tok.value
            )

        return VariableDeclarationNode(type_name, member_name, initializer, type_tok.line, type_tok.column)

    # -------------------------------------------------------------------------
    # DECLARACIONES 'function' Y 'let' / 'var'
    # -------------------------------------------------------------------------

    def _parse_function_keyword_declaration(self) -> Optional[MethodDeclarationNode]:
        fn_tok = self._advance() # Consume 'function'
        curr = self._current_token()

        return_type = "any"
        # Permite 'function int sumar(...)' o 'function sumar(...)'
        if self._is_type_specifier(curr):
            return_type = curr.value
            self._advance()

        name_tok = self._current_token()
        if name_tok.type != TokenType.IDENTIFICADOR:
            self.error_handler.report_syntax_error(
                f"Se esperaba el nombre de la función después de 'function', se encontró '{name_tok.value}'.",
                name_tok.line, name_tok.column,
                offending=name_tok.value
            )
            return None

        fn_name = name_tok.value
        self._advance()

        if self._check(TokenType.PARENTESIS_IZQ):
            return self._finish_method_declaration(return_type, fn_name, fn_tok.line, fn_tok.column)
        else:
            self.error_handler.report_missing_parenthesis(
                name_tok.line, name_tok.column,
                element=f"función '{fn_name}'"
            )
            return self._parse_method_body_block(return_type, fn_name, [], fn_tok.line, fn_tok.column)

    def _parse_let_var_declaration(self) -> Optional[VariableDeclarationNode]:
        kw = self._advance() # Consume 'let' o 'var'
        name_tok = self._current_token()

        if name_tok.type != TokenType.IDENTIFICADOR:
            self.error_handler.report_syntax_error(
                f"Se esperaba el identificador de variable tras '{kw.value}', se encontró '{name_tok.value}'.",
                name_tok.line, name_tok.column,
                offending=name_tok.value
            )
            return None

        var_name = name_tok.value
        self._advance()

        initializer = None
        if self._match(TokenType.OP_ASIGNACION):
            initializer = self._parse_expression()

        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()

        # Las variables con 'let'/'var' usan tipo implícito 'any' que se infiere del inicializador
        return VariableDeclarationNode("any", var_name, initializer, kw.line, kw.column)

    # -------------------------------------------------------------------------
    # PARSEO DE PARÁMETROS Y CUERPO DE MÉTODO
    # -------------------------------------------------------------------------

    def _finish_method_declaration(self, return_type: str, name: str, line: int, col: int) -> MethodDeclarationNode:
        self._advance() # Consume '('

        parameters: List[ParameterNode] = []
        if not self._check(TokenType.PARENTESIS_DER):
            parameters = self._parse_parameters()

        if not self._check(TokenType.PARENTESIS_DER):
            curr = self._current_token()
            self.error_handler.report_missing_parenthesis(
                curr.line, curr.column,
                element=f"parámetros del método '{name}'",
                suggestion=f"Falta ')' de cierre en la lista de parámetros de '{name}'.",
                offending=curr.value
            )
        else:
            self._advance() # Consume ')'

        return self._parse_method_body_block(return_type, name, parameters, line, col)

    def _parse_parameters(self) -> List[ParameterNode]:
        params: List[ParameterNode] = []

        while not self._check(TokenType.PARENTESIS_DER) and not self._is_at_end():
            param = self._parse_single_parameter()
            if param:
                params.append(param)

            if self._match(TokenType.COMA):
                continue

            if self._check(TokenType.PARENTESIS_DER) or self._check(TokenType.LLAVE_IZQ):
                break

            # Detección de falta de coma entre parámetros: ej. 'int a float b'
            curr = self._current_token()
            if self._is_type_specifier(curr) or curr.type == TokenType.IDENTIFICADOR:
                self.error_handler.report_syntax_error(
                    f"Falta coma ',' entre los parámetros del método antes de '{curr.value}'.",
                    curr.line, curr.column,
                    suggestion=f"Separe los parámetros con una coma: ', {curr.value}'.",
                    offending=curr.value
                )
                continue

            self._advance()

        return params

    def _parse_single_parameter(self) -> Optional[ParameterNode]:
        tok = self._current_token()

        # Parámetro tipado: 'int a' o parámetro no tipado: 'a'
        if self._is_type_specifier(tok):
            param_type = tok.value
            self._advance()

            name_tok = self._current_token()
            if name_tok.type != TokenType.IDENTIFICADOR:
                self.error_handler.report_syntax_error(
                    f"Falta el identificador del parámetro de tipo '{param_type}'.",
                    name_tok.line, name_tok.column,
                    offending=name_tok.value
                )
                return ParameterNode(param_type, "<param_invalido>", tok.line, tok.column)

            param_name = name_tok.value
            self._advance()
            return ParameterNode(param_type, param_name, tok.line, tok.column)
        elif tok.type == TokenType.IDENTIFICADOR:
            # Parámetro tipo dinámico: 'a'
            param_name = tok.value
            self._advance()
            return ParameterNode("any", param_name, tok.line, tok.column)
        else:
            self.error_handler.report_syntax_error(
                f"Parámetro inválido '{tok.value}' en la definición del método.",
                tok.line, tok.column,
                offending=tok.value
            )
            self._advance()
            return None

    def _parse_method_body_block(self, return_type: str, name: str, parameters: List[ParameterNode], line: int, col: int) -> MethodDeclarationNode:
        if not self._check(TokenType.LLAVE_IZQ):
            tok = self._current_token()
            self.error_handler.report_missing_brace(
                tok.line, tok.column,
                structure=f"método '{name}'",
                suggestion=f"Falta '{{' para iniciar el cuerpo del método '{name}'.",
                offending=tok.value
            )
            return MethodDeclarationNode(return_type, name, parameters, [], line, col)

        self._advance() # Consume '{'

        body_statements: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body_statements.append(stmt)

        if not self._check(TokenType.LLAVE_DER):
            tok = self._current_token()
            self.error_handler.report_missing_brace(
                tok.line, tok.column,
                structure=f"método '{name}'",
                suggestion=f"Falta '}}' de cierre para el cuerpo del método '{name}'.",
                offending=tok.value
            )
        else:
            self._advance() # Consume '}'

        return MethodDeclarationNode(return_type, name, parameters, body_statements, line, col)

    # -------------------------------------------------------------------------
    # SENTENCIAS Y ESTRUCTURAS DE CONTROL
    # -------------------------------------------------------------------------

    def _parse_statement(self) -> Optional[ASTNode]:
        tok = self._current_token()

        if tok.type == TokenType.PUNTO_Y_COMA:
            self._advance()
            return None

        # Bloque compuesto '{' ... '}'
        if tok.type == TokenType.LLAVE_IZQ:
            return self._parse_block()

        # Retorno: 'return' expr? ';'
        if tok.type == TokenType.KEYWORD_RETURN:
            return self._parse_return_statement()

        # Condicional IF: 'if' '(' cond ')' bloque ('else' bloque)?
        if tok.type == TokenType.KEYWORD_IF:
            return self._parse_if_statement()

        # Ciclo WHILE: 'while' '(' cond ')' bloque
        if tok.type == TokenType.KEYWORD_WHILE:
            return self._parse_while_statement()

        # Manejo de excepciones: 'try' bloque 'catch' '(' id ')' bloque
        if tok.type == TokenType.KEYWORD_TRY:
            return self._parse_try_catch_statement()

        # Declaración 'let' / 'var'
        if tok.type in (TokenType.KEYWORD_LET, TokenType.KEYWORD_VAR):
            return self._parse_let_var_declaration()

        # Declaración con tipo especificado: 'int x = 10;'
        if self._is_type_specifier(tok):
            return self._parse_method_or_variable()

        # Identificador: Asignación, Llamada o Incremento/Decremento
        if tok.type == TokenType.IDENTIFICADOR:
            next_tok = self._peek_token(1)

            # Caso incremento postfijo: 'contador++;'
            if next_tok.type in (TokenType.OP_INCREMENTO, TokenType.OP_DECREMENTO):
                id_name = tok.value
                line, col = tok.line, tok.column
                self._advance() # Consume ID
                op_tok = self._advance() # Consume '++' o '--'
                if self._check(TokenType.PUNTO_Y_COMA):
                    self._advance()
                return PostfixOpNode(id_name, op_tok.value, line, col)

            # Caso llamada calificada: 'console.log(...);'
            if next_tok.type == TokenType.PUNTO:
                return self._parse_qualified_call_statement()

            # Caso llamada simple: 'sumar(5, 3);'
            if next_tok.type == TokenType.PARENTESIS_IZQ:
                return self._parse_call_statement()

            # Caso asignación: 'x = expr;'
            if next_tok.type == TokenType.OP_ASIGNACION:
                return self._parse_assignment_statement()

        # Si llegamos aquí, evaluamos como expresión general terminada en ';'
        expr = self._parse_expression()
        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()
        return expr

    def _parse_block(self) -> BlockNode:
        lbrace = self._advance() # Consume '{'
        statements: List[ASTNode] = []
        while not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            s = self._parse_statement()
            if s:
                statements.append(s)

        if not self._check(TokenType.LLAVE_DER):
            curr = self._current_token()
            self.error_handler.report_missing_brace(
                curr.line, curr.column,
                structure="bloque '{ ... }'",
                suggestion="Cierre el bloque de código con '}'.",
                offending=curr.value
            )
        else:
            self._advance()

        return BlockNode(statements, lbrace.line, lbrace.column)

    def _parse_return_statement(self) -> ReturnNode:
        ret_tok = self._advance() # Consume 'return'
        expr = None
        if not self._check(TokenType.PUNTO_Y_COMA) and not self._check(TokenType.LLAVE_DER) and not self._is_at_end():
            expr = self._parse_expression()

        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()
        else:
            tok = self._current_token()
            self.error_handler.report_syntax_error(
                "Falta ';' tras la sentencia 'return'.",
                tok.line, tok.column,
                suggestion="Coloque ';' al final de 'return'.",
                offending=tok.value
            )

        return ReturnNode(expr, ret_tok.line, ret_tok.column)

    def _parse_if_statement(self) -> IfNode:
        """
        Parseo de 'if' '(' condición ')' '{' then_body '}' ('else' '{' else_body '}')?
        Valida explícitamente la presencia obligatoria de llaves '{' y '}'.
        """
        if_tok = self._advance() # Consume 'if'

        # Paréntesis de apertura '('
        if not self._check(TokenType.PARENTESIS_IZQ):
            self.error_handler.report_missing_parenthesis(
                if_tok.line, if_tok.column,
                element="condición 'if'",
                suggestion="La condición del 'if' debe iniciar con '('."
            )
        else:
            self._advance()

        condition = self._parse_expression()

        # Paréntesis de cierre ')'
        if not self._check(TokenType.PARENTESIS_DER):
            tok = self._current_token()
            self.error_handler.report_missing_parenthesis(
                tok.line, tok.column,
                element="condición 'if'",
                suggestion="La condición del 'if' debe cerrarse con ')'."
            )
        else:
            self._advance()

        # REQUISITO OFICIAL DE RÚBRICA: Comprobación de llaves en la estructura if
        # Ejemplo del profesor: "if (x > 10) console.log(...); // Falta la llave de cierre"
        then_body: List[ASTNode] = []
        if not self._check(TokenType.LLAVE_IZQ):
            tok = self._current_token()
            self.error_handler.report_missing_brace(
                tok.line, tok.column,
                structure="if",
                suggestion="Asegúrese de abrir y cerrar el bloque con llaves: if (...) { ... }.",
                offending=tok.value
            )
            # Permite continuar parseando la sentencia individual
            single_stmt = self._parse_statement()
            if single_stmt:
                then_body.append(single_stmt)
        else:
            then_block = self._parse_block()
            then_body = then_block.statements

        # Rama opcional 'else'
        else_body: Optional[List[ASTNode]] = None
        if self._match(TokenType.KEYWORD_ELSE):
            if not self._check(TokenType.LLAVE_IZQ):
                tok = self._current_token()
                self.error_handler.report_missing_brace(
                    tok.line, tok.column,
                    structure="else",
                    suggestion="El bloque 'else' debe delimitarse con llaves '{ ... }'.",
                    offending=tok.value
                )
                single_else = self._parse_statement()
                else_body = [single_else] if single_else else []
            else:
                else_block = self._parse_block()
                else_body = else_block.statements

        return IfNode(condition, then_body, else_body, if_tok.line, if_tok.column)

    def _parse_while_statement(self) -> WhileNode:
        """
        Parseo de 'while' '(' condición ')' '{' cuerpo '}'.
        Valida que la condición esté entre paréntesis y el cuerpo delimitado por llaves.
        """
        while_tok = self._advance() # Consume 'while'

        if not self._check(TokenType.PARENTESIS_IZQ):
            self.error_handler.report_missing_parenthesis(
                while_tok.line, while_tok.column,
                element="condición 'while'",
                suggestion="La condición del ciclo 'while' debe iniciar con '('."
            )
        else:
            self._advance()

        condition = self._parse_expression()

        if not self._check(TokenType.PARENTESIS_DER):
            tok = self._current_token()
            self.error_handler.report_missing_parenthesis(
                tok.line, tok.column,
                element="condición 'while'",
                suggestion="La condición del ciclo 'while' debe cerrarse con ')'."
            )
        else:
            self._advance()

        body: List[ASTNode] = []
        if not self._check(TokenType.LLAVE_IZQ):
            tok = self._current_token()
            self.error_handler.report_missing_brace(
                tok.line, tok.column,
                structure="while",
                suggestion="El cuerpo del ciclo 'while' debe delimitarse con llaves '{ ... }'.",
                offending=tok.value
            )
            single_stmt = self._parse_statement()
            if single_stmt:
                body.append(single_stmt)
        else:
            block = self._parse_block()
            body = block.statements

        return WhileNode(condition, body, while_tok.line, while_tok.column)

    def _parse_try_catch_statement(self) -> TryCatchNode:
        """
        Parseo de 'try' '{' cuerpo_try '}' 'catch' '(' error_var ')' '{' cuerpo_catch '}'.
        """
        try_tok = self._advance() # Consume 'try'

        try_block = self._parse_block()

        if not self._check(TokenType.KEYWORD_CATCH):
            tok = self._current_token()
            self.error_handler.report_syntax_error(
                "Falta el bloque 'catch' correspondiente a la sentencia 'try'.",
                tok.line, tok.column,
                suggestion="Agregue 'catch (error) { ... }' después del bloque try.",
                offending=tok.value
            )
            return TryCatchNode(try_block.statements, "error", [], try_tok.line, try_tok.column)

        self._advance() # Consume 'catch'

        # Paréntesis de variable de error: '( error )'
        error_var = "error"
        if self._check(TokenType.PARENTESIS_IZQ):
            self._advance()
            if self._check(TokenType.IDENTIFICADOR):
                error_var = self._advance().value
            if self._check(TokenType.PARENTESIS_DER):
                self._advance()

        catch_block = self._parse_block()

        return TryCatchNode(try_block.statements, error_var, catch_block.statements, try_tok.line, try_tok.column)

    def _parse_assignment_statement(self) -> AssignmentNode:
        id_tok = self._advance() # Consume ID
        self._advance() # Consume '='

        expr = self._parse_expression()

        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()
        else:
            tok = self._current_token()
            self.error_handler.report_syntax_error(
                f"Falta ';' tras la asignación a '{id_tok.value}'.",
                tok.line, tok.column,
                suggestion="Agregue ';' al final de la asignación.",
                offending=tok.value
            )

        return AssignmentNode(id_tok.value, expr, id_tok.line, id_tok.column)

    def _parse_call_statement(self) -> MethodCallNode:
        call = self._parse_method_call_expr()
        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()
        return call

    def _parse_qualified_call_statement(self) -> MethodCallNode:
        obj_tok = self._advance() # ej. 'console'
        self._advance() # Consume '.'
        method_tok = self._advance() # ej. 'log' or 'error'

        call = self._finish_call_arguments(method_tok.value, target_object=obj_tok.value, line=obj_tok.line, col=obj_tok.column)
        if self._check(TokenType.PUNTO_Y_COMA):
            self._advance()
        return call

    # -------------------------------------------------------------------------
    # PARSEO DE EXPRESIONES (PRECEDENCIA COMPLETA)
    # -------------------------------------------------------------------------

    def _parse_expression(self) -> ASTNode:
        return self._parse_assignment_expr()

    def _parse_assignment_expr(self) -> ASTNode:
        expr = self._parse_logical_or()

        if self._match(TokenType.OP_ASIGNACION):
            op_tok = self._tokens_prev()
            value = self._parse_assignment_expr()
            if isinstance(expr, IdentifierNode):
                return AssignmentNode(expr.name, value, expr.line, expr.column)
            self.error_handler.report_syntax_error(
                "Destino inválido para la asignación.",
                op_tok.line, op_tok.column
            )

        return expr

    def _parse_logical_or(self) -> ASTNode:
        expr = self._parse_logical_and()
        while self._match(TokenType.OP_OR):
            op = self._tokens_prev().value
            right = self._parse_logical_and()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_logical_and(self) -> ASTNode:
        expr = self._parse_equality()
        while self._match(TokenType.OP_AND):
            op = self._tokens_prev().value
            right = self._parse_equality()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_equality(self) -> ASTNode:
        expr = self._parse_relational()
        while self._match(TokenType.OP_IGUAL, TokenType.OP_DIFERENTE):
            op = self._tokens_prev().value
            right = self._parse_relational()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_relational(self) -> ASTNode:
        expr = self._parse_additive()
        while self._match(TokenType.OP_MENOR, TokenType.OP_MENOR_IGUAL, TokenType.OP_MAYOR, TokenType.OP_MAYOR_IGUAL):
            op = self._tokens_prev().value
            right = self._parse_additive()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_additive(self) -> ASTNode:
        expr = self._parse_multiplicative()
        while self._match(TokenType.OP_SUMA, TokenType.OP_RESTA):
            op = self._tokens_prev().value
            right = self._parse_multiplicative()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_multiplicative(self) -> ASTNode:
        expr = self._parse_unary()
        while self._match(TokenType.OP_MULTIPLICACION, TokenType.OP_DIVISION, TokenType.OP_MODULO):
            op = self._tokens_prev().value
            right = self._parse_unary()
            expr = BinaryOpNode(expr, op, right, expr.line, expr.column)
        return expr

    def _parse_unary(self) -> ASTNode:
        if self._match(TokenType.OP_NOT, TokenType.OP_RESTA, TokenType.OP_SUMA):
            op = self._tokens_prev().value
            line, col = self._tokens_prev().line, self._tokens_prev().column
            operand = self._parse_unary()
            return UnaryOpNode(op, operand, line, col)
        return self._parse_postfix()

    def _parse_postfix(self) -> ASTNode:
        expr = self._parse_primary()
        if isinstance(expr, IdentifierNode) and self._match(TokenType.OP_INCREMENTO, TokenType.OP_DECREMENTO):
            op = self._tokens_prev().value
            return PostfixOpNode(expr.name, op, expr.line, expr.column)
        return expr

    def _parse_primary(self) -> ASTNode:
        tok = self._current_token()

        # Literales numéricos
        if tok.type == TokenType.NUMERO_ENTERO:
            self._advance()
            return LiteralNode(tok.literal_value if tok.literal_value is not None else int(tok.value), "int", tok.line, tok.column)

        if tok.type == TokenType.NUMERO_FLOTANTE:
            self._advance()
            return LiteralNode(tok.literal_value if tok.literal_value is not None else float(tok.value), "float", tok.line, tok.column)

        # Literales cadena
        if tok.type == TokenType.LITERAL_CADENA:
            self._advance()
            val = tok.literal_value if tok.literal_value is not None else tok.value.strip('"')
            return LiteralNode(val, "string", tok.line, tok.column)

        # Literales caracter
        if tok.type == TokenType.LITERAL_CARACTER:
            self._advance()
            val = tok.literal_value if tok.literal_value is not None else tok.value.strip("'")
            return LiteralNode(val, "char", tok.line, tok.column)

        # Literales booleanos
        if tok.type == TokenType.LITERAL_BOOLEANO:
            self._advance()
            val = (tok.value == "true")
            return LiteralNode(val, "boolean", tok.line, tok.column)

        # Identificador o Llamada a Método
        if tok.type == TokenType.IDENTIFICADOR:
            self._advance()
            # Llamada calificada: 'console.log(...)'
            if self._check(TokenType.PUNTO):
                self._advance() # Consume '.'
                sub_tok = self._advance()
                if self._check(TokenType.PARENTESIS_IZQ):
                    return self._finish_call_arguments(sub_tok.value, target_object=tok.value, line=tok.line, col=tok.column)
                return IdentifierNode(f"{tok.value}.{sub_tok.value}", tok.line, tok.column)

            # Llamada a método simple: 'sumar(...)'
            if self._check(TokenType.PARENTESIS_IZQ):
                return self._finish_call_arguments(tok.value, None, tok.line, tok.column)

            return IdentifierNode(tok.value, tok.line, tok.column)

        # Agrupación con paréntesis: '( expr )'
        if tok.type == TokenType.PARENTESIS_IZQ:
            self._advance()
            inner = self._parse_expression()
            if not self._check(TokenType.PARENTESIS_DER):
                self.error_handler.report_missing_parenthesis(
                    tok.line, tok.column,
                    element="expresión entre paréntesis",
                    suggestion="Falta ')' para cerrar la expresión agrupada."
                )
            else:
                self._advance()
            return inner

        # Token inesperado
        err_tok = self._advance()
        self.error_handler.report_syntax_error(
            f"Expresión inesperada o inválida: '{err_tok.value}'.",
            err_tok.line, err_tok.column,
            offending=err_tok.value
        )
        return LiteralNode(None, "error_type", err_tok.line, err_tok.column)

    def _parse_method_call_expr(self) -> MethodCallNode:
        name_tok = self._advance()
        return self._finish_call_arguments(name_tok.value, None, name_tok.line, name_tok.column)

    def _finish_call_arguments(self, method_name: str, target_object: Optional[str], line: int, col: int) -> MethodCallNode:
        self._advance() # Consume '('
        arguments: List[ASTNode] = []

        if not self._check(TokenType.PARENTESIS_DER):
            while True:
                arguments.append(self._parse_expression())
                if self._match(TokenType.COMA):
                    continue
                break

        if not self._check(TokenType.PARENTESIS_DER):
            curr = self._current_token()
            self.error_handler.report_missing_parenthesis(
                curr.line, curr.column,
                element=f"llamada a '{method_name}'",
                suggestion=f"Cierre los argumentos de la llamada a '{method_name}' con ')'."
            )
        else:
            self._advance()

        return MethodCallNode(method_name, arguments, target_object, line, col)

    def _tokens_prev(self) -> Token:
        if self.pos > 0:
            return self.tokens[self.pos - 1]
        return self.tokens[0]

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._tokens_prev().type == TokenType.PUNTO_Y_COMA:
                return
            if self._current_token().type in (
                TokenType.KEYWORD_CLASS,
                TokenType.KEYWORD_FUNCTION,
                TokenType.KEYWORD_IF,
                TokenType.KEYWORD_WHILE,
                TokenType.KEYWORD_RETURN
            ):
                return
            self._advance()
