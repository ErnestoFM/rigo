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

from typing import List


class TestCaseItem:
    """
    Representa un caso de prueba individual con metadatos de regla, categoría y resultado esperado.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        id_num: int,
        title: str,
        category: str,
        code: str,
        is_valid: bool,
        rule_description: str,
        expected_behavior: str
    ):
        self.id_num = id_num
        self.title = title
        self.category = category
        self.code = code.strip()
        self.is_valid = is_valid
        self.rule_description = rule_description
        self.expected_behavior = expected_behavior


# ==============================================================================
# CASOS DE PRUEBA VÁLIDOS (CONFORME A LA RÚBRICA Y EJEMPLOS OFICIALES)
# ==============================================================================

TEST_VALID_01_IF_ELSE = """int a = 15;
int b = 10;
if (a > b) {
    console.log("a es mayor que b");
} else {
    console.log("a no es mayor que b");
}"""

TEST_VALID_02_WHILE_COUNTER = """int contador = 0;
while (contador < 10) {
    console.log(contador);
    contador++;
}"""

TEST_VALID_03_METHOD_CALL = """int sumar(int a, int b) {
    return a + b;
}
int resultado = sumar(5, 3);
console.log(resultado);"""

TEST_VALID_04_METHOD_PARAMS = """int multiplicar(int a, int b) {
    return a * b;
}
int producto = multiplicar(4, 6);
console.log(producto);"""

TEST_VALID_05_RETURN_TYPE_BOOLEAN = """boolean esMayorDeEdad(int edad) {
    return edad >= 18;
}
boolean resultado = esMayorDeEdad(20);
console.log(resultado);"""

TEST_VALID_06_IS_EVEN_FUNCTION = """boolean esPar(int numero) {
    return numero % 2 == 0;
}
boolean resultado = esPar(4);
console.log(resultado);"""

TEST_VALID_07_NESTED_CONTROL = """int x = 20;
if (x > 10) {
    if (x > 15) {
        console.log("x es mayor que 15");
    }
}"""

TEST_VALID_08_TRY_CATCH = """float dividir(float a, float b) {
    return a / b;
}
try {
    float resultado = dividir(10, 2);
    console.log(resultado);
} catch (error) {
    console.error("Error al realizar la division");
}"""

TEST_VALID_09_FULL_CLASS = """class CalculadoraAvanzada {
    float base;
    float altura;

    float calcularArea() {
        return (base * altura) / 2;
    }

    boolean esAreaMayor(float limite) {
        float area = calcularArea();
        if (area > limite) {
            return true;
        } else {
            return false;
        }
    }
}"""


# ==============================================================================
# CASOS DE PRUEBA INVÁLIDOS (DETECCIÓN Y DIAGNÓSTICO DE ERRORES SEMÁNTICOS)
# ==============================================================================

TEST_INVALID_10_IF_NON_BOOLEAN = """if ("texto") {
    console.log("Esto es incorrecto");
}"""

TEST_INVALID_11_WHILE_NON_BOOLEAN = """int contador = 5;
while (contador + 10) {
    console.log("Condicion no booleana");
    contador++;
}"""

TEST_INVALID_12_INFINITE_LOOP = """while (true) {
    console.log("Esto no termina nunca");
}"""

TEST_INVALID_13_ARITY_MISMATCH = """void imprimirMensaje(string mensaje) {
    console.log(mensaje);
}
imprimirMensaje("Hola", "Mundo");"""

TEST_INVALID_14_PARAM_TYPE_MISMATCH = """float dividir(float a, float b) {
    return a / b;
}
float cociente = dividir(10, "texto");"""

TEST_INVALID_15_RETURN_TYPE_MISMATCH = """int obtenerEdad() {
    return "Veinte";
}"""

TEST_INVALID_16_VOID_METHOD_RETURNING_VALUE = """void resetearSistema() {
    console.log("Reiniciando...");
    return 404;
}"""

TEST_INVALID_17_MISPLACED_RETURN = """int x = 10;
return x + 5;"""

TEST_INVALID_18_MISSING_BRACES_IF = """int x = 15;
if (x > 10)
    console.log("x es mayor que 10");"""

TEST_INVALID_19_UNREACHABLE_CODE = """int calcularTotal(int subtotal) {
    return subtotal + 10;
    int extra = 50;
    console.log(extra);
}"""

TEST_INVALID_20_UNDECLARED_VARIABLE = """int a = 10;
int b = variableInexistente * 2;"""


# ==============================================================================
# LISTA ESTRUCTURADA DE CASOS DE PRUEBA
# ==============================================================================

ALL_TEST_CASES: List[TestCaseItem] = [
    # Casos Válidos
    TestCaseItem(
        id_num=1,
        title="Estructura 'if-else' con condición booleana válida",
        category="Estructuras de Control",
        code=TEST_VALID_01_IF_ELSE,
        is_valid=True,
        rule_description="Comprobación de que la condición 'a > b' sea de tipo booleano y que ambas ramas posean bloques adecuadamente cerrados.",
        expected_behavior="Análisis léxico, sintáctico y semántico exitoso con 0 errores. Árbol AST generado y tabla de símbolos con 'a' y 'b'."
    ),
    TestCaseItem(
        id_num=2,
        title="Bucle 'while' con condición de salida e incremento",
        category="Estructuras de Control",
        code=TEST_VALID_02_WHILE_COUNTER,
        is_valid=True,
        rule_description="Verificación de flujo de control: condición 'contador < 10' booleana y variable de control mutada con 'contador++'.",
        expected_behavior="Validación correcta con 0 errores; no se cataloga como bucle infinito al mutar la variable de control."
    ),
    TestCaseItem(
        id_num=3,
        title="Definición y llamada a método con tipos coincidentes",
        category="Validación de Métodos",
        code=TEST_VALID_03_METHOD_CALL,
        is_valid=True,
        rule_description="El método 'sumar' se define con dos parámetros 'int' y retorna 'int'. La llamada pasa dos enteros y asigna a un 'int'.",
        expected_behavior="Registro del método en tabla de símbolos, aridad correcta (2 == 2), tipos compatibles y 0 errores."
    ),
    TestCaseItem(
        id_num=4,
        title="Método con parámetros aritméticos 'multiplicar'",
        category="Validación de Métodos",
        code=TEST_VALID_04_METHOD_PARAMS,
        is_valid=True,
        rule_description="Comprobación de llamada a método con 2 argumentos enteros (4, 6) concordantes con la definición formal.",
        expected_behavior="Resolución del método en el ámbito accesible y retorno de tipo 'int' perfectamente validado."
    ),
    TestCaseItem(
        id_num=5,
        title="Método con tipo de retorno booleano 'esMayorDeEdad'",
        category="Validación de Métodos",
        code=TEST_VALID_05_RETURN_TYPE_BOOLEAN,
        is_valid=True,
        rule_description="Validación de tipo de retorno: la expresión relacional 'edad >= 18' produce 'boolean', coincidiendo con la signatura.",
        expected_behavior="Análisis semántico exitoso; tipo de retorno compatible y asignación a variable booleana válida."
    ),
    TestCaseItem(
        id_num=6,
        title="Función para verificación de paridad 'esPar'",
        category="Validación de Métodos",
        code=TEST_VALID_06_IS_EVEN_FUNCTION,
        is_valid=True,
        rule_description="Verificación de operador aritmético módulo ('%') e igualdad relacional ('==') evaluando a tipo 'boolean'.",
        expected_behavior="Comprobación semántica de tipos en operadores binarios y retorno booleano correcto."
    ),
    TestCaseItem(
        id_num=7,
        title="Estructuras de control condicionales anidadas",
        category="Estructuras de Control",
        code=TEST_VALID_07_NESTED_CONTROL,
        is_valid=True,
        rule_description="Validación de anidamiento de estructuras 'if' internas con ámbitos léxicos jerárquicos independientes.",
        expected_behavior="Creación jerárquica de bloques en la tabla de símbolos y flujo lógico coherente."
    ),
    TestCaseItem(
        id_num=8,
        title="Manejo de excepciones con bloque 'try-catch'",
        category="Manejo de Excepciones",
        code=TEST_VALID_08_TRY_CATCH,
        is_valid=True,
        rule_description="Estructura de gestión de excepciones para llamadas con potencial riesgo de división por cero.",
        expected_behavior="Parseo de bloques 'try' y 'catch', registro de la variable de error y resolución de 'console.log' / 'console.error'."
    ),
    TestCaseItem(
        id_num=9,
        title="Definición de clase orientada a objetos con métodos y campos",
        category="Clases y Métodos",
        code=TEST_VALID_09_FULL_CLASS,
        is_valid=True,
        rule_description="Declaración formal de clase con atributos de campo, métodos de cálculo y llamada inter-método 'calcularArea()'.",
        expected_behavior="Registro de 'ClassSymbol', resolución de campos internos y validación completa sin errores."
    ),

    # Casos Inválidos
    TestCaseItem(
        id_num=10,
        title="Condición 'if' inválida con cadena de texto ('texto')",
        category="Estructuras de Control",
        code=TEST_INVALID_10_IF_NON_BOOLEAN,
        is_valid=False,
        rule_description="Comprobación de condiciones lógicas: 'texto' es de tipo 'string', lo cual viola la regla booleana en 'if'.",
        expected_behavior="Detección de Error Semántico: 'La condición en la estructura if debe ser una expresión booleana, se obtuvo string'."
    ),
    TestCaseItem(
        id_num=11,
        title="Condición 'while' inválida con expresión entera",
        category="Estructuras de Control",
        code=TEST_INVALID_11_WHILE_NON_BOOLEAN,
        is_valid=False,
        rule_description="Comprobación de condición en bucle iterativo: 'contador + 10' evalúa a 'int', no a 'boolean'.",
        expected_behavior="Detección de Error Semántico: 'La condición en la estructura while debe ser de tipo boolean, se obtuvo int'."
    ),
    TestCaseItem(
        id_num=12,
        title="Bucle infinito trivial sin condición de salida ('while (true)')",
        category="Flujo de Control",
        code=TEST_INVALID_12_INFINITE_LOOP,
        is_valid=False,
        rule_description="Validación de flujo de control: condición constante verdadera sin instrucciones de escape (break/return).",
        expected_behavior="Detección de Advertencia/Error de Flujo: 'Bucle infinito detectado: condición constante verdadera sin condición de escape'."
    ),
    TestCaseItem(
        id_num=13,
        title="Llamada a método con número incorrecto de argumentos",
        category="Validación de Métodos",
        code=TEST_INVALID_13_ARITY_MISMATCH,
        is_valid=False,
        rule_description="Chequeo de parámetros (Aridad): 'imprimirMensaje' espera 1 argumento y se le suministran 2.",
        expected_behavior="Detección de Error Semántico: 'Llamada al método imprimirMensaje con 2 argumento(s) en lugar de 1'."
    ),
    TestCaseItem(
        id_num=14,
        title="Llamada a método con tipo de argumento incompatible",
        category="Validación de Métodos",
        code=TEST_INVALID_14_PARAM_TYPE_MISMATCH,
        is_valid=False,
        rule_description="Chequeo de tipos de parámetros: 'dividir' espera 'float' para el segundo parámetro, pero se pasa 'string' ('texto').",
        expected_behavior="Detección de Error Semántico: 'Llamada incorrecta al método dividir: el argumento 2 esperaba float, se pasó string'."
    ),
    TestCaseItem(
        id_num=15,
        title="Método con tipo de retorno incompatible ('obtenerEdad')",
        category="Validación de Métodos",
        code=TEST_INVALID_15_RETURN_TYPE_MISMATCH,
        is_valid=False,
        rule_description="Validación de tipos de retorno: el método declara retornar 'int', pero la instrucción retorna 'string' ('Veinte').",
        expected_behavior="Detección de Error Semántico: 'Tipo de retorno incorrecto en el método obtenerEdad: se esperaba int, pero retorna string'."
    ),
    TestCaseItem(
        id_num=16,
        title="Método 'void' que intenta retornar un valor",
        category="Validación de Métodos",
        code=TEST_INVALID_16_VOID_METHOD_RETURNING_VALUE,
        is_valid=False,
        rule_description="Validación de tipos de retorno: un método declarado como 'void' tiene prohibido retornar expresiones.",
        expected_behavior="Detección de Error Semántico: 'El método está declarado como void y no puede retornar un valor de tipo int'."
    ),
    TestCaseItem(
        id_num=17,
        title="Sentencia 'return' fuera de lugar (ámbito global)",
        category="Flujo de Control",
        code=TEST_INVALID_17_MISPLACED_RETURN,
        is_valid=False,
        rule_description="Validación de flujo de control: instrucción 'return' ubicada a nivel global fuera de cualquier método.",
        expected_behavior="Detección de Error Semántico: 'Sentencia return fuera de lugar: solo está permitida dentro del cuerpo de un método'."
    ),
    TestCaseItem(
        id_num=18,
        title="Falta de llaves delimitadoras en estructura 'if'",
        category="Estructuras de Control",
        code=TEST_INVALID_18_MISSING_BRACES_IF,
        is_valid=False,
        rule_description="Sintaxis de estructuras de control: falta de llaves '{' y '}' en el bloque de código condicional.",
        expected_behavior="Detección de Error Sintáctico: 'Falta de llave en la estructura if en la línea 2'."
    ),
    TestCaseItem(
        id_num=19,
        title="Código inalcanzable tras sentencia 'return' incondicional",
        category="Flujo de Control",
        code=TEST_INVALID_19_UNREACHABLE_CODE,
        is_valid=False,
        rule_description="Validación de accesibilidad de flujo: sentencias posteriores a un return incondicional dentro del mismo bloque.",
        expected_behavior="Detección de Advertencia/Error de Flujo: 'Código inalcanzable (unreachable code) detectado tras sentencia return'."
    ),
    TestCaseItem(
        id_num=20,
        title="Uso de variable no declarada en expresión",
        category="Gestión de Ámbitos y Símbolos",
        code=TEST_INVALID_20_UNDECLARED_VARIABLE,
        is_valid=False,
        rule_description="Validación de tabla de símbolos: uso de 'variableInexistente' sin declaración previa en ningún ámbito.",
        expected_behavior="Detección de Error Semántico: 'Variable variableInexistente no ha sido declarada en el ámbito accesible'."
    ),
]

VALID_TEST_CASES = [t for t in ALL_TEST_CASES if t.is_valid]
INVALID_TEST_CASES = [t for t in ALL_TEST_CASES if not t.is_valid]
