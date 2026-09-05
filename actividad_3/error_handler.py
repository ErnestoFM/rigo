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

class SyntaxErrorItem:
    """
    Representa un error sintáctico individual con información contextual.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, message: str, line: int, column: int, suggestion: str = "", offending_token: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.offending_token = offending_token

    def __str__(self):
        base = f"Error: {self.message} en la línea {self.line}, columna {self.column}."
        if self.suggestion:
            base += f" {self.suggestion}"
        return base

class SyntaxErrorHandler:
    """
    Manejador centralizado de errores sintácticos.
    Captura, clasifica y formatea los errores encontrados durante el análisis sintáctico.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[SyntaxErrorItem] = []

    def add_error(self, message: str, line: int, column: int, suggestion: str = "", offending_token: str = ""):
        """Registra un nuevo error sintáctico."""
        error = SyntaxErrorItem(message, line, column, suggestion, offending_token)
        self.errors.append(error)

    def report_invalid_identifier(self, token_val: str, line: int, column: int):
        """
        Regla específica solicitada:
        'Error: Identificador inválido en la línea X, columna Y. Un identificador debe comenzar con una letra o guion bajo.'
        """
        msg = f"Identificador inválido '{token_val}'"
        sugg = "Un identificador debe comenzar con una letra o guion bajo."
        self.add_error(msg, line, column, sugg, token_val)

    def report_missing_semicolon(self, line: int, column: int):
        """
        Regla específica solicitada:
        'Error: Se esperaba ';' al final de la declaración en la línea X, columna Y.'
        """
        msg = "Se esperaba ';' al final de la declaración"
        sugg = "Asegúrese de terminar la instrucción con un punto y coma (;)."
        self.add_error(msg, line, column, sugg, ";")

    def report_invalid_type(self, found_token: str, line: int, column: int):
        """
        Regla específica solicitada:
        'Error: Tipo no válido en la línea X, columna Y. Los tipos válidos son 'entero', 'flotante', 'booleano', y 'cadena'.'
        """
        msg = f"Tipo no válido '{found_token}'"
        sugg = "Los tipos válidos son 'entero', 'flotante', 'booleano', y 'cadena'."
        self.add_error(msg, line, column, sugg, found_token)

    def report_uninitialized_constant(self, const_name: str, line: int, column: int):
        """
        Regla de constantes: Una constante debe ser inicializada obligatoriamente al declararse.
        """
        msg = f"La constante '{const_name}' debe ser inicializada con un valor"
        sugg = "Las constantes no pueden declararse sin un valor inicial (ej. constante entero MAX = 100;)."
        self.add_error(msg, line, column, sugg, const_name)

    def report_general_syntax_error(self, expected: str, found: str, line: int, column: int):
        """Reporta un error genérico de estructura sintáctica esperada vs encontrada."""
        msg = f"Error sintáctico: Se esperaba {expected}, pero se encontró '{found}'"
        sugg = f"Verifique la estructura de la sentencia alrededor del token '{found}'."
        self.add_error(msg, line, column, sugg, found)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def print_error_report(self):
        """Imprime una tabla elegante y estructurada con todos los errores sintácticos."""
        if not self.has_errors():
            print("\n  [OK] ANÁLISIS SINTÁCTICO EXITOSO: 0 errores detectados.")
            return

        print("\n" + "=" * 95)
        print(f"  [ERROR] REPORTE DE ERRORES SINTÁCTICOS DETECTADOS ({len(self.errors)} ERRORES):")
        print("=" * 95)
        header = f"| {'#':<3} | {'LÍNEA':<5} | {'COL':<4} | {'TOKEN':<12} | {'DESCRIPCIÓN DEL ERROR / SUGERENCIA':<60} |"
        divider = "+" + "-" * 5 + "+" + "-" * 7 + "+" + "-" * 6 + "+" + "-" * 14 + "+" + "-" * 62 + "+"
        print(divider)
        print(header)
        print(divider)

        for i, err in enumerate(self.errors, 1):
            tok_repr = repr(err.offending_token)[1:-1] if err.offending_token else "N/A"
            if len(tok_repr) > 10:
                tok_repr = tok_repr[:8] + ".."
            
            desc = str(err)
            # Acortar si es muy largo para la primera línea
            if len(desc) > 58:
                desc1 = desc[:58]
                desc2 = desc[58:]
                print(f"| {i:<3} | {err.line:<5} | {err.column:<4} | {tok_repr:<12} | {desc1:<60} |")
                print(f"| {' ':<3} | {' ':<5} | {' ':<4} | {' ':<12} | {desc2:<60} |")
            else:
                print(f"| {i:<3} | {err.line:<5} | {err.column:<4} | {tok_repr:<12} | {desc:<60} |")

        print(divider)
        print("=" * 95)
