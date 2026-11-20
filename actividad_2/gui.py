"""
================================================================================
ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from token_type import TokenType, Token
from error_handler import ErrorHandler, LexicalErrorCategory
from lexer import LexerC
from test_cases import ALL_TEST_CASES, TestCaseItem


class LexicalAnalyzerGUI:
    """
    Interfaz Gráfica de Usuario interactiva para la demostración y verificación
    del análisis léxico y gestión de errores léxicos en C.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Compilador C - Actividad 2: Manejo de Errores Léxicos")
        self.root.geometry("1260x820")
        self.root.minsize(1050, 680)

        self.error_handler = ErrorHandler()

        self._configure_styles()
        self._build_header()
        self._build_controls()
        self._build_main_layout()
        self._build_status_bar()

        # Seleccionar primer caso por defecto
        self.combo_cases.current(0)
        self.on_case_selected(None)

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure("Header.TFrame", background="#0F172A")
        style.configure("HeaderTitle.TLabel", background="#0F172A", foreground="#38BDF8", font=("Segoe UI", 13, "bold"))
        style.configure("HeaderSub.TLabel", background="#0F172A", foreground="#94A3B8", font=("Segoe UI", 9))
        style.configure("HeaderTeam.TLabel", background="#0F172A", foreground="#F8FAFC", font=("Segoe UI", 8, "bold"))

        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
        style.configure("Primary.TButton", background="#0284C7", foreground="#FFFFFF")
        style.configure("Success.TButton", background="#10B981", foreground="#FFFFFF")
        style.configure("Secondary.TButton", background="#475569", foreground="#FFFFFF")

        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Consolas", 9), rowheight=24)

    def _build_header(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=(15, 10))
        header_frame.pack(fill=tk.X)

        title_lbl = ttk.Label(
            header_frame,
            text="ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)",
            style="HeaderTitle.TLabel"
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = ttk.Label(
            header_frame,
            text="Materia: Traductores de Lenguaje / Compiladores  •  Profesor: Rigoberto Cárdenas Larios",
            style="HeaderSub.TLabel"
        )
        sub_lbl.pack(anchor=tk.W, pady=(2, 4))

        team_text = (
            "Integrantes (Orden Alfabético por Primer Apellido): "
            "1. DÍAZ TORRES JAZMÍN MONTSERRAT  |  "
            "2. FIERRO MELÉNDEZ ERNESTO HATUEY  |  "
            "3. HERNÁNDEZ GARCÍA HÉCTOR GABRIEL  |  "
            "4. MILLÁN GUERRERO OSWALDO JOSUÉ"
        )
        team_lbl = ttk.Label(header_frame, text=team_text, style="HeaderTeam.TLabel")
        team_lbl.pack(anchor=tk.W)

    def _build_controls(self):
        ctrl_frame = ttk.Frame(self.root, padding=(15, 8))
        ctrl_frame.pack(fill=tk.X)

        ttk.Label(ctrl_frame, text="Casos de Prueba:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))

        case_names = [f"Caso {t.id_num:02d}: {t.title} ({'Válido' if t.is_valid else 'Inválido'})" for t in ALL_TEST_CASES]
        case_names.append("Personalizado (Escribir código libremente)")
        self.combo_cases = ttk.Combobox(ctrl_frame, values=case_names, width=56, state="readonly", font=("Segoe UI", 9))
        self.combo_cases.pack(side=tk.LEFT, padx=(0, 15))
        self.combo_cases.bind("<<ComboboxSelected>>", self.on_case_selected)

        btn_run = ttk.Button(ctrl_frame, text="▶ Analizar Léxicamente", style="Primary.TButton", command=self.action_tokenize)
        btn_run.pack(side=tk.LEFT, padx=4)

        btn_clear = ttk.Button(ctrl_frame, text="🧹 Limpiar Editor", style="Secondary.TButton", command=self.action_clear)
        btn_clear.pack(side=tk.LEFT, padx=4)

    def _build_main_layout(self):
        panes = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=15, pady=(4, 8))

        # Panel Izquierdo: Editor de Código
        left_frame = ttk.LabelFrame(panes, text=" Código Fuente en C ", padding=8)
        panes.add(left_frame, weight=1)

        self.lbl_case_info = ttk.Label(left_frame, text="", font=("Segoe UI", 9, "italic"), foreground="#0369A1", wraplength=550)
        self.lbl_case_info.pack(anchor=tk.W, pady=(0, 6))

        self.txt_source = scrolledtext.ScrolledText(left_frame, font=("Consolas", 11), wrap=tk.NONE, undo=True)
        self.txt_source.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho: Notebook con Pestañas de Resultados
        right_frame = ttk.Frame(panes)
        panes.add(right_frame, weight=2)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Componentes Léxicos (Tokens)
        self.tab_tokens = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tokens, text="  1. Tabla de Tokens  ")
        self._build_tab_tokens()

        # Pestaña 2: Diagnóstico de Errores Léxicos
        self.tab_errors = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_errors, text="  2. Reporte de Errores Léxicos  ")
        self._build_tab_errors()

    def _build_tab_tokens(self):
        cols = ("num", "line", "col", "category", "lexeme")
        self.tree_tokens = ttk.Treeview(self.tab_tokens, columns=cols, show="headings")
        self.tree_tokens.heading("num", text="#")
        self.tree_tokens.heading("line", text="Línea")
        self.tree_tokens.heading("col", text="Col")
        self.tree_tokens.heading("category", text="Categoría Léxica")
        self.tree_tokens.heading("lexeme", text="Lexema / Valor")

        self.tree_tokens.column("num", width=45, anchor=tk.CENTER)
        self.tree_tokens.column("line", width=55, anchor=tk.CENTER)
        self.tree_tokens.column("col", width=50, anchor=tk.CENTER)
        self.tree_tokens.column("category", width=220, anchor=tk.W)
        self.tree_tokens.column("lexeme", width=300, anchor=tk.W)

        scroll = ttk.Scrollbar(self.tab_tokens, orient=tk.VERTICAL, command=self.tree_tokens.yview)
        self.tree_tokens.configure(yscrollcommand=scroll.set)

        self.tree_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=4)

    def _build_tab_errors(self):
        # Panel superior de resumen estadístico
        self.stats_frame = ttk.LabelFrame(self.tab_errors, text=" Resumen Estadístico de Errores ", padding=8)
        self.stats_frame.pack(fill=tk.X, padx=4, pady=(4, 6))

        self.lbl_stats = ttk.Label(self.stats_frame, text="Sin análisis ejecutado.", font=("Segoe UI", 9, "bold"))
        self.lbl_stats.pack(anchor=tk.W)

        # Tabla de errores
        cols = ("num", "line", "col", "cat", "lex", "desc")
        self.tree_errors = ttk.Treeview(self.tab_errors, columns=cols, show="headings")
        self.tree_errors.heading("num", text="#")
        self.tree_errors.heading("line", text="Línea")
        self.tree_errors.heading("col", text="Col")
        self.tree_errors.heading("cat", text="Categoría de Error")
        self.tree_errors.heading("lex", text="Lexema Defectuoso")
        self.tree_errors.heading("desc", text="Descripción y Sugerencia de Corrección")

        self.tree_errors.column("num", width=40, anchor=tk.CENTER)
        self.tree_errors.column("line", width=50, anchor=tk.CENTER)
        self.tree_errors.column("col", width=50, anchor=tk.CENTER)
        self.tree_errors.column("cat", width=190, anchor=tk.W)
        self.tree_errors.column("lex", width=160, anchor=tk.CENTER)
        self.tree_errors.column("desc", width=380, anchor=tk.W)

        scroll_err = ttk.Scrollbar(self.tab_errors, orient=tk.VERTICAL, command=self.tree_errors.yview)
        self.tree_errors.configure(yscrollcommand=scroll_err.set)

        self.tree_errors.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scroll_err.pack(side=tk.RIGHT, fill=tk.Y, pady=4)

    def _build_status_bar(self):
        self.status_bar = ttk.Label(self.root, text=" Sistema Listo. Seleccione un caso de prueba o ingrese código C.", relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_case_selected(self, event):
        idx = self.combo_cases.current()
        if idx < len(ALL_TEST_CASES):
            test = ALL_TEST_CASES[idx]
            self.lbl_case_info.config(text=f"REGLA: {test.rule_description} | ESPERADO: {test.expected_behavior}")
            self.txt_source.delete("1.0", tk.END)
            self.txt_source.insert(tk.END, test.code)
            self.status_bar.config(text=f" Caso {test.id_num:02d} cargado: {test.title}")
            self.action_tokenize()
        else:
            self.lbl_case_info.config(text="Modo libre: Escriba o pegue código en C para evaluar errores léxicos.")
            self.status_bar.config(text=" Modo libre activado.")

    def action_tokenize(self):
        code_text = self.txt_source.get("1.0", tk.END).strip()
        if not code_text:
            messagebox.showwarning("Aviso", "El editor de código está vacío.")
            return

        lexer = LexerC(code_text, self.error_handler)
        tokens = lexer.tokenize()

        # Actualizar tabla de tokens
        for item in self.tree_tokens.get_children():
            self.tree_tokens.delete(item)

        valid_tokens = 0
        for idx, tok in enumerate(tokens, 1):
            if tok.type == TokenType.FIN_DE_ENTRADA:
                continue
            if not tok.is_error:
                valid_tokens += 1
            disp_val = tok.value.replace("\n", "\\n").replace("\r", "")
            self.tree_tokens.insert("", tk.END, values=(idx, tok.line, tok.column, tok.category_name, disp_val))

        # Actualizar tabla de errores
        for item in self.tree_errors.get_children():
            self.tree_errors.delete(item)

        for idx, err in enumerate(self.error_handler.errors, 1):
            sug_text = f"{err.message} | Sugerencia: {err.suggestion}"
            self.tree_errors.insert("", tk.END, values=(idx, err.line, err.column, err.category.value, err.lexeme, sug_text))

        # Actualizar estadísticas
        counts = self.error_handler.count_by_category()
        total_errs = self.error_handler.total_errors

        if total_errs == 0:
            self.lbl_stats.config(
                text=f"✅ 0 ERRORES LÉXICOS. {valid_tokens} tokens válidos reconocidos perfectamente.",
                foreground="#16A34A"
            )
            self.status_bar.config(text=" Análisis finalizado: Código 100% válido léxicamente.")
        else:
            parts = [f"{cat}: {cnt}" for cat, cnt in counts.items() if cnt > 0]
            summary_str = "  |  ".join(parts)
            self.lbl_stats.config(
                text=f"❌ {total_errs} ERRORES DETECTADOS: {summary_str}",
                foreground="#DC2626"
            )
            self.status_bar.config(text=f" Análisis finalizado: {total_errs} errores léxicos detectados.")
            self.notebook.select(self.tab_errors)

    def action_clear(self):
        self.txt_source.delete("1.0", tk.END)
        for item in self.tree_tokens.get_children():
            self.tree_tokens.delete(item)
        for item in self.tree_errors.get_children():
            self.tree_errors.delete(item)
        self.lbl_stats.config(text="Sin análisis ejecutado.", foreground="#000000")
        self.status_bar.config(text=" Editor limpiado.")


def main():
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
