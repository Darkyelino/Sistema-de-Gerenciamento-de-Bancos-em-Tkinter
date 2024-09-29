import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class Banco:
    def __init__(self, numero_banco, nome_banco, taxa_juro, desconto):
        self.numero_banco = numero_banco
        self.nome_banco = nome_banco
        self.taxa_juro = taxa_juro
        self.desconto = desconto
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def remover_conta(self, conta):
        self.contas.remove(conta)

class BancoMenu:
    def __init__(self, master):
        self.janela = master
        self.bancos = self.carregar_bancos()

    def carregar_bancos(self):
        if os.path.exists('bancoapp/bancos.json'):
            with open('bancoapp/bancos.json', 'r') as f:
                bancos_data = json.load(f)
                return [Banco(b['numero_banco'], b['nome_banco'], b['taxa_juro'], b['desconto']) for b in bancos_data]
        return []

    def salvar_bancos(self):
        with open('bancoapp/bancos.json', 'w') as f:
            bancos_data = [{'numero_banco': banco.numero_banco, 'nome_banco': banco.nome_banco, 'taxa_juro': banco.taxa_juro, 'desconto': banco.desconto} for banco in self.bancos]
            json.dump(bancos_data, f, indent=4)

    def banco(self):
        self.nova_janela = tk.Toplevel(self.janela)
        self.nova_janela.title("Bancos")
        self.nova_janela.config(bg="#D3D3D3")
        self.nova_janela.grab_set()
        self.nova_janela.attributes("-topmost", True)

        self.label_numbanco = tk.Label(self.nova_janela, text="NÚMERO DO BANCO:", bg="#D3D3D3", fg='black')
        self.label_numbanco.pack()
        self.entrada_numbanco = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_numbanco.pack()

        self.label_nomebanco = tk.Label(self.nova_janela, text="NOME DO BANCO:", bg="#D3D3D3", fg='black')
        self.label_nomebanco.pack()
        self.entrada_nomebanco = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_nomebanco.pack()

        self.label_taxabanco = tk.Label(self.nova_janela, text="TAXA DE JUROS:", bg="#D3D3D3", fg='black')
        self.label_taxabanco.pack()
        self.entrada_taxabanco = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_taxabanco.pack()

        self.label_descontobanco = tk.Label(self.nova_janela, text="TAXA DE DESCONTO:", bg="#D3D3D3", fg='black')
        self.label_descontobanco.pack()
        self.entrada_descontobanco = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_descontobanco.pack()

        self.frame_botoes = tk.Frame(self.nova_janela, bg="#D3D3D3")
        self.frame_botoes.pack(pady=10, fill='x')
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)

        self.botao_adicionar = tk.Button(self.frame_botoes, text="Adicionar Banco", command=self.adicionar_banco)
        self.botao_adicionar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir Banco", command=self.excluir_banco)
        self.botao_excluir.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.botao_editar = tk.Button(self.frame_botoes, text="Editar Banco", command=self.editar_banco)
        self.botao_editar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.colunas = ("Numero do Banco", "Nome do Banco", "Taxa de Juros", "Taxa de Desconto")
        self.tree = ttk.Treeview(self.nova_janela, columns=self.colunas, show="headings")
        self.tree.heading("Numero do Banco", text="Número do Banco")
        self.tree.heading("Nome do Banco", text="Nome do Banco")
        self.tree.heading("Taxa de Juros", text="Taxa de Juros")
        self.tree.heading("Taxa de Desconto", text="Taxa de Desconto")
        self.tree.pack()

        self.atualizar_treeview()

    def editar_banco(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um banco para editar.", parent=self.nova_janela)
            return

        item_id = selected_item[0]
        numero_banco = self.tree.item(item_id, 'values')[0]

        banco = next((b for b in self.bancos if b.numero_banco == numero_banco), None)
        if banco:
            self.entrada_numbanco.delete(0, tk.END)
            self.entrada_numbanco.insert(0, banco.numero_banco)

            self.entrada_nomebanco.delete(0, tk.END)
            self.entrada_nomebanco.insert(0, banco.nome_banco)

            self.entrada_taxabanco.delete(0, tk.END)
            self.entrada_taxabanco.insert(0, banco.taxa_juro)

            self.entrada_descontobanco.delete(0, tk.END)
            self.entrada_descontobanco.insert(0, banco.desconto)

            self.botao_adicionar.config(command=lambda: self.atualizar_banco(numero_banco))
            self.botao_adicionar.config(text="Atualizar Banco")

    def atualizar_banco(self, numero_banco):
        novo_numero_banco = self.entrada_numbanco.get()
        novo_nome_banco = self.entrada_nomebanco.get()
        nova_taxa_juro = self.entrada_taxabanco.get()
        novo_desconto = self.entrada_descontobanco.get()

        if novo_numero_banco and novo_nome_banco:
            for banco in self.bancos:
                if banco.numero_banco == numero_banco:
                    banco.numero_banco = novo_numero_banco
                    banco.nome_banco = novo_nome_banco
                    banco.taxa_juro = nova_taxa_juro
                    banco.desconto = novo_desconto
                    break

            self.salvar_bancos()
            self.atualizar_treeview()

            self.botao_adicionar.config(text="Adicionar Banco")
            self.botao_adicionar.config(command=self.adicionar_banco)

            self.entrada_numbanco.delete(0, tk.END)
            self.entrada_nomebanco.delete(0, tk.END)
            self.entrada_taxabanco.delete(0, tk.END)
            self.entrada_descontobanco.delete(0, tk.END)

            messagebox.showinfo("Banco Atualizado", "O banco foi atualizado com sucesso.", parent=self.nova_janela)
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.", parent=self.nova_janela)

    def excluir_banco(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um banco para excluir.", parent=self.nova_janela)
            return

        item_id = selected_item[0]
        numero_banco = self.tree.item(item_id, 'values')[0]

        self.bancos = [banco for banco in self.bancos if banco.numero_banco != numero_banco]

        self.salvar_bancos()
        self.atualizar_treeview()
        messagebox.showinfo("Banco Excluído", "O banco foi excluído com sucesso.", parent=self.nova_janela)

    def adicionar_banco(self):
        numero_banco = self.entrada_numbanco.get()
        nome_banco = self.entrada_nomebanco.get()
        taxa_juro = self.entrada_taxabanco.get()
        desconto = self.entrada_descontobanco.get()

        if self.banco_existente(numero_banco):
            messagebox.showwarning("Número de Banco Duplicado", "O número do banco já existe.", parent=self.nova_janela)
            return

        if numero_banco and nome_banco:
            novo_banco = Banco(numero_banco, nome_banco, taxa_juro, desconto)
            self.bancos.append(novo_banco)

            self.entrada_numbanco.delete(0, tk.END)
            self.entrada_nomebanco.delete(0, tk.END)
            self.entrada_taxabanco.delete(0, tk.END)
            self.entrada_descontobanco.delete(0, tk.END)

            self.salvar_bancos()
            self.atualizar_treeview()
            messagebox.showinfo("Banco Adicionado", "O banco foi adicionado com sucesso.", parent=self.nova_janela)
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.", parent=self.nova_janela)

    def atualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for banco in self.bancos:
            self.tree.insert('', 'end', values=(banco.numero_banco, banco.nome_banco, banco.taxa_juro, banco.desconto))

    def banco_existente(self, numero_banco):
        return any(banco.numero_banco == numero_banco for banco in self.bancos)