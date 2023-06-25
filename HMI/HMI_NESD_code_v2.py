import tkinter as tk
from tkinter import ttk

#----------------------- creacion de la ventana -------------------------------------
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('NESD HMI') #titulo de la ventana

screen_w = 1280#int(window.winfo_screenwidth()*0.98) # Informacion de la pantalla
screen_h = 700#int(window.winfo_screenheight()*0.9)

window.geometry(f'{screen_w}x{screen_h}+0+0')
window.resizable(False, False) # para no poder escalar las dimeciones de la ventana

paleta_color = ('#ff1d44',  #rojo
                '#f0f6b9',  #amarillo
                '#9fd9b3',  #verde
                '#3ea3af',  #azul
                '#81657e')  #morado
#----------------------- widgets Plantillas-------------------------------------

class Tank_monitor(ttk.Frame):
  def __init__(self, parent, size, tank_number,level, SeedOuputs):  
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    self.tank_number = max(1,tank_number)
    self.level = level
    self.SeedOutputs = (SeedOuputs[0], SeedOuputs[1])

    #-- configurando grid --
    self.config(width= size[0])
    self.config(height= size[1])
    self.columnconfigure((0,1), weight= 1)
    self.rowconfigure((0,3), weight=1)
    self.rowconfigure(2,weight=2)
    self.rowconfigure(1, weight=7)

    #--Elementos (widgets) del monitor de tolva
    self.tank_size = (int(size[0]),int(size[1]*0.75)) # tamaño del dibujo de la tolva
    self.tank_draw =  tk.Canvas(self, 
                                width= self.tank_size[0], height= self.tank_size[1],
                                background= '#F0F0F0')
    text_size = int(size[1]*0.05)
    self.tank_label = ttk.Label(self, text=f'TOLVA {self.tank_number}', font= f'Arial {text_size} bold')
    text_size = int(size[1]*0.025)
    self.SeedOut1_label = ttk.Label(self, text=f'SALIDA {(self.tank_number*2)-1}', anchor='center', font= f'Arial {text_size} bold')
    self.SeedOut2_label = ttk.Label(self, text=f'SALIDA {(self.tank_number*2)}', anchor='center', font= f'Arial {text_size} bold')
    self.Seed_Count1 = ttk.Label(self, text= f'{0} semillas' ,anchor= 'center', relief= 'groove',font= f'Arial {text_size}') #, state='readonly')
    self.Seed_Count2 = ttk.Label(self, text= f'{0} semillas' ,anchor= 'center', relief= 'groove',font= f'Arial {text_size}') #, state='readonly')

    #-- empaquedato en grid
    self.tank_label.grid(row=0 , column=0, columnspan=2)
    self.tank_draw.grid(row=1, column=0, columnspan=2)
    self.Seed_Count1.grid(row=2,column=0, sticky= 'nswe')
    self.Seed_Count2.grid(row=2,column=1, sticky= 'nswe')
    self.SeedOut1_label.grid(row=3,column=0, sticky= 'nswe')
    self.SeedOut2_label.grid(row=3,column=1, sticky= 'nswe')

    self.update_level()
  
  def update_level(self):
    tank = self.tank_draw
    tank_canvas_size_o = (self.tank_size[0], self.tank_size[1])
    tank.delete(tk.ALL)
    tank_line_wight = 5
    offSet = tank_line_wight*2
    tank_offset = tank_line_wight
    tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

    tank_points = ( (tank_offset,tank_offset),
                    (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset))

    

    self.level.set(max(0,min(self.level.get(),100)))
    self.Seed_Count1.config(text= f'{self.SeedOutputs[0].get()} semillas')
    self.Seed_Count2.config(text= f'{self.SeedOutputs[1].get()} semillas')

    if tank.cget('state') != 'disabled':
      tank.create_polygon(*tank_points, fill='grey', outline='black', width= tank_line_wight)
      if(self.level.get() >= 90):
        tank_line_wight = 8
        offSet = tank_line_wight*2
        tank_offset = tank_line_wight
        tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

        fill_points = ( (tank_offset,tank_offset),
                        (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset))
        tank.create_polygon(*fill_points, fill='green')
      elif (self.level.get() >=60):
        tank_line_wight = 8
        offSet = tank_line_wight*2
        tank_offset = tank_line_wight
        tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

        fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.2)),
                        (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.2)))
        tank.create_polygon(*fill_points, fill='green')
      elif (self.level.get() >=40):
        tank_line_wight = 8
        offSet = tank_line_wight*2
        tank_offset = tank_line_wight
        tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

        fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.4)),
                        (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.4)))
        tank.create_polygon(*fill_points, fill='yellow')
      elif (self.level.get() >=30):
        tank_line_wight = 8
        offSet = tank_line_wight*2
        tank_offset = tank_line_wight
        tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

        fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.55)),
                        (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.55)))
        tank.create_polygon(*fill_points, fill='orange')
      elif (self.level.get() <30):
        tank_line_wight = 8
        offSet = tank_line_wight*2|1
        tank_offset = tank_line_wight
        tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

        fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                        (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                        (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)))
        tank.create_polygon(*fill_points, fill='red')
      tank.create_text((int(tank_canvas_size[0]/2),int(tank_canvas_size[1]*3/8)),
                      text=f' {self.level.get()}%', fill='black', font= 'Arial 80 bold')
    else:
      tank.create_polygon(*tank_points, fill='#C9C9C9', outline='grey', width= tank_line_wight)
      tank.create_text((int(tank_canvas_size[0]/2),int(tank_canvas_size[1]*3/8)),
                        text='   SIN\nTOLVA', fill='grey', font= 'Arial 60 bold',anchor='center')
    
    self.parent.after(100, self.update_level)
  
  def disabled_monitor(self):
    self.tank_label.config(state='disabled')
    self.tank_draw.config(state='disabled')
    self.Seed_Count1.config(state='disabled')
    self.Seed_Count2.config(state='disabled')
    self.SeedOut1_label.config(state='disabled')
    self.SeedOut2_label.config(state='disabled')

  def enable_monitor(self):
    self.tank_label.config(state='normal')
    self.tank_draw.config(state='normal')
    self.Seed_Count1.config(state='normal')
    self.Seed_Count2.config(state='normal')
    self.SeedOut1_label.config(state='normal')
    self.SeedOut2_label.config(state='normal')

class Odometry_monitor(ttk.Frame):
  def __init__(self, parent, odometry_data):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    self.tractor_img = tk.PhotoImage(file='resources/tractor_odometri_300.png',width=300)
    self.odometry_data = odometry_data
    #-- configurando grid --
    self.columnconfigure((0,1), weight=1)
    self.rowconfigure((0,2,3,4,5),weight=1)
    self.rowconfigure(1,weight=2)

    #--Elementos (widgets) --
    font_size = 30 #self.grid_info()

    self.monitor_title = ttk.Label(self, text= 'ODOMETRÍA' , font= f'Arial {font_size} bold' , anchor='center')
    self.tractor_draw = ttk.Label(self,image= self.tractor_img , anchor='center')
    self.tractor_draw.config(relief= 'groove') # marca el cuadro de label para imagen

    font_size = 30 #self.grid_info()
    self.speed_title = ttk.Label(self, text= 'Velocidad de Siembra', font= f'Arial {font_size} bold' , anchor='center' )
    self.speed_unit  = ttk.Label(self, text= 'Km/hr', font= f'Arial {font_size}' , anchor='center' )
    self.speed_var_text = ttk.Label(self, text= f'{self.odometry_data[0].get()}',  font= f'Arial {font_size}' , 
                                    anchor='center' , relief='groove')

    self.distance_title = ttk.Label(self, text= 'Distancia de Siembra', font= f'Arial {font_size} bold' , anchor='center' )
    self.distance_unit  = ttk.Label(self, text= 'm', font= f'Arial {font_size}' , anchor='center' )
    self.distance_var_text = ttk.Label(self, text= f'{self.odometry_data[1].get()}',  font= f'Arial {font_size}' , anchor='center', relief='groove')

    #-- empaquedato en grid--
    self.monitor_title.grid(row=0 , column=0, columnspan=2, sticky='nswe' )
    self.tractor_draw.grid(row=1, column=0, columnspan=2, sticky= 'nswe' )
    self.speed_title.grid(row=2, column=0, columnspan=2, sticky= 'nswe')
    self.speed_var_text.grid(row=3, column=0, sticky= 'nswe')
    self.speed_unit.grid(row=3, column=1, sticky='nswe')
    self.distance_title.grid(row=4, column=0, columnspan=2, sticky= 'nswe')
    self.distance_var_text.grid(row=5, column=0, sticky= 'nswe')
    self.distance_unit.grid(row=5, column=1, sticky='nswe')

    #-- eventos
    self.update_monitor()

  def update_monitor(self):
    self.speed_var_text.config(text = f'{self.odometry_data[0].get()}')
    self.distance_var_text.config(text = f'{self.odometry_data[1].get()}')
    self.parent.after(100, self.update_monitor)
  
  def disabled_monitor(self):
    self.monitor_title.config(state='disabled')
    self.tractor_draw.config(state='disabled')
    self.speed_title.config(state='disabled')
    self.speed_var_text.config(state='disabled')
    self.speed_unit.config(state='disabled')
    self.distance_title.config(state='disabled')
    self.distance_var_text.config(state='disabled')
    self.distance_unit.config(state='disabled')
  
  def enable_monitor(self):
    self.monitor_title.config(state='normal')
    self.tractor_draw.config(state='normal')
    self.speed_title.config(state='normal')
    self.speed_var_text.config(state='normal')
    self.speed_unit.config(state='normal')
    self.distance_title.config(state='normal')
    self.distance_var_text.config(state='normal')
    self.distance_unit.config(state='normal')

class Option_btns(ttk.Frame):
  def __init__(self, parent, Btn_UP_name, Btn_DOWN_name, height, font_text):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    self.height = height
    #-- configurando grid --
    self.config(height=self.height)
    self.rowconfigure((0,1), weight=1)
    self.columnconfigure(0, weight=1)

    #--Elementos (widgets) --
    self.Btn_UP = tk.Button(self, text= Btn_UP_name, font=font_text, background= paleta_color[3])
    self.Btn_DOWN = tk.Button(self, text= Btn_DOWN_name, font=font_text, background= paleta_color[3])

    #-- empaquedato en grid --
    self.Btn_UP.grid(row= 0, column=0, sticky='swe', ipady= int(self.height*0.1) , pady=10)
    self.Btn_DOWN.grid(row= 1, column=0, sticky='nwe',ipady= int(self.height*0.1), pady=10)

  def config_fuctions(self,Btn_UP_func, Btn_DOWN_func):
    self.Btn_UP.config(command= Btn_UP_func)
    self.Btn_DOWN.config(command= Btn_DOWN_func)

  def config_btns_names(self,Btn_UP_name, Btn_DOWN_name):
    self.Btn_UP.config(text= Btn_UP_name)
    self.Btn_DOWN.config(text= Btn_DOWN_name)

  def disabled_btns(self):
    self.Btn_UP.config(state='disabled')
    self.Btn_DOWN.config(state='disabled')

  def enabled_btns(self):
    self.Btn_UP.config(state='normal')
    self.Btn_DOWN.config(state='normal')

class Parameters_btns(ttk.Frame):
  def __init__(self,parent,Prt_UP_name, Prt_DOWN_name , height):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limite
    #-- configurando grid --
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=2)
    self.rowconfigure((0,1), weight=1)

    #--Elementos (widgets) --
    self.parameter_btns = Option_btns(self,Btn_UP_name= Prt_UP_name, Btn_DOWN_name= Prt_DOWN_name, height= height,
                                      font_text='Arial 15 bold')
    self.parameter_value_up = ttk.Label(self,text='#', background='white', font='Arial 15 bold' , anchor='center', relief='groove')
    self.parameter_value_down = ttk.Label(self,text='#', background='white', font='Arial 15 bold', anchor='center', relief='groove')

    #-- empaquedato en grid--
    self.parameter_btns.grid(row=0,rowspan=2,column=0, sticky='nswe')
    self.parameter_value_up.grid(row=0, column=1, sticky='swe', pady=int(height*0.1), ipady=int(height*0.05))
    self.parameter_value_down.grid(row=1, column=1, sticky='nwe', pady=int(height*0.1), ipady=int(height*0.05))
    #-- eventos --

  def config_btn_funtions(self, Prt_UP_func, Prt_DOWN_func):
    self.parameter_btns.config_fuctions(Btn_UP_func=Prt_UP_func, Btn_DOWN_func= Prt_DOWN_func)
  
  def disabled_parameters(self):
    self.parameter_btns.disabled_btns()
    self.parameter_value_up.config(state='disabled')
    self.parameter_value_down.config(state='disabled')

  def enable_parameters(self):
    self.parameter_btns.enabled_btns()
    self.parameter_value_up.config(state='normal')
    self.parameter_value_down.config(state='normal')

class Select_btns(ttk.Frame):
  def __init__(self, parent,Btn_OK_name, Btn_BACK_name):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent

    #-- configurando grid --
    self.rowconfigure(0,weight=1)
    self.columnconfigure((0,1), weight= 1)

    #--Elementos (widgets) --
    self.Btn_OK = tk.Button(self, text= Btn_OK_name, background= paleta_color[2],
                            font= 'Arial 15 bold', foreground='white')
    self.Btn_BACK = tk.Button(self, text= Btn_BACK_name, background=paleta_color[0],
                              font= 'Arial 15 bold', foreground='white')

    #-- empaquedato en grid --
    self.Btn_OK.grid(row=0,column=0, sticky= 'nswe')
    self.Btn_BACK.grid(row=0, column=1, sticky= 'nswe')

  def config_fuctions(self,Btn_OK_func, Btn_BACK_func):
    self.Btn_OK.config(command= Btn_OK_func)
    self.Btn_BACK.config(command= Btn_BACK_func)



class initial_tab(ttk.Frame):
  def __init__(self, parent, size):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    #-- configurando grid --
    self.config(width= size[0], height= size[1])
    self.columnconfigure((0,2),weight=1)
    self.columnconfigure(1,weight=4)
    self.rowconfigure(0,weight=2)
    self.rowconfigure(1, weight=2)
    self.rowconfigure(2,weight=1)

    #-- Elementos (widgets) --
    self.photo_ipn = tk.PhotoImage(file='resources/LOGOTIPO_IPN_300.png',width=300)
    self.photo_upiiz = tk.PhotoImage(file='resources/UPIIZ_logo_300.png',width=300)
    
    self.IPN_LOGO = ttk.Label(self, image= self.photo_ipn)#text='poner logo', anchor='center')
    self.UPIIZ_LOGO = ttk.Label(self, image= self.photo_upiiz)#text='poner logo', anchor='center')
    self.main_title = ttk.Label(self, text= 'N E S D', anchor='center' , font='Arial 40 bold')
    self.secod_title = tk.Label( self, 
                                  text='"Sistema de Control y Monitoreo\nde Dosificación de Semilla"',
                                  anchor='center',
                                  font='Arial 30 bold')
    self.INICIAR_btn = tk.Button( self, text='INICIAR',font= 'Arial 30 bold',
                                  foreground='white',
                                  background= paleta_color[2])
    #self.OK_BACK_btns = Select_btns(self, Btn_OK_name= 'INICIAR',
    #                                Btn_BACK_name='Ocultar boton')
    #-- empaquedato en grid --
    self.IPN_LOGO.grid(row=0,column=0, sticky='nswe')
    self.UPIIZ_LOGO.grid(row=0, column=2, sticky='nswe')
    self.main_title.grid(row=0, column=1, sticky='nswe')
    self.secod_title.grid(row=1,column=1, sticky='nswe')
    self.INICIAR_btn.grid(row=2, column=1, sticky='nswe')

class config_tab(ttk.Frame):
  def __init__(self, parent, size):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    #-- configurando grid --
    self.rowconfigure((0,2), weight=1)
    self.rowconfigure(1, weight=8)
    self.columnconfigure(0,weight=2)
    self.columnconfigure((1,2),weight=1)
    
    #-- Elementos (widgets) --
    self.siembra_parameters = Parameters_btns(self,
                                              Prt_UP_name='CANTIDAD\nDE\nSEMILLA',
                                              Prt_DOWN_name='DISTANCIA',
                                              height= size[1])
    self.main_title = tk.Label( self, text='Inserte los parametros para la siembra:',
                                font='Arial 20 bold')
    self.description_label = tk.Label(self,text= 'Descipcion de boton seleccionado',
                                      font='Arial 20 bold', anchor='center')
    self.dispensacion_check_label = tk.Label(self, text=' ', font='Arial 20 bold', anchor='center')
    self.OK_btn = tk.Button(self,text='ACEPTAR',
                            background=paleta_color[2],
                            foreground='white',
                            font='Arial 15 bold')
    #-- empaquedato en grid --
    self.main_title.grid(row=0,column=0,columnspan=2,sticky='nswe')
    self.siembra_parameters.grid(row=1,column=0, sticky='we')
    self.description_label.grid(row=1,column=2,columnspan=2, sticky='nswe',)
    self.dispensacion_check_label.grid(row=2, column=1, sticky='nswe')
    self.OK_btn.grid(row=2,column=2, sticky='nswe')

class test_tab(ttk.Frame):
  def __init__(self, parent, size , tank_parameters, odometry_parameters):
    super().__init__(parent)
    self.parent = parent
    self.main_frame_size = size
    self.motitor_tank_size = (int(self.main_frame_size[0]*0.25) , int(self.main_frame_size[1]*0.85)) 

    self.tank_parameters = tank_parameters
    self.odometry_parameters = odometry_parameters
    #-- Frames principales
    self.selection_test_tab = ttk.Frame(self,
                                        width= self.main_frame_size[0],
                                        height= self.main_frame_size[1])
    self.sensores_test_tab = ttk.Frame(self,
                                        width= self.main_frame_size[0],
                                        height= self.main_frame_size[1])
    self.conection_test_tab = ttk.Frame(self,
                                        width= self.main_frame_size[0],
                                        height= self.main_frame_size[1])
    
    #-- configurando grid --
    self.rowconfigure(0,weight=1)
    self.columnconfigure(0,weight=1)

    self.selection_test_tab.rowconfigure(0,weight=1)
    self.selection_test_tab.columnconfigure(0,weight=2)
    self.selection_test_tab.columnconfigure(1,weight=8)

    self.sensores_test_tab.columnconfigure(0, weight=1)
    self.sensores_test_tab.columnconfigure((1,2), weight=5)
    self.sensores_test_tab.columnconfigure(3,weight=3)
    self.sensores_test_tab.rowconfigure(0,weight=9)
    self.sensores_test_tab.rowconfigure(1,weight=2)

    self.conection_test_tab.columnconfigure(0, weight=1)
    self.conection_test_tab.columnconfigure(1, weight=3)
    self.conection_test_tab.rowconfigure((0,1,2,4), weight=1)
    self.conection_test_tab.rowconfigure(3,weight=6)

    #--Elementos (widgets) --
    #Para deciption tab
    self.maid_descrip_label = ttk.Label(self.selection_test_tab, text='Selecciona ALGO' , anchor='center')
    self.selection_test_btns = Option_btns( self.selection_test_tab,
                                            Btn_UP_name='PRUEBAS\nDE\nCONEXIÓN',
                                            Btn_DOWN_name='PRUEBA\nDE\nSENSORES',
                                            height= self.motitor_tank_size[1],
                                            font_text='Arial 18 bold')

    #Para sensor tab
    self.sensores_tank_monitor = Tank_monitor(self.sensores_test_tab, size= self.motitor_tank_size, 
                                      level= tank_parameters[0], tank_number=1, 
                                      SeedOuputs= (tank_parameters[1], tank_parameters[2]))
    self.sensores_tank_selec_btns = Option_btns(self.sensores_test_tab, Btn_UP_name= 'TOLVA1', Btn_DOWN_name= ' ', 
                                                height= self.motitor_tank_size[1],
                                                font_text='Arial 15 bold')
    self.sensores_decription_label = ttk.Label( self.sensores_test_tab,
                                                font= 'Arial 20 bold',
                                                anchor='center',
                                                text='Decripcion del menu de pruebas\npara los sensores')
    self.sensores_OKBACK_btns = Select_btns(self.sensores_test_tab, Btn_OK_name= 'ACEPTAR', Btn_BACK_name= 'ATRÁS')
    self.sensores_odometry_monitor = Odometry_monitor(self.sensores_test_tab, odometry_data= self.odometry_parameters)
    self.sensores_set_seed_dispence_btns = Parameters_btns( self.sensores_test_tab, 
                                                            Prt_UP_name= f'SALIDA\nDE\nSEMILLAS {self.sensores_tank_monitor.tank_number*2 -1}',
                                                            Prt_DOWN_name= f'SALIDA\nDE\nSEMILLAS {self.sensores_tank_monitor.tank_number*2}',
                                                            height= self.motitor_tank_size[1])
    self.sensores_tank_selec_btns.Btn_DOWN.grid_forget()
    self.sensores_OKBACK_btns.Btn_OK.grid_forget()

    #Para conection tab 
    self.conextion_test_btns = Option_btns(self.conection_test_tab,
                                            Btn_UP_name='PRUEBA\nCONEXIÓN\nINALAMBRICA',
                                            Btn_DOWN_name='PRUEBA\nINTERCONEXIÓN\nMÓDULOS',
                                            height= self.motitor_tank_size[1],
                                            font_text='Arial 20 bold')
    self.conection_title1_label = ttk.Label(self.conection_test_tab, 
                                            text='Estado de Conexión', anchor='center',
                                            font='Arial 30 bold',
                                            relief='groove')
    self.conection_state_label = ttk.Label( self.conection_test_tab, 
                                            text='SIN CONEXIÓN',
                                            anchor='center',
                                            font='Arial 30 bold',
                                            background= paleta_color[0],
                                            foreground= 'white',
                                            relief='groove')
    self.conection_title2_label = ttk.Label(self.conection_test_tab,
                                            text='Módulos Disponibles',
                                            anchor='center',
                                            font='Arial 30 bold',
                                            relief='groove')
    self.conection_module_list = ttk.Treeview(self.conection_test_tab,
                                              columns=('Tipo de Módulo','Función','Estado'),
                                              show='headings')
    self.conection_module_list.heading('Tipo de Módulo', text='Tipo de Módulo')
    self.conection_module_list.heading('Función', text='Función')
    self.conection_module_list.heading('Estado', text='Estado')
    self.conection_setBack_btns = Select_btns(self.conection_test_tab,
                                              Btn_OK_name='OCULTAR',
                                              Btn_BACK_name='ATRÁS')
    self.conection_setBack_btns.Btn_OK.grid_forget()

    #-- empaquedato en grid --
    self.selection_test_tab.grid(row=0, column=0, sticky='nswe')
    self.selection_test_btns.grid(row=0, column=0, sticky='nswe')
    self.maid_descrip_label.grid(row=0, column=1, sticky='nswe')


    #->self.sensores_test_tab.grid(row=0, column=0, sticky='nswe')
    #->self.sensores_tank_monitor.grid(row=0, column=2, columnspan=1, sticky='nswe')
    self.sensores_decription_label.grid(row=0,column=1,columnspan=2, sticky='nswe')
    self.sensores_tank_selec_btns.grid(row=0, column=0, sticky='nswe')
    self.sensores_odometry_monitor.grid(row=0,column=3, sticky= 'nswe')
    self.sensores_OKBACK_btns.grid(row=1, column=3, sticky= 'nswe')
    
    #->self.conection_test_tab.grid(row=0, column=0, sticky='nswe')
    self.conextion_test_btns.grid(row=0,rowspan=5,column=0, sticky='nswe')
    self.conection_title1_label.grid(row=0,column=1, sticky='nswe')
    self.conection_state_label.grid(row=1, column=1, sticky='ns', ipadx=20)
    self.conection_title2_label.grid(row=2,column=1, sticky='nswe')
    self.conection_module_list.grid(row=3, column=1, sticky='nswe')
    self.conection_setBack_btns.grid(row=4,column=1, sticky='nswe')


    self.sensores_tank_selec_btns.disabled_btns()
    self.sensores_set_seed_dispence_btns.disabled_parameters()
    self.sensores_tank_monitor.disabled_monitor()
    self.sensores_odometry_monitor.disabled_monitor()
    #-- eventos --
    def change2SensorTestTab():
      self.selection_test_tab.grid_forget()
      self.conection_test_tab.grid_forget()
      self.sensores_test_tab.grid(row=0, column=0, sticky='nswe')

    def change2SelectTestTab():
      self.sensores_test_tab.grid_forget()
      self.conection_test_tab.grid_forget()
      self.selection_test_tab.grid(row=0, column=0, sticky='nswe')

    def change2ConectionTestTab():
      self.selection_test_tab.grid_forget()
      self.sensores_test_tab.grid_forget()
      self.conection_test_tab.grid(row=0, column=0, sticky='nswe')

    def chage2SensorTestSensor():
      self.sensores_tank_monitor.grid_forget()
      self.sensores_set_seed_dispence_btns.grid_forget()
      self.sensores_decription_label.grid(row=0,column=1,columnspan=2, sticky='nswe')
      self.sensores_tank_selec_btns.grid(row=0,column=0, sticky='nswe')
      self.sensores_OKBACK_btns.config_fuctions(Btn_OK_func= lambda: print('ocultar btn'),
                                                Btn_BACK_func= change2SelectTestTab)
      self.sensores_OKBACK_btns.Btn_OK.grid_forget()

    def set_tolva1():
      self.sensores_decription_label.grid_forget()
      self.sensores_tank_monitor.grid(row=0, column=2, columnspan=1, sticky='nswe')
      self.sensores_tank_selec_btns.grid_forget()
      self.sensores_set_seed_dispence_btns.grid(row=0,column=0,columnspan=2, sticky='nswe')
      
      self.sensores_OKBACK_btns.config_fuctions(Btn_OK_func= lambda: print('ocultar btn'),
                                                Btn_BACK_func= chage2SensorTestSensor)
      self.sensores_OKBACK_btns.Btn_OK.grid_forget()

    def doTestConection():
      #Insertar codigo para test de conexion de MADC
      self.conection_state_label.config(text='¡CONECTADO!', background=paleta_color[2])
      self.conextion_test_btns.Btn_UP.config(state='disable')
      self.sensores_tank_selec_btns.enabled_btns()
      self.sensores_set_seed_dispence_btns.enable_parameters()
      self.sensores_tank_monitor.enable_monitor()
      self.sensores_odometry_monitor.enable_monitor()

    self.selection_test_btns.config_fuctions( Btn_UP_func= change2ConectionTestTab,
                                              Btn_DOWN_func= change2SensorTestTab)
    self.sensores_OKBACK_btns.config_fuctions( Btn_OK_func= lambda: print('xd'),
                                        Btn_BACK_func= change2SelectTestTab)
    self.sensores_tank_selec_btns.config_fuctions(Btn_UP_func= set_tolva1,
                                                  Btn_DOWN_func= lambda: print('ocultar boton'))
    self.conection_setBack_btns.config_fuctions(Btn_OK_func= lambda: print('ocultar boton'),
                                                Btn_BACK_func= change2SelectTestTab)
    self.conextion_test_btns.config_fuctions( Btn_UP_func=doTestConection,
                                              Btn_DOWN_func= lambda: print('Config. Funcion'))

class monitor_tab(ttk.Frame):
  def __init__(self, parent, size, tank_parameters, odometry_parameters):
    super().__init__(parent)
    self.parent = parent
    self.main_size = size
    self.motitor_tank_size = (int(self.main_size[0]*0.25) , int(self.main_size[1]*0.85))
    #-- configurando grid --
    self.rowconfigure(0,weight=6)
    self.rowconfigure((1,2),weight=2)
    self.columnconfigure((0,1,2), weight=1)
    
    #-- Elementos (widgets) --
    self.monitor_tolva1  = Tank_monitor(  self, size= self.motitor_tank_size,
                                          tank_number= 1, level= tank_parameters[0],
                                          SeedOuputs= (tank_parameters[1], tank_parameters[2]))
    self.monitor_odometry = Odometry_monitor( self, odometry_data= odometry_parameters)
    self.monitor_start_btn = tk.Button( self, text= 'INICIAR MONITOREO', 
                                        background= paleta_color[2],
                                        anchor= 'center',
                                        command=self.sistem_monitor_enabled)
    self.monitor_PauseBack_btns = Select_btns(self, Btn_OK_name= 'PAUSAR',
                                              Btn_BACK_name= 'ATRÁS')
    self.monitor_SiembraParameter_label = tk.Label( self,text='Poner los parametros\nde Siembra',
                                                    anchor='center')
    self.monitor_warning_label = tk.Label(self, 
                                          text= 'SE NECESITA CONFIGURAR PRIMERO:\n-> CONEXIÓN INALAMBRICA DE SISTEMA \n-> PARAMETROS DE SIEMBRE')
    #-- empaquedato en grid --
    self.monitor_tolva1.grid(row=0,rowspan=3, column=0,columnspan=2, sticky= 'nswe')
    self.monitor_odometry.grid(row=0,column=2, sticky= 'nswe')
    self.monitor_SiembraParameter_label.grid(row=1,column=2, sticky='nswe')
    self.monitor_start_btn.grid(row=2,column=2, sticky='nswe')
    #-- Eventos --

  def disabled(self):
    self.monitor_tolva1.disabled_monitor()
    self.monitor_odometry.disabled_monitor()
    self.monitor_SiembraParameter_label.config(state='disabled')
    self.monitor_start_btn.config(state='disabled')
    self.monitor_warning_label.place(anchor='center', relx=0.5, rely=0.5)
  
  def enabled(self):
    self.monitor_tolva1.enable_monitor()
    self.monitor_odometry.enable_monitor()
    self.monitor_SiembraParameter_label.config(state='normal')
    self.monitor_start_btn.config(state='normal')
    self.monitor_warning_label.place_forget()

  def sistem_monitor_enabled(self):
    self.monitor_start_btn.grid_forget()
    self.monitor_PauseBack_btns.grid(row=2,column=2, sticky='nswe')


#----------------------- variables tkinter -------------------------------------
level1 = tk.IntVar(value=0)
SeedOut_t1 = (tk.IntVar(value=0),tk.IntVar(value=0))

tractor_odometry = (tk.DoubleVar(value=0),tk.IntVar(value=0))#(tk.IntVar(value=0), tk.IntVar(value=10))
tolva_variables = (level1,SeedOut_t1[0],SeedOut_t1[1])

#----------------------- widgets -------------------------------------
panel_pestanas = ttk.Notebook(window, width= int(screen_w), height=int(screen_h*0.99))

pestana_inicial = initial_tab(panel_pestanas, size=(int(screen_w),int(screen_h*0.99)) )

pestana_config = config_tab(panel_pestanas, size=(int(screen_w),int(screen_h*0.99)))

pestana_tests = test_tab( panel_pestanas,size=(int(screen_w),int(screen_h*0.99)),
                          tank_parameters= tolva_variables, odometry_parameters= tractor_odometry)

pestana_monitor = monitor_tab(  panel_pestanas, size= (int(screen_w),int(screen_h*0.99)),
                                tank_parameters= tolva_variables, odometry_parameters= tractor_odometry)

pestana_monitor.disabled()

#----------------------- enpaquetado -------------------------------------
panel_pestanas.add(pestana_inicial,  text= '      INICIO     ')
panel_pestanas.add(pestana_config,   text= '  CONFIGURACIÓN  ')
panel_pestanas.add(pestana_tests ,   text= '     PRUEBAS     ')
panel_pestanas.add(pestana_monitor , text= '     MONITOR     ')
panel_pestanas.pack(expand=True)


#----------------------- EVENTOS ---------------------- ---------------
def incress_level(event):
  level1.set(level1.get()+1)
  #monitor1.update_level()

def decress_level(event):
  level1.set(level1.get()-1)
  #monitor1.update_level()

window.bind('<KeyPress-w>', incress_level)
window.bind('<KeyPress-s>', decress_level)
window.bind('<KeyPress-o>', lambda event: tractor_odometry[0].set(tractor_odometry[0].get() + 1))
window.bind('<KeyPress-l>', lambda event: tractor_odometry[0].set(tractor_odometry[0].get() - 1))

pestana_inicial.INICIAR_btn.config(command= lambda: panel_pestanas.select(1))

def doConection_v2():
  pestana_tests.conection_state_label.config(text='¡CONECTADO!', background=paleta_color[2])
  pestana_tests.conextion_test_btns.Btn_UP.config(state='disable')
  pestana_tests.sensores_tank_selec_btns.enabled_btns()
  pestana_tests.sensores_set_seed_dispence_btns.enable_parameters()
  pestana_tests.sensores_tank_monitor.enable_monitor()
  pestana_tests.sensores_odometry_monitor.enable_monitor()

  pestana_monitor.enabled()

pestana_tests.conextion_test_btns.Btn_UP.config(command= doConection_v2)

#----------------------- Ciclo principal donde corre el programa de la interfaz -------------------------------------
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada