import tkinter as tk
from tkinter import ttk

class GestorDatosGUI(tk.Tk):
    """
    Gestor simple de datos con Tkinter.

    """

    def __init__(self):
        super().__init__()
        self.title("Gestor Simple de Actividades Pendientes")
        self.geometry("540x380")
        self.minsize(500, 340)

        # Estado en memoria (opcional, útil si se desea persistir o validar duplicados)
        self.items = []

        # --------- Frame de entrada y acciones ----------
        frm_top = ttk.Frame(self, padding=10)
        frm_top.grid(row=0, column=0, sticky="nsew")

        lbl = ttk.Label(frm_top, text="Ingrese un ítem:")
        lbl.grid(row=0, column=0, padx=(0, 8), pady=(0, 6), sticky="w")

        self.var_input = tk.StringVar()
        entry = ttk.Entry(frm_top, textvariable=self.var_input, width=38)
        entry.grid(row=0, column=1, padx=(0, 8), pady=(0, 6), sticky="ew")
        entry.focus()

        btn_agregar = ttk.Button(frm_top, text="Añadir Actividad", command=self.on_agregar)
        btn_agregar.grid(row=0, column=2, padx=(0, 6), pady=(0, 6), sticky="ew")

        btn_limpiar = ttk.Button(frm_top, text="Limpiar Texto", command=self.on_limpiar)
        btn_limpiar.grid(row=0, column=3, padx=(0, 6), pady=(0, 6), sticky="ew")

        btn_eliminar = ttk.Button(frm_top, text="Eliminar Actividad", command=self.on_eliminar)
        btn_eliminar.grid(row=0, column=4, padx=(0, 0), pady=(0, 6), sticky="ew")

        # Enter para agregar rápidamente
        entry.bind("<Return>", lambda e: self.on_agregar())

        frm_top.columnconfigure(1, weight=1)

        # --------- Frame del listado ----------
        frm_list = ttk.Frame(self, padding=(10, 0, 10, 10))
        frm_list.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(
            frm_list,
            height=12,
            activestyle="dotbox",
            selectmode=tk.EXTENDED  # permite selección múltiple
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frm_list, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Doble clic para editar-cargar el ítem al Entry
        self.listbox.bind("<Double-Button-1>", self.on_editar_item)

        frm_list.rowconfigure(0, weight=1)
        frm_list.columnconfigure(0, weight=1)

        # --------- Barra de estado ----------
        self.var_status = tk.StringVar(value="Listo")
        status = ttk.Label(self, textvariable=self.var_status, anchor="w", relief="sunken")
        status.grid(row=2, column=0, sticky="ew")

    # ---------------- Lógica de eventos ----------------
    def on_agregar(self):
        """
        Agrega el texto no vacío del Entry a la lista y al Listbox.
        Inserta al final para mantener orden cronológico. [2]
        """
        texto = self.var_input.get().strip()
        if not texto:
            self._set_status("No se puede agregar texto vacío.")
            self.bell()
            return
        self.items.append(texto)
        self.listbox.insert("end", texto)  # patrón estándar de inserción. [2]
        self.var_input.set("")
        self._set_status(f"Agregado: {texto}")

    def on_limpiar(self):
        """
        Comportamiento dual:
        - Si hay selección en la lista, elimina los seleccionados.
        - Si no hay selección, limpia el campo de texto.
        """
        sel = self.listbox.curselection()
        if sel:
            eliminados = []
            for idx in reversed(sel):  # mantener índices correctos. [3]
                eliminados.append(self.listbox.get(idx))
                self.listbox.delete(idx)  # elimina en ese índice. [3][7]
                if idx < len(self.items):
                    self.items.pop(idx)
            self._set_status(f"Eliminado(s): {', '.join(eliminados)}")
        else:
            self.var_input.set("")
            self._set_status("Campo de texto limpiado.")

    def on_eliminar(self):
        """
        Elimina explícitamente los elementos seleccionados en la Listbox.
        Recorre índices en reversa para evitar corrimiento. [3][7]
        """
        sel = self.listbox.curselection()  # índices seleccionados. [7]
        if not sel:
            self._set_status("No hay selección para eliminar.")
            self.bell()
            return
        eliminados = []
        for idx in reversed(sel):
            eliminados.append(self.listbox.get(idx))
            self.listbox.delete(idx)  # borrar selección. [3]
            if idx < len(self.items):
                self.items.pop(idx)
        self._set_status(f"Eliminado(s): {', '.join(eliminados)}")

    def on_editar_item(self, event):
        """
        Doble clic: carga el valor del elemento seleccionado en el Entry
        para editar y volver a agregar si se desea. [7]
        """
        try:
            idx = self.listbox.curselection()  # primer índice seleccionado. [7]
        except IndexError:
            return
        valor = self.listbox.get(idx)
        self.var_input.set(valor)
        self._set_status(f"Editando ítem #{idx + 1}")

    # ---------------- Utilidades ----------------
    def _set_status(self, msg: str):
        """Actualiza la barra de estado con un mensaje breve."""
        self.var_status.set(msg)

if __name__ == "__main__":
    app = GestorDatosGUI()
    app.mainloop()
