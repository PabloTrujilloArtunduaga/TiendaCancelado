import tkinter as tk
import tkinter.messagebox as messagebox
from db import conectar
import psycopg2






def crud_producto(parent, refrescar_tabla):
    producto_id = None

    # ===== CARD CONTENEDORA =====
    container = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )
    container.pack(fill="x", padx=30, pady=(10, 25))

    # ===== HEADER =====
    header = tk.Frame(container, bg="#f1f5f9")
    header.pack(fill="x")

    tk.Label(
        header,
        text="Formulario de Producto",
        bg="#f1f5f9",
        fg="#1e293b",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(15, 5))

    tk.Label(
        header,
        text="Crear, editar o eliminar productos",
        bg="#f1f5f9",
        fg="#64748b",
        font=("Segoe UI", 10)
    ).pack(pady=(0, 15))

    # ===== FORM =====
    form = tk.Frame(container, bg="white")
    form.pack(fill="x", padx=30, pady=20)

    label_cfg = {
        "bg": "white",
        "fg": "#374151",
        "font": ("Segoe UI", 11)
    }

    entry_cfg = {
        "font": ("Segoe UI", 10),
        "bd": 1,
        "relief": "solid"
    }

    # Grid responsive
    form.grid_columnconfigure(1, weight=1)
    form.grid_columnconfigure(3, weight=1)

    def campo(texto, fila, col):
        tk.Label(form, text=texto, **label_cfg)\
            .grid(row=fila, column=col, sticky="w", pady=(6, 2))
        entry = tk.Entry(form, **entry_cfg)
        entry.grid(row=fila + 1, column=col, sticky="ew", padx=(0, 20), pady=(0, 10))
        return entry

    nombre = campo("Nombre", 0, 0)
    categoria = campo("Categoría", 0, 2)

    descripcion = campo("Descripción", 2, 0)
    proveedor = campo("Proveedor", 2, 2)

    precio = campo("Precio", 4, 0)
    stock = campo("Stock", 4, 2)

    # ---------- FUNCIONES (NO TOCADAS) ----------
    def cargar_datos(valores):
        nonlocal producto_id
        producto_id = valores[0]

        nombre.delete(0, tk.END)
        descripcion.delete(0, tk.END)
        categoria.delete(0, tk.END)
        precio.delete(0, tk.END)
        stock.delete(0, tk.END)
        proveedor.delete(0, tk.END)

        nombre.insert(0, valores[1])
        descripcion.insert(0, valores[2])
        categoria.insert(0, valores[3])
        precio.insert(0, valores[4])
        stock.insert(0, valores[5])
        proveedor.insert(0, valores[6])

    def editar_producto():
        nonlocal producto_id
        if producto_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla para editar")
            return
        if nombre.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo producto está vacío")
            return
        if descripcion.get().strip() == "":
            messagebox.showwarning("Advertencia", "Descripción vacía")
            return
        if categoria.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo categoría está vacío")
            return
        if precio.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo precio está vacío")
            return
        if stock.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo cantidad está vacío")
            return
        if proveedor.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo proveedor está vacío")
            return
        try:
            precio_valor = float(precio.get())
            stock_valor = int(stock.get())
        except ValueError:
            messagebox.showerror("Error", "Precio o stock inválidos")
            return
        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE productos
                        SET nombre=%s, descripcion=%s, categoria=%s,
                            precio=%s, stock=%s, proveedor=%s
                        WHERE id_producto=%s
                    """, (
                        nombre.get(), descripcion.get(), categoria.get(),
                        precio_valor, stock_valor, proveedor.get(), producto_id
                    ))
                    conn.commit()
            refrescar_tabla()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"{e}")

    def limpiar():
        nombre.delete(0, tk.END)
        descripcion.delete(0, tk.END)
        categoria.delete(0, tk.END)
        precio.delete(0, tk.END)
        stock.delete(0, tk.END)
        proveedor.delete(0, tk.END)

    def crear_producto():
        if nombre.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo producto está vacío")
            return
        if descripcion.get().strip() == "":
            messagebox.showwarning("Advertencia", "Descripción vacía")
            return
        if categoria.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo categoría está vacío")
            return
        if precio.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo precio está vacío")
            return
        if stock.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo cantidad está vacío")
            return
        if proveedor.get().strip() == "":
            messagebox.showwarning("Advertencia", "El campo proveedor está vacío")
            return
        try:
            precio_valor = float(precio.get())
            stock_valor = int(stock.get())
        except ValueError:
            messagebox.showerror("Error", "Precio o stock inválidos")
            return
        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO productos
                        (nombre, descripcion, categoria, precio, stock, proveedor)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """, (
                        nombre.get(), descripcion.get(), categoria.get(),
                        precio_valor, stock_valor, proveedor.get()
                    ))
                    conn.commit()
            refrescar_tabla()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            limpiar()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"{e}")

    def eliminar_producto():
        nonlocal producto_id
        if producto_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla para eliminar")
            return
        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM productos WHERE id_producto=%s", (producto_id,))
                    conn.commit()
            refrescar_tabla()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            limpiar()
            producto_id = None
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"{e}")

    # ===== BOTONES =====
    botones = tk.Frame(container, bg="white")
    botones.pack(pady=(10, 20))

    btn_cfg = {
        "width": 12,
        "font": ("Segoe UI", 11, "bold"),
        "bd": 0,
        "cursor": "hand2"
    }

    tk.Button(botones, text="Crear", bg="#22c55e", fg="white",
              command=crear_producto, **btn_cfg).grid(row=0, column=0, padx=6)

    tk.Button(botones, text="Editar", bg="#3b82f6", fg="white",
              command=editar_producto, **btn_cfg).grid(row=0, column=1, padx=6)

    tk.Button(botones, text="Eliminar", bg="#ef4444", fg="white",
              command=eliminar_producto, **btn_cfg).grid(row=0, column=2, padx=6)

    tk.Button(botones, text="Limpiar", bg="#64748b", fg="white",
              command=limpiar, **btn_cfg).grid(row=0, column=3, padx=6)

    return cargar_datos
