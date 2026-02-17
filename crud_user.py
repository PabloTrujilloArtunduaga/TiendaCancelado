import tkinter as tk
import tkinter.messagebox as messagebox
import bcrypt
from db import conectar
import psycopg2


def crud_usuario(parent, refrescar_tabla):
    user_id = None
    # ===== CARD CONTENEDORA =====
    container = tk.Frame(parent, bg="white", bd=1, relief="solid")
    container.pack(fill="x", padx=30, pady=(10, 25))

    # ===== HEADER =====
    header = tk.Frame(container, bg="#f1f5f9")
    header.pack(fill="x")

    tk.Label(
        header,
        text="Formulario de Usuario",
        bg="#f1f5f9",
        fg="#1e293b",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(15, 5))

    tk.Label(
        header,
        text="Crear, editar o eliminar usuarios",
        bg="#f1f5f9",
        fg="#64748b",
        font=("Segoe UI", 10)
    ).pack(pady=(0, 15))

    # ===== FORM =====
    form = tk.Frame(container, bg="white")
    form.pack(fill="x", padx=30, pady=20)

    label_cfg = {"bg": "white", "fg": "#374151", "font": ("Segoe UI", 11)}
    entry_cfg = {"font": ("Segoe UI", 10), "bd": 1, "relief": "solid"}

    form.grid_columnconfigure(1, weight=1)
    form.grid_columnconfigure(3, weight=1)

    def campo(texto, fila, col, show=None):
        tk.Label(form, text=texto, **label_cfg)\
            .grid(row=fila, column=col, sticky="w", pady=(6, 2))
        entry = tk.Entry(form, show=show, **entry_cfg)
        entry.grid(row=fila + 1, column=col, sticky="ew",
                   padx=(0, 20), pady=(0, 10))
        return entry

    nombre = campo("Nombre", 0, 0)
    password = campo("Contraseña", 0, 2, show="*")
    rol = campo("Rol ID", 2, 0)

    # ===== FUNCIONES =====
    def cargar_datos(valores):
        nonlocal user_id
        user_id = valores[0]  

        nombre.delete(0, tk.END)
        rol.delete(0, tk.END)
        password.delete(0, tk.END)

        nombre.insert(0, valores[1])  
        rol.insert(0, valores[2])  

    def limpiar():
        nonlocal user_id
        user_id = None
        nombre.delete(0, tk.END)
        password.delete(0, tk.END)
        rol.delete(0, tk.END)

    def crear_user():
        if nombre.get().strip() == "" or password.get().strip() == "" or rol.get().strip() == "":
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return

        try:
            rol_id = int(rol.get())
        except ValueError:
            messagebox.showerror("Error", "Rol inválido")
            return

        hashed = bcrypt.hashpw(password.get().encode(), bcrypt.gensalt()).decode()

        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO usuarios (nombre, password_hash, rol_id)
                        VALUES (%s, %s, %s)
                    """, (nombre.get(), hashed, rol_id))
                    conn.commit()
            refrescar_tabla()
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
            limpiar()
        except psycopg2.Error as e:
            messagebox.showerror("Error", str(e))

    def editar_user():
        if user_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return
        try:
            rol_id = int(rol.get())
        except ValueError:
            messagebox.showerror("Error", "Rol inválido")
            return

        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    if password.get().strip():
                        hashed = bcrypt.hashpw(
                            password.get().encode(), bcrypt.gensalt()
                        ).decode()
                        cur.execute("""
                            UPDATE usuarios
                            SET nombre=%s, password_hash=%s, rol_id=%s
                            WHERE id=%s
                        """, (nombre.get(), hashed, rol_id, user_id))
                    else:
                        cur.execute("""
                            UPDATE usuarios
                            SET nombre=%s, rol_id=%s
                            WHERE id=%s
                        """, (nombre.get(), rol_id, user_id))
                    conn.commit()
            refrescar_tabla()
            messagebox.showinfo("Éxito", "Usuario actualizado")

        except psycopg2.Error as e:
            messagebox.showerror("Error", str(e))

    def eliminar_user():
        nonlocal user_id
        if user_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            return
        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
                    conn.commit()
            refrescar_tabla()
            messagebox.showinfo("Éxito", "Usuario eliminado")
            limpiar()
        except psycopg2.Error as e:
            messagebox.showerror("Error", str(e))
    # ===== BOTONES =====
    botones = tk.Frame(container, bg="white")
    botones.pack(pady=(10, 20))

    btn_cfg = {"width": 12, "font": ("Segoe UI", 11, "bold"), "bd": 0}

    tk.Button(botones, text="Crear", bg="#22c55e",
              fg="white", command=crear_user, **btn_cfg).grid(row=0, column=0, padx=6)

    tk.Button(botones, text="Editar", bg="#3b82f6",
              fg="white", command=editar_user, **btn_cfg).grid(row=0, column=1, padx=6)

    tk.Button(botones, text="Eliminar", bg="#ef4444",
              fg="white", command=eliminar_user, **btn_cfg).grid(row=0, column=2, padx=6)

    tk.Button(botones, text="Limpiar", bg="#64748b",
              fg="white", command=limpiar, **btn_cfg).grid(row=0, column=3, padx=6)

    return cargar_datos
