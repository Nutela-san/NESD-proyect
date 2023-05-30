import tkinter as tk
from tkinter import ttk

#       ---Widgets---
# Los widgets son los componentes basicos para contruir la interfaz en tkinter
# , engeneral para cualquier framework para programar GUI's
#  
#En tkinter existen dos familas para widgets, los de familia tkinter(tk, originales y 
# desactualizados) y los familia ttk(nuevos)
# 

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk

window.title('La super ventana') #titulo de la ventana
window.geometry('800x500')  # determina el tamaño de la ventana defomar gemetry('anchoxalto')
                            # los tamaños son en pixeles

#creacion de widgets (familia tk)

area_texto = tk.Text(master=window) #para area de texto, Text(master = 'lugar al que petenece el widget')
                                    #Nota, esto solo crea el widget pero no indica si lo debe desplegar
                                    #en la ventana de la interfaz o en el lugar designado como master


#creacion de widgets (familia ttk)

nota_widget = ttk.Label(master=window, text= 'Noto que notas que esto es una nota')

cuadro_texto = ttk.Entry(master= window)

def funcion_boton(): 
    print('presionaste el boton')

boton = ttk.Button(master= window , text= 'EL BOTON' , command= funcion_boton)


#     --creando la disposicion de los widgets en la interfaz con el metodo pack()--
# el metodo pack deslpliega los widgets de arriba hacia abajo (por defecto) , y el orden en
# el que se empaquetan los widgets afecta en su disposicion

nota_widget.pack()
area_texto.pack() #despliega el widget en el master
cuadro_texto.pack()
boton.pack()


#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

print("solo se imprime hasta despues de cerrar la ventana.")