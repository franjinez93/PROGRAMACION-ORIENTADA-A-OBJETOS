import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import time


class ListaTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.resizable(False, False)

        # Modelo: [{'id', 'tarea', 'fecha', 'hora', 'done'}]
        self.tareas = []
        self.next_id = 1

        # Fondo blanco global
        self.root.configure(bg="white")

        # Estilos ttk para fondo claro
        style = ttk.Style()
        try:
            style.theme_use("default")
        except Exception:
            pass
        style.configure("TFrame", background="white")
        style.configure("TLabelframe", background="white")
        style.configure("TLabelframe.Label", background="white", foreground="#111")
        style.configure("Treeview",
                        background="white",
                        fieldbackground="white",
                        foreground="#111",
                        rowheight=26,
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background="#f3f4f6",
                        foreground="#111",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#dbeafe")])

        # Barra superior con botones
        bar = ttk.Frame(root, padding=(10, 8), style="TFrame")
        bar.grid(row=0, column=0, sticky="ew")

        self.btn_add = tk.Button(bar, text="Añadir Tarea",
                                 command=self.agregar_tarea,
                                 font=("Segoe UI", 10, "bold"),
                                 bg="#22c55e", fg="white",
                                 activebackground="#16a34a", activeforeground="white",
                                 relief="flat", padx=10, pady=6)
        self.btn_add.grid(row=0, column=0, padx=(0, 8))

        self.btn_complete = tk.Button(bar, text="Marcar como Completada",
                                      command=self.completar_tarea,
                                      font=("Segoe UI", 10, "bold"),
                                      bg="#3b82f6", fg="white",
                                      activebackground="#2563eb", activeforeground="white",
                                      relief="flat", padx=10, pady=6)
        self.btn_complete.grid(row=0, column=1, padx=8)

        self.btn_delete = tk.Button(bar, text="Eliminar Tarea",
                                    command=self.eliminar_tarea,
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#ef4444", fg="white",
                                    activebackground="#dc2626", activeforeground="white",
                                    relief="flat", padx=10, pady=6)
        self.btn_delete.grid(row=0, column=2, padx=(8, 0))

        # Panel de entrada: tarea, fecha y hora
        inputs = ttk.LabelFrame(root, text="Nueva tarea", padding=(12, 8), style="TLabelframe")
        inputs.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        inputs.columnconfigure(1, weight=1)

        # Campo de tarea
        ttk.Label(inputs, text="Tarea:", background="white").grid(row=0, column=0, padx=(0, 6), pady=4, sticky="w")
        self.entry_tarea = tk.Entry(inputs, font=("Segoe UI", 10), bg="white", fg="#111",
                                    insertbackground="#111", relief="solid", borderwidth=1)
        self.entry_tarea.grid(row=0, column=1, padx=(0, 8), pady=4, sticky="ew")

        # Selector de fecha con calendario
        ttk.Label(inputs, text="Fecha:", background="white").grid(row=0, column=2, padx=(0, 6), pady=4, sticky="w")
        self.date_picker = DateEntry(inputs,
                                     width=12,
                                     background='darkblue',
                                     foreground='white',
                                     borderwidth=2,
                                     font=("Segoe UI", 10),
                                     date_pattern='yyyy-mm-dd',
                                     showweeknumbers=False,
                                     firstweekday='monday',
                                     headersbackground='lightblue',
                                     normalbackground='white',
                                     selectbackground='lightblue',
                                     weekendbackground='white')
        self.date_picker.grid(row=0, column=3, padx=(0, 8), pady=4)

        # Frame para selectores de hora
        time_frame = tk.Frame(inputs, bg="white")
        time_frame.grid(row=0, column=4, padx=(0, 8), pady=4)

        ttk.Label(inputs, text="Hora:", background="white").grid(row=0, column=4, padx=(0, 6), pady=4, sticky="w")

        # Frame interno para los selectores de tiempo
        time_selectors = tk.Frame(inputs, bg="white")
        time_selectors.grid(row=0, column=5, padx=(0, 8), pady=4)

        # Selector de horas
        self.hour_var = tk.StringVar(value=str(datetime.now().hour).zfill(2))
        self.hour_spinbox = tk.Spinbox(time_selectors,
                                       from_=0, to=23,
                                       width=3,
                                       textvariable=self.hour_var,
                                       font=("Segoe UI", 10),
                                       bg="white", fg="#111",
                                       buttonbackground="lightgray",
                                       format="%02.0f")
        self.hour_spinbox.grid(row=0, column=0)

        tk.Label(time_selectors, text=":", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=1)

        # Selector de minutos
        self.minute_var = tk.StringVar(value=str(datetime.now().minute).zfill(2))
        self.minute_spinbox = tk.Spinbox(time_selectors,
                                         from_=0, to=59,
                                         width=3,
                                         textvariable=self.minute_var,
                                         font=("Segoe UI", 10),
                                         bg="white", fg="#111",
                                         buttonbackground="lightgray",
                                         format="%02.0f")
        self.minute_spinbox.grid(row=0, column=2)

        # Botón de autocompletar fecha/hora actual
        self.btn_now = tk.Button(inputs, text="Ahora",
                                 command=self.set_ahora,
                                 font=("Segoe UI", 9, "bold"),
                                 bg="#0ea5e9", fg="white",
                                 activebackground="#0284c7", activeforeground="white",
                                 relief="flat", padx=8, pady=4)
        self.btn_now.grid(row=0, column=6, padx=(8, 0))

        # Treeview: Tarea | Fecha | Hora | Estado
        self.tree = ttk.Treeview(
            root,
            columns=("Tarea", "Fecha", "Hora", "Estado"),
            show="headings",
            height=14
        )
        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("Tarea", width=320, anchor="w")
        self.tree.column("Fecha", width=110, anchor="center")
        self.tree.column("Hora", width=90, anchor="center")
        self.tree.column("Estado", width=120, anchor="center")
        self.tree.grid(row=2, column=0, padx=10, pady=(0, 10))

        # Tags visuales para diferentes estados - letra siempre negra
        self.tree.tag_configure("done", background="#facc15", foreground="#000000")  # amarillo con letra negra
        self.tree.tag_configure("pending", background="#ffffff", foreground="#000000")  # blanco con letra negra

        # Eventos
        self.entry_tarea.bind("<Return>", self.agregar_tarea)  # Enter añade
        self.tree.bind("<Double-1>", self.toggle_completada)  # Doble clic alterna
        self.root.bind("<space>", self.toggle_completada)  # Espacio alterna
        self.root.bind("<Delete>", lambda e: self.eliminar_tarea())  # Supr elimina

        # Menú contextual
        self.menu = tk.Menu(root, tearoff=0, bg="white", fg="#111",
                            activebackground="#e5e7eb", activeforeground="#111")
        self.tree.bind("<Button-3>", self.mostrar_menu)

        # Centrar
        self.centrar_ventana(800, 560)

    # ---------- Utilidades ----------
    def centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def set_ahora(self):
        ahora = datetime.now()
        # Actualizar el selector de fecha
        self.date_picker.set_date(ahora.date())
        # Actualizar los selectores de hora
        self.hour_var.set(str(ahora.hour).zfill(2))
        self.minute_var.set(str(ahora.minute).zfill(2))

    def get_selected_datetime(self):
        """Obtiene la fecha y hora seleccionadas en formato string"""
        fecha = self.date_picker.get()  # Ya viene en formato YYYY-MM-DD
        hora = f"{self.hour_var.get().zfill(2)}:{self.minute_var.get().zfill(2)}"
        return fecha, hora

    def _refrescar_tree(self):
        self.tree.delete(*self.tree.get_children())
        for t in self.tareas:
            estado = "Completada" if t['done'] else "Pendiente"
            # Seleccionar tag según el estado - siempre con letra negra
            tags = ("done",) if t['done'] else ("pending",)
            self.tree.insert(
                "", tk.END, iid=str(t['id']),
                values=(t['tarea'], t['fecha'], t['hora'], estado),
                tags=tags
            )

    def _seleccion_actual(self):
        sel = self.tree.selection()
        if not sel:
            return None
        iid = sel[0]
        for t in self.tareas:
            if str(t['id']) == iid:
                return t
        return None

    # ---------- Validaciones simples ----------
    def _validar_fecha(self, texto):
        if not texto:
            return False
        try:
            datetime.strptime(texto, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _validar_hora(self, texto):
        if not texto:
            return False
        try:
            datetime.strptime(texto, "%H:%M")
            return True
        except ValueError:
            return False

    # ---------- Acciones ----------
    def agregar_tarea(self, event=None):
        tarea = self.entry_tarea.get().strip()

        if not tarea:
            messagebox.showwarning("Advertencia", "No puedes añadir una tarea vacía.")
            return

        # Obtener fecha y hora de los selectores
        fecha, hora = self.get_selected_datetime()

        # Validación de formato (aunque los selectores deberían garantizar formato correcto)
        if not self._validar_fecha(fecha):
            messagebox.showwarning("Formato inválido", "Fecha inválida. Usa YYYY-MM-DD.")
            return
        if not self._validar_hora(hora):
            messagebox.showwarning("Formato inválido", "Hora inválida. Usa HH:MM en 24h.")
            return

        self.tareas.append({'id': self.next_id, 'tarea': tarea, 'fecha': fecha, 'hora': hora, 'done': False})
        self.next_id += 1

        # Limpiar entrada de tarea; mantener fecha/hora para añadir varias seguidas
        self.entry_tarea.delete(0, tk.END)
        self._refrescar_tree()

    def completar_tarea(self):
        t = self._seleccion_actual()
        if not t:
            messagebox.showinfo("Info", "Selecciona una tarea para marcarla.")
            return
        t['done'] = not t['done']
        self._refrescar_tree()
        self.tree.selection_set(str(t['id']))

    def eliminar_tarea(self):
        t = self._seleccion_actual()
        if not t:
            messagebox.showinfo("Info", "Selecciona una tarea para eliminarla.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar la tarea seleccionada?"):
            return
        self.tareas = [x for x in self.tareas if x['id'] != t['id']]
        self._refrescar_tree()

    def toggle_completada(self, event=None):
        t = self._seleccion_actual()
        if not t:
            return
        t['done'] = not t['done']
        self._refrescar_tree()
        self.tree.selection_set(str(t['id']))

    def mostrar_menu(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        self.tree.selection_set(item)
        t = self._seleccion_actual()
        if not t:
            return
        self.menu.delete(0, tk.END)
        if t['done']:
            self.menu.add_command(label="Marcar como pendiente", command=self.completar_tarea)
        else:
            self.menu.add_command(label="Marcar como completada", command=self.completar_tarea)
        self.menu.add_separator()
        self.menu.add_command(label="Eliminar", command=self.eliminar_tarea)
        self.menu.tk_popup(event.x_root, event.y_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = ListaTareasApp(root)
    root.mainloop()