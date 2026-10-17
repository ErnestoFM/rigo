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

from typing import List, Optional
from enum import Enum


class ErrorPhase(Enum):
    """Fase del compilador donde se detecta la anomalía."""
    LEXICA = "LÉXICA"
    SINTACTICA = "SINTÁCTICA"
    SEMANTICA = "SEMÁNTICA"
    FLUJO_CONTROL = "FLUJO DE CONTROL"


class CompilationError:
    """
    Representa un error o advertencia diagnosticado durante las fases de análisis
    (léxico, sintáctico, semántico o de flujo de control).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        phase: ErrorPhase,
        category: str,
        message: str,
        line: int,
        column: int,
        suggestion: str = "",
        offending_text: str = "",
        is_warning: bool = False
    ):
        self.phase = phase
        self.category = category
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.offending_text = offending_text
        self.is_warning = is_warning

    def __str__(self) -> str:
        nivel = "ADVERTENCIA" if self.is_warning else "ERROR"
        linea_str = f"Línea {self.line:2d}, Columna {self.column:2d}"
        res = f"[{nivel} {self.phase.value} - {self.category}] en {linea_str}: {self.message}"
        if self.offending_text:
            res += f" | Elemento afectado: '{self.offending_text}'"
        if self.suggestion:
            res += f"\n       --> Sugerencia de corrección: {self.suggestion}"
        return res

    def to_dict(self) -> dict:
        return {
            "phase": self.phase.value,
            "category": self.category,
            "level": "ADVERTENCIA" if self.is_warning else "ERROR",
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "offending": self.offending_text,
            "suggestion": self.suggestion
        }


class CompilerErrorHandler:
    """
    Gestor centralizado de errores y advertencias de compilación para el análisis
    sintáctico y semántico de estructuras de control, métodos y clases.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.errors: List[CompilationError] = []

    def clear(self):
        self.errors.clear()

    def has_errors(self) -> bool:
        return any(not e.is_warning for e in self.errors)

    def has_warnings(self) -> bool:
        return any(e.is_warning for e in self.errors)

    def get_errors(self) -> List[CompilationError]:
        return [e for e in self.errors if not e.is_warning]

    def get_warnings(self) -> List[CompilationError]:
        return [e for e in self.errors if e.is_warning]

    def add_error(
        self,
        phase: ErrorPhase,
        category: str,
        message: str,
        line: int,
        column: int,
        suggestion: str = "",
        offending_text: str = "",
        is_warning: bool = False
    ):
        err = CompilationError(
            phase=phase,
            category=category,
            message=message,
            line=line,
            column=column,
            suggestion=suggestion,
            offending_text=offending_text,
            is_warning=is_warning
        )
        self.errors.append(err)

    # -------------------------------------------------------------------------
    # MÉTODOS ESPECIALIZADOS PARA ERRORES SINTÁCTICOS
    # -------------------------------------------------------------------------

    def report_missing_brace(self, line: int, col: int, structure: str, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.SINTACTICA,
            category="FALTA_DE_LLAVE",
            message=f"Falta de llave en la estructura `{structure}`.",
            line=line,
            column=col,
            suggestion=suggestion or f"Asegúrese de cerrar adecuadamente el bloque con '}}' para `{structure}`.",
            offending_text=offending
        )

    def report_missing_parenthesis(self, line: int, col: int, element: str, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.SINTACTICA,
            category="PARENTESIS_FALTANTE",
            message=f"Falta de paréntesis en `{element}`.",
            line=line,
            column=col,
            suggestion=suggestion or "Verifique que todos los paréntesis '(' y ')' estén balanceados.",
            offending_text=offending
        )

    def report_syntax_error(self, message: str, line: int, col: int, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.SINTACTICA,
            category="SINTAXIS_INVALIDA",
            message=message,
            line=line,
            column=col,
            suggestion=suggestion,
            offending_text=offending
        )

    # -------------------------------------------------------------------------
    # MÉTODOS ESPECIALIZADOS PARA ERRORES SEMÁNTICOS (RÚBRICA ACTIVIDAD 9)
    # -------------------------------------------------------------------------

    def report_condition_type_error(self, line: int, col: int, structure: str, actual_type: str, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="CONDICION_LOGICA_INVALIDA",
            message=f"La condición en la estructura `{structure}` debe ser una expresión booleana (`boolean`), pero se obtuvo tipo `{actual_type}`.",
            line=line,
            column=col,
            suggestion=suggestion or f"Reemplace o compare la expresión para que evalúe a booleano (ej. {offending} != 0 o comparación relacional).",
            offending_text=offending
        )

    def report_infinite_loop(self, line: int, col: int, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.FLUJO_CONTROL,
            category="BUCLE_INFINITO",
            message="Bucle infinito detectado: la estructura iterativa posee una condición constante verdadera y no contiene condiciones de salida ni sentencias de escape.",
            line=line,
            column=col,
            suggestion=suggestion or "Agregue una variable de control con condición de parada o una instrucción de salida (break/return).",
            offending_text=offending,
            is_warning=False
        )

    def report_misplaced_return(self, line: int, col: int, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="RETURN_FUERA_DE_LUGAR",
            message="Sentencia 'return' fuera de lugar: solo está permitida dentro del cuerpo de un método o función.",
            line=line,
            column=col,
            suggestion=suggestion or "Mueva la instrucción 'return' dentro de un método válido o elimínela del ámbito global.",
            offending_text=offending
        )

    def report_unreachable_code(self, line: int, col: int, suggestion: str = "", offending: str = ""):
        self.add_error(
            phase=ErrorPhase.FLUJO_CONTROL,
            category="CODIGO_INALCANZABLE",
            message="Código inalcanzable (unreachable code) detectado tras una sentencia de escape incondicional ('return').",
            line=line,
            column=col,
            suggestion=suggestion or "Elimine el código posterior al return o reestructure el flujo lógico.",
            offending_text=offending,
            is_warning=False
        )

    def report_method_argument_count_mismatch(self, line: int, col: int, method_name: str, expected_count: int, actual_count: int, suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="NUMERO_ARGUMENTOS_INCORRECTO",
            message=f"Llamada al método `{method_name}` con {actual_count} argumento(s) en lugar de {expected_count}.",
            line=line,
            column=col,
            suggestion=suggestion or f"Proporcione exactamente {expected_count} argumento(s) según la definición del método.",
            offending_text=method_name
        )

    def report_method_argument_type_mismatch(self, line: int, col: int, method_name: str, param_name: str, expected_type: str, actual_type: str, arg_index: int, suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="TIPO_PARAMETRO_INCOMPATIBLE",
            message=f"Llamada incorrecta al método `{method_name}`: el argumento {arg_index} ('{param_name}') esperaba tipo `{expected_type}`, pero se pasó `{actual_type}`.",
            line=line,
            column=col,
            suggestion=suggestion or f"Convierta el argumento a `{expected_type}` o ajuste la signatura del método.",
            offending_text=f"{method_name}(arg {arg_index})"
        )

    def report_return_type_mismatch(self, line: int, col: int, method_name: str, expected_type: str, actual_type: str, suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="TIPO_RETORNO_INCOMPATIBLE",
            message=f"Tipo de retorno incorrecto en el método `{method_name}`: se esperaba `{expected_type}`, pero retorna `{actual_type}`.",
            line=line,
            column=col,
            suggestion=suggestion or f"Retorne un valor compatible con `{expected_type}` o cambie el tipo de retorno declarado.",
            offending_text=method_name
        )

    def report_void_method_returning_value(self, line: int, col: int, method_name: str, actual_type: str, suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="RETORNO_EN_METODO_VOID",
            message=f"El método `{method_name}` está declarado como `void` y no puede retornar un valor de tipo `{actual_type}`.",
            line=line,
            column=col,
            suggestion=suggestion or "Use 'return;' sin expresión o modifique el tipo de retorno del método.",
            offending_text=method_name
        )

    def report_undeclared_symbol(self, line: int, col: int, symbol_name: str, symbol_kind: str = "variable", suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="SIMBOLO_NO_DECLARADO",
            message=f"{symbol_kind.capitalize()} `{symbol_name}` no ha sido declarada en el ámbito accesible.",
            line=line,
            column=col,
            suggestion=suggestion or f"Declare '{symbol_name}' antes de su uso.",
            offending_text=symbol_name
        )

    def report_duplicate_symbol(self, line: int, col: int, symbol_name: str, symbol_kind: str = "variable", suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="SIMBOLO_DUPLICADO",
            message=f"Redeclaración de {symbol_kind} `{symbol_name}` en el mismo ámbito.",
            line=line,
            column=col,
            suggestion=suggestion or f"Use un nombre diferente para evitar colisión de identificadores.",
            offending_text=symbol_name
        )

    def report_type_mismatch_assignment(self, line: int, col: int, target_name: str, target_type: str, expr_type: str, suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="ASIGNACION_TIPO_INCOMPATIBLE",
            message=f"Incompatibilidad de tipos en la asignación a `{target_name}`: no se puede asignar tipo `{expr_type}` a una variable de tipo `{target_type}`.",
            line=line,
            column=col,
            suggestion=suggestion or f"Asegúrese de que el valor asignado sea compatible con `{target_type}`.",
            offending_text=target_name
        )

    def report_binary_op_type_error(self, line: int, col: int, op: str, left_type: str, right_type: str, suggestion: str = ""):
        self.add_error(
            phase=ErrorPhase.SEMANTICA,
            category="OPERADOR_TIPO_INCOMPATIBLE",
            message=f"El operador binario '{op}' no puede aplicarse a los operandos de tipo `{left_type}` y `{right_type}`.",
            line=line,
            column=col,
            suggestion=suggestion or "Utilice operandos con tipos numéricos compatibles.",
            offending_text=op
        )

    def format_console_report(self) -> str:
        """Formatea todos los diagnósticos en una tabla estética para consola."""
        if not self.errors:
            return "  ESTADO: [CORRECTO / EXITOSO] (0 Errores, 0 Advertencias)"

        lines = []
        tot_err = len(self.get_errors())
        tot_warn = len(self.get_warnings())
        lines.append(f"  DIAGNÓSTICO DEL ANALIZADOR ({tot_err} Errores, {tot_warn} Advertencias):")
        lines.append("  " + "─" * 95)
        for i, err in enumerate(self.errors, 1):
            icono = "❌" if not err.is_warning else "⚠️"
            lines.append(f"  {icono} [{i:02d}] {err}")
        lines.append("  " + "─" * 95)
        return "\n".join(lines)
