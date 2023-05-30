import tkinter as tk
from tkinter import ttk

#window config
window = tk.Tk()
window.title('Grid')
window.geometry('600x400')

#widgets 
label1 = ttk.Label(window,text= 'Label 1', background= 'red' , anchor= 'center')
label2 = ttk.Label(window,text= 'Label 2', background= 'blue',anchor= 'center')
label3 = ttk.Label(window,text= 'Label 3', background= 'green',anchor= 'center')
label4 = ttk.Label(window,text= 'Label 4', background= 'yellow', anchor= 'e')

button1 = ttk.Button(window, text= 'Button 1')
button2 = ttk.Button(window, text= 'Button 2')

entry = ttk.Entry(window)

#defined a grid
window.columnconfigure((0,1,2),weight= 1)
window.columnconfigure(3,weight=10)

window.rowconfigure(0,weight=2)
window.rowconfigure(1,weight=1)


#place widgets  
                            #sticky= n(north)s(sur)e(esth)w(westh)
label1.grid(row=0, column=0, sticky='nsew')
label2.grid(row=0, column=1, sticky='ew')
label3.grid(row=0, column=2, sticky='sew')
label4.grid(row=0,column=3,sticky='new')

button1.grid(row=1, column=0, sticky='sew')
button2.grid(row=1, column=3, sticky= 'nsew')

entry.grid(row=1,column=1, columnspan=2, sticky='ew')

#run 
window.mainloop()   