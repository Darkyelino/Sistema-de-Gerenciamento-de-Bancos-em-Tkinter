import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import json
import os

class SaqueDeposito:
    def __init__(self, master, contas):
        self.janela = master
        self.contas = contas
        self.bancos = self.carregar_bancos()  # Carregar as taxas de desconto dos bancos

    def carregar_bancos(self):
        if os.path.exists('bancoapp/bancos.json'):
            with open('bancoapp/bancos.json', 'r', encoding='utf-8') as f:
                bancos_data = json.load(f)
                # Usar o nome do banco como chave, armazenando a taxa de desconto
                return {banco['nome_banco'].strip().lower(): float(banco['desconto']) for banco in bancos_data}
        return {}

    def saquedeposito(self):
        self.nova_janela = tk.Toplevel(self.janela)
        self.nova_janela.title("Saque & Depósito")
        self.nova_janela.config(bg="#D3D3D3")
        self.nova_janela.grab_set()

        self.label_valor = tk.Label(self.nova_janela, text="VALOR:", bg="#D3D3D3", fg='black')
        self.label_valor.pack(pady=10)
        self.entrada_valor = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_valor.pack(pady=10)

        self.frame_botoes = tk.Frame(self.nova_janela, bg="#D3D3D3")
        self.frame_botoes.pack(pady=10, fill='x')
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)

        self.botao_deposito = tk.Button(self.frame_botoes, text="Depósito", command=self.depositar)
        self.botao_deposito.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.botao_saque = tk.Button(self.frame_botoes, text="Saque", command=self.sacar)
        self.botao_saque.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.botao_relatorio = tk.Button(self.frame_botoes, text="Gerar Relatório", command=self.gerar_relatorio)
        self.botao_relatorio.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        colunas = ("Numero", "Titular", "Saldo", "Tipo", "Banco")
        self.tree = ttk.Treeview(self.nova_janela, columns=colunas, show="headings")
        self.tree.heading("Numero", text="Número")
        self.tree.heading("Titular", text="Titular")
        self.tree.heading("Saldo", text="Saldo")
        self.tree.heading("Tipo", text="Tipo de Conta")
        self.tree.heading("Banco", text="Banco")
        self.tree.pack(pady=10, fill='both', expand=True)

        self.atualizar_treeview()

    def atualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for conta in self.contas:
            self.tree.insert('', 'end', values=(conta.numero, conta.titular, conta.saldo, conta.tipo, conta.banco))

    def registrar_operacao(self, conta, operacao, valor):
        data = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(f"{conta.numero}_extrato.txt", "a") as arquivo:
            arquivo.write(f"{data}, {operacao}, R${valor:.2f}, Saldo Final: R${conta.saldo:.2f}\n")

    def aplicar_desconto(self, conta, valor):
        nome_banco = conta.banco.strip().lower()
        taxa_desconto = self.bancos.get(nome_banco, 0)
        valor_com_desconto = valor * (1 - taxa_desconto / 100)
        return valor_com_desconto

    def depositar(self):
        valor = self.entrada_valor.get()
        if not valor.isdigit():
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um valor numérico válido.")
            return
        valor = float(valor)
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma conta para fazer o depósito.")
            return
        item_id = selected_item[0]
        numero = self.tree.item(item_id, 'values')[0]
        conta = next((conta for conta in self.contas if conta.numero == numero), None)
        if conta:
            if conta.tipo == "Conta Corrente":
                valor = self.aplicar_desconto(conta, valor)
            conta.saldo = float(conta.saldo) + valor

            self.salvar_contas()
            self.atualizar_treeview()
            self.registrar_operacao(conta, "Depósito", valor)
            messagebox.showinfo("Depósito", f"Depósito de R${valor:.2f} realizado com sucesso.")

    def sacar(self):
        valor = self.entrada_valor.get()
        if not valor.isdigit():
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um valor numérico válido.")
            return
        valor = float(valor)
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma conta para fazer o saque.")
            return
        item_id = selected_item[0]
        numero = self.tree.item(item_id, 'values')[0]
        conta = next((conta for conta in self.contas if conta.numero == numero), None)
        if conta:
            if conta.saldo >= valor:
                if conta.tipo == "Conta Corrente":
                    valor = self.aplicar_desconto(conta, valor)
                conta.saldo = float(conta.saldo) - valor

                self.salvar_contas()
                self.atualizar_treeview()
                self.registrar_operacao(conta, "Saque", valor)
                messagebox.showinfo("Saque", f"Saque de R${valor:.2f} realizado com sucesso.")
            else:
                messagebox.showwarning("Saldo Insuficiente", "O saldo da conta é insuficiente para este saque.")

    def gerar_relatorio(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma conta para gerar o relatório.")
            return
        item_id = selected_item[0]
        numero = self.tree.item(item_id, 'values')[0]
        conta = next((conta for conta in self.contas if conta.numero == numero), None)
        if conta:
            try:
                with open(f"{conta.numero}_extrato.txt", "r") as arquivo:
                    relatorio = arquivo.read()
                messagebox.showinfo("Relatório", f"Extrato obtido:\n\n{relatorio}")
            except FileNotFoundError:
                messagebox.showwarning("Arquivo não encontrado", "Nenhuma operação foi registrada para esta conta ainda.")

    def salvar_contas(self):
            with open('bancoapp/contas.json', 'w', encoding='utf-8') as f:
                contas_data = [{'numero': conta.numero, 'titular': conta.titular, 'saldo': conta.saldo, 'tipo': conta.tipo, 'banco': conta.banco} for conta in self.contas]
                json.dump(contas_data, f, indent=4)