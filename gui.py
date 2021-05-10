import tkinter
from tkinter import *
from tkinter import ttk
import pyperclip
from tkinter import messagebox as mb
import database
import dicionario_de_siglas
import glob


class Janela:
    def __init__(self, root: Tk):
        self.db = database.Database("siglas.db")
        janela_width = 810
        janela_height = 600
        self.root = root
        self.root.title("Siglas de ultrassom")
        self.root.geometry(f"{janela_width}x{janela_height}")
        self.root.resizable(0, 0)

        # notebook
        nb = ttk.Notebook(self.root)
        nb.place(x=0, y=0, width=janela_width, height=janela_height)

        # frames (abas)
        tab_principal = Frame(nb)
        nb.add(tab_principal, text="Principal")

        tab_add_siglas = Frame(nb)
        nb.add(tab_add_siglas, text="Gerenciar siglas")

        tab_mascaras = Frame(nb)
        nb.add(tab_mascaras, text="Máscaras")

        tab_sobre = Frame(nb)
        nb.add(tab_sobre, text="Sobre")
        lb_sobre = Label(tab_sobre,
                         text="Siglas para Ultrassom\nVersão: 0.0.0\n\n\nAutor: Fabio Guerra\nEmail:fabioguerrra@hotmail.com")
        lb_sobre.place(x=int(janela_width / 3), y=int(janela_height / 5))

        # TAB PRINCIPAL
        lb_processar = Label(tab_principal, text="Clique em 'Processar texto' para substituir as siglas")
        lb_processar.place(x=5, y=30)
        self.processar_texto = Button(tab_principal, text="Processar texto", command=self.copiar_texto)
        self.processar_texto.place(x=10, y=60)

        self.previewBox = Text(tab_principal, state='disabled')
        self.previewBox.place(x=10, y=100, width=janela_width - 20, height=janela_height - 130)

        # TAB SIGLAS
        lb_inserir = Label(tab_add_siglas, text="Adicionar siglas. Formato: <#sigla:texto>")
        lb_inserir.place(x=5, y=30)

        self.e_sigla = Entry(tab_add_siglas, state='disabled')

        self.e_sigla.place(x=5, y=60)
        lb_dois_pontos = Label(tab_add_siglas, text=":")
        lb_dois_pontos.place(x=180, y=60)

        self.e_texto = Entry(tab_add_siglas, state='disabled')
        self.e_texto.place(x=195, y=60, width=600)

        self.btn_nova = Button(tab_add_siglas, text="Nova", command=self.nova)
        self.btn_nova.place(x=5, y=100)

        self.btn_salvar = Button(tab_add_siglas, text="Salvar", state='disabled', command=self.salvar)
        self.btn_salvar.place(x=75, y=100)

        self.btn_cancelar = Button(tab_add_siglas, text="Cancelar", state='disabled', command=self.cancelar)
        self.btn_cancelar.place(x=150, y= 100)

        self.view_siglas = Listbox(tab_add_siglas)
        self.view_siglas.place(x=5, y=150, width=666, height=417)
        self.view_siglas.bind('<<ListboxSelect>>', self.get_selected_row)

        # botões ver todas e excluir

        self.btn_view = Button(tab_add_siglas, text="Ver siglas", command=self.ver_siglas)
        self.btn_view.place(x=685, y=150)

        self.btn_excluir = Button(tab_add_siglas, text="Excluir", command=self.delete)
        self.btn_excluir.place(x=685, y=200)

        # Tab máscaras
        self.mascaras_box = Listbox(tab_mascaras)
        self.mascaras_box.place(x=0, y=0, width=janela_width - 5, height=janela_height - 20)
        self.fill_list_box_mascaras()
        self.mascaras_box.bind('<<ListboxSelect>>', self.get_mascara_selecinada)

    def copiar_texto(self):
        conteudo = str(pyperclip.paste())
        self.previewBox.config(state=tkinter.NORMAL)
        self.previewBox.delete('1.0', END)
        dic = dicionario_de_siglas.siglas()

        for key, value in dic.items():

            conteudo = conteudo.replace(key, value)

        pyperclip.copy(conteudo)
        self.previewBox.insert(END, conteudo)
        self.previewBox.config(state='disabled')

    def nova(self):
        self.e_sigla.config(state=tkinter.NORMAL)
        self.e_sigla.focus()
        self.e_sigla.insert(0, "#")
        self.e_texto.config(state=tkinter.NORMAL)
        self.btn_cancelar.config(state=tkinter.NORMAL)
        self.btn_nova.config(state=DISABLED)
        self.btn_salvar.config(state=tkinter.NORMAL)

    def cancelar(self):
        self.e_texto.delete(0, END)
        self.e_texto.config(state=DISABLED)
        self.e_sigla.delete(0, END)
        self.e_sigla.config(state=DISABLED)
        self.btn_nova.config(state=tkinter.NORMAL)
        self.btn_salvar.config(state=DISABLED)  
        self.btn_cancelar.config(state=DISABLED)     

    def salvar(self):
        if len(self.e_sigla.get()) == 1 or self.e_sigla.get()[0] != "#":
            mb.showerror("Sigla inválida", "Sua sigla é inválida!")
        elif len(self.e_texto.get()) <= 1:
            mb.showerror("Texto inválido", "Insira um texto válido!")
        else:
            self.btn_nova.config(state=tkinter.NORMAL)

            self.db.insert(self.e_sigla.get(), self.e_texto.get())
            self.e_sigla.delete(0, END)
            self.e_sigla.config(state=DISABLED)
            self.e_texto.delete(0, END)
            self.e_texto.config(state=DISABLED)
            self.btn_salvar.config(state=DISABLED)
            self.btn_cancelar.columnconfigure(state=DISABLED)
            self.ver_siglas()

    def ver_siglas(self):
        self.view_siglas.delete(0, END)
        result = self.db.view()
        self.view_siglas.insert(END, "ID  SIGLA : TEXTO")
        for row in result:
            self.view_siglas.insert(END, f"{row[0]}. {row[1]} : {row[2]}")

    def get_selected_row(self, event):
        if len(self.view_siglas.curselection()) == 0:
            return None
        global selected_tuple
        index = self.view_siglas.curselection()[0]
        selected_tuple = self.view_siglas.get(index)
        
        print(f"{selected_tuple}")

    def delete(self):
        #id = selected_tuple[0]
        id = str(selected_tuple).split()
        id = id[0].replace(".", "")
        
        self.db.delete(int(id))
        self.ver_siglas()

    def fill_list_box_mascaras(self):
        exames = sorted(glob.glob("laudos/*.txt"))
        exame_list = [exame.replace(".txt", "").replace(r"laudos/", "") for exame in exames]

        for exame in exame_list:
            self.mascaras_box.insert(END, exame)

    def get_mascara_selecinada(self, event):
        index = self.mascaras_box.curselection()[0]
        selected_tuple = self.mascaras_box.get(index)
        dir = f"laudos/{selected_tuple}.txt"
        with open(dir) as file:
            pyperclip.copy(str(file.read()))
