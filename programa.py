import pickle
import getpass
import tkinter as tk
from tkinter import messagebox
import subprocess

def crear_cuenta():
    nombre_usuario = nombre_entry.get()
    contraseña = contraseña_entry.get()
    
    if nombre_usuario and contraseña:
        with open("cuentas.pkl", "rb") as archivo:
            try:
                datos = pickle.load(archivo)
                if nombre_usuario in datos:
                    messagebox.showwarning("Cuenta existente", "Ya existe una cuenta con ese nombre de usuario.")
                else:
                    datos[nombre_usuario] = contraseña
                    with open("cuentas.pkl", "wb") as archivo:
                        pickle.dump(datos, archivo)
                    messagebox.showinfo("Cuenta creada", "¡Cuenta creada exitosamente!")
                    ventana_registro.withdraw()  # Ocultar la ventana de registro
            except EOFError:
                datos = {nombre_usuario: contraseña}
                with open("cuentas.pkl", "wb") as archivo:
                    pickle.dump(datos, archivo)
                messagebox.showinfo("Cuenta creada", "¡Cuenta creada exitosamente!")
                ventana_registro.withdraw()  # Ocultar la ventana de registro
    else:
        messagebox.showwarning("Datos faltantes", "Debes ingresar un nombre de usuario y una contraseña.")

def ingresar():
    nombre_usuario = nombre_entry.get()
    contraseña = contraseña_entry.get()
    
    with open("cuentas.pkl", "rb") as archivo:
        try:
            datos = pickle.load(archivo)
            if nombre_usuario in datos and datos[nombre_usuario] == contraseña:
                messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido, {}!".format(nombre_usuario))
                ventana_inicio_sesion.withdraw()  # Ocultar la ventana de inicio de sesión
                realizar_tarea(nombre_usuario)  # Mostrar la ventana de la tarea adicional
            else:
                messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")
        except EOFError:
            messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")

def realizar_tarea(nombre_usuario):
    ventana_tarea = tk.Toplevel()  # Ventana secundaria para la tarea adicional
    ventana_tarea.title("Tarea Adicional")
    ventana_tarea.geometry("300x150")
    
    # Ejecutar un comando en la terminal
    comando = "echo 'Hola, {}!'".format(nombre_usuario)
    resultado = subprocess.check_output(comando, shell=True)
    resultado = resultado.decode("utf-8")

    resultado_label = tk.Label(ventana_tarea, text=resultado)
    resultado_label.pack()

# Verificar si existe una cuenta previa
try:
    with open("cuentas.pkl", "rb") as archivo:
        datos = pickle.load(archivo)
except FileNotFoundError:
    datos = {}

# Crear la ventana de registro si no hay cuentas registradas
if not datos:
    ventana_registro = tk.Tk()
    ventana_registro.title("Registro")
    ventana_registro.geometry("300x150")

    nombre_label = tk.Label(ventana_registro, text="Nombre de usuario:")
    nombre_label.pack()
    nombre_entry = tk.Entry(ventana_registro)
    nombre_entry.pack()

    contraseña_label = tk.Label(ventana_registro, text="Contraseña:")
    contraseña_label.pack()
    contraseña_entry = tk.Entry(ventana_registro, show="*")
    contraseña_entry.pack()

    registro_button = tk.Button(ventana_registro, text="Crear cuenta", command=crear_cuenta)
    registro_button.pack()

    ventana_registro.mainloop()

# Iniciar sesión
ventana_inicio_sesion = tk.Tk()
ventana_inicio_sesion.title("Inicio de sesión")
ventana_inicio_sesion.geometry("300x150")

nombre_label = tk.Label(ventana_inicio_sesion, text="Nombre de usuario:")
nombre_label.pack()
nombre_entry = tk.Entry(ventana_inicio_sesion)
nombre_entry.pack()

contraseña_label = tk.Label(ventana_inicio_sesion, text="Contraseña:")
contraseña_label.pack()
contraseña_entry = tk.Entry(ventana_inicio_sesion, show="*")
contraseña_entry.pack()

inicio_sesion_button = tk.Button(ventana_inicio_sesion, text="Iniciar sesión", command=ingresar)
inicio_sesion_button.pack()

ventana_inicio_sesion.mainloop()
