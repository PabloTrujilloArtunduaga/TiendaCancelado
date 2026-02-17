import psycopg2
from tkinter import messagebox

def conectar():
    try:
        conn = psycopg2.connect(
            dbname="tienda",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la BD:\n{e}")