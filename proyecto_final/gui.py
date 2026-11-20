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

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, List, Dict, Any
from compiler_pipeline import CompilerPipeline, CompilationResult
from test_cases import TEST_CASES, TestCase
from virtual_machine import VirtualMachine


class CompilerIDE:
    """
    Entorno de Desarrollo Integrado (IDE) Multi-Pestaña para el Compilador de C.
    Proporciona 8 pestañas interactivas dedicadas a cada fase de compilación y ejecución.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Compilador Integral de C - Proyecto Final | Traductores de Lenguaje (CUCEI)")
        self.root.geometry("1280x820")
        self.root.minsize(1024, 700)

        self.last_result: Optional[CompilationResult] = None
        self.step_vm: Optional[VirtualMachine] = None
        self.step_index: int = 0

        self._configure_styles()
        self._build_header()
        self._build_toolbar()
        self._build_notebook()
        self._build_statusbar()

        # Cargar caso 1 por defecto
        self._load_test_case_by_index(0)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configuración de estilos visuales
        style.configure("Header.TFrame", background="#1e293b")
        style.configure("Header.TLabel", background="#1e293b", foreground="#f8fafc", font=("Segoe UI", 11, "bold"))
        style.configure("SubHeader.TLabel", background="#1e293b", foreground="#94a3b8", font=("Segoe UI", 9))
        style.configure("Team.TLabel", background="#1e293b", foreground="#38bdf8", font=("Segoe UI", 9, "bold"))

        style.configure("Toolbar.TFrame", background="#f1f5f9", padding=6)
        style.configure("Action.TButton", font=("Segoe UI", 9, "bold"), padding=4)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e2e8f0")
        style.configure("Treeview", font=("Consolas", 9), rowheight=22)

    def _build_header(self):
        hdr_frame = ttk.Frame(self.root, style="Header.TFrame", padding=(12, 8))
        hdr_frame.pack(fill=tk.X)

        lbl_title = ttk.Label(
            hdr_frame,
            text="UNIVERSIDAD DE GUADALAJARA — CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS (CUCEI)",
            style="Header.TLabel"
        )
        lbl_title.pack(anchor=tk.W)

        lbl_sub = ttk.Label(
            hdr_frame,
            text="Traductores de Lenguaje | Profesor: Rigoberto Cárdenas Larios | Proyecto Final: Compilador de C",
            style="SubHeader.TLabel"
        )
        lbl_sub.pack(anchor=tk.W, pady=(2, 4))

        lbl_team = ttk.Label(
            hdr_frame,
            text="EQUIPO: 1. Díaz Torres Jazmín Montserrat  |  2. Fierro Meléndez Ernesto Hatuey  |  3. Hernández García Héctor Gabriel  |  4. Millán Guerrero Oswaldo Josué",
            style="Team.TLabel"
        )
        lbl_team.pack(anchor=tk.W)

    def _build_toolbar(self):
        tool_frame = ttk.Frame(self.root, style="Toolbar.TFrame")
        tool_frame.pack(fill=tk.X)

        ttk.Label(tool_frame, text="Batería de Pruebas (10 Casos):", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(6, 4))

        case_names = [f"[{tc.id}] {tc.name} ({tc.category})" for tc in TEST_CASES]
        self.combo_cases = ttk.Combobox(tool_frame, values=case_names, state="readonly", width=55)
        self.combo_cases.current(0)
        self.combo_cases.pack(side=tk.LEFT, padx=4)
        self.combo_cases.bind("<<ComboboxSelected>>", self._on_case_selected)

        btn_load = ttk.Button(tool_frame, text="Cargar Código", command=self._on_load_clicked)
        btn_load.pack(side=tk.LEFT, padx=4)

        ttk.Separator(tool_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)

        btn_run = ttk.Button(tool_frame, text="▶ Compilar y Ejecutar", style="Action.TButton", command=self.compile_and_run)
        btn_run.pack(side=tk.LEFT, padx=4)

        btn_step = ttk.Button(tool_frame, text="⏭ Paso a Paso (VM)", command=self.step_execution)
        btn_step.pack(side=tk.LEFT, padx=4)

        btn_clear = ttk.Button(tool_frame, text="↺ Limpiar", command=self.clear_all)
        btn_clear.pack(side=tk.LEFT, padx=4)

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # Tab 1: Código Fuente C
        self.tab_source = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_source, text=" 1. Código Fuente C ")
        self._init_tab_source()

        # Tab 2: Analizador Léxico (Tokens)
        self.tab_lex = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_lex, text=" 2. Tokens (Léxico) ")
        self._init_tab_lex()

        # Tab 3: Analizador Sintáctico (AST)
        self.tab_ast = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ast, text=" 3. Árbol Sintáctico (AST) ")
        self._init_tab_ast()

        # Tab 4: Tabla de Símbolos
        self.tab_sym = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sym, text=" 4. Tabla de Símbolos ")
        self._init_tab_sym()

        # Tab 5: Código Intermedio TAC
        self.tab_tac = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tac, text=" 5. TAC Original ")
        self._init_tab_tac()

        # Tab 6: TAC Optimizado & Bitácora
        self.tab_opt = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_opt, text=" 6. TAC Optimizado ")
        self._init_tab_opt()

        # Tab 7: Ensamblador & Memoria
        self.tab_asm = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_asm, text=" 7. Ensamblador / Memoria ")
        self._init_tab_asm()

        # Tab 8: Máquina Virtual (VM)
        self.tab_vm = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vm, text=" 8. Máquina Virtual (VM) ")
        self._init_tab_vm()

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Listo. Seleccione un caso de prueba o escriba su código en C y presione 'Compilar y Ejecutar'.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9), padding=(6, 4))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN DE PESTAÑAS
    # -------------------------------------------------------------------------

    def _init_tab_source(self):
        frame = ttk.Frame(self.tab_source, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        info_lbl = ttk.Label(
            frame,
            text="Editor de Código C — Soporta Tipos (int, float, string, bool), Clases, Métodos, If/Else, Switch/Case, While, For, Do-While y Print:",
            font=("Segoe UI", 9, "bold")
        )
        info_lbl.pack(anchor=tk.W, pady=(0, 4))

        self.txt_source = scrolledtext.ScrolledText(frame, font=("Consolas", 11), wrap=tk.NONE, undo=True)
        self.txt_source.pack(fill=tk.BOTH, expand=True)

    def _init_tab_lex(self):
        frame = ttk.Frame(self.tab_lex, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        cols = ("idx", "line", "col", "type", "val")
        self.tree_tokens = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        self.tree_tokens.heading("idx", text="#")
        self.tree_tokens.heading("line", text="Línea")
        self.tree_tokens.heading("col", text="Columna")
        self.tree_tokens.heading("type", text="Tipo de Token")
        self.tree_tokens.heading("val", text="Lexema / Valor")

        self.tree_tokens.column("idx", width=50, anchor=tk.CENTER)
        self.tree_tokens.column("line", width=70, anchor=tk.CENTER)
        self.tree_tokens.column("col", width=80, anchor=tk.CENTER)
        self.tree_tokens.column("type", width=220, anchor=tk.W)
        self.tree_tokens.column("val", width=380, anchor=tk.W)

        scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_tokens.yview)
        self.tree_tokens.configure(yscrollcommand=scroll_y.set)

        self.tree_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_tab_ast(self):
        frame = ttk.Frame(self.tab_ast, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        lbl = ttk.Label(frame, text="Representación Jerárquica del Árbol de Sintaxis Abstracta (AST):", font=("Segoe UI", 9, "bold"))
        lbl.pack(anchor=tk.W, pady=(0, 4))

        self.txt_ast = scrolledtext.ScrolledText(frame, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_ast.pack(fill=tk.BOTH, expand=True)

    def _init_tab_sym(self):
        frame = ttk.Frame(self.tab_sym, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        cols = ("name", "type", "scope", "addr", "val", "init")
        self.tree_sym = ttk.Treeview(frame, columns=cols, show="headings")
        self.tree_sym.heading("name", text="Identificador")
        self.tree_sym.heading("type", text="Tipo de Dato")
        self.tree_sym.heading("scope", text="Ámbito (Scope)")
        self.tree_sym.heading("addr", text="Dirección Memoria RAM")
        self.tree_sym.heading("val", text="Valor Almacenado")
        self.tree_sym.heading("init", text="Inicializado")

        self.tree_sym.column("name", width=160, anchor=tk.W)
        self.tree_sym.column("type", width=120, anchor=tk.CENTER)
        self.tree_sym.column("scope", width=120, anchor=tk.CENTER)
        self.tree_sym.column("addr", width=180, anchor=tk.CENTER)
        self.tree_sym.column("val", width=180, anchor=tk.W)
        self.tree_sym.column("init", width=100, anchor=tk.CENTER)

        scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_sym.yview)
        self.tree_sym.configure(yscrollcommand=scroll_y.set)

        self.tree_sym.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_tab_tac(self):
        frame = ttk.Frame(self.tab_tac, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        lbl = ttk.Label(frame, text="Código Intermedio de Tres Direcciones (TAC) — Sin Optimizar:", font=("Segoe UI", 9, "bold"))
        lbl.pack(anchor=tk.W, pady=(0, 4))

        self.txt_tac = scrolledtext.ScrolledText(frame, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_tac.pack(fill=tk.BOTH, expand=True)

    def _init_tab_opt(self):
        frame = ttk.Frame(self.tab_opt, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        f_left = ttk.Frame(paned)
        f_right = ttk.Frame(paned)
        paned.add(f_left, weight=3)
        paned.add(f_right, weight=2)

        lbl_l = ttk.Label(f_left, text="Código Intermedio Optimizado (Plegado, Copias, DCE, CSE):", font=("Segoe UI", 9, "bold"))
        lbl_l.pack(anchor=tk.W, pady=(0, 4))
        self.txt_tac_opt = scrolledtext.ScrolledText(f_left, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_tac_opt.pack(fill=tk.BOTH, expand=True)

        lbl_r = ttk.Label(f_right, text="Bitácora de Optimizaciones Aplicadas:", font=("Segoe UI", 9, "bold"))
        lbl_r.pack(anchor=tk.W, pady=(0, 4))
        self.txt_opt_log = scrolledtext.ScrolledText(f_right, font=("Consolas", 9), wrap=tk.WORD)
        self.txt_opt_log.pack(fill=tk.BOTH, expand=True)

    def _init_tab_asm(self):
        frame = ttk.Frame(self.tab_asm, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        f_left = ttk.Frame(paned)
        f_right = ttk.Frame(paned)
        paned.add(f_left, weight=3)
        paned.add(f_right, weight=2)

        lbl_l = ttk.Label(f_left, text="Código Máquina y Ensamblador con Direcciones Físicas (0x1000...):", font=("Segoe UI", 9, "bold"))
        lbl_l.pack(anchor=tk.W, pady=(0, 4))
        self.txt_asm = scrolledtext.ScrolledText(f_left, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_asm.pack(fill=tk.BOTH, expand=True)

        lbl_r = ttk.Label(f_right, text="Métricas de Reducción y Mapa de Segmentos:", font=("Segoe UI", 9, "bold"))
        lbl_r.pack(anchor=tk.W, pady=(0, 4))
        self.txt_metrics = scrolledtext.ScrolledText(f_right, font=("Consolas", 9), wrap=tk.WORD)
        self.txt_metrics.pack(fill=tk.BOTH, expand=True)

    def _init_tab_vm(self):
        frame = ttk.Frame(self.tab_vm, padding=6)
        frame.pack(fill=tk.BOTH, expand=True)

        # Panel superior: Registros y Banderas
        top_box = ttk.LabelFrame(frame, text="Estado de Hardware CPU RISC de 32 bits (Registros y Banderas)", padding=6)
        top_box.pack(fill=tk.X, pady=(0, 6))

        self.lbl_regs = ttk.Label(top_box, text="R1: 0  |  R2: 0  |  R3: 0  |  R4: 0  |  R5: 0  |  R6: 0  |  R7: 0  |  R8: 0", font=("Consolas", 10, "bold"), foreground="#0369a1")
        self.lbl_regs.pack(anchor=tk.W)

        self.lbl_flags = ttk.Label(top_box, text="PC: 0x1000  |  Banderas: ZF=0, SF=0, OF=0  |  Ciclos: 0", font=("Consolas", 10))
        self.lbl_flags.pack(anchor=tk.W, pady=(2, 0))

        # Panel inferior: PanedWindow con Historial de Instrucciones, Consola de Salida y Memoria RAM
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        f_hist = ttk.Frame(paned)
        f_console = ttk.Frame(paned)
        paned.add(f_hist, weight=3)
        paned.add(f_console, weight=2)

        lbl_h = ttk.Label(f_hist, text="Historial de Ejecución Ciclo por Ciclo (Fetch -> Decode -> Execute):", font=("Segoe UI", 9, "bold"))
        lbl_h.pack(anchor=tk.W, pady=(0, 4))
        self.txt_vm_hist = scrolledtext.ScrolledText(f_hist, font=("Consolas", 9), wrap=tk.NONE)
        self.txt_vm_hist.pack(fill=tk.BOTH, expand=True)

        lbl_c = ttk.Label(f_console, text="Consola de Salida Estándar y Volcado de Memoria RAM:", font=("Segoe UI", 9, "bold"))
        lbl_c.pack(anchor=tk.W, pady=(0, 4))
        self.txt_vm_out = scrolledtext.ScrolledText(f_console, font=("Consolas", 10), bg="#0f172a", fg="#22c55e", insertbackground="white")
        self.txt_vm_out.pack(fill=tk.BOTH, expand=True)

    # -------------------------------------------------------------------------
    # CONTROLADORES DE EVENTOS
    # -------------------------------------------------------------------------

    def _on_case_selected(self, event=None):
        idx = self.combo_cases.current()
        if 0 <= idx < len(TEST_CASES):
            self._load_test_case_by_index(idx)

    def _on_load_clicked(self):
        self._on_case_selected()

    def _load_test_case_by_index(self, idx: int):
        tc = TEST_CASES[idx]
        self.txt_source.delete("1.0", tk.END)
        self.txt_source.insert("1.0", tc.source_code)
        self.status_var.set(f"Cargado [{tc.id}]: {tc.name} ({tc.category}) — {tc.description}")

    def clear_all(self):
        self.txt_source.delete("1.0", tk.END)
        for item in self.tree_tokens.get_children():
            self.tree_tokens.delete(item)
        self.txt_ast.delete("1.0", tk.END)
        for item in self.tree_sym.get_children():
            self.tree_sym.delete(item)
        self.txt_tac.delete("1.0", tk.END)
        self.txt_tac_opt.delete("1.0", tk.END)
        self.txt_opt_log.delete("1.0", tk.END)
        self.txt_asm.delete("1.0", tk.END)
        self.txt_metrics.delete("1.0", tk.END)
        self.txt_vm_hist.delete("1.0", tk.END)
        self.txt_vm_out.delete("1.0", tk.END)
        self.lbl_regs.config(text="R1: 0  |  R2: 0  |  R3: 0  |  R4: 0  |  R5: 0  |  R6: 0  |  R7: 0  |  R8: 0")
        self.lbl_flags.config(text="PC: 0x1000  |  Banderas: ZF=0, SF=0, OF=0  |  Ciclos: 0")
        self.status_var.set("Editor y pestañas limpiados.")
        self.last_result = None
        self.step_vm = None

    def compile_and_run(self):
        code = self.txt_source.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "El editor de código fuente está vacío.")
            return

        # Ejecutar pipeline completo
        res = CompilerPipeline.compile_and_run(code)
        self.last_result = res

        # 1. Pestaña Tokens
        for item in self.tree_tokens.get_children():
            self.tree_tokens.delete(item)
        for idx, tok in enumerate(res.tokens, 1):
            self.tree_tokens.insert("", tk.END, values=(idx, tok.line, tok.column, tok.type.name, repr(tok.value)))

        # 2. Pestaña AST
        self.txt_ast.delete("1.0", tk.END)
        if res.ast_tree_str:
            self.txt_ast.insert("1.0", res.ast_tree_str)
        elif res.error_stage in ("LÉXICO", "SINTÁCTICO"):
            self.txt_ast.insert("1.0", f"[COMPILACIÓN DETENIDA EN FASE {res.error_stage}]\n\n" + "\n".join(str(e) for e in res.errors))

        # 3. Pestaña Tabla de Símbolos
        for item in self.tree_sym.get_children():
            self.tree_sym.delete(item)
        for sym in res.symbols_list:
            addr_str = f"0x{sym.address:04X}" if sym.address is not None else "N/A"
            val_str = str(sym.value) if sym.value is not None else "(no asignado)"
            init_str = "SÍ" if sym.is_initialized else "NO"
            self.tree_sym.insert("", tk.END, values=(sym.name, sym.type_name, sym.scope, addr_str, val_str, init_str))

        # 4. Pestaña TAC Original
        self.txt_tac.delete("1.0", tk.END)
        if res.tac_unoptimized:
            tac_text = "\n".join(str(t) for t in res.tac_unoptimized)
            self.txt_tac.insert("1.0", tac_text)

        # 5. Pestaña TAC Optimizado & Bitácora
        self.txt_tac_opt.delete("1.0", tk.END)
        self.txt_opt_log.delete("1.0", tk.END)
        if res.tac_optimized:
            opt_text = "\n".join(str(t) for t in res.tac_optimized)
            self.txt_tac_opt.insert("1.0", opt_text)
            log_text = "\n".join(res.optimization_log) if res.optimization_log else "No se requirieron podas adicionales."
            self.txt_opt_log.insert("1.0", log_text)

        # 6. Pestaña Ensamblador & Métricas
        self.txt_asm.delete("1.0", tk.END)
        self.txt_metrics.delete("1.0", tk.END)
        if res.machine_code_opt:
            asm_lines = [inst.to_memory_asm() for inst in res.machine_code_opt]
            self.txt_asm.insert("1.0", "\n".join(asm_lines))

            m = res.code_metrics
            metrics_txt = f"""MÉTRICAS DE OPTIMIZACIÓN DE CÓDIGO MÁQUINA:
------------------------------------------------------------
Instrucciones Originales (Sin Optimizar): {m.get('unoptimized_count', 0)}
Instrucciones Optimizadas:                {m.get('optimized_count', 0)}
Instrucciones Ahorradas (Peephole & Reg): {m.get('instructions_saved', 0)}
Ganancia de Eficiencia:                   {m.get('efficiency_gain_pct', 0)}%

DISTRIBUCIÓN DE SEGMENTOS DE MEMORIA:
------------------------------------------------------------
Segmento de Código (Instrucciones): 0x1000 - 0x1FFF
Segmento de Datos (Variables):       0x2000 - 0x2FFF
Segmento de Resultados/Temporales:  0x3000 - 0x3FFF
"""
            self.txt_metrics.insert("1.0", metrics_txt)

        # 7. Pestaña Máquina Virtual
        self.txt_vm_hist.delete("1.0", tk.END)
        self.txt_vm_out.delete("1.0", tk.END)

        if res.success:
            self.status_var.set("¡Compilación y ejecución en Máquina Virtual completadas EXITOSAMENTE (0 errores)!")
            hist_lines = [str(h) for h in res.vm_history]
            self.txt_vm_hist.insert("1.0", "\n".join(hist_lines))

            out_display = "=== SALIDA DE CONSOLA ===\n" + "\n".join(res.vm_output) + "\n\n"
            out_display += "=== VOLCADO DE MEMORIA RAM FINAL ===\n" + res.vm_memory_dump + "\n\n"
            out_display += "=== ESTADO DE REGISTROS ===\n" + res.vm_registers_dump
            self.txt_vm_out.insert("1.0", out_display)

            # Actualizar tarjetas de hardware
            last_state = res.vm_history[-1] if res.vm_history else None
            if last_state:
                regs_str = "  |  ".join([f"{r}: {v}" for r, v in sorted(last_state.registers.items())])
                self.lbl_regs.config(text=regs_str)
                flags_str = f"PC: 0x{last_state.pc:04X}  |  ZF={last_state.flags.get('ZF', 0)} SF={last_state.flags.get('SF', 0)} OF={last_state.flags.get('OF', 0)}  |  Ciclos: {len(res.vm_history)}"
                self.lbl_flags.config(text=flags_str)

            # Cambiar a la pestaña de VM para ver el resultado
            self.notebook.select(self.tab_vm)

        else:
            self.status_var.set(f"Compilación INTERRUMPIDA en fase [{res.error_stage}]. Se detectaron {len(res.errors)} errores.")
            err_summary = f"=== ERROR EN FASE: [{res.error_stage}] ===\n\n"
            err_summary += "\n".join(str(e) for e in res.errors)
            if res.execution_error:
                err_summary += f"\nError de Ejecución VM: {res.execution_error}"
            self.txt_vm_out.insert("1.0", err_summary)

            # Si es léxico, mostrar tab 2; si sintáctico, tab 3; si semántico, tab 4
            if res.error_stage == "LÉXICO":
                self.notebook.select(self.tab_lex)
            elif res.error_stage == "SINTÁCTICO":
                self.notebook.select(self.tab_ast)
            elif res.error_stage == "SEMÁNTICO":
                self.notebook.select(self.tab_sym)
            else:
                self.notebook.select(self.tab_vm)

    def step_execution(self):
        """Ejecuta una única instrucción paso a paso en la Máquina Virtual."""
        if not self.last_result or not self.last_result.success:
            self.compile_and_run()
            if not self.last_result or not self.last_result.success:
                return

        # Inicializar VM de paso a paso si no existe
        if self.step_vm is None:
            self.step_vm = VirtualMachine(max_cycles=3000)
            initial_data = {}
            for sym in self.last_result.symbols_list:
                if sym.address is not None and sym.value is not None and isinstance(sym.value, (int, float, bool)):
                    initial_data[sym.address] = int(sym.value)
            symbol_names = {s.name: s.address for s in self.last_result.symbols_list if s.address is not None}
            self.step_vm.load_from_memory_structures(
                self.last_result.machine_code_opt,
                initial_data=initial_data,
                symbol_names=symbol_names
            )
            self.txt_vm_hist.delete("1.0", tk.END)
            self.txt_vm_out.delete("1.0", tk.END)

        if self.step_vm.step():
            st = self.step_vm.execution_history[-1]
            self.txt_vm_hist.insert(tk.END, str(st) + "\n")
            self.txt_vm_hist.see(tk.END)

            regs_str = "  |  ".join([f"{r}: {v}" for r, v in sorted(st.registers.items())])
            self.lbl_regs.config(text=regs_str)
            flags_str = f"PC: 0x{self.step_vm.pc:04X}  |  ZF={st.flags.get('ZF', 0)} SF={st.flags.get('SF', 0)}  |  Ciclos: {self.step_vm.cycle_count}"
            self.lbl_flags.config(text=flags_str)

            out_display = "=== SALIDA DE CONSOLA ===\n" + "\n".join(self.step_vm.output_buffer) + "\n\n"
            out_display += "=== VOLCADO DE MEMORIA RAM ===\n" + self.step_vm.dump_memory_state()
            self.txt_vm_out.delete("1.0", tk.END)
            self.txt_vm_out.insert("1.0", out_display)
            self.status_var.set(f"Paso ejecutado. PC=0x{self.step_vm.pc:04X}, Ciclo {self.step_vm.cycle_count}.")
            self.notebook.select(self.tab_vm)
        else:
            self.status_var.set("Ejecución finalizada (HALT alcanzado o fin de programa).")
            self.step_vm = None


def main():
    root = tk.Tk()
    app = CompilerIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
