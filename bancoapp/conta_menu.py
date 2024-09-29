import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from banco_menu import BancoMenu
from cliente_menu import ClienteMenu
import json
import os

class Conta:
    def __init__(self, numero, titular, saldo, tipo, banco=None):
        self.numero = numero
        self.titular = titular
        self.saldo = float(saldo)
        self.tipo = tipo
        self.banco = banco
        self.clientes = []

class ContaMenu:     
    def __init__(self, master):
        self.janela = master
        self.contas = self.carregar_contas()
        self.banco_menu = BancoMenu(master)
        self.bancos = self.banco_menu.carregar_bancos()
        self.cliente_menu = ClienteMenu(master, self.contas)
        self.clientes = self.cliente_menu.carregar_clientes()

    def carregar_contas(self):
        if os.path.exists('bancoapp/contas.json'):
            with open('bancoapp/contas.json', 'r', encoding='utf-8') as f:
                contas_data = json.load(f)
                return [Conta(c['numero'], c['titular'], c['saldo'], c['tipo'], c['banco']) for c in contas_data]
        return []

    def salvar_contas(self):
        with open('bancoapp/contas.json', 'w', encoding='utf-8') as f:
            contas_data = [{'numero': conta.numero, 'titular': conta.titular, 'saldo': conta.saldo, 'tipo': conta.tipo, 'banco': conta.banco} for conta in self.contas]
            json.dump(contas_data, f, indent=4)
    
    def gerar_numero_conta(self):
        if not self.contas:
            return "1"
        return str(max(int(conta.numero) for conta in self.contas) + 1)

    def conta(self):
        self.nova_janela = tk.Toplevel(self.janela)
        self.nova_janela.title("Contas")
        self.nova_janela.config(bg="#D3D3D3")
        self.nova_janela.grab_set()
        self.nova_janela.attributes("-topmost", True)

        self.label_numero_conta = tk.Label(self.nova_janela, text="NÚMERO DA CONTA:", bg="#D3D3D3", fg='black')
        self.label_numero_conta.pack()
        self.label_numero_conta_valor = tk.Label(self.nova_janela, text="O número da sua conta será gerado automaticamente", bg="#D3D3D3", fg='black')
        self.label_numero_conta_valor.pack()

        self.label_titular_conta = tk.Label(self.nova_janela, text="TITULAR DA CONTA:", bg="#D3D3D3", fg='black')
        self.label_titular_conta.pack()
        self.entrada_titular_conta = ttk.Combobox(self.nova_janela, values=[cliente.nome for cliente in self.clientes], state='readonly')
        self.entrada_titular_conta.pack()

        self.label_saldo_conta = tk.Label(self.nova_janela, text="SALDO DA CONTA:", bg="#D3D3D3", fg='black')
        self.label_saldo_conta.pack()
        self.entrada_saldo_conta = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_saldo_conta.pack()

        self.label_tipo_conta = tk.Label(self.nova_janela, text="TIPO DE CONTA:", bg="#D3D3D3", fg='black')
        self.label_tipo_conta.pack()
        self.tipo_conta = ttk.Combobox(self.nova_janela, values=["Conta Corrente", "Conta Poupança"], state="readonly")
        self.tipo_conta.pack()

        self.label_selecionar_banco = tk.Label(self.nova_janela, text="SELECIONE O BANCO:", bg="#D3D3D3", fg='black')
        self.label_selecionar_banco.pack()
        self.banco_selecionado = ttk.Combobox(self.nova_janela, values=[banco.nome_banco for banco in self.bancos], state='readonly')
        self.banco_selecionado.pack()

        self.frame_botoes = tk.Frame(self.nova_janela, bg="#D3D3D3")
        self.frame_botoes.pack(pady=10, fill='x')
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)

        self.botao_adicionar = tk.Button(self.frame_botoes, text="Adicionar Conta", command=self.adicionar_conta)
        self.botao_adicionar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir Conta", command=self.excluir_conta)
        self.botao_excluir.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.botao_editar = tk.Button(self.frame_botoes, text="Editar Conta", command=self.editar_conta)
        self.botao_editar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        colunas = ("Numero", "Titular", "Saldo", "Tipo", "Banco")
        self.tree = ttk.Treeview(self.nova_janela, columns=colunas, show="headings")
        self.tree.heading("Numero", text="Número")
        self.tree.heading("Titular", text="Titular")
        self.tree.heading("Saldo", text="Saldo")
        self.tree.heading("Tipo", text="Tipo de Conta")
        self.tree.heading("Banco", text="Banco")
        self.tree.pack()

        self.atualizar_treeview()

    def editar_conta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma conta para editar.", parent=self.nova_janela)
            return

        item_id = selected_item[0]
        numero = self.tree.item(item_id, 'values')[0]

        conta = next((conta for conta in self.contas if conta.numero == numero), None)
        if conta:
            self.label_numero_conta_valor.config(text=conta.numero)

            self.entrada_titular_conta.set("")
            self.entrada_titular_conta.set(conta.titular)

            self.entrada_saldo_conta.delete(0, tk.END)
            self.entrada_saldo_conta.insert(0, conta.saldo)

            self.tipo_conta.set("")
            self.tipo_conta.set(conta.tipo)

            self.banco_selecionado.set("")
            self.banco_selecionado.set(conta.banco)

            self.botao_adicionar.config(command=lambda: self.atualizar_conta(numero))
            self.botao_adicionar.config(text="Atualizar Conta")

    def atualizar_conta(self, numero):
        novo_titular = self.entrada_titular_conta.get()
        novo_saldo = self.entrada_saldo_conta.get()
        novo_tipo = self.tipo_conta.get()
        novo_banco = self.banco_selecionado.get()

        if novo_saldo < '0':
            messagebox.showwarning("Saldo Negativo", "O Saldo não pode ser negativo", parent=self.nova_janela)
        else:
            if novo_titular and novo_saldo:
                for conta in self.contas:
                    if conta.numero == numero:
                        conta.titular = novo_titular
                        conta.saldo = novo_saldo
                        conta.tipo = novo_tipo
                        conta.banco = novo_banco
                        break

                self.salvar_contas()
                self.atualizar_treeview()

                self.botao_adicionar.config(text="Adicionar Conta")
                self.botao_adicionar.config(command=self.adicionar_conta)

                self.label_numero_conta_valor.config(text="O número da sua conta será gerado automaticamente")
                self.entrada_titular_conta.set("")
                self.entrada_saldo_conta.delete(0, tk.END)
                self.tipo_conta.set("")
                self.banco_selecionado.set("")

                messagebox.showinfo("Conta Atualizada", "A conta foi atualizada com sucesso.", parent=self.nova_janela)
            else:
                messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.", parent=self.nova_janela)

    def excluir_conta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma conta para excluir.", parent=self.nova_janela)
            return

        item_id = selected_item[0]
        numero = self.tree.item(item_id, 'values')[0]

        conta = next((conta for conta in self.contas if conta.numero == numero), None)

        if conta:
            saldo = float(conta.saldo)
            if saldo == 0:
                self.contas = [conta for conta in self.contas if conta.numero != numero]

                self.salvar_contas()
                self.atualizar_treeview()
                messagebox.showinfo("Conta Excluída", "A conta foi excluída com sucesso.", parent=self.nova_janela)
            else:
                messagebox.showwarning("Saldo Não Zerado", "A conta não pode ser excluída, pois o saldo não está zerado.", parent=self.nova_janela)

    def adicionar_conta(self):
        numero = self.gerar_numero_conta()
        titular = self.entrada_titular_conta.get()
        saldo = self.entrada_saldo_conta.get()
        tipo = self.tipo_conta.get()
        banco = self.banco_selecionado.get()

        if saldo < '0':
            messagebox.showwarning("Saldo Negativo", "O Saldo não pode ser negativo", parent=self.nova_janela)
        else:
            if numero and titular and saldo and tipo and banco:
                nova_conta = Conta(numero, titular, saldo, tipo, banco)
                self.contas.append(nova_conta)

                self.label_numero_conta_valor = tk.Entry(text="O número da sua conta será gerado automaticamente")
                self.entrada_titular_conta.set("")
                self.entrada_saldo_conta.delete(0, tk.END)
                self.banco_selecionado.set("")
                self.tipo_conta.set("")

                self.salvar_contas()
                self.atualizar_treeview()
            else:
                messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos.", parent=self.nova_janela)

    def atualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for conta in self.contas:
            self.tree.insert('', 'end', values=(conta.numero, conta.titular, conta.saldo, conta.tipo, conta.banco))
