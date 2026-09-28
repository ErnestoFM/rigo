"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import ALL_TEST_CASES

class SyntaxAnalyzerExpressionsGUI:
    """
    Interfaz Gráfica de Usuario (GUI) interactiva para el Analizador Sintáctico
    de Expresiones Aritméticas y Lógicas con visualización de AST y diagnóstico de errores.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Compilador - Actividad 4: Análisis Sintáctico de Expresiones Aritméticas y Lógicas")
        self.root.geometry("1200x820")
        self.root.minsize(1000, 700)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.root.configure(bg="#181825")

        self._prepare_cases_map()
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Cargar caso 1 válido por defecto
        first_case_key = list(self.cases_map.keys())[0]
        self._load_selected_case(first_case_key)

    def _prepare_cases_map(self):
        self.cases_map = {}
        for cat, items in ALL_TEST_CASES.items():
            for name, expr in items:
                display_key = f"[{cat[:3].upper()}] {name}"
                self.cases_map[display_key] = expr

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e1e2e", padx=18, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS",
            font=("Segoe UI", 13, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa"
        )
        title_label.pack(anchor="w")

        subtitle = "Profesor: Rigoberto Cárdenas Larios  |  Traductores de Lenguaje / Compiladores\n" \
                   "Integrantes del Equipo (Orden Alfabético por Primer Apellido):\n" \
                   "1. DIAZ TORRES JAZMIN MONTSERRAT  |  2. FIERRO MELÉNDEZ ERNESTO HATUEY\n" \
                   "3. HERNANDEZ GARCIA HECTOR GABRIEL  |  4. MILLAN GUERRERO OSWALDO JOSUE"

        members_label = tk.Label(
            header_frame,
            text=subtitle,
            font=("Segoe UI", 9),
            bg="#1e1e2e",
            fg="#cdd6f4",
            justify="left"
        )
        members_label.pack(anchor="w", pady=(4, 0))

    def _create_main_content(self):
        main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL, bg="#181825", sashwidth=6, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # ---------------- Panel Superior: Editor y Controles ----------------
        top_frame = tk.Frame(main_pane, bg="#181825")
        main_pane.add(top_frame, minsize=240)

        control_frame = tk.Frame(top_frame, bg="#181825")
        control_frame.pack(fill=tk.X, pady=(0, 6))

        lbl_select = tk.Label(control_frame, text="Cargar Caso de Prueba:", font=("Segoe UI", 10, "bold"), bg="#181825", fg="#a6adc8")
        lbl_select.pack(side=tk.LEFT, padx=(0, 8))

        self.case_var = tk.StringVar()
        case_keys = list(self.cases_map.keys())
        case_combo = ttk.Combobox(
            control_frame,
            textvariable=self.case_var,
            values=case_keys,
            state="readonly",
            width=58,
            font=("Segoe UI", 9)
        )
        case_combo.pack(side=tk.LEFT, padx=(0, 10))
        case_combo.bind("<<ComboboxSelected>>", lambda e: self._load_selected_case(self.case_var.get()))

        btn_analyze = tk.Button(
            control_frame,
            text="▶ ANALIZAR SINTAXIS",
            command=self.analyze_expression,
            font=("Segoe UI", 9, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            padx=14,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_analyze.pack(side=tk.LEFT, padx=5)

        btn_clear = tk.Button(
            control_frame,
            text="Limpiar",
            command=self._clear_editor,
            font=("Segoe UI", 9),
            bg="#45475a",
            fg="#cdd6f4",
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_clear.pack(side=tk.LEFT, padx=5)

        # Barra de botones rápidos de operadores
        quick_op_frame = tk.Frame(top_frame, bg="#181825")
        quick_op_frame.pack(fill=tk.X, pady=(2, 6))

        lbl_ops = tk.Label(quick_op_frame, text="Insertar Operador:", font=("Segoe UI", 8, "bold"), bg="#181825", fg="#9399b2")
        lbl_ops.pack(side=tk.LEFT, padx=(0, 6))

        quick_ops = ["+", "-", "*", "/", "%", "^", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "(", ")"]
        for op in quick_ops:
            b = tk.Button(
                quick_op_frame,
                text=op,
                command=lambda o=op: self._insert_operator(o),
                font=("Consolas", 8, "bold"),
                bg="#313244",
                fg="#cdd6f4",
                activebackground="#45475a",
                padx=5,
                pady=1,
                relief=tk.FLAT,
                cursor="hand2"
            )
            b.pack(side=tk.LEFT, padx=2)

        # Editor de Expresión
        editor_label = tk.Label(top_frame, text="Expresión de Entrada a Analizar:", font=("Segoe UI", 9, "bold"), bg="#181825", fg="#cdd6f4")
        editor_label.pack(anchor="w")

        self.code_editor = scrolledtext.ScrolledText(
            top_frame,
            wrap=tk.WORD,
            font=("Consolas", 13),
            bg="#11111b",
            fg="#cdd6f4",
            insertbackground="#f5e0dc",
            height=3,
            relief=tk.FLAT,
            padx=8,
            pady=8
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # ---------------- Panel Inferior: Pestañas de Resultados ----------------
        bottom_frame = tk.Frame(main_pane, bg="#181825")
        main_pane.add(bottom_frame, minsize=350)

        notebook = ttk.Notebook(bottom_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Árbol de Sintaxis Abstracta (AST)
        tab_ast = tk.Frame(notebook, bg="#11111b")
        notebook.add(tab_ast, text="  🌳 Árbol Sintáctico (AST)  ")

        self.ast_text = scrolledtext.ScrolledText(
            tab_ast,
            font=("Consolas", 10),
            bg="#11111b",
            fg="#89b4fa",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.ast_text.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Errores Sintácticos
        tab_errors = tk.Frame(notebook, bg="#181825")
        notebook.add(tab_errors, text="  ❌ Errores Sintácticos  ")

        error_cols = ("#", "Línea", "Columna", "Categoría", "Token", "Mensaje Estándar", "Sugerencia Pedagógica")
        self.error_tree = ttk.Treeview(tab_errors, columns=error_cols, show="headings")

        self.error_tree.heading("#", text="#")
        self.error_tree.heading("Línea", text="Línea")
        self.error_tree.heading("Columna", text="Columna")
        self.error_tree.heading("Categoría", text="Categoría")
        self.error_tree.heading("Token", text="Token")
        self.error_tree.heading("Mensaje Estándar", text="Mensaje Estándar de Error")
        self.error_tree.heading("Sugerencia Pedagógica", text="Sugerencia Pedagógica")

        self.error_tree.column("#", width=35, anchor="center")
        self.error_tree.column("Línea", width=55, anchor="center")
        self.error_tree.column("Columna", width=65, anchor="center")
        self.error_tree.column("Categoría", width=160, anchor="w")
        self.error_tree.column("Token", width=70, anchor="center")
        self.error_tree.column("Mensaje Estándar", width=250, anchor="w")
        self.error_tree.column("Sugerencia Pedagógica", width=340, anchor="w")

        err_scroll = ttk.Scrollbar(tab_errors, orient=tk.VERTICAL, command=self.error_tree.yview)
        self.error_tree.configure(yscrollcommand=err_scroll.set)
        self.error_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        err_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña 3: Tokens Léxicos
        tab_tokens = tk.Frame(notebook, bg="#181825")
        notebook.add(tab_tokens, text="  🔍 Tokens Léxicos  ")

        tok_cols = ("#", "Tipo de Token", "Lexema", "Línea", "Columna")
        self.tok_tree = ttk.Treeview(tab_tokens, columns=tok_cols, show="headings")

        self.tok_tree.heading("#", text="#")
        self.tok_tree.heading("Tipo de Token", text="Tipo de Token")
        self.tok_tree.heading("Lexema", text="Lexema / Valor")
        self.tok_tree.heading("Línea", text="Línea")
        self.tok_tree.heading("Columna", text="Columna")

        self.tok_tree.column("#", width=40, anchor="center")
        self.tok_tree.column("Tipo de Token", width=220, anchor="w")
        self.tok_tree.column("Lexema", width=180, anchor="w")
        self.tok_tree.column("Línea", width=70, anchor="center")
        self.tok_tree.column("Columna", width=70, anchor="center")

        tok_scroll = ttk.Scrollbar(tab_tokens, orient=tk.VERTICAL, command=self.tok_tree.yview)
        self.tok_tree.configure(yscrollcommand=tok_scroll.set)
        self.tok_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tok_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña 4: Reglas de la Gramática
        tab_grammar = tk.Frame(notebook, bg="#11111b")
        notebook.add(tab_grammar, text="  📜 Reglas de la Gramática  ")

        grammar_text = scrolledtext.ScrolledText(
            tab_grammar,
            font=("Consolas", 10),
            bg="#11111b",
            fg="#a6adc8",
            relief=tk.FLAT,
            padx=12,
            pady=12
        )
        grammar_text.pack(fill=tk.BOTH, expand=True)

        grammar_content = """================================================================================
GRAMÁTICA FORMAL DE EXPRESIONES ARITMÉTICAS Y LÓGICAS (EBNF / BNF)
================================================================================

expresion            -> expresion_logica | expresion_aritmetica

expresion_logica     -> termino_logico (( '&&' | '||' ) termino_logico)*

termino_logico       -> expresion_aritmetica ( '==' | '!=' | '>' | '<' | '>=' | '<=' ) expresion_aritmetica
                      | expresion_aritmetica
                      | '!' termino_logico

expresion_aritmetica -> termino (( '+' | '-' ) termino)*

termino              -> factor (( '*' | '/' | '%' | '^' ) factor)*

factor               -> IDENTIFICADOR
                      | NUMERO_ENTERO
                      | NUMERO_FLOTANTE
                      | '(' expresion ')'
                      | ( '+' | '-' ) factor

================================================================================
EXPLICACIÓN DE REGLAS SINTÁCTICAS Y PRECEDENCIA:
================================================================================
1. Precedencia de Operadores (De mayor a menor prioridad):
   - Nivel 1 (Máxima): Paréntesis '(' ')' y factores unarios (+, -, !).
   - Nivel 2: Operadores exponenciales / potencias (^, **).
   - Nivel 3: Operadores multiplicativos (*, /, %).
   - Nivel 4: Operadores aditivos (+, -).
   - Nivel 5: Operadores relacionales de comparación (==, !=, <, <=, >, >=).
   - Nivel 6: Conjunción lógica (&&, and).
   - Nivel 7 (Mínima): Disyunción lógica (||, or).

2. Gestión de Errores Sintácticos Requeridos:
   - Operador sin término: 'x + * y', '5 +', '+ 10'
   - Comparación inválida: '10 >', '> 5', '10 > && 4'
   - Paréntesis desbalanceados: '(a - b', '5 / (2 + )', '(x + y)) * 2'
   - Expresión lógica incompleta: '10 > 5 &&', '&& 3 <= 4'
   - Falta de operador: 'a + b c'
"""
        grammar_text.insert(tk.END, grammar_content)
        grammar_text.configure(state="disabled")

    def _create_status_bar(self):
        self.status_bar = tk.Label(
            self.root,
            text="Listo para analizar expresiones. Integrantes: Díaz, Fierro, Hernández, Millán.",
            font=("Segoe UI", 9),
            bg="#1e1e2e",
            fg="#a6adc8",
            anchor="w",
            padx=12,
            pady=4
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _load_selected_case(self, case_key: str):
        if case_key in self.cases_map:
            code = self.cases_map[case_key]
            self.case_var.set(case_key)
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert(tk.END, code)
            self.analyze_expression()

    def _clear_editor(self):
        self.code_editor.delete("1.0", tk.END)
        self.ast_text.delete("1.0", tk.END)
        for item in self.error_tree.get_children():
            self.error_tree.delete(item)
        for item in self.tok_tree.get_children():
            self.tok_tree.delete(item)
        self.status_bar.configure(text="Editor limpio.", fg="#a6adc8")

    def _insert_operator(self, op: str):
        if op == "( )":
            self.code_editor.insert(tk.INSERT, "()")
            pos = self.code_editor.index(tk.INSERT)
            line, col = pos.split(".")
            self.code_editor.mark_set(tk.INSERT, f"{line}.{int(col)-1}")
        else:
            self.code_editor.insert(tk.INSERT, f" {op} ")
        self.code_editor.focus_set()

    def analyze_expression(self):
        raw_code = self.code_editor.get("1.0", tk.END).strip()
        if not raw_code:
            self.status_bar.configure(text="Advertencia: Ingrese una expresión.", fg="#f38ba8")
            return

        # Limpiar resultados previos
        self.ast_text.delete("1.0", tk.END)
        for item in self.error_tree.get_children():
            self.error_tree.delete(item)
        for item in self.tok_tree.get_children():
            self.tok_tree.delete(item)

        # 1. Análisis Léxico
        lexer = Lexer(raw_code)
        tokens = lexer.tokenize()

        for i, t in enumerate(tokens, 1):
            if t.type.name != "EOF":
                self.tok_tree.insert("", tk.END, values=(i, t.type.name, t.value, t.line, t.column))

        # 2. Análisis Sintáctico
        error_handler = SyntaxErrorHandler()
        parser = Parser(tokens, error_handler)
        ast = parser.parse()

        # 3. Presentación del AST
        self.ast_text.insert(tk.END, f"EXPRESIÓN ANALIZADA: '{raw_code}'\n")
        self.ast_text.insert(tk.END, "=" * 80 + "\n\n")
        self.ast_text.insert(tk.END, ast.to_tree_str(prefix=""))

        # 4. Presentación de Errores
        if error_handler.has_errors():
            for i, err in enumerate(error_handler.errors, 1):
                std_msg = f"Error: {err.message} en la línea {err.line}, columna {err.column}."
                self.error_tree.insert("", tk.END, values=(
                    i, err.line, err.column, err.category, err.offending_token or "-", std_msg, err.suggestion
                ))
            err_count = len(error_handler.errors)
            self.status_bar.configure(
                text=f"❌ Se detectaron {err_count} errores sintácticos. Consulte la pestaña de errores.",
                fg="#f38ba8"
            )
        else:
            self.status_bar.configure(
                text="✔ Análisis Sintáctico exitoso: 0 errores detectados. Expresión válida conforme a la gramática.",
                fg="#a6e3a1"
            )

def main():
    root = tk.Tk()
    app = SyntaxAnalyzerExpressionsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
