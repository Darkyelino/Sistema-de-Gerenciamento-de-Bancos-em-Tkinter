import tkinter as tk
from tkinter import ttk 
from banco_menu import BancoMenu 
from conta_menu import ContaMenu
from cliente_menu import ClienteMenu
from saquedeposito import SaqueDeposito
from rendimento import ContaPoupancaMenu
# Importações feitas!

# Classe principal
class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Sistema Bancário Siri")
        self.janela.geometry("700x500")
        self.janela.config(bg="#D3D3D3")

        self.label_boasvindas = tk.Label(text="Boas Vindas ao Sistema de Gerenciamento de Banco",  fg='black', font=("Arial", 16), bg="#D3D3D3")
        self.label_boasvindas.pack(pady=5)

        self.img = tk.PhotoImage(file='bancoapp/siri.png')
        self.img = self.img.subsample(1, 1)
        self.label_img = tk.Label(self.janela, image=self.img, bg="#D3D3D3")
        self.label_img.pack(pady=20)

        self.bancos = []
        self.contas = []
        self.clientes = []

        self.banco_menu = BancoMenu(self.janela)
        self.conta_menu = ContaMenu(self.janela)
        self.cliente_menu = ClienteMenu(self.janela, self.conta_menu.contas)
        self.saque_deposito = SaqueDeposito(self.janela, self.conta_menu.contas)
        self.rendimento = ContaPoupancaMenu(self.janela)

        self.home()

    def home(self):
        self.menu_barra = tk.Menu(self.janela)
        self.janela.config(menu=self.menu_barra)

        self.menu_entidades = tk.Menu(self.menu_barra, tearoff=0)
        self.menu_barra.add_cascade(label="Menu", menu=self.menu_entidades)
        self.menu_entidades.add_command(label="Banco", command=self.banco_menu.banco)
        self.menu_entidades.add_command(label="Conta", command=self.conta_menu.conta)
        self.menu_entidades.add_command(label="Cliente", command=self.cliente_menu.cliente)
        self.menu_entidades.add_separator()
        self.menu_entidades.add_command(label="Sair", command=self.janela.quit)

        self.menu_acoes = tk.Menu(self.menu_barra, tearoff=0)
        self.menu_barra.add_cascade(label="Ações", menu=self.menu_acoes)
        self.menu_acoes.add_command(label="Depósito & Saque", command=self.saque_deposito.saquedeposito)
        self.menu_acoes.add_command(label="Render", command=self.rendimento.rendimento)

# Inicializando a aplicação
janela = tk.Tk()
app = Tela(janela)
janela.mainloop()