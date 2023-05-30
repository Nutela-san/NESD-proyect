import tkinter as tk
from tkinter import ttk

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('NESD HMI') #titulo de la ventana


screen_w = int(window.winfo_screenwidth()*0.9) # Informacion de la pantalla
screen_h = int(window.winfo_screenheight()*0.9)

window.geometry(f'{screen_w}x{screen_h}+0+0')
window.resizable(False, False) # para no poder escalar las dimeciones de la ventana

#variables tkinter


#widgets
panel_pestanas = ttk.Notebook(window)


pestana_monitor = ttk.Frame(panel_pestanas, cursor= 'none', width= int(screen_w), height=int(screen_h*0.9))





#eventos


#enpaquetado 
panel_pestanas.pack(pady= 10)
pestana_monitor.pack(expand=True)

panel_pestanas.add(pestana_monitor, text= 'Monotor1')

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada


#window.update()


print("solo se imprime hasta despues de cerrar la ventana.")