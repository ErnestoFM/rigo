"""
================================================================================
PROYECTO FINAL: COMPILADOR INTEGRAL DE LENGUAJE C
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Dict, Set, Optional, Tuple, Any
from tac_instruction import TACInstruction
from error_handler import CompilerErrorHandler


class TACOptimizer:
    """
    Optimizador de código intermedio TAC.
    Aplica:
    1. Eliminación de instrucciones inalcanzables.
    2. Eliminación de asignaciones sobrescritas inmediatamente (Dead Stores).
    3. Plegado y propagación de constantes y copias.
    4. Eliminación de cálculos repetidos (CSE).
    5. Eliminación de variables no utilizadas (DCE).

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_handler: Optional[CompilerErrorHandler] = None):
        self.error_handler = error_handler or CompilerErrorHandler()

    @property
    def optimization_log(self) -> List[str]:
        return list(self.error_handler.optimization_logs)

    def optimize(self, instructions: List[TACInstruction], critical_vars: Optional[Set[str]] = None) -> List[TACInstruction]:
        current = [i for i in instructions if i.op != "COMMENT"]
        crit_vars = critical_vars or {"result", "return_value"}

        # También cualquier variable usada en un print es crítica
        for instr in current:
            if instr.op == "PRINT" and instr.arg1:
                crit_vars.add(instr.arg1)

        max_iter = 8
        for _ in range(max_iter):
            before = [str(i) for i in current]

            current = self.eliminate_unreachable(current)
            current = self.eliminate_dead_stores(current)
            current = self.propagate_and_fold(current)
            current = self.eliminate_cse(current)
            current = self.eliminate_dead_vars(current, crit_vars)

            after = [str(i) for i in current]
            if before == after:
                break

        return current

    def eliminate_unreachable(self, instrs: List[TACInstruction]) -> List[TACInstruction]:
        res: List[TACInstruction] = []
        is_dead = False
        for i in instrs:
            if i.is_label or i.op == "LABEL":
                is_dead = False
                res.append(i)
                continue
            if is_dead:
                self.error_handler.log_optimization(f"[Poda Inalcanzable] Descartada: '{str(i)}'")
                continue
            res.append(i)
            if i.is_unconditional_jump():
                is_dead = True
        return res

    def eliminate_dead_stores(self, instrs: List[TACInstruction]) -> List[TACInstruction]:
        res: List[TACInstruction] = []
        n = len(instrs)
        for idx in range(n):
            curr = instrs[idx]
            if curr.is_assignment() and curr.result and idx + 1 < n:
                nxt = instrs[idx + 1]
                if nxt.is_assignment() and nxt.result == curr.result and curr.result not in nxt.get_used_vars():
                    self.error_handler.log_optimization(f"[Poda Dead Store] Asignación redundante eliminada: '{str(curr)}'")
                    continue
            res.append(curr)
        return res

    def propagate_and_fold(self, instrs: List[TACInstruction]) -> List[TACInstruction]:
        res: List[TACInstruction] = []
        constants: Dict[str, Any] = {}
        copies: Dict[str, str] = {}

        for instr in instrs:
            if instr.is_label or instr.is_jump() or instr.op in ("CALL", "CREATE"):
                constants.clear()
                copies.clear()
                res.append(instr)
                continue

            def resolve(arg: Optional[str]) -> Optional[str]:
                if not arg:
                    return arg
                return copies.get(arg, arg)

            a1 = resolve(instr.arg1)
            a2 = resolve(instr.arg2)

            if instr.op == "=" and a1 is not None:
                if self._is_const(a1):
                    val = self._parse_const(a1)
                    constants[instr.result] = val
                    instr.arg1 = str(val)
                    res.append(instr)
                    continue
                else:
                    if instr.result:
                        # No sustituir una variable persistente de usuario con un temporal volátil
                        if not (a1.startswith("t") and a1[1:].isdigit() and not (instr.result.startswith("t") and instr.result[1:].isdigit())):
                            copies[instr.result] = a1
                    instr.arg1 = a1
                    res.append(instr)
                    continue

            if instr.op in ("+", "-", "*", "/", "%") and a1 and a2:
                v1 = constants.get(a1, self._parse_const(a1) if self._is_const(a1) else None)
                v2 = constants.get(a2, self._parse_const(a2) if self._is_const(a2) else None)

                if v1 is not None and v2 is not None:
                    if instr.op in ("/", "%") and v2 == 0:
                        res.append(instr)
                        continue
                    try:
                        folded = self._calc(instr.op, v1, v2)
                        constants[instr.result] = folded
                        self.error_handler.log_optimization(f"[Plegado Constantes] {v1} {instr.op} {v2} = {folded}")
                        res.append(TACInstruction("=", arg1=str(folded), result=instr.result, comment=f"Plegado: {v1}{instr.op}{v2}"))
                        continue
                    except Exception:
                        pass

                if v1 is not None:
                    a1 = str(v1)
                if v2 is not None:
                    a2 = str(v2)

            instr.arg1 = a1
            instr.arg2 = a2
            res.append(instr)

        return res

    def eliminate_cse(self, instrs: List[TACInstruction]) -> List[TACInstruction]:
        res: List[TACInstruction] = []
        expr_map: Dict[Tuple[str, str, str], str] = {}
        replacements: Dict[str, str] = {}

        for instr in instrs:
            if instr.is_label or instr.is_jump():
                expr_map.clear()

            a1 = replacements.get(instr.arg1, instr.arg1) if instr.arg1 else None
            a2 = replacements.get(instr.arg2, instr.arg2) if instr.arg2 else None

            if instr.is_assignment() and instr.op not in ("=", "RETURN", "CALL", "CREATE", "PRINT", "ERROR") and a1 and a2:
                key = (instr.op, min(str(a1), str(a2)), max(str(a1), str(a2))) if instr.op in ("+", "*") else (instr.op, str(a1), str(a2))
                if key in expr_map:
                    orig_var = expr_map[key]
                    replacements[instr.result] = orig_var
                    self.error_handler.log_optimization(f"[CSE] Reusando '{orig_var}' para '{instr.result}'")
                    instr = TACInstruction("=", arg1=orig_var, result=instr.result, comment=f"Reuso CSE de {orig_var}")
                else:
                    expr_map[key] = instr.result
                    instr.arg1 = a1
                    instr.arg2 = a2
            else:
                instr.arg1 = a1
                instr.arg2 = a2

            if instr.is_assignment() and instr.result:
                mv = instr.result
                expr_map = {k: v for k, v in expr_map.items() if k[1] != mv and k[2] != mv}

            res.append(instr)
        return res

    def eliminate_dead_vars(self, instrs: List[TACInstruction], crit_vars: Set[str]) -> List[TACInstruction]:
        used: Set[str] = set(crit_vars)
        for i in instrs:
            if i.is_conditional_jump():
                used.update(i.get_used_vars())
            elif i.op in ("RETURN", "PRINT") and i.arg1:
                used.add(i.arg1)
            else:
                used.update(i.get_used_vars())

        res: List[TACInstruction] = []
        for i in instrs:
            if i.is_assignment() and i.result and i.result not in used:
                self.error_handler.log_optimization(f"[DCE] Eliminada variable muerta '{i.result}'")
                continue
            res.append(i)
        return res

    def _is_const(self, val_str: str) -> bool:
        if not val_str:
            return False
        clean = val_str.strip()
        if clean.startswith('"') and clean.endswith('"'):
            return True
        if clean.lstrip('-').replace('.', '', 1).isdigit():
            return True
        return clean in ("true", "false")

    def _parse_const(self, val_str: str) -> Any:
        clean = val_str.strip()
        if clean.startswith('"') and clean.endswith('"'):
            return clean[1:-1]
        if clean in ("true", "false"):
            return clean == "true"
        if "." in clean:
            return float(clean)
        return int(clean)

    def _calc(self, op: str, v1: Any, v2: Any) -> Any:
        if op == "+":
            return v1 + v2
        if op == "-":
            return v1 - v2
        if op == "*":
            return v1 * v2
        if op == "/":
            return v1 // v2 if isinstance(v1, int) and isinstance(v2, int) else v1 / v2
        if op == "%":
            return v1 % v2
        return v1
