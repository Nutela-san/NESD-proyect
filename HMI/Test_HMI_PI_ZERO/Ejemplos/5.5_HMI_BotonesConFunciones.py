import tkinter as tk
from tkinter import ttk

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('BOTONES') #titulo de la ventana
#window.geometry('600x400')


#variables tkinter
var_text = tk.StringVar(value='text')

#widgets
text_in =  ttk.Entry(window, textvariable= var_text)

def btn_func(parametro): # el primer metodo se manda a llamar en una funcin lambda
  print(parametro.get())

def btn_func2(parametro):   # el segundo metodo neceista de una funcion interna que se retorna
  def funcion_interna():
      print(parametro.get())
  return funcion_interna

boton = ttk.Button(window, text='PRINT', command= lambda: btn_func(var_text))
boton2= ttk.Button(window, text='PRINT', command= btn_func2(var_text))
#enpaquetado 

text_in.pack()
boton.pack()
boton2.pack()

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

print("solo se imprime hasta despues de cerrar la ventana.")