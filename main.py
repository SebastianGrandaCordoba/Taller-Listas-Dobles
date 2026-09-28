import tkinter as tk
from tkinter import ttk, messagebox

from lista_doble import ListaDoble


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario de Celulares - Lista Doble")
        self.root.geometry("1150x720")
        self.root.minsize(950, 620)

        self.lista = ListaDoble()
        self.cargar_datos()

        self.configurar_estilos()
        self.crear_interfaz()
        self.actualizar()

    def cargar_datos(self):
        productos = [
            {"nombre": "iPhone 13", "marca": "Apple", "modelo": "13", "precio": 1899000, "stock": 5},
            {"nombre": "iPhone 14 Pro", "marca": "Apple", "modelo": "14 Pro", "precio": 2799000, "stock": 3},
            {"nombre": "iPhone 15 Pro Max", "marca": "Apple", "modelo": "15 Pro Max", "precio": 3899000, "stock": 4},
            {"nombre": "Galaxy S24 Ultra", "marca": "Samsung", "modelo": "S24 Ultra", "precio": 4299000, "stock": 2},
        ]
        for producto in productos:
            self.lista.append(producto)

    def configurar_estilos(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"),
                        foreground="white", background="#5b4bc4")
        style.map("Primary.TButton", background=[("active", "#493aa8")])

        style.configure("Treeview", rowheight=32, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))

    def crear_interfaz(self):
        self.root.configure(bg="#f3f4f8")

        header = tk.Frame(self.root, bg="#171b2b", height=82)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="CELLVAULT", bg="#171b2b", fg="white",
                 font=("Segoe UI", 21, "bold")).pack(side="left", padx=28, pady=17)
        tk.Label(header, text="Inventario • Lista doblemente enlazada",
                 bg="#171b2b", fg="#aeb5c8", font=("Segoe UI", 10)).pack(side="left")

        body = tk.Frame(self.root, bg="#f3f4f8")
        body.pack(fill="both", expand=True, padx=22, pady=18)

        # Panel izquierdo
        left = tk.Frame(body, bg="#ffffff", highlightbackground="#dfe2ea",
                        highlightthickness=1, padx=18, pady=16)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.configure(width=310)
        left.pack_propagate(False)

        tk.Label(left, text="GESTIONAR PRODUCTO", bg="white", fg="#5b4bc4",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(left, text="Crear y modificar nodos", bg="white", fg="#6f7788",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 15))

        self.entries = {}
        campos = [("Nombre", "Ej. iPhone 16 Pro"),
                  ("Marca", "Apple"),
                  ("Modelo", "16 Pro"),
                  ("Precio", "2999000"),
                  ("Stock", "5")]

        for nombre, placeholder in campos:
            tk.Label(left, text=nombre, bg="white", fg="#343b4d",
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(7, 4))
            entry = ttk.Entry(left)
            entry.pack(fill="x")
            entry.insert(0, placeholder)
            self.entries[nombre] = entry

        ttk.Separator(left).pack(fill="x", pady=17)

        tk.Label(left, text="POSICIÓN", bg="white", fg="#343b4d",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
        self.posicion = ttk.Entry(left)
        self.posicion.pack(fill="x")
        self.posicion.insert(0, "0")

        ttk.Button(left, text="＋ Agregar al final", style="Primary.TButton",
                   command=self.agregar_final).pack(fill="x", pady=(15, 6))
        ttk.Button(left, text="＋ Agregar al inicio",
                   command=self.agregar_inicio).pack(fill="x", pady=3)
        ttk.Button(left, text="Insertar en posición",
                   command=self.insertar).pack(fill="x", pady=3)
        ttk.Button(left, text="Eliminar posición",
                   command=self.eliminar).pack(fill="x", pady=3)

        # Panel derecho
        right = tk.Frame(body, bg="#f3f4f8")
        right.pack(side="left", fill="both", expand=True)

        stats = tk.Frame(right, bg="#f3f4f8")
        stats.pack(fill="x", pady=(0, 14))

        self.lbl_nodos = self.crear_stat(stats, "NODOS", "0")
        self.lbl_stock = self.crear_stat(stats, "STOCK", "0")
        self.lbl_head = self.crear_stat(stats, "HEAD", "NULL")
        self.lbl_tail = self.crear_stat(stats, "TAIL", "NULL")

        # Visualización de enlaces
        diagram = tk.Frame(right, bg="white", highlightbackground="#dfe2ea",
                           highlightthickness=1, padx=15, pady=12)
        diagram.pack(fill="x", pady=(0, 14))

        top = tk.Frame(diagram, bg="white")
        top.pack(fill="x")
        tk.Label(top, text="ESTRUCTURA DE LA LISTA", bg="white",
                 fg="#5b4bc4", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(top, text="HEAD → TAIL", command=lambda: self.mostrar_recorrido(True)).pack(side="right", padx=3)
        ttk.Button(top, text="TAIL → HEAD", command=lambda: self.mostrar_recorrido(False)).pack(side="right", padx=3)

        self.canvas = tk.Canvas(diagram, height=160, bg="#fafbff", highlightthickness=0)
        self.canvas.pack(fill="x", pady=(10, 0))

        # Tabla
        table_frame = tk.Frame(right, bg="white", highlightbackground="#dfe2ea",
                               highlightthickness=1, padx=12, pady=12)
        table_frame.pack(fill="both", expand=True)

        tk.Label(table_frame, text="PRODUCTOS / NODOS", bg="white",
                 fg="#5b4bc4", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))

        columns = ("indice", "nombre", "marca", "precio", "stock", "prev", "next")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=9)
        headings = {
            "indice": "#", "nombre": "Producto", "marca": "Marca",
            "precio": "Precio", "stock": "Stock", "prev": "Prev", "next": "Next"
        }
        widths = {"indice": 40, "nombre": 180, "marca": 100, "precio": 120,
                  "stock": 65, "prev": 55, "next": 55}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.column("nombre", anchor="w")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        bottom = tk.Frame(right, bg="#f3f4f8")
        bottom.pack(fill="x", pady=(10, 0))

        self.buscar_entry = ttk.Entry(bottom)
        self.buscar_entry.pack(side="left", fill="x", expand=True)
        self.buscar_entry.insert(0, "Buscar producto...")
        ttk.Button(bottom, text="Buscar", command=self.buscar).pack(side="left", padx=6)
        ttk.Button(bottom, text="Mostrar todo", command=self.actualizar).pack(side="left")

    def crear_stat(self, parent, titulo, valor):
        card = tk.Frame(parent, bg="white", highlightbackground="#dfe2ea",
                        highlightthickness=1, padx=13, pady=10)
        card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(card, text=titulo, bg="white", fg="#858da0",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        label = tk.Label(card, text=valor, bg="white", fg="#202638",
                         font=("Segoe UI", 14, "bold"))
        label.pack(anchor="w", pady=(3, 0))
        return label

    def datos_formulario(self):
        try:
            producto = {
                "nombre": self.entries["Nombre"].get().strip(),
                "marca": self.entries["Marca"].get().strip(),
                "modelo": self.entries["Modelo"].get().strip(),
                "precio": float(self.entries["Precio"].get()),
                "stock": int(self.entries["Stock"].get())
            }
            if not producto["nombre"] or not producto["marca"] or not producto["modelo"]:
                raise ValueError("Completa nombre, marca y modelo.")
            if producto["precio"] < 0 or producto["stock"] < 0:
                raise ValueError("Precio y stock no pueden ser negativos.")
            return producto
        except ValueError as e:
            messagebox.showerror("Datos inválidos", str(e))
            return None

    def agregar_final(self):
        producto = self.datos_formulario()
        if producto:
            self.lista.append(producto)
            self.actualizar()
            messagebox.showinfo("Lista doble", "Nodo agregado al final.")

    def agregar_inicio(self):
        producto = self.datos_formulario()
        if producto:
            self.lista.prepend(producto)
            self.actualizar()
            messagebox.showinfo("Lista doble", "Nodo agregado al inicio.")

    def insertar(self):
        producto = self.datos_formulario()
        if not producto:
            return
        try:
            indice = int(self.posicion.get())
            self.lista.insert(indice, producto)
            self.actualizar()
            messagebox.showinfo("Lista doble", f"Nodo insertado en la posición {indice}.")
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        try:
            indice = int(self.posicion.get())
            producto = self.lista.remove(indice)
            self.actualizar()
            messagebox.showinfo("Lista doble", f"Se eliminó: {producto['nombre']}")
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))

    def buscar(self):
        termino = self.buscar_entry.get().strip().lower()
        if not termino or termino == "buscar producto...":
            self.actualizar()
            return

        encontrados = []
        actual = self.lista.head
        indice = 0
        while actual:
            p = actual.producto
            texto = f"{p['nombre']} {p['marca']} {p['modelo']}".lower()
            if termino in texto:
                encontrados.append((indice, p))
            actual = actual.next
            indice += 1

        self.cargar_tabla(encontrados)

    def actualizar(self):
        datos = []
        actual = self.lista.head
        indice = 0
        while actual:
            datos.append((indice, actual.producto))
            actual = actual.next
            indice += 1

        self.cargar_tabla(datos)
        self.actualizar_stats()
        self.dibujar_lista(True)

    def cargar_tabla(self, datos):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for indice, p in datos:
            prev = indice - 1 if indice > 0 else "NULL"
            next_ = indice + 1 if indice < self.lista.length - 1 else "NULL"
            self.tree.insert("", "end", values=(
                indice, p["nombre"], p["marca"], self.cop(p["precio"]),
                p["stock"], prev, next_
            ))

    def actualizar_stats(self):
        self.lbl_nodos.config(text=str(self.lista.length))
        self.lbl_stock.config(text=str(self.lista.stock_total()))
        self.lbl_head.config(text=self.lista.head.producto["nombre"] if self.lista.head else "NULL")
        self.lbl_tail.config(text=self.lista.tail.producto["nombre"] if self.lista.tail else "NULL")

    def mostrar_recorrido(self, adelante):
        self.dibujar_lista(adelante)

    def dibujar_lista(self, adelante=True):
        self.canvas.delete("all")
        nodos = self.lista.recorrido_adelante() if adelante else self.lista.recorrido_atras()

        if not nodos:
            self.canvas.create_text(450, 80, text="NULL", fill="#777f91",
                                    font=("Segoe UI", 12, "bold"))
            return

        x = 15
        y = 55
        ancho = 155
        alto = 75

        for i, nodo in enumerate(nodos):
            p = nodo.producto
            es_head = nodo == self.lista.head
            es_tail = nodo == self.lista.tail

            color = "#eeeafd" if es_head else "#fff4df" if es_tail else "#eef2f8"
            borde = "#6555c9" if es_head else "#e3a82b" if es_tail else "#cdd3df"

            self.canvas.create_rectangle(x, y, x+ancho, y+alto,
                                         fill=color, outline=borde, width=2)
            etiqueta = "HEAD" if es_head else "TAIL" if es_tail else f"NODO {i}"
            self.canvas.create_text(x+10, y+12, text=etiqueta,
                                   anchor="w", fill="#5b4bc4",
                                   font=("Segoe UI", 8, "bold"))
            self.canvas.create_text(x+10, y+36, text=p["nombre"],
                                   anchor="w", fill="#202638",
                                   font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x+10, y+57, text=f"prev ↔ next",
                                   anchor="w", fill="#737c8f",
                                   font=("Segoe UI", 8))

            if i < len(nodos)-1:
                if adelante:
                    self.canvas.create_line(x+ancho, y+37, x+ancho+48, y+37,
                                            fill="#8992a5", width=2,
                                            arrow=tk.LAST)
                else:
                    self.canvas.create_line(x+ancho, y+37, x+ancho+48, y+37,
                                            fill="#8992a5", width=2,
                                            arrow=tk.FIRST)
            x += ancho + 52

            if x > 900 and i < len(nodos)-1:
                # Mantener visible el inicio cuando hay muchos nodos.
                break

    @staticmethod
    def cop(valor):
        return f"${valor:,.0f}".replace(",", ".")


if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
