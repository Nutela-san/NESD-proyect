#import serial
#import tkinter as tk
#from tkinter import ttk
#from serial.tools import list_ports
#
#puerto_seleccionado = None
#ser = None
#
#def seleccionar_puerto(event):
#    global puerto_seleccionado, ser
#
#    if ser is not None and ser.is_open:
#        ser.close()
#
#    puerto_seleccionado = combobox.get()
#
#    try:
#        ser = serial.Serial(puerto_seleccionado, 115200)
#        etiqueta.config(text="Conectado al puerto: " + puerto_seleccionado)
#        ventana.after(100, leer_puerto_serial)
#    except serial.SerialException:
#        etiqueta.config(text="Error al conectar al puerto " + puerto_seleccionado)
#
#def leer_puerto_serial():
#    global ser
#
#    if ser is None or not ser.is_open:
#        return
#
#    try:
#        if ser.in_waiting > 0:
#            dato = ser.readline().strip().decode()
#            etiqueta.config(text="Valor: " + dato)
#    except serial.SerialException:
#        etiqueta.config(text="Error al leer el puerto serial")
#
#    ventana.after(100, leer_puerto_serial)
#
#def enviar_datos():
#    global ser
#
#    if ser is None or not ser.is_open:
#        etiqueta.config(text="No hay conexión establecida")
#        return
#
#    texto = texto_out.get() + '\n'
#    ser.write(texto.encode())
#    texto_out.set('')
#
#
#ventana = tk.Tk()
#ventana.title("Lectura y Escritura en Puerto Serial")
#ventana.geometry("300x250")
#
#etiqueta = tk.Label(ventana, text="Seleccione un puerto serial")
#etiqueta.pack(pady=10)
#
#puertos_disponibles = [port.device for port in list_ports.comports()]
#combobox = ttk.Combobox(ventana, values=puertos_disponibles)
#combobox.bind("<<ComboboxSelected>>", seleccionar_puerto)
#combobox.pack()
#
#etiqueta_valor = tk.Label(ventana, text="Valor: ")
#etiqueta_valor.pack(pady=10)
#
#etiqueta_entrada = tk.Label(ventana, text="Texto a enviar:")
#etiqueta_entrada.pack(pady=5)
#
#texto_out = tk.StringVar()
#entrada_texto = tk.Entry(ventana, width=20 , textvariable= texto_out)
#entrada_texto.pack()
#
#boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_datos)
#boton_enviar.pack(pady=10)
#
#ventana.bind('<Return>', lambda event: enviar_datos())
#
#ventana.mainloop()
#if ser is not None:
#    ser.close()

#import serial
#import tkinter as tk
#from tkinter import ttk
#from serial.tools import list_ports
#
#puerto_seleccionado = None
#ser = None
#
#def seleccionar_puerto(event):
#    global puerto_seleccionado, ser
#
#    if ser is not None and ser.is_open:
#        ser.close()
#
#    puerto_seleccionado = combobox.get()
#
#    try:
#        ser = serial.Serial(puerto_seleccionado, 115200)
#        etiqueta.config(text="Conectado al puerto: " + puerto_seleccionado)
#        ventana.after(100, leer_puerto_serial)
#        entrada_texto.config(state=tk.NORMAL)  # Habilitar entrada de texto
#        boton_enviar.config(state=tk.NORMAL)  # Habilitar botón de enviar
#    except serial.SerialException:
#        etiqueta.config(text="Error al conectar al puerto " + puerto_seleccionado)
#        entrada_texto.config(state=tk.DISABLED)  # Deshabilitar entrada de texto
#        boton_enviar.config(state=tk.DISABLED)  # Deshabilitar botón de enviar
#
#def leer_puerto_serial():
#    global ser
#
#    if ser is None or not ser.is_open:
#        return
#
#    try:
#        if ser.in_waiting > 0:
#            dato = ser.readline().strip().decode()
#            etiqueta.config(text="Valor: " + dato)
#    except serial.SerialException:
#        etiqueta.config(text="Error al leer el puerto serial")
#
#    ventana.after(100, leer_puerto_serial)
#
#def enviar_datos():
#    global ser
#
#    if ser is None or not ser.is_open:
#        etiqueta.config(text="No hay conexión establecida")
#        return
#
#    texto = texto_out.get() + '\n'
#    ser.write(texto.encode())
#    texto_out.set('')
#
#ventana = tk.Tk()
#ventana.title("Lectura y Escritura en Puerto Serial")
#ventana.geometry("300x250")
#
#etiqueta = tk.Label(ventana, text="Seleccione un puerto serial")
#etiqueta.pack(pady=10)
#
#puertos_disponibles = [port.device for port in list_ports.comports()]
#combobox = ttk.Combobox(ventana, values=puertos_disponibles)
#combobox.bind("<<ComboboxSelected>>", seleccionar_puerto)
#combobox.pack()
#
#etiqueta_valor = tk.Label(ventana, text="Valor: ")
#etiqueta_valor.pack(pady=10)
#
#etiqueta_entrada = tk.Label(ventana, text="Texto a enviar:")
#etiqueta_entrada.pack(pady=5)
#
#texto_out = tk.StringVar()
#entrada_texto = tk.Entry(ventana, width=20, textvariable=texto_out, state=tk.DISABLED)  # Inicialmente deshabilitada
#entrada_texto.pack()
#
#boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_datos, state=tk.DISABLED)  # Inicialmente deshabilitado
#boton_enviar.pack(pady=10)
#
#ventana.bind('<Return>', lambda event: enviar_datos())
#
#ventana.mainloop()
#
#if ser is not None:
#    ser.close()

#import serial
#import tkinter as tk
#from tkinter import ttk
#from serial.tools import list_ports
#
## Función para extraer el valor numérico del comando recibido
#def obtener_valor_comando(comando):
#    try:
#        valor = int(comando.split('=')[1].strip())
#        return valor
#    except (ValueError, IndexError):
#        return None
#
## Función para leer el puerto serial
#def leer_puerto_serial():
#    global ser
#
#    if ser is None or not ser.is_open:
#        return
#
#    try:
#        if ser.in_waiting > 0:
#            comando = ser.readline().strip().decode()
#            valor = obtener_valor_comando(comando)
#
#            if valor is not None:
#                barra_carga['value'] = valor
#    except serial.SerialException:
#        pass
#
#    ventana.after(100, leer_puerto_serial)
#
## Crear instancia de Serial
#ser = serial.Serial('COM14', 115200)
#
#ventana = tk.Tk()
#ventana.title("Control de Nivel")
#ventana.geometry("300x150")
#
#barra_label = tk.Label(ventana, text="Nivel:")
#barra_label.pack(pady=10)
#
#barra_carga = ttk.Progressbar(ventana, orient=tk.HORIZONTAL, length=200, mode='determinate')
#barra_carga.pack(pady=10)
#
#ventana.after(100, leer_puerto_serial)  # Iniciar la lectura del puerto serial
#
#ventana.mainloop()
#
## Cerrar el puerto serial
#ser.close()

import tkinter as tk
from tkinter import ttk
from serial.tools import list_ports
import serial

class ConexionSerialFrame(tk.Frame):
    def __init__(self, parent, etiqueta_texto):
        super().__init__(parent)
        self.parent = parent
        self.puertos_disponibles = []

        self.etiqueta_texto = etiqueta_texto

        self.label = tk.Label(self, text="Conexión Serial")
        self.label.pack(pady=10)

        self.combobox = ttk.Combobox(self, state="readonly")
        self.combobox.pack(pady=10)

        self.boton_conectar = ttk.Button(self, text="Conectar", command=self.conectar)
        self.boton_conectar.pack(pady=10)

    def obtener_puertos_disponibles(self):
        self.puertos_disponibles = [port.device for port in list_ports.comports()]
        self.combobox["values"] = self.puertos_disponibles

    def conectar(self):
        puerto_seleccionado = self.combobox.get()
        if puerto_seleccionado:
            try:
                self.ser = serial.Serial(puerto_seleccionado, 115200)
                self.etiqueta_texto.config(state="normal")
                self.etiqueta_texto.delete("1.0", tk.END)
                self.boton_conectar.config(state="disabled")
                self.combobox.config(state="disabled")
                self.etiqueta_texto.insert(tk.END, "Conexión establecida con el puerto serial: " + puerto_seleccionado + "\n")
                self.leer_puerto_serial()
            except serial.SerialException:
                self.etiqueta_texto.insert(tk.END, "Error al conectar al puerto " + puerto_seleccionado + "\n")

    def leer_puerto_serial(self):
        if self.ser is None or not self.ser.is_open:
            return

        try:
            if self.ser.in_waiting > 0:
                dato = self.ser.readline().strip().decode()
                self.etiqueta_texto.insert(tk.END, dato + "\n")
        except serial.SerialException:
            self.etiqueta_texto.insert(tk.END, "Error al leer el puerto serial\n")

        self.parent.after(100, self.leer_puerto_serial)


# Ejemplo de uso
ventana = tk.Tk()
ventana.title("Ejemplo de Conexión Serial")
ventana.geometry("400x400")

etiqueta_texto = tk.Text(ventana, state="disabled", height=10, width=40)
etiqueta_texto.pack(pady=20)

frame_conexion_serial = ConexionSerialFrame(ventana, etiqueta_texto)
frame_conexion_serial.pack()

frame_conexion_serial.obtener_puertos_disponibles()

ventana.mainloop()
if frame_conexion_serial.ser is not None:
    frame_conexion_serial.ser.close()
