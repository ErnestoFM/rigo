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

import re
from typing import List, Optional
from tac_instruction import TACInstruction
from error_handler import CompilerErrorHandler


class TACParser:
    """
    Analizador sintáctico para código intermedio de tres direcciones (TAC).
    Parsea representaciones textuales de TAC en objetos TACInstruction estructurados,
    validando sintaxis de etiquetas, saltos condicionales/incondicionales y asignaciones.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, error_handler: Optional[CompilerErrorHandler] = None):
        self.error_handler = error_handler or CompilerErrorHandler()

    def parse(self, text: str) -> List[TACInstruction]:
        instructions: List[TACInstruction] = []
        lines = text.strip().splitlines()

        for line_no, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue

            # Separar comentario inline si existe
            comment = None
            if "#" in line:
                code_part, comment_part = line.split("#", 1)
                line = code_part.strip()
                comment = comment_part.strip()

            if not line:
                # Línea que era puramente comentario
                if comment:
                    instructions.append(TACInstruction("COMMENT", comment=comment))
                continue

            # 1. Etiquetas: 'L1:'
            if line.endswith(":"):
                lbl_name = line[:-1].strip()
                instructions.append(TACInstruction("LABEL", result=lbl_name, comment=comment, is_label=True))
                continue

            # 2. Salto incondicional: 'goto L2'
            m_goto = re.match(r'^goto\s+([a-zA-Z_0-9]+)$', line)
            if m_goto:
                target = m_goto.group(1)
                instructions.append(TACInstruction("GOTO", result=target, comment=comment))
                continue

            # 3. Salto condicional negado: 'if not t1 goto L2'
            m_if_not = re.match(r'^if\s+not\s+([a-zA-Z_0-9]+)\s+goto\s+([a-zA-Z_0-9]+)$', line)
            if m_if_not:
                cond_var = m_if_not.group(1)
                target = m_if_not.group(2)
                instructions.append(TACInstruction("IF_NOT_GOTO", arg1=cond_var, result=target, comment=comment))
                continue

            # 4. Salto condicional relacional: 'if a > 10 goto L1' o 'if t2 == 1 goto L1'
            m_if_cmp = re.match(r'^if\s+([a-zA-Z_0-9]+)\s*(==|!=|<=|>=|<|>)\s*([a-zA-Z_0-9]+|"[^"]*")\s+goto\s+([a-zA-Z_0-9]+)$', line)
            if m_if_cmp:
                left = m_if_cmp.group(1)
                op = m_if_cmp.group(2)
                right = m_if_cmp.group(3).strip()
                target = m_if_cmp.group(4)
                instructions.append(TACInstruction("IF_CMP_GOTO", arg1=left, arg2=f"{op} {right}", result=target, comment=comment))
                continue

            # 5. Salto condicional simple: 'if t1 goto L1'
            m_if = re.match(r'^if\s+([a-zA-Z_0-9]+)\s+goto\s+([a-zA-Z_0-9]+)$', line)
            if m_if:
                cond_var = m_if.group(1)
                target = m_if.group(2)
                instructions.append(TACInstruction("IF_GOTO", arg1=cond_var, result=target, comment=comment))
                continue

            # Caso de salto condicional con sintaxis u operador inválido (ej. 'if a <> 10 goto L1')
            if line.startswith("if ") and " goto " in line:
                self.error_handler.report_error(
                    "Error Sintáctico de Salto Condicional",
                    f"Condición de salto o sintaxis relacional inválida en: '{raw_line.strip()}'.",
                    line=line_no,
                    suggestion="Utilice operadores relacionales válidos: '==', '!=', '<', '>', '<=', '>='."
                )
                continue

            # 6. Retorno: 'return t7' o 'return'
            m_ret = re.match(r'^return(?:\s+(.+))?$', line)
            if m_ret:
                val = m_ret.group(1).strip() if m_ret.group(1) else None
                instructions.append(TACInstruction("RETURN", arg1=val, comment=comment))
                continue

            # 7. Llamada: 'call L6'
            m_call = re.match(r'^call\s+(.+)$', line)
            if m_call:
                target = m_call.group(1).strip()
                instructions.append(TACInstruction("CALL", arg1=target, comment=comment))
                continue

            # 8. Creación de objeto: 'obj = create Persona'
            m_create = re.match(r'^([a-zA-Z_0-9]+)\s*=\s*create\s+([a-zA-Z_0-9]+)$', line)
            if m_create:
                res_var = m_create.group(1)
                cls_name = m_create.group(2)
                instructions.append(TACInstruction("CREATE", arg1=cls_name, result=res_var, comment=comment))
                continue

            # 9. Asignación con Operación Binaria: 'z = x + y', 't1 = a * 2'
            m_bin = re.match(r'^([a-zA-Z_0-9]+)\s*=\s*([^\s+\-*/%]+)\s*([\+\-\*/%])\s*(.+)$', line)
            if m_bin:
                res_var = m_bin.group(1)
                left = m_bin.group(2)
                op = m_bin.group(3)
                right = m_bin.group(4).strip()
                instructions.append(TACInstruction(op, arg1=left, arg2=right, result=res_var, comment=comment))
                continue

            # 10. Asignación con Operación Unaria: 't1 = -a', 't1 = !flag'
            m_un = re.match(r'^([a-zA-Z_0-9]+)\s*=\s*([!\-])\s*([a-zA-Z_0-9]+)$', line)
            if m_un:
                res_var = m_un.group(1)
                op = m_un.group(2)
                arg = m_un.group(3)
                instructions.append(TACInstruction(op, arg1=arg, result=res_var, comment=comment))
                continue

            # 11. Asignación simple: 'x = 10', 'temp = a', 'result = temp'
            m_assign = re.match(r'^([a-zA-Z_0-9]+)\s*=\s*(.+)$', line)
            if m_assign:
                res_var = m_assign.group(1)
                val = m_assign.group(2).strip()
                instructions.append(TACInstruction("=", arg1=val, result=res_var, comment=comment))
                continue

            # 12. Error guard: 'error "Mensaje"'
            m_err = re.match(r'^error\s+"([^"]+)"$', line)
            if m_err:
                msg = m_err.group(1)
                instructions.append(TACInstruction("ERROR", arg1=msg, comment=comment))
                continue

            # Si ninguna regla coincide, es un error sintáctico de TAC
            self.error_handler.report_error(
                "Error Sintáctico de Código Intermedio",
                f"Instrucción TAC mal formada o desconocida: '{raw_line.strip()}'.",
                line=line_no,
                suggestion="Verifique el formato: 'var = op1 op op2', 'goto Label', 'Label:'."
            )

        return instructions
