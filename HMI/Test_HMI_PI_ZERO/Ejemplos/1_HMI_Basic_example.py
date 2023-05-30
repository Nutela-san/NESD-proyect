import tkinter as tk
from tkinter import ttk

def write_text():
    #print(entrySTR.get())
    out_string_name.set(entrySTR.get())

#window
window = tk.Tk()
window.title('test hmi')
window.geometry('500x250')

#title
title_label = ttk.Label(master= window, text= 'kiubole',font= 'Arial 20')
title_label.pack()

#input field
input_frame = ttk.Frame(master=window)
entrySTR = tk.StringVar()
entry =  ttk.Entry(master=input_frame, textvariable=entrySTR)
button = ttk.Button(master=input_frame, text= 'Secret',command= write_text)

entry.pack(side= 'left' , padx= 10)         
button.pack(side='left')

input_frame.pack(pady= 10)

#out label
out_string_name = tk.StringVar()
out_label = ttk.Label(master=window, text='?' ,font='Arial 10',textvariable= out_string_name)
out_label.pack(pady=10)

#run 
window.mainloop()