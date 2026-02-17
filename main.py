import tkinter as tk
import tkinter.messagebox as messagebox
import bcrypt
from db import conectar
from admin import abrir_admin
from user import abrir_usuario


# ----------------- Ventana de registro -----------------
def registro_ventana():
    windows.withdraw()

    registro_win = tk.Toplevel()
    registro_win.title("Registro de Usuario")
    registro_win.state("zoomed")
    registro_win.configure(bg="#ecf0f1")

    # CONTENEDOR CENTRAL
    card = tk.Frame(registro_win, bg="white", padx=40, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="Registro de Usuario",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=(0, 20))

    def volver():
        registro_win.destroy()
        windows.deiconify()
        windows.state("zoomed")

    def registrar_usuario():
        usuario = nombre_registro_entry.get()
        contraseña_entry = contraseña_registro_entry.get()

        if usuario == "" or contraseña_entry == "":
            messagebox.showerror("Error", "Complete todos los campos.")
            return

        if any(char.isdigit() for char in usuario):
            messagebox.showerror("Error", "El nombre no puede contener números.")
            return

        hashed_password = bcrypt.hashpw(
            contraseña_entry.encode("utf-8"),
            bcrypt.gensalt()
        )

        rol_asignado = 2

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO usuarios (nombre, password_hash, rol_id)
                VALUES (%s, %s, %s)
            """, (usuario, hashed_password, rol_asignado))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            volver()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # CAMPOS
    
    tk.Label(card, text="Nombre de usuario", bg="white").pack(anchor="w")
    nombre_registro_entry = tk.Entry(card, width=30)
    nombre_registro_entry.pack(pady=8)

    tk.Label(card, text="Contraseña", bg="white").pack(anchor="w")
    contraseña_registro_entry = tk.Entry(card, width=30, show="*")
    contraseña_registro_entry.pack(pady=8)

    # BOTONES
    tk.Button(
        card,
        text="Registrarse",
        width=25,
        bg="#3498db",
        fg="white",
        bd=0,
        command=registrar_usuario
    ).pack(pady=(20, 8))

    tk.Button(
        card,
        text="Volver",
        width=25,
        bg="#7f8c8d",
        fg="white",
        bd=0,
        command=volver
    ).pack()


# ----------------- LOGIN -----------------
def login():
    nombre = nombre_entry.get()
    contraseña = contraseña_entry.get()

    if nombre == "" or contraseña == "":
        messagebox.showerror("Error", "Complete todos los campos.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT password_hash, rol_id
            FROM usuarios
            WHERE nombre = %s
        """, (nombre,))

        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if data is None:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        stored_password_hash, rol = data
        stored_password_hash = bytes(stored_password_hash)

        if bcrypt.checkpw(
            contraseña.encode("utf-8"),
            stored_password_hash
        ):
            windows.withdraw()

            nombre_entry.delete(0, tk.END)
            contraseña_entry.delete(0, tk.END)

            if int(rol) == 2:
                abrir_usuario(nombre, windows)
                return

            if int(rol) == 1:
                abrir_admin(nombre, windows)
                return

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------------- VENTANA PRINCIPAL -----------------
windows = tk.Tk()
windows.title("Tienda")
windows.state("zoomed")
windows.configure(bg="#ecf0f1")

# CONTENEDOR LOGIN
login_card = tk.Frame(windows, bg="white", padx=50, pady=50)
login_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    login_card,
    text="Bienvenido a la Tienda",
    font=("Arial", 24, "bold"),
    bg="white"
).pack(pady=(0, 10))

tk.Label(
    login_card,
    text="Iniciar Sesión",
    font=("Arial", 16),
    bg="white",
    fg="gray"
).pack(pady=(0, 20))

# CAMPOS
imagen_user = tk.PhotoImage(file="image/user.jpg")
tk.Label(login_card, image=imagen_user, bg="white").pack(pady=10)

tk.Label(login_card, text="Usuario", bg="white").pack(anchor="w")
nombre_entry = tk.Entry(login_card, width=30)
nombre_entry.pack(pady=8)

tk.Label(login_card, text="Contraseña", bg="white").pack(anchor="w")
contraseña_entry = tk.Entry(login_card, width=30, show="*")
contraseña_entry.pack(pady=8)

# BOTONES
tk.Button(
    login_card,
    text="Iniciar Sesión",
    width=28,
    height=2,
    bg="#2ecc71",
    fg="white",
    bd=0,
    command=login
).pack(pady=(20, 8))

tk.Button(
    login_card,
    text="Registrarse",
    width=28,
    height=2,
    bg="#f39c12",
    fg="white",
    bd=0,
    command=registro_ventana
).pack(pady=6)

tk.Button(
    login_card,
    text="Salir",
    width=28,
    height=2,
    bg="#e74c3c",
    fg="white",
    bd=0,
    command=windows.quit
).pack(pady=6)

windows.mainloop()
