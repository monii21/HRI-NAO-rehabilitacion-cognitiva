import tkinter as tk
import style 
import config
import xml.dom.minidom as md

#VARIABLES
NAME_WINDOW="Interfaz de Usuario"
WIDTH_FRAME="650"
HEIGHT_FRAME="400"
COLOR_FRAME="grey"
COLOR_WINDOW="black"
COLOR_LABEL="CadetBlue1"
FONT_LABEL="Roman 10 bold"
FONT_BUTTON="Roman 10 italic bold"


class Home(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background = style.BACKGROUND)
        self.controller = controller
        self.gameMode = tk.StringVar(self,value="Normal")

        self.init_widgets()

    
    def move_to_game(self):
        self.controller.mode=self.gameMode.get()
        self.controller.show_frame(Game)
    
    def init_widgets(self):
        tk.Label(
            self,
            text="HOLA BIENVENIDO",
            justify = tk.CENTER,
            **style.STYLE
        ).pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=22,
            pady=11
        )
    

        optionsFrame = tk.Frame(self)
        optionsFrame.configure(background=style.COMPONENT)
        optionsFrame.pack(
            side = tk.TOP,
            fill = tk.BOTH,
            expand = True,
            padx = 22,
            pady =11
        )
        tk.Label(
            optionsFrame,
            text = "Elige el tipo de Ejercicio",
            justify=tk.CENTER,
            **style.STYLE
        ).pack(
            side = tk.TOP,
            fill = tk.X,
            padx = 22,
            pady=11
        )

        for(key,values)in config.MODES.items():
            tk.Radiobutton(
                optionsFrame,
                text=key,
                variable=self.gameMode,
                value = values,
                activebackground=style.BACKGROUND,
                activeforeground=style.TEXT,
                **style.STYLE
            ).pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=5,
                pady=5
            )
        
        tk.Button(
            self,
            text="EMPEZAR!!",
            command=self.move_to_game,
            **style.STYLE,
            relief=tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side=tk.TOP,
            fill=tk.X,
            padx=22,
            pady=11
        )


class Ejercicio(tk.Frame):

    def __init__(self, parent, controller):
         super().__init__(parent)
         self.configure(background = style.BACKGROUND)
         self.controller = controller

class Game(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.configure(background=style.BACKGROUND)
        self.controller=controller

    def buttonGuardar():
        doc = md.parse("prueba.xml")
        root = doc.documentElement
        pruebas = root.firstChild
        ejercicio= doc.createElement("Ejercicio")
        ejercicio.setAttribute("numero", tk.CuadroEjercicio.get())
        pruebas.appendChild(ejercicio)
        aciertos= doc.createElement("Aciertos")
        aciertos.setAttribute("n.Aciertos", tk.CuadroAciertos.get())
        ejercicio.appendChild(aciertos)
        f=open("prueba.xml","w")
        doc.writexml(f)


    def buttonCrear():
        f=open("prueba.xml","w")
        doc = md.parseString("<" +tk.CuadroNombre.get() +"/>")
        root = doc.documentElement
        pruebas = doc.createElement("Pruebas")
        root.appendChild(pruebas)
        doc.writexml(f)

    #FRAME
    miFrame=tk.Frame() #creamos un frame, donde van a ir todos los widgets
    miFrame.pack(fill="both", expand="True") #para que al redimensionar la ventana se expand el frame tambien
    miFrame.config(bg=COLOR_FRAME)
    miFrame.config(width=WIDTH_FRAME, height=HEIGHT_FRAME)
    miFrame.config(bd=35)
    miFrame.config(relief="groove")

    #1º WIDGET 
    nombrePaciente=tk.Label(miFrame, text="Nombre del Paciente:")
    nombrePaciente.grid(pady=5, row=0, column=0, sticky="w")
    nombrePaciente.config(bg=COLOR_LABEL, font=FONT_LABEL)

    CuadroNombre=tk.Entry(miFrame)
    CuadroNombre.grid(padx=5,row=0, column=1) #ubicamos el cuadro de texto en la matriz que divide el frame


    #2º WIDGET
    numEjercicio=tk.Label(miFrame, text="Número del ejercicio:")
    numEjercicio.grid(pady=5, row=1, column=0,sticky="w")
    numEjercicio.config(bg=COLOR_LABEL, font=FONT_LABEL)

    CuadroEjercicio=tk.Entry(miFrame)
    CuadroEjercicio.grid(padx=5,row=1, column=1) #ubicamos el cuadro de texto en la matriz que divide el frame

    #3º WIDGET
    numAciertos=tk.Label(miFrame, text="Número de Aciertos:")
    numAciertos.grid(pady=5, row=2 , column=0,sticky="w")
    numAciertos.config(bg=COLOR_LABEL, font=FONT_LABEL)

    CuadroAciertos=tk.Entry(miFrame)
    CuadroAciertos.grid(padx=5,row=2, column=1) #ubicamos el cuadro de texto en la matriz que divide el frame

    #4º WIDGET
    botonGuardar=tk.Button(miFrame, font=FONT_BUTTON, fg="white", bg="blue", text="Guardar", width=30, command=buttonGuardar).grid(padx=10, pady=10, row=3, column=0, columnspan=2)

    #5º WIDGET
    botonStart=tk.Button(miFrame, font=FONT_BUTTON, fg="white", bg="red", text="Empezar Base de Datos", width=30, command=buttonCrear).grid(padx=10, pady=10, row=4, column=0, columnspan=2)

    