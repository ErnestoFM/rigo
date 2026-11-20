"""
================================================================================
ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL (LENGUAJE C EN PYTHON)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Dict, Any


class TestCase:
    """
    Representa un caso de prueba para el analizador sintáctico de estructuras de control.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        id_num: int,
        name: str,
        category: str,
        is_valid: bool,
        code: str,
        expected_behavior: str
    ):
        self.id_num = id_num
        self.name = name
        self.category = category
        self.is_valid = is_valid
        self.code = code.strip()
        self.expected_behavior = expected_behavior


TEST_CASES: List[TestCase] = [
    # --------------------------------------------------------------------------
    # CASOS VÁLIDOS (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=1,
        name="Sentencia Condicional if-else Completa",
        category="Estructura Condicional Válida (Rúbrica)",
        is_valid=True,
        code="""
if (x > 0) {
    x = x + 1;
} else {
    x = x - 1;
}
""",
        expected_behavior="Generación exitosa del AST: nodo IfNode con rama Then y rama Else entre llaves."
    ),

    TestCase(
        id_num=2,
        name="Bucle Iterativo while Estándar",
        category="Estructura Iterativa Válida (Rúbrica)",
        is_valid=True,
        code="""
while (y < 10) {
    y = y + 1;
}
""",
        expected_behavior="Generación exitosa del AST: nodo WhileNode con condición y bloque de cuerpo entre llaves."
    ),

    TestCase(
        id_num=3,
        name="Bucle Determinado for Estándar",
        category="Estructura Iterativa Válida (Rúbrica)",
        is_valid=True,
        code="""
for (i = 0; i < 10; i = i + 1) {
    suma = suma + i;
}
""",
        expected_behavior="Generación exitosa del AST: nodo ForNode con inicialización, condición, actualización y bloque."
    ),

    TestCase(
        id_num=4,
        name="Estructuras Anidadas (for con if-else interno)",
        category="Estructuras de Control Anidadas Válidas",
        is_valid=True,
        code="""
for (int i = 0; i < 100; i++) {
    if (i % 2 == 0) {
        pares = pares + 1;
    } else {
        impares = impares + 1;
    }
}
""",
        expected_behavior="AST multinivel con bucle for conteniendo una estructura condicional if-else."
    ),

    TestCase(
        id_num=5,
        name="Programa Completo en C con Función main y Control Múltiple",
        category="Programa Completo Válido",
        is_valid=True,
        code="""
int main() {
    int total = 0;
    int k = 1;
    while (k <= 5) {
        if (k > 2) {
            total = total + k * 2;
        } else {
            total = total + 1;
        }
        k = k + 1;
    }
    return total;
}
""",
        expected_behavior="AST de función main con declaraciones, bucle while, condicional if-else y sentencia return."
    ),

    # --------------------------------------------------------------------------
    # CASOS INVÁLIDOS CON GESTIÓN DE ERRORES (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=6,
        name="Error en if: Paréntesis de Cierre Faltante",
        category="Error de Paréntesis en Condicional (Rúbrica)",
        is_valid=False,
        code="""
if (x > 0 {
    x = x + 1;
}
""",
        expected_behavior="Detección y reporte: 'Paréntesis de cierre ')' faltante en estructura 'if''."
    ),

    TestCase(
        id_num=7,
        name="Error en while: Paréntesis de Apertura Faltante",
        category="Error de Paréntesis en Bucle while (Rúbrica)",
        is_valid=False,
        code="""
while y < 10) {
    y = y + 1;
}
""",
        expected_behavior="Detección y reporte: 'Paréntesis de apertura '(' faltante en estructura 'while''."
    ),

    TestCase(
        id_num=8,
        name="Error en for: Paréntesis de Apertura Faltante",
        category="Error de Paréntesis en Bucle for (Rúbrica)",
        is_valid=False,
        code="""
for i = 0; i < 10; i = i + 1) {
    suma = suma + i;
}
""",
        expected_behavior="Detección y reporte: 'Paréntesis de apertura '(' faltante en estructura 'for''."
    ),

    TestCase(
        id_num=9,
        name="Error en if: Bloque de Sentencias Sin Llaves Requeridas",
        category="Error de Bloque Obligatorio (Rúbrica)",
        is_valid=False,
        code="""
if (x > 0)
    x = x + 1;
""",
        expected_behavior="Detección y reporte: 'Bloque de sentencias faltante o sin llaves '{' en la estructura 'if''."
    ),

    TestCase(
        id_num=10,
        name="Error en while: Llave de Cierre Faltante al Final",
        category="Error de Llaves Desbalanceadas (Rúbrica)",
        is_valid=False,
        code="""
while (y < 10) {
    y = y + 1;
""",
        expected_behavior="Detección y reporte: 'Llave de cierre '}' faltante en bloque de estructura 'while''."
    )
]
