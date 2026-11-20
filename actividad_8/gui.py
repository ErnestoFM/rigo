"""
================================================================================
ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - VERIFICACIÓN DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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
from semantic_analyzer import SemanticAnalyzer
from symbol_table import SymbolTable
from semantic_errors import SemanticErrorHandler
from test_cases import TEST_CASES, TestCase


class CompilerGUI:
    """
    Interfaz Gráfica de Usuario (Tkinter) para la Verificación de Expresiones Aritméticas y Lógicas.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Actividad 8: Análisis Semántico - Verificación de Expresiones Aritméticas y Lógicas (C)")
        self.root.geometry("1150, 780")
        self.root.minsize(980, 680)

        self._configure_styles()
        self._build_header()
        self._build_main_panels()
        self._build_footer()

        self._load_case_by_index(0)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TFrame", background="#0f172a")
        style.configure("HeaderTitle.TLabel", background="#0f172a", foreground="#ffffff", font=("Segoe UI", 13, "bold"))
        style.configure("HeaderSub.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Consolas", 9), rowheight=24)

    def _build_header(self):
        header = ttk.Frame(self.root, style="Header.TFrame", padding=10)
        header.pack(fill=tk.X)

        title = ttk.Label(
            header,
            text="ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - EXPRESIONES ARITMÉTICAS Y LÓGICAS (C)",
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
        ctrl_frame = ttk.Frame(self.root, padding=8)
        ctrl_frame.pack(fill=tk.X)

        ttk.Label(ctrl_frame, text="Caso de Prueba:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 6))

        self.case_var = tk.StringVar()
        options = [f"#{t.id_num:02d} - {t.name} ({'Válido' if t.is_valid else 'Con Error'})" for t in TEST_CASES]
        self.combo = ttk.Combobox(ctrl_frame, textvariable=self.case_var, values=options, state="readonly", width=58)
        self.combo.pack(side=tk.LEFT, padx=6)
        self.combo.bind("<<ComboboxSelected>>", self._on_case_selected)

        btn_analyze = ttk.Button(ctrl_frame, text="▶ Validar Expresiones", command=self._analyze_code)
        btn_analyze.pack(side=tk.LEFT, padx=10)

        btn_clear = ttk.Button(ctrl_frame, text="Limpiar", command=self._clear_all)
        btn_clear.pack(side=tk.LEFT)

        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Editor de Código
        left_frame = ttk.LabelFrame(main_paned, text="Código de Expresiones en C (Editable)", padding=6)
        main_paned.add(left_frame, weight=1)

        self.txt_code = scrolledtext.ScrolledText(left_frame, font=("Consolas", 11), wrap=tk.NONE)
        self.txt_code.pack(fill=tk.BOTH, expand=True)

        # Resultados
        right_frame = ttk.LabelFrame(main_paned, text="Validación Semántica y Evaluación", padding=6)
        main_paned.add(right_frame, weight=2)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Tabla de Símbolos y Valores
        tab_symbols = ttk.Frame(self.notebook)
        self.notebook.add(tab_symbols, text="Tabla de Símbolos")

        cols = ("id", "tipo", "valor", "ubicacion")
        self.tree = ttk.Treeview(tab_symbols, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("id", text="Identificador")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("valor", text="Valor Evaluado")
        self.tree.heading("ubicacion", text="Línea:Col")

        self.tree.column("id", width=120, anchor=tk.W)
        self.tree.column("tipo", width=90, anchor=tk.CENTER)
        self.tree.column("valor", width=160, anchor=tk.CENTER)
        self.tree.column("ubicacion", width=90, anchor=tk.CENTER)

        tree_scroll = ttk.Scrollbar(tab_symbols, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Tab 2: Errores en Expresiones
        tab_err = ttk.Frame(self.notebook)
        self.notebook.add(tab_err, text="Errores en Expresiones")
        self.txt_err = scrolledtext.ScrolledText(tab_err, font=("Consolas", 10), wrap=tk.WORD, background="#fff5f5")
        self.txt_err.pack(fill=tk.BOTH, expand=True)

        # Tab 3: AST Anotado
        tab_ast = ttk.Frame(self.notebook)
        self.notebook.add(tab_ast, text="AST Anotado")
        self.txt_ast = scrolledtext.ScrolledText(tab_ast, font=("Consolas", 10), wrap=tk.NONE, background="#f8fafc")
        self.txt_ast.pack(fill=tk.BOTH, expand=True)

    def _build_footer(self):
        footer = ttk.Frame(self.root, padding=6)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        self.lbl_status = ttk.Label(footer, text="Listo. Seleccione un caso de prueba.", font=("Segoe UI", 9))
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
        self.lbl_status.config(text=f"Cargado Caso #{test.id_num}: {test.name}")
        self._analyze_code()

    def _analyze_code(self):
        code = self.txt_code.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "El área de código está vacía.")
            return

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        symbol_table = SymbolTable()
        error_handler = SemanticErrorHandler()
        analyzer = SemanticAnalyzer(symbol_table, error_handler)
        is_valid = analyzer.analyze(ast)

        # 1. Poblar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, sym in symbol_table.symbols.items():
            val_str = str(sym.value) if sym.value is not None else "(indefinido)"
            if sym.data_type == "string" and sym.value is not None:
                val_str = f'"{sym.value}"'
            loc_str = f"L:{sym.line}, C:{sym.column}"
            self.tree.insert("", tk.END, values=(sym.name, sym.data_type, val_str, loc_str))

        # 2. Mostrar Errores
        self.txt_err.delete("1.0", tk.END)
        if error_handler.has_errors:
            self.txt_err.insert(tk.END, error_handler.to_formatted_table())
            self.txt_err.insert(tk.END, "\n\n" + "=" * 60 + "\nDIAGNÓSTICOS DETALLADOS Y SUGERENCIAS:\n" + "=" * 60 + "\n\n")
            for err in error_handler.errors:
                self.txt_err.insert(tk.END, err.to_diagnostic_string() + "\n\n")
            self.notebook.select(1)
            self.lbl_status.config(text=f"❌ Se detectaron {len(error_handler.errors)} error(es) en expresiones.")
        else:
            self.txt_err.insert(tk.END, "✅ ¡Validación de Expresiones Exitosa!\nTodas las operaciones aritméticas y lógicas son válidas y consistentes.")
            self.notebook.select(0)
            self.lbl_status.config(text=f"✅ Expresiones validadas con éxito. {len(symbol_table.symbols)} variable(s) evaluada(s).")

        # 3. Mostrar AST
        self.txt_ast.delete("1.0", tk.END)
        self.txt_ast.insert(tk.END, ast.to_tree_str())

    def _clear_all(self):
        self.txt_code.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.txt_err.delete("1.0", tk.END)
        self.txt_ast.delete("1.0", tk.END)
        self.lbl_status.config(text="Áreas de texto limpias.")


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
