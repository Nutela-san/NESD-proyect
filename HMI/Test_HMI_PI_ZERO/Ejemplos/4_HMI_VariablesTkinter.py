import tkinter as tk
from tkinter import ttk

#           --- Variables incluidas en el paquete Tkinter----
# Las variables tkinter son varaibles dieñadas para trabajar en conjunto con los widgets
# de tal forma que estos puede modificar las varibles de forma facil. 
# Fundamentalmente estas variables son estructuras de datos las cuales tkinter puede
# aprovechar en conjunto con los widgets. 

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('Variables de Tkinter') #titulo de la ventana


#variables tkinter
texto_nota1 = tk.StringVar()
              #tk.IntVar()
              #tk.DoubleVar()
              #tk.BooleanVar()
texto_nota2 = tk.StringVar()
#widgets
nota1 = ttk.Label(master= window, text= 'un titulo inicial' , textvariable= texto_nota1)
text_in = ttk.Entry(master= window, textvariable= texto_nota1)

nota2 = ttk.Label(master= window, text= 'un titulo inicial' , textvariable= texto_nota2)
def func_btn():
    texto_nota2.set(text_in.get())
    texto_nota1.set('') # limpia el texto de la entrada usando la variable tk

boton = ttk.Button(master= window, text= 'puttext',command=func_btn)
#enpaquetado 
nota2.pack()
nota1.pack()
text_in.pack()
boton.pack()

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

print("solo se imprime hasta despues de cerrar la ventana.")


