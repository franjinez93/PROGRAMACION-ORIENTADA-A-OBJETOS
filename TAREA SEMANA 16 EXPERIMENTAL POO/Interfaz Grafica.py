import tkinter as tk
from tkinter import ttk, messagebox
from Inventario import Inventario


class SistemaInventarioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario - UEA")
        self.root.geometry("900x650")
        self.root.configure(bg='#F0F8FF')

        # Colores pastel
        self.colores = {
            'fondo': '#F0F8FF',
            'boton_agregar': '#98FB98',
            'boton_modificar': '#FFB6C1',
            'boton_eliminar': '#FFD700',
            'boton_listar': '#87CEFA',
            'boton_limpiar': '#DDA0DD',
            'boton_salir': '#FFA07A',
            'boton_buscar': '#20B2AA',
            'frame': '#E6E6FA',
            'texto': '#2F4F4F'
        }

        # Atajos de teclado
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.bind('<Delete>', lambda e: self.eliminar_con_tecla())

        self.inventario = Inventario()
        self.crear_pantalla_principal()

    def crear_boton_pastel(self, parent, text, command, color, width=15):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=self.colores['texto'],
            font=('Arial', 9, 'bold'),
            width=width,
            relief='raised',
            bd=2,
            padx=10,
            pady=5
        )

    def crear_pantalla_principal(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colores['fondo'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # INFORMACIÓN DEL ESTUDIANTE (ACTUALIZADO CON AMBOS NOMBRES)
        info_frame = tk.LabelFrame(
            main_frame,
            text="INFORMACIÓN DEL ESTUDIANTE",
            bg=self.colores['frame'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(info_frame, text="Estudiante 1: Pianda Rosado Madelin Ibeth",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10, 'bold')).pack(anchor='w')
        tk.Label(info_frame, text="Estudiante 2: Jinez Montesdeoca Edgar Francisco",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10, 'bold')).pack(anchor='w')
        tk.Label(info_frame, text="Paralelo: UEA-L-UFB-030-A",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text="Semestre: Segundo Semestre",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text="Carrera: Ingeniería en Tecnologías de la Información",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text="Asignatura: Programación Orientada a Objetos",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text="Práctica N°: 4 - Sistema de Gestión de Inventario",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text="Docente: Santiago Israel Nogales Guerrero",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 10)).pack(anchor='w')

        # TÍTULO PRINCIPAL
        titulo_frame = tk.Frame(main_frame, bg=self.colores['fondo'])
        titulo_frame.pack(fill=tk.X, pady=10)

        tk.Label(titulo_frame, text="SISTEMA DE GESTIÓN DE INVENTARIO",
                 bg=self.colores['fondo'], fg='#2E8B57', font=('Arial', 16, 'bold')).pack()

        # MENÚ CON OPCIONES (Productos y Salir)
        menu_frame = tk.Frame(main_frame, bg=self.colores['fondo'])
        menu_frame.pack(fill=tk.X, pady=15)

        self.crear_boton_pastel(
            menu_frame,
            "📦 PRODUCTOS",
            self.abrir_gestion_productos,
            self.colores['boton_listar'],
            width=25
        ).pack(side=tk.LEFT, padx=10)

        self.crear_boton_pastel(
            menu_frame,
            "🚪 SALIR",
            self.root.quit,
            self.colores['boton_salir'],
            width=15
        ).pack(side=tk.RIGHT, padx=10)

        # Lista de productos
        lista_frame = tk.LabelFrame(
            main_frame,
            text="INVENTARIO ACTUAL - PRODUCTOS REGISTRADOS",
            bg=self.colores['frame'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        lista_frame.pack(fill=tk.BOTH, expand=True)

        # TreeView
        style = ttk.Style()
        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground=self.colores['texto'],
                        rowheight=25,
                        fieldbackground="#FFFFFF")
        style.map('Treeview', background=[('selected', '#4CAF50')])

        columns = ('ID', 'Nombre', 'Cantidad', 'Precio')
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=12, style="Treeview")

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='NOMBRE DEL PRODUCTO')
        self.tree.heading('Cantidad', text='CANTIDAD')
        self.tree.heading('Precio', text='PRECIO ($)')

        self.tree.column('ID', width=80, anchor='center')
        self.tree.column('Nombre', width=300, anchor='w')
        self.tree.column('Cantidad', width=100, anchor='center')
        self.tree.column('Precio', width=120, anchor='e')

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Atajos
        atajos_frame = tk.Frame(main_frame, bg=self.colores['fondo'])
        atajos_frame.pack(fill=tk.X, pady=5)

        tk.Label(atajos_frame, text="Atajos: [Delete] Eliminar producto seleccionado | [Escape] Salir",
                 bg=self.colores['fondo'], fg='gray', font=('Arial', 8)).pack(side=tk.LEFT)

        self.actualizar_lista()

    def abrir_gestion_productos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestión de Productos - Sistema de Inventario")
        ventana.geometry("700x600")
        ventana.configure(bg=self.colores['fondo'])
        ventana.resizable(False, False)

        ventana.transient(self.root)
        ventana.grab_set()

        self.crear_formulario_productos(ventana)

    def crear_formulario_productos(self, parent):
        main_frame = tk.Frame(parent, bg=self.colores['fondo'], padx=25, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo_frame = tk.Frame(main_frame, bg=self.colores['fondo'])
        titulo_frame.pack(fill=tk.X, pady=15)

        tk.Label(titulo_frame, text="🎯 GESTIÓN DE PRODUCTOS",
                 bg=self.colores['fondo'], fg='#2E8B57', font=('Arial', 18, 'bold')).pack()

        tk.Label(titulo_frame, text="Complete los datos del producto:",
                 bg=self.colores['fondo'], fg=self.colores['texto'], font=('Arial', 11)).pack(pady=5)

        # Formulario
        form_frame = tk.LabelFrame(
            main_frame,
            text="DATOS DEL PRODUCTO",
            bg=self.colores['frame'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=15
        )
        form_frame.pack(fill=tk.X, pady=15)

        tk.Label(form_frame, text="ID del Producto:",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 9, 'bold')).grid(row=0, column=0,
                                                                                                     sticky='w', pady=8)
        self.entry_id = tk.Entry(form_frame, width=35, font=('Arial', 10), bg='white', fg=self.colores['texto'])
        self.entry_id.grid(row=0, column=1, padx=10, pady=8, sticky='ew')

        tk.Label(form_frame, text="Nombre del Producto:",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 9, 'bold')).grid(row=1, column=0,
                                                                                                     sticky='w', pady=8)
        self.entry_nombre = tk.Entry(form_frame, width=35, font=('Arial', 10), bg='white', fg=self.colores['texto'])
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=8, sticky='ew')

        tk.Label(form_frame, text="Cantidad en Stock:",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 9, 'bold')).grid(row=2, column=0,
                                                                                                     sticky='w', pady=8)
        self.entry_cantidad = tk.Entry(form_frame, width=35, font=('Arial', 10), bg='white', fg=self.colores['texto'])
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=8, sticky='ew')

        tk.Label(form_frame, text="Precio Unitario ($):",
                 bg=self.colores['frame'], fg=self.colores['texto'], font=('Arial', 9, 'bold')).grid(row=3, column=0,
                                                                                                     sticky='w', pady=8)
        self.entry_precio = tk.Entry(form_frame, width=35, font=('Arial', 10), bg='white', fg=self.colores['texto'])
        self.entry_precio.grid(row=3, column=1, padx=10, pady=8, sticky='ew')

        form_frame.columnconfigure(1, weight=1)

        # Botones de operaciones
        botones_frame = tk.LabelFrame(
            main_frame,
            text="OPERACIONES DISPONIBLES",
            bg=self.colores['frame'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=15
        )
        botones_frame.pack(fill=tk.X, pady=20)

        # Fila 1
        fila1 = tk.Frame(botones_frame, bg=self.colores['frame'])
        fila1.pack(pady=5)

        self.crear_boton_pastel(fila1, "➕ INGRESAR PRODUCTO", self.ingresar_producto, self.colores['boton_agregar'],
                                20).pack(side=tk.LEFT, padx=8)
        self.crear_boton_pastel(fila1, "✏️ MODIFICAR PRODUCTO", self.modificar_producto,
                                self.colores['boton_modificar'], 20).pack(side=tk.LEFT, padx=8)

        # Fila 2
        fila2 = tk.Frame(botones_frame, bg=self.colores['frame'])
        fila2.pack(pady=5)

        self.crear_boton_pastel(fila2, "🗑️ ELIMINAR PRODUCTO", self.eliminar_producto, self.colores['boton_eliminar'],
                                20).pack(side=tk.LEFT, padx=8)
        self.crear_boton_pastel(fila2, "📋 LISTAR PRODUCTOS", self.actualizar_lista, self.colores['boton_listar'],
                                20).pack(side=tk.LEFT, padx=8)

        # Botones extra
        botones_extra_frame = tk.Frame(botones_frame, bg=self.colores['frame'])
        botones_extra_frame.pack(pady=10)

        self.crear_boton_pastel(botones_extra_frame, "🔍 BUSCAR POR ID", self.buscar_producto,
                                self.colores['boton_buscar'], 18).pack(side=tk.LEFT, padx=5)
        self.crear_boton_pastel(botones_extra_frame, "🧹 LIMPIAR CAMPOS", self.limpiar_campos,
                                self.colores['boton_limpiar'], 18).pack(side=tk.LEFT, padx=5)

        # Ayuda
        ayuda_frame = tk.Frame(main_frame, bg=self.colores['fondo'])
        ayuda_frame.pack(fill=tk.X, pady=10)

        tk.Label(ayuda_frame,
                 text="💡 Para modificar o eliminar, primero ingrese el ID y use los botones correspondientes",
                 bg=self.colores['fondo'], fg='blue', font=('Arial', 9), justify='center').pack()

    def ingresar_producto(self):
        try:
            id_producto = int(self.entry_id.get())
            nombre = self.entry_nombre.get().strip()
            cantidad = int(self.entry_cantidad.get())
            precio = float(self.entry_precio.get())

            if not nombre:
                messagebox.showerror("Error", "El nombre del producto no puede estar vacío")
                return

            if cantidad < 0:
                messagebox.showerror("Error", "La cantidad no puede ser negativa")
                return

            if precio < 0:
                messagebox.showerror("Error", "El precio no puede ser negativo")
                return

            if self.inventario.agregar_producto(id_producto, nombre, cantidad, precio):
                messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente al inventario")
                self.actualizar_lista()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", f"El ID {id_producto} ya existe en el inventario")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos en ID, Cantidad y Precio")

    def modificar_producto(self):
        try:
            id_producto = int(self.entry_id.get())
            nombre = self.entry_nombre.get().strip()
            cantidad = int(self.entry_cantidad.get()) if self.entry_cantidad.get() else None
            precio = float(self.entry_precio.get()) if self.entry_precio.get() else None

            if self.inventario.modificar_producto(id_producto, nombre, cantidad, precio):
                messagebox.showinfo("Éxito", f"Producto con ID {id_producto} modificado correctamente")
                self.actualizar_lista()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", f"No se encontró ningún producto con ID {id_producto}")

        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")

    def eliminar_producto(self):
        try:
            id_producto = int(self.entry_id.get())
            producto = self.inventario.productos.get(id_producto)
            if producto:
                if messagebox.askyesno("Confirmar Eliminación",
                                       f"¿Está seguro de eliminar el producto:\n'{producto.get_nombre()} (ID: {id_producto})'?"):
                    if self.inventario.eliminar_producto(id_producto):
                        messagebox.showinfo("Éxito", "Producto eliminado correctamente del inventario")
                        self.actualizar_lista()
                        self.limpiar_campos()
            else:
                messagebox.showerror("Error", f"No se encontró ningún producto con ID {id_producto}")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")

    def buscar_producto(self):
        try:
            id_producto = int(self.entry_id.get())
            producto = self.inventario.productos.get(id_producto)
            if producto:
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, producto.get_nombre())
                self.entry_cantidad.delete(0, tk.END)
                self.entry_cantidad.insert(0, str(producto.get_cantidad()))
                self.entry_precio.delete(0, tk.END)
                self.entry_precio.insert(0, str(producto.get_precio()))
                messagebox.showinfo("Producto Encontrado", f"Producto encontrado: {producto.get_nombre()}")
            else:
                messagebox.showerror("Error", f"No se encontró ningún producto con ID {id_producto}")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")

    def eliminar_con_tecla(self):
        seleccion = self.tree.selection()
        if seleccion:
            id_producto = int(self.tree.item(seleccion[0])['values'][0])
            nombre_producto = self.tree.item(seleccion[0])['values'][1]
            if messagebox.askyesno("Confirmar Eliminación",
                                   f"¿Está seguro de eliminar el producto:\n'{nombre_producto} (ID: {id_producto})'?"):
                if self.inventario.eliminar_producto(id_producto):
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.actualizar_lista()

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = self.inventario.mostrar_todos_productos()
        for producto in productos:
            self.tree.insert('', tk.END, values=(
                producto.get_id(),
                producto.get_nombre(),
                producto.get_cantidad(),
                f"${producto.get_precio():.2f}"
            ))

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.LabelFrame) and "INVENTARIO ACTUAL" in child.cget('text'):
                        child.configure(text=f"INVENTARIO ACTUAL - {len(productos)} PRODUCTOS REGISTRADOS")

    def limpiar_campos(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_id.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaInventarioGUI(root)
    root.mainloop()