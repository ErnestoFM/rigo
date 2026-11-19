"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - INTERFAZ GRÁFICA DE USUARIO (GUI)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Optional, List, Dict, Any

from intermediate_code import TACGenerator, Quadruple
from symbol_table_mem import MemorySymbolTable
from code_generator import CodeGenerator, MachineInstruction
from executable_format import ExecutableBuilder, ExecutableHeader
from virtual_machine import VirtualMachine
from test_cases import ALL_TEST_CASES, TestCaseCodeGeneration

from lexer import Lexer
from parser import Parser
from error_handler import CompilerErrorHandler


class CodeGeneratorGUI:
    """
    Interfaz Gráfica de Usuario interactiva para la demostración de la Actividad 13:
    Traducción de Código Intermedio a Código Máquina, Asignación de Memoria,
    Optimización y Emulación en Máquina Virtual.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Compilador - Actividad 13: Generación de Código Máquina y Entorno de Ejecución")
        self.root.geometry("1320x860")
        self.root.minsize(1100, 700)

        # Estado del compilador
        self.tac_generator = TACGenerator()
        self.symbol_table = MemorySymbolTable()
        self.code_generator = CodeGenerator(self.symbol_table)
        self.vm = VirtualMachine(max_cycles=200)

        self.current_unopt: List[MachineInstruction] = []
        self.current_opt: List[MachineInstruction] = []
        self.current_quads: List[Quadruple] = []

        self._configure_styles()
        self._build_header()
        self._build_control_panel()
        self._build_main_notebook()
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
        style.configure("Warning.TButton", background="#F59E0B", foreground="#FFFFFF")
        style.configure("Secondary.TButton", background="#475569", foreground="#FFFFFF")

        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Consolas", 9), rowheight=24)

    def _build_header(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=(15, 10))
        header_frame.pack(fill=tk.X)

        title_lbl = ttk.Label(
            header_frame,
            text="ACTIVIDAD 13: GENERACIÓN DE CÓDIGO (CÓDIGO INTERMEDIO A CÓDIGO MÁQUINA EJECUTABLE)",
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

    def _build_control_panel(self):
        ctrl_frame = ttk.Frame(self.root, padding=(15, 8))
        ctrl_frame.pack(fill=tk.X)

        # Selector de casos
        ttk.Label(ctrl_frame, text="Casos de Prueba:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))

        case_names = [f"Caso {t.id_num:02d}: {t.title} ({'Válido' if t.is_valid else 'Inválido'})" for t in ALL_TEST_CASES]
        case_names.append("Personalizado (Escribir libremente)")
        self.combo_cases = ttk.Combobox(ctrl_frame, values=case_names, width=54, state="readonly", font=("Segoe UI", 9))
        self.combo_cases.pack(side=tk.LEFT, padx=(0, 15))
        self.combo_cases.bind("<<ComboboxSelected>>", self.on_case_selected)

        # Botones de Acción
        btn_compile = ttk.Button(ctrl_frame, text="▶ Compilar y Mapear", style="Primary.TButton", command=self.action_compile)
        btn_compile.pack(side=tk.LEFT, padx=4)

        btn_run = ttk.Button(ctrl_frame, text="⚙ Ejecutar VM Completa", style="Success.TButton", command=self.action_run_vm)
        btn_run.pack(side=tk.LEFT, padx=4)

        btn_step = ttk.Button(ctrl_frame, text="⏭ Paso a Paso (Step)", style="Warning.TButton", command=self.action_step_vm)
        btn_step.pack(side=tk.LEFT, padx=4)

        btn_reset = ttk.Button(ctrl_frame, text="🔄 Reiniciar VM", style="Secondary.TButton", command=self.action_reset_vm)
        btn_reset.pack(side=tk.LEFT, padx=4)

        btn_export = ttk.Button(ctrl_frame, text="💾 Exportar .bin / .asm", command=self.action_export_binary)
        btn_export.pack(side=tk.RIGHT, padx=4)

    def _build_main_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(4, 8))

        # Pestaña 1: Editor y Entrada
        self.tab_editor = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_editor, text="  1. Entrada de Código  ")
        self._build_tab_editor()

        # Pestaña 2: Código Intermedio (TAC)
        self.tab_tac = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tac, text="  2. Código Intermedio (Cuádruplos)  ")
        self._build_tab_tac()

        # Pestaña 3: Mapeo y Optimizaciones
        self.tab_code = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_code, text="  3. Código Máquina y Optimización  ")
        self._build_tab_code()

        # Pestaña 4: Tabla de Símbolos y Memoria
        self.tab_mem = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mem, text="  4. Asignación de Memoria (0x1000/0x2000)  ")
        self._build_tab_mem()

        # Pestaña 5: Máquina Virtual / Emulador
        self.tab_vm = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vm, text="  5. Emulador de Procesador (VM)  ")
        self._build_tab_vm()

    def _build_tab_editor(self):
        top_info = ttk.Frame(self.tab_editor, padding=8)
        top_info.pack(fill=tk.X)

        self.lbl_rule_info = ttk.Label(top_info, text="", font=("Segoe UI", 9, "italic"), foreground="#0369A1", wraplength=1250)
        self.lbl_rule_info.pack(anchor=tk.W)

        self.txt_source = scrolledtext.ScrolledText(self.tab_editor, wrap=tk.WORD, font=("Consolas", 11), undo=True)
        self.txt_source.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _build_tab_tac(self):
        cols = ("idx", "op", "arg1", "arg2", "res", "rep")
        self.tree_tac = ttk.Treeview(self.tab_tac, columns=cols, show="headings")
        self.tree_tac.heading("idx", text="#")
        self.tree_tac.heading("op", text="Operador")
        self.tree_tac.heading("arg1", text="Argumento 1")
        self.tree_tac.heading("arg2", text="Argumento 2")
        self.tree_tac.heading("res", text="Resultado")
        self.tree_tac.heading("rep", text="Representación Cuádruplo (OP, ARG1, ARG2, RES)")

        self.tree_tac.column("idx", width=50, anchor=tk.CENTER)
        self.tree_tac.column("op", width=110, anchor=tk.CENTER)
        self.tree_tac.column("arg1", width=140, anchor=tk.CENTER)
        self.tree_tac.column("arg2", width=140, anchor=tk.CENTER)
        self.tree_tac.column("res", width=140, anchor=tk.CENTER)
        self.tree_tac.column("rep", width=350, anchor=tk.W)

        scroll_tac = ttk.Scrollbar(self.tab_tac, orient=tk.VERTICAL, command=self.tree_tac.yview)
        self.tree_tac.configure(yscrollcommand=scroll_tac.set)

        self.tree_tac.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scroll_tac.pack(side=tk.RIGHT, fill=tk.Y, pady=8)

    def _build_tab_code(self):
        # Panel superior de métricas
        metrics_frame = ttk.LabelFrame(self.tab_code, text=" Resumen y Métricas de Optimización de Instrucciones ", padding=8)
        metrics_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        self.lbl_metrics = ttk.Label(metrics_frame, text="Compile el programa para visualizar la comparativa de eficiencia.", font=("Segoe UI", 9, "bold"))
        self.lbl_metrics.pack(anchor=tk.W)

        # Panel dividido en dos: Sin Optimizar vs Optimizado
        panes = ttk.PanedWindow(self.tab_code, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Lado izquierdo: Estándar
        frame_left = ttk.LabelFrame(panes, text=" Código Máquina Estándar (Sin Optimizar) ", padding=4)
        panes.add(frame_left, weight=1)
        self.txt_unopt = scrolledtext.ScrolledText(frame_left, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_unopt.pack(fill=tk.BOTH, expand=True)

        # Lado derecho: Optimizado
        frame_right = ttk.LabelFrame(panes, text=" Código Máquina Optimizado (Encadenamiento en Registros / Peephole) ", padding=4)
        panes.add(frame_right, weight=1)
        self.txt_opt = scrolledtext.ScrolledText(frame_right, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_opt.pack(fill=tk.BOTH, expand=True)

    def _build_tab_mem(self):
        cols = ("name", "addr", "type", "val", "cat")
        self.tree_mem = ttk.Treeview(self.tab_mem, columns=cols, show="headings")
        self.tree_mem.heading("name", text="Símbolo / Identificador")
        self.tree_mem.heading("addr", text="Dirección Hex")
        self.tree_mem.heading("type", text="Tipo de Dato")
        self.tree_mem.heading("val", text="Valor Inicial")
        self.tree_mem.heading("cat", text="Segmento / Categoría")

        self.tree_mem.column("name", width=180, anchor=tk.CENTER)
        self.tree_mem.column("addr", width=140, anchor=tk.CENTER)
        self.tree_mem.column("type", width=120, anchor=tk.CENTER)
        self.tree_mem.column("val", width=160, anchor=tk.CENTER)
        self.tree_mem.column("cat", width=200, anchor=tk.CENTER)

        scroll_mem = ttk.Scrollbar(self.tab_mem, orient=tk.VERTICAL, command=self.tree_mem.yview)
        self.tree_mem.configure(yscrollcommand=scroll_mem.set)

        self.tree_mem.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scroll_mem.pack(side=tk.RIGHT, fill=tk.Y, pady=8)

    def _build_tab_vm(self):
        # Panel superior: Registros y Banderas
        top_hw = ttk.Frame(self.tab_vm, padding=8)
        top_hw.pack(fill=tk.X)

        lbl_reg_box = ttk.LabelFrame(top_hw, text=" Banco de Registros (R1..R8) y Estado del CPU ", padding=8)
        lbl_reg_box.pack(fill=tk.X)

        self.lbl_regs = ttk.Label(lbl_reg_box, text="R1: 0  |  R2: 0  |  R3: 0  |  R4: 0  |  R5: 0  |  R6: 0  |  R7: 0  |  R8: 0", font=("Consolas", 11, "bold"), foreground="#0F766E")
        self.lbl_regs.pack(anchor=tk.W)

        self.lbl_flags = ttk.Label(lbl_reg_box, text="PC: 0x1000  |  ZF (Zero Flag): 0  |  SF (Sign Flag): 0  |  Ciclos Totales: 0  |  Estatus: Listo", font=("Segoe UI", 9, "bold"), foreground="#334155")
        self.lbl_flags.pack(anchor=tk.W, pady=(4, 0))

        # Panel medio: Trazas de Ciclos y Memoria RAM
        mid_panes = ttk.PanedWindow(self.tab_vm, orient=tk.HORIZONTAL)
        mid_panes.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Historial de instrucciones ejecutadas
        frame_trace = ttk.LabelFrame(mid_panes, text=" Trazas del Ciclo Fetch-Decode-Execute ", padding=4)
        mid_panes.add(frame_trace, weight=2)
        self.txt_trace = scrolledtext.ScrolledText(frame_trace, font=("Consolas", 9), wrap=tk.NONE)
        self.txt_trace.pack(fill=tk.BOTH, expand=True)

        # Volcado de memoria RAM
        frame_ram = ttk.LabelFrame(mid_panes, text=" Memoria RAM (Segmentos 0x2000 y 0x3000) ", padding=4)
        mid_panes.add(frame_ram, weight=1)
        self.txt_ram = scrolledtext.ScrolledText(frame_ram, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_ram.pack(fill=tk.BOTH, expand=True)

        # Consola de salida
        frame_out = ttk.LabelFrame(self.tab_vm, text=" Buffer de Salida por Consola (Instrucciones PRINT) ", padding=4)
        frame_out.pack(fill=tk.X, padx=8, pady=(4, 8))
        self.txt_output = scrolledtext.ScrolledText(frame_out, height=4, font=("Consolas", 10))
        self.txt_output.pack(fill=tk.X)

    def _build_status_bar(self):
        self.status_bar = ttk.Label(self.root, text=" Sistema Listo. Seleccione un caso de prueba o escriba su código.", relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_case_selected(self, event):
        idx = self.combo_cases.current()
        if idx < len(ALL_TEST_CASES):
            test = ALL_TEST_CASES[idx]
            self.lbl_rule_info.config(text=f"REGLA [{test.category}]: {test.rule_description} | ESPERADO: {test.expected_behavior}")
            self.txt_source.delete("1.0", tk.END)
            self.txt_source.insert(tk.END, test.code_input)
            self.status_bar.config(text=f" Caso {test.id_num:02d} cargado: {test.title}")
            self.action_compile()
        else:
            self.lbl_rule_info.config(text="Modo libre: Ingrese código fuente o código intermedio TAC personalizado.")
            self.status_bar.config(text=" Modo libre activado.")

    def action_compile(self):
        code_text = self.txt_source.get("1.0", tk.END).strip()
        if not code_text:
            messagebox.showwarning("Aviso", "El editor de código está vacío.")
            return

        idx = self.combo_cases.current()
        test_case = ALL_TEST_CASES[idx] if idx < len(ALL_TEST_CASES) else None
        is_source = test_case.is_source_code if test_case else ("class " in code_text or "int " in code_text or "function " in code_text)

        # 1. Código Intermedio
        self.tac_generator = TACGenerator()
        if is_source:
            err_h = CompilerErrorHandler()
            lexer = Lexer(code_text, err_h)
            tokens = lexer.tokenize()
            parser = Parser(tokens, err_h)
            ast = parser.parse()
            self.current_quads = self.tac_generator.generate_from_ast(ast)
        else:
            self.current_quads = self.tac_generator.parse_tac_text(code_text)

        # Actualizar vista de TAC
        for item in self.tree_tac.get_children():
            self.tree_tac.delete(item)

        for i, q in enumerate(self.current_quads, 1):
            self.tree_tac.insert("", tk.END, values=(i, q.op, q.arg1 or "-", q.arg2 or "-", q.result or "-", str(q)))

        # 2. Asignación de Memoria y Tabla de Símbolos
        self.symbol_table = MemorySymbolTable()
        if test_case and test_case.initial_data:
            for v_name, val in test_case.initial_data.items():
                is_res = v_name.lower().startswith("res")
                self.symbol_table.allocate_variable(v_name, initial_value=val, is_result=is_res)

        self.code_generator = CodeGenerator(self.symbol_table)
        self.current_unopt = self.code_generator.generate_unoptimized(self.current_quads)
        self.current_opt = self.code_generator.generate_optimized(self.current_quads)
        metrics = self.code_generator.get_optimization_metrics()

        # Actualizar Pestaña de Código Máquina
        self.txt_unopt.delete("1.0", tk.END)
        for inst in self.current_unopt:
            self.txt_unopt.insert(tk.END, inst.to_memory_asm() + "\n")

        self.txt_opt.delete("1.0", tk.END)
        for inst in self.current_opt:
            self.txt_opt.insert(tk.END, inst.to_memory_asm() + "\n")

        self.lbl_metrics.config(
            text=f"Instrucciones Sin Optimizar: {metrics['unoptimized_count']}  |  "
                 f"Optimizadas: {metrics['optimized_count']}  |  "
                 f"Instrucciones Ahorradas: {metrics['instructions_saved']}  |  "
                 f"Ganancia de Eficiencia: {metrics['efficiency_gain_pct']}%"
        )

        # Actualizar Pestaña de Memoria
        for item in self.tree_mem.get_children():
            self.tree_mem.delete(item)

        sorted_syms = sorted(self.symbol_table.symbols.values(), key=lambda s: s.address)
        for s in sorted_syms:
            self.tree_mem.insert("", tk.END, values=(s.name, s.hex_address, s.data_type, s.initial_value, s.category))

        # Cargar en Máquina Virtual
        self.action_reset_vm()
        self.status_bar.config(text=f" Compilación y mapeo finalizados exitosamente. {len(self.current_opt)} instrucciones generadas.")

    def action_reset_vm(self):
        """Reinicia la VM con las estructuras del caso actual."""
        initial_data = {s.address: (int(s.initial_value) if isinstance(s.initial_value, (int, float, bool)) else 0) for s in self.symbol_table.symbols.values()}
        symbol_names = {s.name: s.address for s in self.symbol_table.symbols.values()}

        self.vm.load_from_memory_structures(
            instructions=self.current_opt,
            initial_data=initial_data,
            symbol_names=symbol_names,
            entry_point=0x1000
        )

        self._update_vm_ui()
        self.txt_trace.delete("1.0", tk.END)
        self.txt_output.delete("1.0", tk.END)
        self.status_bar.config(text=" Máquina Virtual reiniciada y lista en PC 0x1000.")

    def action_step_vm(self):
        if self.vm.is_halted:
            messagebox.showinfo("VM", "La ejecución ha alcanzado HALT o se encuentra detenida.")
            return

        can_continue = self.vm.step()
        self._update_vm_ui()

        if self.vm.execution_history:
            last = self.vm.execution_history[-1]
            self.txt_trace.insert(tk.END, str(last) + "\n")
            self.txt_trace.see(tk.END)

        if not can_continue:
            if self.vm.error_message:
                messagebox.showerror("Error de Ejecución en CPU", self.vm.error_message)
            else:
                self.status_bar.config(text=" Ejecución finalizada: HALT alcanzado con éxito.")

    def action_run_vm(self):
        self.action_reset_vm()
        success = self.vm.run()
        self._update_vm_ui()

        self.txt_trace.delete("1.0", tk.END)
        for snap in self.vm.execution_history:
            self.txt_trace.insert(tk.END, str(snap) + "\n")
        self.txt_trace.see(tk.END)

        self.notebook.select(self.tab_vm)

        if success:
            self.status_bar.config(text=f" Ejecución de VM completada en {self.vm.cycle_count} ciclos. HALT alcanzado.")
        else:
            self.status_bar.config(text=f" Ejecución detenida: {self.vm.error_message}")
            messagebox.showinfo("Resultado de Ejecución", f"Aviso del Procesador:\n{self.vm.error_message}")

    def _update_vm_ui(self):
        reg_text = "  |  ".join([f"{r}: {v}" for r, v in sorted(self.vm.registers.items())])
        self.lbl_regs.config(text=reg_text)

        status_str = "DETENIDO (HALT)" if self.vm.is_halted else ("ERROR" if self.vm.error_message else "ACTIVO")
        self.lbl_flags.config(
            text=f"PC: 0x{self.vm.pc:04X}  |  ZF: {self.vm.flags['ZF']}  |  SF: {self.vm.flags['SF']}  |  Ciclos: {self.vm.cycle_count}  |  Estatus: {status_str}"
        )

        self.txt_ram.delete("1.0", tk.END)
        self.txt_ram.insert(tk.END, self.vm.dump_memory_state())

        self.txt_output.delete("1.0", tk.END)
        for out in self.vm.output_buffer:
            self.txt_output.insert(tk.END, out + "\n")

    def action_export_binary(self):
        if not self.current_opt:
            messagebox.showwarning("Aviso", "Primero debe compilar las instrucciones.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("Archivos Binarios Ejecutables (*.bin)", "*.bin"), ("Todos los archivos", "*.*")],
            title="Guardar Archivo Binario Ejecutable"
        )
        if file_path:
            ExecutableBuilder.build_binary(self.current_opt, self.symbol_table, file_path)
            asm_path = os.path.splitext(file_path)[0] + ".asm"
            ExecutableBuilder.generate_asm_file(self.current_opt, self.symbol_table, asm_path, program_title="Exportado desde GUI")
            messagebox.showinfo("Exportación Exitosa", f"Archivos generados correctamente:\n• Binario: {file_path}\n• Desensamblado: {asm_path}")


def main():
    root = tk.Tk()
    app = CodeGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

