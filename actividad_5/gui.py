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

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import TEST_CASES, TestCase


class CompilerGUI:
    """
    Interfaz Gráfica de Usuario (Tkinter) para el Analizador Sintáctico de Estructuras de Control.
    Permite cargar casos de prueba de la rúbrica, editar código C arbitrario,
    visualizar el Árbol AST jerárquico y consultar diagnósticos de errores sintácticos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Actividad 5: Analizador Sintáctico de Estructuras de Control (C en Python)")
        self.root.geometry("1100, 750")
        self.root.minsize(950, 650)

        self._configure_styles()
        self._build_header()
        self._build_main_panels()
        self._build_footer()

        # Cargar caso 1 por defecto
        self._load_case_by_index(0)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TFrame", background="#1a365d")
        style.configure("HeaderTitle.TLabel", background="#1a365d", foreground="#ffffff", font=("Segoe UI", 13, "bold"))
        style.configure("HeaderSub.TLabel", background="#1a365d", foreground="#cbd5e0", font=("Segoe UI", 9))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background="#2b6cb0", foreground="#ffffff")

    def _build_header(self):
        header = ttk.Frame(self.root, style="Header.TFrame", padding=10)
        header.pack(fill=tk.X)

        title = ttk.Label(
            header,
            text="ACTIVIDAD 5: ANÁLISIS SINTÁCTICO DE ESTRUCTURAS DE CONTROL (C)",
            style="HeaderTitle.TLabel"
        )
        title.pack(anchor=tk.W)

        team_text = (
            "Integrantes: 1. DÍAZ TORRES JAZMÍN MONTSERRAT | 2. FIERRO MELÉNDEZ ERNESTO HATUEY | "
            "3. HERNÁNDEZ GARCÍA HÉCTOR GABRIEL | 4. MILLÁN GUERRERO OSWALDO JOSUÉ"
        )
        team_lbl = ttk.Label(header, text=team_text, style="HeaderSub.TLabel")
        team_lbl.pack(anchor=tk.W, pady=(2, 0))

        prof_lbl = ttk.Label(
            header,
            text="Profesor: Rigoberto Cárdenas Larios | Materia: Traductores de Lenguaje (CUCEI)",
            style="HeaderSub.TLabel"
        )
        prof_lbl.pack(anchor=tk.W)

    def _build_main_panels(self):
        # Barra superior de selección de casos de prueba
        ctrl_frame = ttk.Frame(self.root, padding=8)
        ctrl_frame.pack(fill=tk.X)

        ttk.Label(ctrl_frame, text="Seleccionar Caso de Prueba:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 6))

        self.case_var = tk.StringVar()
        options = [f"#{t.id_num:02d} - {t.name} ({'Válido' if t.is_valid else 'Con Error'})" for t in TEST_CASES]
        self.combo = ttk.Combobox(ctrl_frame, textvariable=self.case_var, values=options, state="readonly", width=55)
        self.combo.pack(side=tk.LEFT, padx=6)
        self.combo.bind("<<ComboboxSelected>>", self._on_case_selected)

        btn_analyze = ttk.Button(ctrl_frame, text="▶ Analizar Sintaxis", command=self._analyze_code)
        btn_analyze.pack(side=tk.LEFT, padx=10)

        btn_clear = ttk.Button(ctrl_frame, text="Limpiar", command=self._clear_all)
        btn_clear.pack(side=tk.LEFT)

        # Paned Window central: Código (izq) y AST / Diagnósticos (der)
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Panel Izquierdo: Editor de Código
        left_frame = ttk.LabelFrame(main_paned, text="Código Fuente en C (Editable)", padding=6)
        main_paned.add(left_frame, weight=1)

        self.txt_code = scrolledtext.ScrolledText(left_frame, font=("Consolas", 11), wrap=tk.NONE)
        self.txt_code.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho: Pestañas con AST y Errores
        right_frame = ttk.LabelFrame(main_paned, text="Resultados del Análisis Sintáctico", padding=6)
        main_paned.add(right_frame, weight=1)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Árbol AST
        tab_ast = ttk.Frame(self.notebook)
        self.notebook.add(tab_ast, text="Árbol Sintáctico (AST)")
        self.txt_ast = scrolledtext.ScrolledText(tab_ast, font=("Consolas", 10), wrap=tk.NONE, background="#f8fafc")
        self.txt_ast.pack(fill=tk.BOTH, expand=True)

        # Tab 2: Tabla de Errores y Diagnósticos
        tab_err = ttk.Frame(self.notebook)
        self.notebook.add(tab_err, text="Diagnósticos de Errores")
        self.txt_err = scrolledtext.ScrolledText(tab_err, font=("Consolas", 10), wrap=tk.WORD, background="#fff5f5")
        self.txt_err.pack(fill=tk.BOTH, expand=True)

    def _build_footer(self):
        footer = ttk.Frame(self.root, padding=6)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        self.lbl_status = ttk.Label(footer, text="Listo. Seleccione un caso de prueba o escriba su código en C.", font=("Segoe UI", 9))
        self.lbl_status.pack(side=tk.LEFT)

    def _on_case_selected(self, event=None):
        idx = self.combo.current()
        if idx >= 0:
            self._load_case_by_index(idx)

    def _load_case_by_index(self, idx: int):
        test = TEST_CASES[idx]
        self.combo.current(idx)
        self.txt_code.delete("1.0", tk.END)
        self.txt_code.insert(tk.END, test.code)
        self.lbl_status.config(text=f"Cargado Caso #{test.id_num}: {test.name} - {test.expected_behavior}")
        self._analyze_code()

    def _analyze_code(self):
        code = self.txt_code.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "El área de código está vacía.")
            return

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        error_handler = SyntaxErrorHandler()
        parser = Parser(tokens, error_handler)
        ast = parser.parse()

        # Mostrar AST
        self.txt_ast.delete("1.0", tk.END)
        self.txt_ast.insert(tk.END, ast.to_tree_str())

        # Mostrar Errores
        self.txt_err.delete("1.0", tk.END)
        if error_handler.has_errors:
            self.txt_err.insert(tk.END, error_handler.to_formatted_table())
            self.txt_err.insert(tk.END, "\n\n" + "=" * 60 + "\nDETALLES Y SUGERENCIAS:\n" + "=" * 60 + "\n")
            for err in error_handler.errors:
                self.txt_err.insert(tk.END, err.to_diagnostic_string() + "\n\n")
            self.notebook.select(1)  # Seleccionar tab de errores
            self.lbl_status.config(text=f"❌ Se detectaron {len(error_handler.errors)} error(es) sintáctico(s). Revise la pestaña de diagnósticos.")
        else:
            self.txt_err.insert(tk.END, "✅ ¡Análisis Sintáctico Exitoso!\nNo se encontraron errores de sintaxis en el código.")
            self.notebook.select(0)  # Seleccionar tab de AST
            self.lbl_status.config(text="✅ Análisis sintáctico completado sin errores. Árbol AST generado correctamente.")

    def _clear_all(self):
        self.txt_code.delete("1.0", tk.END)
        self.txt_ast.delete("1.0", tk.END)
        self.txt_err.delete("1.0", tk.END)
        self.lbl_status.config(text="Áreas de texto limpias.")


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
