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

from typing import List


class TestCase:
    """
    Representa un caso de prueba para la verificación de generación de código
    intermedio para control de flujo, métodos y clases.

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
        name="Estructura Condicional if-else (Ejemplo Rúbrica)",
        category="Estructuras Condicionales",
        is_valid=True,
        code="""
if (x > y) {
    z = x;
} else {
    z = y;
}
""",
        expected_behavior="Genera temporales y saltos if/else con etiquetas L1 (then) y L2 (end) con comentarios descriptivos."
    ),

    TestCase(
        id_num=2,
        name="Estructura de Selección Múltiple switch-case (Ejemplo Rúbrica)",
        category="Estructuras Condicionales",
        is_valid=True,
        code="""
switch (n) {
    case 1:
        result = "Uno";
        break;
    case 2:
        result = "Dos";
        break;
    default:
        result = "Otro";
}
""",
        expected_behavior="Genera saltos condicionales if t2 == 1, if t2 == 2, goto default y etiquetas L1..L4."
    ),

    TestCase(
        id_num=3,
        name="Bucles while, for y do-while (Ejemplos Rúbrica)",
        category="Bucles y Ciclos",
        is_valid=True,
        code="""
while (i < 10) {
    i = i + 1;
}

for (int i = 0; i < 5; i++) {
    sum = sum + i;
}

do {
    count = count + 1;
} while (count < 10);
""",
        expected_behavior="Genera TAC para while (L1..L2 con if not), for (init, condición, actualización, L3..L4), y do-while (L5 y condición al final)."
    ),

    TestCase(
        id_num=4,
        name="Definición y Llamada de Métodos (Ejemplo Rúbrica)",
        category="Métodos y Funciones",
        is_valid=True,
        code="""
int suma(int a, int b) {
    return a + b;
}

result = suma(5, 3);
""",
        expected_behavior="Genera definición con etiqueta L_metodo, paso de parámetros t8=5, t9=3, instrucción 'call' y asignación de 'return_value'."
    ),

    TestCase(
        id_num=5,
        name="Clases, Métodos de Clase y Creación/Uso de Objetos (Ejemplo Rúbrica)",
        category="Clases y Objetos",
        is_valid=True,
        code="""
class Persona {
    int edad;
    void celebrarCumpleaños() {
        edad = edad + 1;
    }
}

Persona p = new Persona();
p.celebrarCumpleaños();
""",
        expected_behavior="Genera definición de clase con método, creación de instancia con 'obj = create Persona' y llamada 'call' al método del objeto."
    ),

    # --------------------------------------------------------------------------
    # CASOS INVÁLIDOS (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=6,
        name="Llamada a Método o Función No Declarada",
        category="Errores Semánticos en Métodos",
        is_valid=False,
        code="""
result = calcularFactorial(10);
""",
        expected_behavior="Detecta y reporta error semántico por llamada a función 'calcularFactorial' no definida en la tabla de símbolos."
    ),

    TestCase(
        id_num=7,
        name="Aridad Incorrecta en Llamada a Método (Número de Argumentos)",
        category="Errores Semánticos en Métodos",
        is_valid=False,
        code="""
int suma(int a, int b) {
    return a + b;
}

result = suma(5, 3, 10);
""",
        expected_behavior="Detecta discrepancia de aridad: la función 'suma' espera 2 argumentos pero se pasaron 3."
    ),

    TestCase(
        id_num=8,
        name="Instanciación de Clase No Declarada",
        category="Errores Semánticos en Clases",
        is_valid=False,
        code="""
Vehiculo v = new Vehiculo();
""",
        expected_behavior="Detecta intento de instanciar clase 'Vehiculo' no declarada en el ámbito del compilador."
    ),

    TestCase(
        id_num=9,
        name="Invocación de Método Inexistente en Objeto de Clase",
        category="Errores Semánticos en Clases",
        is_valid=False,
        code="""
class Persona {
    int edad;
    void celebrarCumpleaños() {
        edad = edad + 1;
    }
}

Persona p = new Persona();
p.volar();
""",
        expected_behavior="Detecta que la clase 'Persona' no posee ningún método denominado 'volar'."
    ),

    TestCase(
        id_num=10,
        name="Tipo Incompatible en Condición de Control de Flujo",
        category="Errores Semánticos en Control de Flujo",
        is_valid=False,
        code="""
if ("condicion_invalida_no_booleana") {
    z = 10;
}
""",
        expected_behavior="Detecta condición no booleana (cadena literal) en estructura condicional 'if'."
    ),
]
