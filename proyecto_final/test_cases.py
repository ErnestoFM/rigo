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

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TestCase:
    id: str
    name: str
    category: str  # "VÁLIDO" o "INVÁLIDO"
    target_phase: str
    description: str
    source_code: str
    expected_success: bool
    expected_output: Optional[str] = None
    expected_error_type: Optional[str] = None


TEST_CASES: List[TestCase] = [
    TestCase(
        id="CP01",
        name="Expresiones Aritméticas y Variables",
        category="VÁLIDO",
        target_phase="Completa (Lex -> AST -> Sem -> TAC -> Opt -> ASM -> VM)",
        description="Evalúa precedencia de operadores aritméticos, asignación de variables y salida estándar.",
        source_code="""int a = 15;
int b = 5;
int c = 2;
int resultado = a + b * c - (a / b);
print(resultado);
""",
        expected_success=True,
        expected_output="> 22"
    ),
    TestCase(
        id="CP02",
        name="Estructuras de Control Condicional (If-Else y Switch-Case)",
        category="VÁLIDO",
        target_phase="Completa (Control de flujo y bifurcaciones condicionales)",
        description="Evalúa estructuras condicionales compuestas if-else y bifurcación selectiva switch-case con break.",
        source_code="""int edad = 20;
int categoria = 0;
if (edad >= 18) {
    categoria = 1;
} else {
    categoria = 2;
}

int bono = 0;
switch (categoria) {
    case 1:
        bono = 500;
        break;
    case 2:
        bono = 100;
        break;
    default:
        bono = 0;
}
print(bono);
""",
        expected_success=True,
        expected_output="> 500"
    ),
    TestCase(
        id="CP03",
        name="Estructuras de Control Iterativas (Bucle While)",
        category="VÁLIDO",
        target_phase="Completa (Bucles, saltos condicionales e incondicionales)",
        description="Calcula la sumatoria de enteros del 1 al 5 mediante un bucle while interactuando con memoria RAM.",
        source_code="""int contador = 1;
int acumulador = 0;
while (contador <= 5) {
    acumulador = acumulador + contador;
    contador = contador + 1;
}
print(acumulador);
""",
        expected_success=True,
        expected_output="> 15"
    ),
    TestCase(
        id="CP04",
        name="Definición e Invocación de Funciones con Parámetros",
        category="VÁLIDO",
        target_phase="Completa (Subrutinas, call stack, paso de parámetros y retornos)",
        description="Declara una función para calcular el área de un triángulo, pasando argumentos y retornando valor.",
        source_code="""int calcularArea(int base, int altura) {
    int area = (base * altura) / 2;
    return area;
}
int b = 10;
int h = 8;
int res = calcularArea(b, h);
print(res);
""",
        expected_success=True,
        expected_output="> 40"
    ),
    TestCase(
        id="CP05",
        name="Programación Orientada a Objetos (Clases y Métodos)",
        category="VÁLIDO",
        target_phase="Completa (Clases, atributos de instancia, métodos y mensajes)",
        description="Declara una clase Banco con atributos y método de depósito, instanciando un objeto e invocándolo.",
        source_code="""class Banco {
    int saldo;
    void depositar(int monto) {
        saldo = saldo + monto;
        print(saldo);
    }
}
Banco cuenta;
cuenta.depositar(750);
""",
        expected_success=True,
        expected_output="> 750"
    ),
    TestCase(
        id="CP06",
        name="Detección de Error Léxico (Caracteres no reconocidos)",
        category="INVÁLIDO",
        target_phase="Análisis Léxico",
        description="Contiene caracteres ilegales (@ y #) que no pertenecen al alfabeto del lenguaje C.",
        source_code="""int total = 100;
int valor = 50 @# 20;
print(total);
""",
        expected_success=False,
        expected_error_type="Error Léxico"
    ),
    TestCase(
        id="CP07",
        name="Detección de Error Sintáctico (Paréntesis de condición no cerrado)",
        category="INVÁLIDO",
        target_phase="Análisis Sintáctico",
        description="Estructura if con condición mal formada por omisión del paréntesis de cierre.",
        source_code="""int a = 10;
if (a > 5 {
    print(a);
}
""",
        expected_success=False,
        expected_error_type="Error Sintáctico"
    ),
    TestCase(
        id="CP08",
        name="Detección de Error Semántico (Incompatibilidad de Tipos)",
        category="INVÁLIDO",
        target_phase="Análisis Semántico",
        description="Intento de asignar una constante de tipo string a una variable declarada int.",
        source_code="""int numero = "cadena_invalida";
print(numero);
""",
        expected_success=False,
        expected_error_type="Error Semántico"
    ),
    TestCase(
        id="CP09",
        name="Detección de Error Semántico (Función No Declarada)",
        category="INVÁLIDO",
        target_phase="Análisis Semántico",
        description="Invocación a la función 'sumarValores' que no ha sido definida en la tabla de símbolos.",
        source_code="""int a = 10;
int b = sumarValores(a, 20);
print(b);
""",
        expected_success=False,
        expected_error_type="Error Semántico"
    ),
    TestCase(
        id="CP10",
        name="Detección de Error Semántico en POO (Método Inexistente)",
        category="INVÁLIDO",
        target_phase="Análisis Semántico",
        description="Llamada al método 'acelerar' sobre un objeto de la clase 'Auto' donde el método no existe.",
        source_code="""class Auto {
    int velocidad;
}
Auto miAuto;
miAuto.acelerar();
""",
        expected_success=False,
        expected_error_type="Error Semántico"
    )
]
