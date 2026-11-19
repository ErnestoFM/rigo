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

from typing import List


class SyntaxErrorItem:
    """
    Representa un error sintáctico con su ubicación y descripción estandarizada.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, message: str, line: int, column: int, category: str = "ERROR SINTÁCTICO", suggestion: str = "", offending_token: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.category = category
        self.suggestion = suggestion
        self.offending_token = offending_token

    def __str__(self) -> str:
        base = f"Error: {self.message} en la línea {self.line}, columna {self.column}."
        if self.suggestion:
            base += f" {self.suggestion}"
        return base


class SyntaxErrorHandler:
    """
    Manejador centralizado de errores sintácticos para métodos y clases.
    Garantiza el cumplimiento exacto de la nomenclatura y reglas de la rúbrica oficial.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[SyntaxErrorItem] = []

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def add_error(self, message: str, line: int, column: int, category: str = "ERROR SINTÁCTICO", suggestion: str = "", offending_token: str = ""):
        error = SyntaxErrorItem(message, line, column, category, suggestion, offending_token)
        self.errors.append(error)

    # -------------------------------------------------------------------------
    # REGLAS ESPECÍFICAS REQUERIDAS POR LA RÚBRICA DEL PROFESOR
    # -------------------------------------------------------------------------

    def report_invalid_class_body(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Regla oficial:
        'Error: Cuerpo de clase inválido en la declaración de 'class' en la línea X, columna Y.'
        """
        msg = "Cuerpo de clase inválido en la declaración de 'class'"
        sugg = suggestion or "Asegúrese de abrir '{' y cerrar '}' el cuerpo de la clase con declaraciones válidas de métodos o variables."
        self.add_error(msg, line, column, category="CUERPO_CLASE_INVALIDO", suggestion=sugg, offending_token=offending)

    def report_invalid_return_type(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Regla oficial:
        'Error: Tipo de retorno inválido en la declaración de método en la línea X, columna Y.'
        """
        msg = "Tipo de retorno inválido en la declaración de método"
        sugg = suggestion or "El tipo de retorno debe ser 'int', 'float', 'void', 'char', 'boolean' o un identificador de clase."
        self.add_error(msg, line, column, category="TIPO_RETORNO_INVALIDO", suggestion=sugg, offending_token=offending)

    def report_invalid_parameter(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Regla oficial:
        'Error: Parámetro inválido en la declaración de método en la línea X, columna Y.'
        """
        msg = "Parámetro inválido en la declaración de método"
        sugg = suggestion or "Cada parámetro debe tener la forma 'tipo identificador' (e.g. 'int a') y estar separados por coma."
        self.add_error(msg, line, column, category="PARAMETRO_INVALIDO", suggestion=sugg, offending_token=offending)

    def report_missing_comma_parameters(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Variante detallada del ejemplo de la práctica (int a float b):
        'Error: Parámetro inválido en la declaración de método en la línea X, columna Y. Falta coma entre parámetros.'
        """
        msg = "Parámetro inválido en la declaración de método"
        sugg = suggestion or "Falta una coma ',' para separar las definiciones de parámetros consecutivos."
        self.add_error(msg, line, column, category="FALTA_COMA_PARAMETROS", suggestion=sugg, offending_token=offending)

    def report_missing_parenthesis(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Variante del ejemplo de la práctica (void otroMetodo { // Faltan paréntesis):
        'Error: Falta paréntesis en la declaración de método en la línea X, columna Y.'
        """
        msg = "Falta paréntesis en la declaración de método"
        sugg = suggestion or "La declaración del método requiere paréntesis obligatorios '(' y ')' para la lista de parámetros."
        self.add_error(msg, line, column, category="FALTAN_PARENTESIS", suggestion=sugg, offending_token=offending)

    def report_unbalanced_braces(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Reporta llaves '{' o '}' no cerradas o desbalanceadas.
        """
        msg = "Llaves desbalanceadas o falta '}' de cierre"
        sugg = suggestion or "Verifique que todos los bloques de clase y método estén correctamente cerrados con '}'."
        self.add_error(msg, line, column, category="LLAVES_DESBALANCEADAS", suggestion=sugg, offending_token=offending)

    def report_invalid_statement(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Reporta una sentencia inválida en el cuerpo de un método.
        """
        msg = "Sentencia inválida en el cuerpo del método"
        sugg = suggestion or "Asegúrese de usar sentencias válidas (asignación, retorno, llamada a método, declaración local o control de flujo)."
        self.add_error(msg, line, column, category="SENTENCIA_INVALIDA", suggestion=sugg, offending_token=offending)

    def report_missing_class_name(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Reporta falta de nombre de clase.
        """
        msg = "Falta identificador (nombre) en la declaración de clase"
        sugg = suggestion or "La palabra clave 'class' debe ser seguida por un identificador válido (e.g. 'class MiClase')."
        self.add_error(msg, line, column, category="NOMBRE_CLASE_INVALIDO", suggestion=sugg, offending_token=offending)

    def report_missing_semicolon(self, line: int, column: int, suggestion: str = "", offending: str = ""):
        """
        Reporta falta de punto y coma al final de una sentencia o variable.
        """
        msg = "Falta ';' al final de la instrucción"
        sugg = suggestion or "Cada declaración de variable o sentencia simple debe terminar con punto y coma ';'."
        self.add_error(msg, line, column, category="FALTA_PUNTO_Y_COMA", suggestion=sugg, offending_token=offending)
