"""
================================================================================
ACTIVIDAD 12: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Dict, Set, Optional, Tuple
from tac_instruction import TACInstruction
from error_handler import CompilerErrorHandler


class TACOptimizer:
    """
    Optimizador de Código Intermedio de Tres Direcciones (TAC).
    Aplica técnicas estándar de optimización de compiladores:
    1. Eliminación de Instrucciones Inalcanzables (tras saltos incondicionales).
    2. Eliminación de Asignaciones Innecesarias / Sobrescritas (Dead Store Elimination).
    3. Eliminación de Cálculos Repetidos (Common Subexpression Elimination - CSE).
    4. Plegado y Propagación de Constantes y Copias (Constant Folding & Propagation).
    5. Eliminación de Variables y Código Muerto (Dead Code Elimination).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_handler: Optional[CompilerErrorHandler] = None):
        self.error_handler = error_handler or CompilerErrorHandler()

    def optimize(self, instructions: List[TACInstruction], critical_vars: Optional[Set[str]] = None) -> List[TACInstruction]:
        """
        Ejecuta todas las fases de optimización en múltiples pasadas hasta alcanzar
        un punto fijo (donde no se produzcan más cambios).
        """
        current_instrs = [instr for instr in instructions if instr.op != "COMMENT"]

        # Verificación semántica previa: etiquetas existentes y variables no inicializadas
        self._verify_intermediate_code(current_instrs)
        if self.error_handler.has_errors:
            return current_instrs

        # Definir variables críticas que no deben ser eliminadas (ej. 'result', 'return_value')
        crit_vars = critical_vars if critical_vars is not None else {"result", "return_value"}

        # Iterar hasta alcanzar punto fijo
        max_iterations = 10
        iteration = 0
        changed = True

        while changed and iteration < max_iterations:
            iteration += 1
            before_len = len(current_instrs)
            before_str = [str(i) for i in current_instrs]

            # 1. Eliminación de código inalcanzable
            current_instrs = self.eliminate_unreachable_code(current_instrs)

            # 2. Eliminación de asignaciones sobrescritas inmediatamente
            current_instrs = self.eliminate_dead_stores(current_instrs)

            # 3. Plegado y propagación de constantes y copias
            current_instrs = self.propagate_and_fold_constants(current_instrs)

            # 4. Eliminación de cálculos repetidos (CSE)
            current_instrs = self.eliminate_common_subexpressions(current_instrs)

            # 5. Eliminación de variables no utilizadas (DCE)
            current_instrs = self.eliminate_dead_variables(current_instrs, crit_vars)

            after_str = [str(i) for i in current_instrs]
            changed = (before_str != after_str)

        return current_instrs

    # -------------------------------------------------------------------------
    # VERIFICACIÓN SEMÁNTICA PREVIA
    # -------------------------------------------------------------------------

    def _verify_intermediate_code(self, instructions: List[TACInstruction]):
        defined_labels: Set[str] = set()
        defined_vars: Set[str] = set()

        for instr in instructions:
            if instr.is_label or instr.op == "LABEL":
                lbl = instr.result or instr.arg1
                if lbl:
                    defined_labels.add(lbl.rstrip(":"))

        # Detección de saltos a etiquetas inexistentes y variables no inicializadas
        for line_idx, instr in enumerate(instructions, start=1):
            if instr.is_jump():
                target = instr.result
                if target and target not in defined_labels:
                    self.error_handler.report_error(
                        "Error Semántico de Control de Flujo",
                        f"Salto hacia etiqueta inexistente '{target}'.",
                        line=line_idx,
                        suggestion=f"Defina la etiqueta '{target}:' o corrija el destino del salto."
                    )

            # Verificar lectura de variables no inicializadas
            used = instr.get_used_vars()
            for v in used:
                # Comprobar si la variable fue definida previamente (o si es parámetro externo común)
                if v not in defined_vars and v not in ("a", "b", "c", "x", "y", "z", "n", "count", "i", "sum", "temp"):
                    self.error_handler.report_error(
                        "Error Semántico de Variable",
                        f"La variable '{v}' se utiliza en un cálculo pero nunca fue inicializada.",
                        line=line_idx,
                        suggestion=f"Asigne un valor a '{v}' antes de utilizarla."
                    )

            if instr.is_assignment() and instr.result:
                defined_vars.add(instr.result)

    # -------------------------------------------------------------------------
    # 1. ELIMINACIÓN DE INSTRUCCIONES INALCANZABLES
    # -------------------------------------------------------------------------

    def eliminate_unreachable_code(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Elimina aquellas instrucciones que se encuentran inmediatamente después
        de un salto incondicional ('goto L') y antes de la siguiente etiqueta ('L:').
        """
        optimized: List[TACInstruction] = []
        is_unreachable = False

        for instr in instructions:
            # Si encontramos una etiqueta, el código vuelve a ser alcanzable
            if instr.is_label or instr.op == "LABEL":
                is_unreachable = False
                optimized.append(instr)
                continue

            if is_unreachable:
                # Instrucción código muerto detectada
                self.error_handler.log_optimization(
                    "Eliminación de Código Inalcanzable",
                    f"Instrucción inalcanzable descartada tras salto incondicional.",
                    original_code=str(instr)
                )
                continue

            optimized.append(instr)

            # Un salto incondicional marca el inicio de una zona inalcanzable
            if instr.is_unconditional_jump():
                is_unreachable = True

        return optimized

    # -------------------------------------------------------------------------
    # 2. ELIMINACIÓN DE ASIGNACIONES INNECESARIAS / SOBRESCRITAS (DEAD STORES)
    # -------------------------------------------------------------------------

    def eliminate_dead_stores(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Si una variable se asigna ('temp = a') y se sobrescribe inmediatamente ('temp = b')
        sin ninguna lectura intermedia en el mismo bloque básico, la primera es redundante.
        """
        optimized: List[TACInstruction] = []
        n = len(instructions)

        for i in range(n):
            curr = instructions[i]

            if curr.is_assignment() and curr.result and i + 1 < n:
                var_name = curr.result
                next_instr = instructions[i + 1]

                # Caso 1: La siguiente instrucción asigna a la misma variable sin leerla
                if next_instr.is_assignment() and next_instr.result == var_name:
                    if var_name not in next_instr.get_used_vars():
                        self.error_handler.log_optimization(
                            "Eliminación de Asignación Redundante",
                            f"Variable '{var_name}' sobrescrita inmediatamente sin lectura previa.",
                            original_code=str(curr)
                        )
                        continue

            optimized.append(curr)

        return optimized

    # -------------------------------------------------------------------------
    # 3. ELIMINACIÓN DE CÁLCULOS REPETIDOS (COMMON SUBEXPRESSION ELIMINATION)
    # -------------------------------------------------------------------------

    def eliminate_common_subexpressions(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Identifica expresiones idénticas (mismo operador y operandos) cuyos valores
        ya han sido calculados y cuyos operandos no han sido modificados.
        """
        optimized: List[TACInstruction] = []
        # Mapa: (op, arg1, arg2) -> nombre_temporal
        available_expressions: Dict[Tuple[str, str, str], str] = {}
        # Reemplazos pendientes: var_redundante -> var_original
        replacements: Dict[str, str] = {}

        for instr in instructions:
            # Si hay etiquetas o saltos, reiniciamos el análisis local de bloque
            if instr.is_label or instr.is_jump():
                available_expressions.clear()

            # Aplicar reemplazos conocidos a los operandos
            new_arg1 = replacements.get(instr.arg1, instr.arg1) if instr.arg1 else None
            new_arg2 = replacements.get(instr.arg2, instr.arg2) if instr.arg2 else None

            if instr.is_assignment() and instr.op not in ("=", "RETURN", "CALL", "CREATE", "ERROR") and new_arg1 and new_arg2:
                # Normalizar operaciones conmutativas (+ y *)
                if instr.op in ("+", "*") and str(new_arg1) > str(new_arg2):
                    expr_key = (instr.op, str(new_arg2), str(new_arg1))
                else:
                    expr_key = (instr.op, str(new_arg1), str(new_arg2))

                if expr_key in available_expressions:
                    prev_temp = available_expressions[expr_key]
                    replacements[instr.result] = prev_temp
                    self.error_handler.log_optimization(
                        "Eliminación de Cálculos Repetidos (CSE)",
                        f"Expresión '{new_arg1} {instr.op} {new_arg2}' ya calculada en '{prev_temp}'. Reemplazando '{instr.result}' por '{prev_temp}'.",
                        original_code=str(instr)
                    )
                    # Convertir a asignación simple o descartar si se eliminará en DCE
                    instr = TACInstruction("=", arg1=prev_temp, result=instr.result, comment=f"Reemplazo CSE con {prev_temp}")
                else:
                    available_expressions[expr_key] = instr.result
                    instr.arg1 = new_arg1
                    instr.arg2 = new_arg2
            else:
                instr.arg1 = new_arg1
                instr.arg2 = new_arg2

            # Invalidar expresiones si sus operandos son modificados
            if instr.is_assignment() and instr.result:
                mod_var = instr.result
                keys_to_remove = [k for k in available_expressions if k[1] == mod_var or k[2] == mod_var]
                for k in keys_to_remove:
                    del available_expressions[k]

            optimized.append(instr)

        return optimized

    # -------------------------------------------------------------------------
    # 4. PLEGADO Y PROPAGACIÓN DE CONSTANTES Y COPIAS
    # -------------------------------------------------------------------------

    def propagate_and_fold_constants(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Propaga constantes conocidas y realiza el plegado de operaciones
        aritméticas en tiempo de compilación.
        """
        optimized: List[TACInstruction] = []
        constants: Dict[str, Any] = {}
        copies: Dict[str, str] = {}

        for instr in instructions:
            if instr.is_label or instr.is_jump():
                constants.clear()
                copies.clear()
                optimized.append(instr)
                continue

            # Sustituir operandos si son copias o constantes conocidas
            def resolve_arg(arg: Optional[str]) -> Optional[str]:
                if not arg:
                    return arg
                if arg in copies:
                    return copies[arg]
                return arg

            arg1 = resolve_arg(instr.arg1)
            arg2 = resolve_arg(instr.arg2)

            # Caso 1: Asignación simple de constante: 'x = 10'
            if instr.op == "=" and arg1 is not None and self._is_constant(arg1):
                val = self._parse_constant(arg1)
                constants[instr.result] = val
                instr.arg1 = str(val)
                optimized.append(instr)
                continue

            # Caso 2: Asignación de copia: 'temp = b'
            if instr.op == "=" and arg1 is not None and not self._is_constant(arg1):
                if instr.result:
                    copies[instr.result] = arg1
                instr.arg1 = arg1
                optimized.append(instr)
                continue

            # Caso 3: Operación binaria evaluable con constantes
            if instr.op in ("+", "-", "*", "/", "%") and arg1 is not None and arg2 is not None:
                val1 = constants.get(arg1, self._parse_constant(arg1) if self._is_constant(arg1) else None)
                val2 = constants.get(arg2, self._parse_constant(arg2) if self._is_constant(arg2) else None)

                # Detección preventiva de división por cero
                if instr.op in ("/", "%") and val2 == 0:
                    self.error_handler.report_error(
                        "Error Aritmético en Optimización",
                        f"División por cero detectada durante el plegado de constantes: '{arg1} {instr.op} 0'.",
                        suggestion="Verifique que el divisor no sea cero para evitar excepciones en ejecución."
                    )
                    optimized.append(instr)
                    continue

                if val1 is not None and val2 is not None:
                    # Plegado completo a constante!
                    try:
                        res_val = self._fold_arithmetic(instr.op, val1, val2)
                        constants[instr.result] = res_val
                        self.error_handler.log_optimization(
                            "Plegado de Constantes (Constant Folding)",
                            f"Evaluación en compilación: {val1} {instr.op} {val2} = {res_val}.",
                            original_code=str(instr)
                        )
                        optimized.append(TACInstruction("=", arg1=str(res_val), result=instr.result, comment=f"Plegado: {val1}{instr.op}{val2}"))
                        continue
                    except ZeroDivisionError:
                        pass

                # Propagación de un operando constante si se conoce
                if val1 is not None:
                    arg1 = str(val1)
                if val2 is not None:
                    arg2 = str(val2)

            # Caso 4: Simplificación algebraica: x + 0 -> x, x * 1 -> x, x * 0 -> 0
            if instr.op == "+" and arg2 == "0":
                self.error_handler.log_optimization("Simplificación Algebraica", f"{arg1} + 0 -> {arg1}", str(instr))
                optimized.append(TACInstruction("=", arg1=arg1, result=instr.result, comment="Simplificación x + 0"))
                continue
            if instr.op == "*" and arg2 == "1":
                self.error_handler.log_optimization("Simplificación Algebraica", f"{arg1} * 1 -> {arg1}", str(instr))
                optimized.append(TACInstruction("=", arg1=arg1, result=instr.result, comment="Simplificación x * 1"))
                continue
            if instr.op == "*" and (arg1 == "0" or arg2 == "0"):
                self.error_handler.log_optimization("Simplificación Algebraica", f"Multiplicación por cero -> 0", str(instr))
                optimized.append(TACInstruction("=", arg1="0", result=instr.result, comment="Multiplicación por cero"))
                continue

            instr.arg1 = arg1
            instr.arg2 = arg2
            optimized.append(instr)

        return optimized

    def _is_constant(self, val_str: str) -> bool:
        if not val_str:
            return False
        clean = val_str.strip()
        if clean.startswith('"') and clean.endswith('"'):
            return True
        if clean.lstrip('-').replace('.', '', 1).isdigit():
            return True
        return clean in ("true", "false")

    def _parse_constant(self, val_str: str) -> Any:
        clean = val_str.strip()
        if clean.startswith('"') and clean.endswith('"'):
            return clean[1:-1]
        if clean in ("true", "false"):
            return clean == "true"
        if "." in clean:
            return float(clean)
        return int(clean)

    def _fold_arithmetic(self, op: str, v1: Any, v2: Any) -> Any:
        if op == "+":
            return v1 + v2
        elif op == "-":
            return v1 - v2
        elif op == "*":
            return v1 * v2
        elif op == "/":
            return v1 // v2 if isinstance(v1, int) and isinstance(v2, int) else v1 / v2
        elif op == "%":
            return v1 % v2
        return v1

    # -------------------------------------------------------------------------
    # 5. ELIMINACIÓN DE VARIABLES NO UTILIZADAS (DEAD CODE ELIMINATION)
    # -------------------------------------------------------------------------

    def eliminate_dead_variables(self, instructions: List[TACInstruction], critical_vars: Set[str]) -> List[TACInstruction]:
        """
        Calcula qué variables son leídas en alguna instrucción posterior.
        Cualquier asignación a una variable que nunca es leída ni es crítica es eliminada.
        """
        # Calcular el conjunto de todas las variables leídas/usadas en el código
        used_variables: Set[str] = set(critical_vars)

        for instr in instructions:
            # Las variables usadas en saltos condicionales son obligatoriamente vivas
            if instr.is_conditional_jump():
                used_variables.update(instr.get_used_vars())
            elif instr.op == "RETURN" and instr.arg1:
                used_variables.add(instr.arg1)
            else:
                used_variables.update(instr.get_used_vars())

        optimized: List[TACInstruction] = []
        for instr in instructions:
            if instr.is_assignment() and instr.result:
                var_def = instr.result
                # Si la variable definida NO se usa nunca y no es crítica, se elimina
                if var_def not in used_variables:
                    self.error_handler.log_optimization(
                        "Eliminación de Variable No Utilizada (DCE)",
                        f"La variable '{var_def}' se inicializa o calcula pero nunca se utiliza.",
                        original_code=str(instr)
                    )
                    continue

            optimized.append(instr)

        return optimized
