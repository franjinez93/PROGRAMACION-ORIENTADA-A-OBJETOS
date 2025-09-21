import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import calendar


class DatePicker(tk.Toplevel):
    """
    Widget personalizado para selección de fechas
    """

    def __init__(self, parent, initial_date=None):
        super().__init__(parent)
        self.parent = parent
        self.selected_date = None

        self.title("Seleccionar Fecha")
        self.geometry("300x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.winfo_screenheight() // 2) - (250 // 2)
        self.geometry(f"300x250+{x}+{y}")

        # Fecha inicial
        if initial_date:
            self.current_date = initial_date
        else:
            self.current_date = date.today()

        self.create_widgets()
        self.update_calendar()

    def create_widgets(self):
        # Frame superior para navegación
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=10)

        self.btn_prev = ttk.Button(nav_frame, text="<", width=3, command=self.prev_month)
        self.btn_prev.pack(side=tk.LEFT, padx=5)

        self.lbl_month_year = ttk.Label(nav_frame, text="", font=("Arial", 12, "bold"))
        self.lbl_month_year.pack(side=tk.LEFT, padx=20)

        self.btn_next = ttk.Button(nav_frame, text=">", width=3, command=self.next_month)
        self.btn_next.pack(side=tk.LEFT, padx=5)

        # Frame para el calendario
        cal_frame = ttk.Frame(self)
        cal_frame.pack(pady=10)

        # Etiquetas de días de la semana
        days = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'Do']
        for i, day in enumerate(days):
            ttk.Label(cal_frame, text=day, font=("Arial", 9, "bold")).grid(row=0, column=i, padx=2, pady=2)

        # Botones para los días
        self.day_buttons = []
        for week in range(6):
            week_buttons = []
            for day in range(7):
                btn = tk.Button(cal_frame, text="", width=3, height=1,
                                command=lambda w=week, d=day: self.select_day(w, d))
                btn.grid(row=week + 1, column=day, padx=1, pady=1)
                week_buttons.append(btn)
            self.day_buttons.append(week_buttons)

        # Frame para botones de acción
        action_frame = ttk.Frame(self)
        action_frame.pack(pady=20)

        ttk.Button(action_frame, text="Hoy", command=self.select_today).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Aceptar", command=self.accept).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT, padx=5)

    def update_calendar(self):
        # Actualizar etiqueta del mes y año
        month_names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                       'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.lbl_month_year.config(text=f"{month_names[self.current_date.month - 1]} {self.current_date.year}")

        # Obtener calendario del mes
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        # Limpiar todos los botones
        for week in self.day_buttons:
            for btn in week:
                btn.config(text="", state=tk.DISABLED, bg="SystemButtonFace")

        # Llenar los días
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue

                btn = self.day_buttons[week_num][day_num]
                btn.config(text=str(day), state=tk.NORMAL)

                # Destacar día actual
                if (self.current_date.year == date.today().year and
                        self.current_date.month == date.today().month and
                        day == date.today().day):
                    btn.config(bg="lightblue")
                else:
                    btn.config(bg="white")

    def prev_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()

    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()

    def select_day(self, week, day):
        if self.day_buttons[week][day]['text']:
            selected_day = int(self.day_buttons[week][day]['text'])
            self.selected_date = date(self.current_date.year, self.current_date.month, selected_day)
            self.accept()

    def select_today(self):
        self.selected_date = date.today()
        self.accept()

    def accept(self):
        self.destroy()

    def cancel(self):
        self.selected_date = None
        self.destroy()


class AgendaPersonalGUI(tk.Tk):
    """
    Agenda Personal con Tkinter - Gestión completa de eventos y tareas
    """

    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("800x600")
        self.minsize(700, 500)

        # Estado en memoria para almacenar eventos
        self.eventos = []
        self.evento_counter = 1

        self.create_widgets()
        self.center_window()

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # --------- Frame principal ----------
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configurar peso de filas y columnas
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # --------- Frame de entrada de datos ----------
        entrada_frame = ttk.LabelFrame(main_frame, text="Nuevo Evento/Tarea", padding=15)
        entrada_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Fecha
        ttk.Label(entrada_frame, text="Fecha:").grid(row=0, column=0, padx=(0, 8), pady=5, sticky="w")

        fecha_frame = ttk.Frame(entrada_frame)
        fecha_frame.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="ew")

        self.var_fecha = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
        self.entry_fecha = ttk.Entry(fecha_frame, textvariable=self.var_fecha, width=12, state="readonly")
        self.entry_fecha.pack(side=tk.LEFT)

        self.btn_fecha = ttk.Button(fecha_frame, text="📅", width=3, command=self.abrir_datepicker)
        self.btn_fecha.pack(side=tk.LEFT, padx=(5, 0))

        # Hora
        ttk.Label(entrada_frame, text="Hora:").grid(row=0, column=2, padx=(0, 8), pady=5, sticky="w")

        hora_frame = ttk.Frame(entrada_frame)
        hora_frame.grid(row=0, column=3, padx=(0, 20), pady=5, sticky="ew")

        self.var_hora = tk.StringVar(value="09:00")
        self.spinbox_hora = tk.Spinbox(hora_frame, textvariable=self.var_hora,
                                       values=[f"{h:02d}:{m:02d}" for h in range(24) for m in [0, 15, 30, 45]],
                                       width=8, wrap=True, state="readonly")
        self.spinbox_hora.pack()

        # Descripción
        ttk.Label(entrada_frame, text="Descripción:").grid(row=1, column=0, padx=(0, 8), pady=5, sticky="nw")

        self.var_descripcion = tk.StringVar()
        self.entry_descripcion = ttk.Entry(entrada_frame, textvariable=self.var_descripcion, width=50)
        self.entry_descripcion.grid(row=1, column=1, columnspan=3, padx=(0, 0), pady=5, sticky="ew")
        self.entry_descripcion.focus()

        # Enter para agregar rápidamente
        self.entry_descripcion.bind("<Return>", lambda e: self.agregar_evento())

        # Configurar expansión de columnas
        entrada_frame.columnconfigure(1, weight=1)
        entrada_frame.columnconfigure(3, weight=1)

        # --------- Frame de botones de acción ----------
        botones_frame = ttk.Frame(entrada_frame)
        botones_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        self.btn_agregar = ttk.Button(botones_frame, text="Agregar Evento", command=self.agregar_evento)
        self.btn_agregar.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_limpiar = ttk.Button(botones_frame, text="Limpiar Campos", command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.LEFT, padx=(0, 10))

        # --------- Frame de lista de eventos ----------
        lista_frame = ttk.LabelFrame(main_frame, text="Eventos y Tareas Programadas", padding=10)
        lista_frame.grid(row=1, column=0, sticky="nsew")
        lista_frame.rowconfigure(0, weight=1)
        lista_frame.columnconfigure(0, weight=1)

        # TreeView para mostrar eventos
        columns = ("ID", "Fecha", "Hora", "Descripción")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=12)

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Descripción", text="Descripción")

        self.tree.column("ID", width=50, minwidth=40)
        self.tree.column("Fecha", width=100, minwidth=80)
        self.tree.column("Hora", width=80, minwidth=60)
        self.tree.column("Descripción", width=400, minwidth=200)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el TreeView
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Scrollbar horizontal
        scrollbar_h = ttk.Scrollbar(lista_frame, orient="horizontal", command=self.tree.xview)
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=scrollbar_h.set)

        # --------- Frame de botones de gestión ----------
        gestion_frame = ttk.Frame(main_frame)
        gestion_frame.grid(row=2, column=0, pady=(10, 0))

        self.btn_eliminar = ttk.Button(gestion_frame, text="Eliminar Evento Seleccionado",
                                       command=self.eliminar_evento)
        self.btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_salir = ttk.Button(gestion_frame, text="Salir", command=self.salir_aplicacion)
        self.btn_salir.pack(side=tk.LEFT)

        # --------- Barra de estado ----------
        self.var_status = tk.StringVar(value="Listo - Agenda Personal")
        self.status_bar = ttk.Label(main_frame, textvariable=self.var_status,
                                    relief="sunken", anchor="w")
        self.status_bar.grid(row=3, column=0, sticky="ew", pady=(10, 0))

    def abrir_datepicker(self):
        """Abrir el selector de fechas personalizado"""
        try:
            fecha_actual = datetime.strptime(self.var_fecha.get(), "%d/%m/%Y").date()
        except:
            fecha_actual = date.today()

        picker = DatePicker(self, fecha_actual)
        self.wait_window(picker)

        if picker.selected_date:
            self.var_fecha.set(picker.selected_date.strftime("%d/%m/%Y"))
            self.set_status(f"Fecha seleccionada: {picker.selected_date.strftime('%d/%m/%Y')}")

    def agregar_evento(self):
        """Agregar un nuevo evento a la agenda"""
        # Validar campos
        fecha_str = self.var_fecha.get().strip()
        hora_str = self.var_hora.get().strip()
        descripcion = self.var_descripcion.get().strip()

        if not descripcion:
            messagebox.showwarning("Advertencia", "La descripción del evento no puede estar vacía.")
            self.entry_descripcion.focus()
            return

        # Validar formato de fecha
        try:
            fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA")
            return

        # Crear evento
        evento = {
            'id': self.evento_counter,
            'fecha': fecha_obj,
            'hora': hora_str,
            'descripcion': descripcion,
            'fecha_str': fecha_str
        }

        self.eventos.append(evento)
        self.evento_counter += 1

        # Agregar al TreeView
        self.tree.insert("", "end", values=(evento['id'], evento['fecha_str'],
                                            evento['hora'], evento['descripcion']))

        # Limpiar campos y actualizar estado
        self.limpiar_campos()
        self.set_status(f"Evento agregado: {descripcion} - {fecha_str} {hora_str}")
        self.ordenar_eventos()

    def eliminar_evento(self):
        """Eliminar el evento seleccionado"""
        seleccion = self.tree.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un evento para eliminar.")
            return

        # Confirmación
        item = self.tree.item(seleccion[0])
        evento_info = item['values']

        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el evento?\n\n"
            f"Fecha: {evento_info[1]}\n"
            f"Hora: {evento_info[2]}\n"
            f"Descripción: {evento_info[3]}"
        )

        if respuesta:
            # Eliminar del TreeView
            self.tree.delete(seleccion[0])

            # Eliminar de la lista en memoria
            evento_id = evento_info[0]
            self.eventos = [e for e in self.eventos if e['id'] != evento_id]

            self.set_status(f"Evento eliminado: {evento_info[3]}")

    def ordenar_eventos(self):
        """Ordenar eventos por fecha y hora"""
        # Obtener todos los elementos del TreeView
        items = []
        for child in self.tree.get_children():
            item = self.tree.item(child)
            items.append((child, item['values']))

        # Ordenar por fecha y hora
        def sort_key(item):
            try:
                fecha = datetime.strptime(item[1][1], "%d/%m/%Y").date()
                hora = datetime.strptime(item[1][2], "%H:%M").time()
                return datetime.combine(fecha, hora)
            except:
                return datetime.now()

        items.sort(key=sort_key)

        # Reordenar en el TreeView
        for index, (child, values) in enumerate(items):
            self.tree.move(child, "", index)

    def limpiar_campos(self):
        """Limpiar todos los campos de entrada"""
        self.var_fecha.set(date.today().strftime("%d/%m/%Y"))
        self.var_hora.set("09:00")
        self.var_descripcion.set("")
        self.entry_descripcion.focus()
        self.set_status("Campos limpiados")

    def salir_aplicacion(self):
        """Salir de la aplicación con confirmación"""
        if self.eventos:
            respuesta = messagebox.askyesno(
                "Confirmar Salida",
                f"Tiene {len(self.eventos)} evento(s) en su agenda.\n"
                "¿Está seguro de que desea salir?"
            )
            if respuesta:
                self.destroy()
        else:
            self.destroy()

    def set_status(self, mensaje):
        """Actualizar la barra de estado"""
        self.var_status.set(mensaje)
        # Volver al mensaje por defecto después de 3 segundos
        self.after(3000, lambda: self.var_status.set("Listo - Agenda Personal"))


if __name__ == "__main__":
    app = AgendaPersonalGUI()
    app.mainloop()