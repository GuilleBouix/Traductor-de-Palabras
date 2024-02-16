from tkinter import *
from customtkinter import *
import os
from translate import Translator
import pyperclip


# DIRECTORIO
if getattr(sys, 'frozen', False):
    directorio_base = sys._MEIPASS
else:
    directorio_base = os.path.dirname(os.path.abspath(__file__))
icono = os.path.join(directorio_base, "icon.ico")


# VENTANA PRINCIPAL
root = Tk()
root.resizable(False,False)
root.title("Traductor de Palabras")
root.config(background="#3d4855")
if os.path.exists(icono):
    root.iconbitmap(icono)

# Traductor
traductor = Translator(
    from_lang='spanish',
    to_lang='english',
)


# Frame Principal
main_frame = Frame(root, background='#3d4855')
main_frame.grid(padx=30,pady=30)


# Traducciones
lbl_español = Label(main_frame,
                    background='#3d4855',
                    fg='white',
                    text='ESPAÑOL',
                    font=('Montserrat Bold',12))
lbl_español.grid(row=0,sticky=W,pady=10)

lbl_english = Label(main_frame,
                    background='#3d4855',
                    fg='white',
                    text='INGLES',
                    font=('Montserrat Bold',12))
lbl_english.grid(row=0,column=2,sticky=W,pady=10)

txt_spanish = CTkEntry(main_frame,
                       width=300,
                       height=70,
                       fg_color=('white','#73808f'),
                       border_width=0,
                       corner_radius=20,
                       text_color='white',
                       font=('Montserrat',20))
txt_spanish.grid(row=1,sticky=W)

btn_cambiar_idioma = CTkButton(main_frame,
                               width=50,
                               fg_color=('#ff8000','#ff8000'),
                               font=('Montserrat',30),
                               text='\uf0ec',
                               text_color='black',
                               hover_color='#ff9600',
                               corner_radius=100,
                               cursor='hand2',
                               command=lambda: cambiar_idioma())
btn_cambiar_idioma.grid(row=1,column=1,padx=20)

txt_ingles = CTkEntry(main_frame,
                       state='readonly',
                       width=300,
                       height=70,
                       fg_color=('white','#73808f'),
                       border_width=0,
                       corner_radius=20,
                       text_color='white',
                       font=('Montserrat',20))
txt_ingles.grid(row=1,column=2,sticky=W)


# Contar Carácteres Ingresados
def limitar_caracteres(event):
    texto = txt_spanish.get()[:20]
    txt_spanish.delete(0, END)
    txt_spanish.insert(0, texto)
    actualizar_contador()
def actualizar_contador():
    caracteres_ingresados = len(txt_spanish.get())
    contador_caracteres.config(text=f'{caracteres_ingresados} / 20')

    if caracteres_ingresados == 20:
        contador_caracteres.config(fg='red')
    else:
        contador_caracteres.config(fg='white')
contador_caracteres = Label(main_frame,
                            text='0 / 20',
                            fg='white',
                            background='#3d4855',
                            font=('Montserrat',10))
contador_caracteres.grid(row=2,sticky=E,padx=10)
txt_spanish.bind('<KeyRelease>', limitar_caracteres)


# Botones
buttons_frame = Frame(main_frame,background='#3d4855')
buttons_frame.grid(row=3,pady=30,columnspan=3)

btn_limpiar = CTkButton(buttons_frame,
                        width=200,
                        height=60,
                        fg_color=('#ff8000','#ff8000'),
                        font=('Montserrat',25),
                        text='\uf12d Limpiar',
                        text_color='black',
                        hover_color='#ff9600',
                        corner_radius=25,
                        cursor='hand2',
                        command=lambda:limpiar_texto())
btn_limpiar.grid(row=0)

btn_traducir = CTkButton(buttons_frame,
                        width=200,
                        height=60,
                        fg_color=('#ff8000','#ff8000'),
                        font=('Montserrat',25),
                        text='\uf1ab Traducir',
                        text_color='black',
                        hover_color='#ff9600',
                        corner_radius=25,
                        cursor='hand2',
                        command=lambda: traducir_texto())
btn_traducir.grid(row=0,column=1,padx=15)

btn_copiar = CTkButton(buttons_frame,
                        width=200,
                        height=60,
                        fg_color=('#ff8000','#ff8000'),
                        font=('Montserrat',25),
                        text='\uf0c5 Copiar',
                        text_color='black',
                        hover_color='#ff9600',
                        corner_radius=25,
                        cursor='hand2',
                        command=lambda:copiar_traduccion())
btn_copiar.grid(row=0,column=2)


# Funciones
def traducir_texto():
    txt_ingles.configure(state='normal')
    txt_ingles.delete(0, 'end')
    texto = txt_spanish.get()
    texto_traducido = traductor.translate(texto)
    
    txt_ingles.insert(INSERT,texto_traducido)
    txt_ingles.configure(state='readonly')

def limpiar_texto():
    txt_ingles.configure(state='normal')
    txt_ingles.delete(0, 'end')
    txt_ingles.configure(state='readonly')
    txt_spanish.delete(0, 'end')

def copiar_traduccion():
    txt_ingles.configure(state='normal')
    contenido_entry = txt_ingles.get()
    pyperclip.copy(contenido_entry)
    txt_ingles.configure(state='readonly')
    
def cambiar_idioma():
    global traductor
    if lbl_english.cget("text") == 'ESPAÑOL':
        lbl_english.config(text='INGLES')
        lbl_español.config(text='ESPAÑOL')
        
        traductor = Translator(
            from_lang='spanish',
            to_lang='english')
    else:
        lbl_english.config(text='ESPAÑOL')
        lbl_español.config(text='INGLES')
        
        traductor = Translator(
            from_lang='english',
            to_lang='spanish') 
     
    txt_ingles.configure(state='normal')
    txt_ingles.delete(0, 'end')
    txt_ingles.configure(state='readonly')
    txt_spanish.delete(0, 'end')

def lost_focus(Event):
    if(Event.widget == root):
        root.focus()
root.bind("<Button-1>", lost_focus)


# Centrar Ventana
root.update_idletasks()
width = root.winfo_reqwidth()
height = root.winfo_reqheight()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f'{width}x{height}+{x}+{y-50}')


# Bucle Principal
root.mainloop()