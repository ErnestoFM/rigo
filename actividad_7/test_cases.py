"""
================================================================================
ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
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


class TestCase:
    """
    Representa un caso de prueba para la verificación semántica,
    la gestión de la tabla de símbolos y el control de ámbitos.

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
        name="Asignación y Operaciones Válidas de Mismo Tipo (int)",
        category="Verificación de Tipos Válida (Rúbrica)",
        is_valid=True,
        code="""
int a;
a = 5;
int b = 10;
int c = a + b;
""",
        expected_behavior="Inserción y actualización exitosa de 'a', 'b', 'c' como int en la tabla de símbolos global sin errores de tipos."
    ),

    TestCase(
        id_num=2,
        name="Gestión de Ámbito Global y Local en Función (Ejemplo Rúbrica)",
        category="Gestión de Ámbito Válida (Rúbrica)",
        is_valid=True,
        code="""
int variable_global;
void miFuncion() {
    int variable_local;
    variable_global = 5;
    variable_local = 10;
}
""",
        expected_behavior="Acceso válido a 'variable_global' desde la función y uso de 'variable_local' restringido al ámbito local de 'miFuncion'."
    ),

    TestCase(
        id_num=3,
        name="Tipos Flotantes y Caracteres con Operaciones Válidas",
        category="Tipos de Datos Primitivos Válidos",
        is_valid=True,
        code="""
float pi = 3.14;
float radio = 2.5;
float area = pi * radio;
char letra = 'A';
""",
        expected_behavior="Registro correcto de variables de tipo 'float' y 'char' en la tabla de símbolos con operaciones homogéneas."
    ),

    TestCase(
        id_num=4,
        name="Enmascaramiento de Variable Global por Ámbito Local (Shadowing)",
        category="Resolución de Ámbitos Jerárquicos",
        is_valid=True,
        code="""
int total = 100;
void procesar() {
    int total = 50;
    total = total + 10;
}
""",
        expected_behavior="La variable local 'total' enmascara válidamente a la global en 'procesar' sin generar colisión ni error."
    ),

    TestCase(
        id_num=5,
        name="Control de Flujo con Tipos y Variables Coherentes",
        category="Estructuras de Control y Expresiones Válidas",
        is_valid=True,
        code="""
int contador = 0;
int limite = 10;
while (contador < limite) {
    if (contador > 5) {
        contador = contador + 2;
    } else {
        contador = contador + 1;
    }
}
""",
        expected_behavior="Evaluación semántica exitosa de expresiones relacionales y aritméticas entre variables int declaradas."
    ),

    # --------------------------------------------------------------------------
    # CASOS INVÁLIDOS CON GESTIÓN DE ERRORES (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=6,
        name="Error de Tipo: Asignación de float a int",
        category="Incompatibilidad de Tipos (Rúbrica)",
        is_valid=False,
        code="""
int x;
float y = 3.5;
x = y;
""",
        expected_behavior="Detección de 'Tipo Incompatible en Asignación: se esperaba int pero se obtuvo float'."
    ),

    TestCase(
        id_num=7,
        name="Error de Tipo: Asignación de int a float",
        category="Incompatibilidad de Tipos (Rúbrica)",
        is_valid=False,
        code="""
int a;
a = 5;
float b;
b = a;
""",
        expected_behavior="Detección de 'Tipo Incompatible en Asignación: se esperaba float pero se obtuvo int'."
    ),

    TestCase(
        id_num=8,
        name="Error de Identificador: Variable No Declarada",
        category="Identificador No Declarado (Rúbrica)",
        is_valid=False,
        code="""
c = 10;
""",
        expected_behavior="Detección de 'Identificador No Declarado: 'c' en línea 1'."
    ),

    TestCase(
        id_num=9,
        name="Error de Ámbito: Acceso a Variable Local Fuera de su Función",
        category="Violación de Ámbito (Scope)",
        is_valid=False,
        code="""
void miFuncion() {
    int variable_local = 10;
}
variable_local = 20;
""",
        expected_behavior="Detección de 'Identificador No Declarado: 'variable_local' en el ámbito global'."
    ),

    TestCase(
        id_num=10,
        name="Error de Redeclaración: Identificador Duplicado en el Mismo Ámbito",
        category="Redeclaración en Mismo Ámbito",
        is_valid=False,
        code="""
int saldo = 100;
int saldo = 200;
""",
        expected_behavior="Detección de 'Redeclaración de Identificador en Mismo Ámbito: 'saldo''."
    )
]
