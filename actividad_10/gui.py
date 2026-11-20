"""
================================================================================
ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
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
from tac_generator import TACGenerator
from symbol_table import SymbolTable
from error_handler import TACErrorHandler
from test_cases import TEST_CASES, TestCase


class CompilerGUI:
    """
    Interfaz Gráfica de Usuario (Tkinter) para la Generación de Código Intermedio.
    Permite visualizar el código fuente en C, el Código Intermedio de Tres Direcciones
    (TAC) con comentarios y explicaciones, y el panel de diagnósticos y guardas.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Actividad 10: Generador de Código Intermedio de Tres Direcciones (TAC)")
        self.root.geometry("1180, 780")
        self.root.minsize(980, 680)

        self._configure_styles()
        self._build_header()
        self._build_main_panels()
        self._build_footer()

        self._load_case_by_index(0)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TFrame", background="#1e293b")
        style.configure("HeaderTitle.TLabel", background="#1e293b", foreground="#ffffff", font=("Segoe UI", 13, "bold"))
        style.configure("HeaderSub.TLabel", background="#1e293b", foreground="#94a3b8", font=("Segoe UI", 9))

    def _build_header(self):
        header = ttk.Frame(self.root, style="Header.TFrame", padding=10)
        header.pack(fill=tk.X)

        title = ttk.Label(
            header,
            text="ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)",
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
        self.combo = ttk.Combobox(ctrl_frame, textvariable=self.case_var, values=options, state="readonly", width=62)
        self.combo.pack(side=tk.LEFT, padx=6)
        self.combo.bind("<<ComboboxSelected>>", self._on_case_selected)

        btn_analyze = ttk.Button(ctrl_frame, text="▶ Generar Código Intermedio", command=self._analyze_code)
        btn_analyze.pack(side=tk.LEFT, padx=10)

        btn_clear = ttk.Button(ctrl_frame, text="Limpiar", command=self._clear_all)
        btn_clear.pack(side=tk.LEFT)

        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Editor de Código Fuente C
        left_frame = ttk.LabelFrame(main_paned, text="Código Fuente en C (Editable)", padding=6)
        main_paned.add(left_frame, weight=1)

        self.txt_code = scrolledtext.ScrolledText(left_frame, font=("Consolas", 11), wrap=tk.NONE)
        self.txt_code.pack(fill=tk.BOTH, expand=True)

        # Resultados de Código Intermedio y Diagnósticos
        right_frame = ttk.LabelFrame(main_paned, text="Código Intermedio (Tres Direcciones - TAC)", padding=6)
        main_paned.add(right_frame, weight=2)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Código Intermedio TAC
        tab_tac = ttk.Frame(self.notebook)
        self.notebook.add(tab_tac, text="Código Intermedio (TAC)")
        self.txt_tac = scrolledtext.ScrolledText(tab_tac, font=("Consolas", 10), wrap=tk.NONE, background="#0f172a", foreground="#38bdf8")
        self.txt_tac.pack(fill=tk.BOTH, expand=True)

        # Tab 2: Validaciones y Errores
        tab_err = ttk.Frame(self.notebook)
        self.notebook.add(tab_err, text="Validaciones y Errores")
        self.txt_err = scrolledtext.ScrolledText(tab_err, font=("Consolas", 10), wrap=tk.WORD, background="#fff5f5")
        self.txt_err.pack(fill=tk.BOTH, expand=True)

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
        error_handler = TACErrorHandler()
        generator = TACGenerator(symbol_table, error_handler)
        instructions = generator.generate(ast)

        # Mostrar TAC
        self.txt_tac.delete("1.0", tk.END)
        self.txt_tac.insert(tk.END, generator.to_formatted_tac_string())

        # Mostrar Errores / Guardas
        self.txt_err.delete("1.0", tk.END)
        if error_handler.has_errors:
            self.txt_err.insert(tk.END, error_handler.to_formatted_table())
            self.txt_err.insert(tk.END, "\n\n" + "=" * 60 + "\nDIAGNÓSTICOS DETALLADOS:\n" + "=" * 60 + "\n\n")
            for err in error_handler.errors:
                self.txt_err.insert(tk.END, err.to_diagnostic_string() + "\n\n")
            self.notebook.select(1)
            self.lbl_status.config(text=f"❌ Se emitieron guardas de validación ({len(error_handler.errors)} error/bloqueo).")
        else:
            self.txt_err.insert(tk.END, "✅ ¡Código Intermedio Generado Exitosamente!\nNo se presentaron discrepancias de tipos ni divisiones por cero.")
            self.notebook.select(0)
            self.lbl_status.config(text=f"✅ Código Intermedio generado con éxito ({len(instructions)} instrucciones TAC).")

    def _clear_all(self):
        self.txt_code.delete("1.0", tk.END)
        self.txt_tac.delete("1.0", tk.END)
        self.txt_err.delete("1.0", tk.END)
        self.lbl_status.config(text="Áreas de texto limpias.")


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
