import tkinter as tk
from tkinter import ttk


def funcion_boton():
    #obteneidno al informacion de la entrada del texto
    var_texto =entrada_texto.get()
    print("la entrada de texto se desabilito")
    #acualiazando la nota
    nota.configure(text= var_texto)
    #nota.config(text='otro texto')
    #nota['text'] = 'otro texto'
    #todos funcionan igual
    entrada_texto.configure(state= 'disable')
    

def funcion_boton2():
    entrada_texto.configure(state= 'enable')
    print('estamos de vuelta')
    nota['text'] = 'estamos de vuelta'


#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk

window.title('obteniendo y seteando widgets') #titulo de la ventana
window.geometry('400x100')  # determina el tamaño de la ventana defomar gemetry('anchoxalto')
                            # los tamaños son en pixeles

#           ---widgets---

# cada widget tiene el metodo config, que sirve para actualizar los datos en el widget7
# tambien cada widget posee el metodo state, que e suna funcion boleaana para habilitar y desabilitar el widget

nota = ttk.Label(master= window, text= 'UN TEXTO')
entrada_texto = ttk.Entry(master= window)
boton = ttk.Button(master=window, text= 'texto de boton', command= funcion_boton)
boton2 = ttk.Button(master=window, text= 'rehabilitar texto', command= funcion_boton2)



#enpaquetando 

nota.pack()
entrada_texto.pack()
boton.pack()
boton2.pack()

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

print("solo se imprime hasta despues de cerrar la ventana.")