import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class Cliente:
    def __init__(self, numero, nome, endereco, cpf):
        self.numero = numero
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf

class ClienteMenu:
    def __init__(self, master, contas):
        self.janela = master
        self.clientes = self.carregar_clientes()
        self.contas = contas

    def carregar_clientes(self):
        if os.path.exists('bancoapp/clientes.json'):
            try:
                with open('bancoapp/clientes.json', 'r') as f:
                    clientes_data = json.load(f)
                    return [Cliente(c['numero'], c['nome'], c['endereco'], c['cpf']) for c in clientes_data]
            except json.JSONDecodeError:
                return []
        return []

    def salvar_clientes(self):
        with open('bancoapp/clientes.json', 'w') as f:
            clientes_data = [{'numero': cliente.numero, 'nome': cliente.nome, 'endereco': cliente.endereco, 'cpf': cliente.cpf} for cliente in self.clientes]
            json.dump(clientes_data, f, indent=4)

    def gerar_numero_conta(self):
        if not self.clientes:
            return "1"
        return str(max(int(cliente.numero) for cliente in self.clientes) + 1)

    def cliente(self):
        self.nova_janela = tk.Toplevel(self.janela)
        self.nova_janela.title("Clientes")
        self.nova_janela.config(bg="#D3D3D3")
        self.nova_janela.grab_set()
        self.nova_janela.attributes("-topmost", True)

        self.label_numcliente = tk.Label(self.nova_janela, text="NÚMERO DO CLIENTE:", bg="#D3D3D3", fg='black')
        self.label_numcliente.pack()
        self.label_numcliente_valor = tk.Label(self.nova_janela, text="O seu número de identificação será gerado automaticamente", bg="#D3D3D3", fg='black')
        self.label_numcliente_valor.pack()

        self.label_nome = tk.Label(self.nova_janela, text="NOME:", bg="#D3D3D3", fg='black')
        self.label_nome.pack()
        self.entrada_nome = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_nome.pack()

        self.label_endereco = tk.Label(self.nova_janela, text="ENDEREÇO:", bg="#D3D3D3", fg='black')
        self.label_endereco.pack()
        self.entrada_endereco = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_endereco.pack()

        self.label_cpf = tk.Label(self.nova_janela, text="CPF:", bg="#D3D3D3", fg='black')
        self.label_cpf.pack()
        self.entrada_cpf = tk.Entry(self.nova_janela, bg="#D3D3D3", fg='black')
        self.entrada_cpf.pack()

        self.frame_botoes = tk.Frame(self.nova_janela, bg="#D3D3D3")
        self.frame_botoes.pack(pady=10, fill='x')
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)

        self.botao_adicionar = tk.Button(self.frame_botoes, text="Adicionar Cliente", command=self.adicionar_cliente)
        self.botao_adicionar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.botao_remover = tk.Button(self.frame_botoes, text="Remover Cliente", command=self.remover_cliente)
        self.botao_remover.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.botao_editar = tk.Button(self.frame_botoes, text="Editar Cliente", command=self.editar_cliente)
        self.botao_editar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.colunas = ("Numero", "Nome", "Endereco", "CPF")
        self.tree = ttk.Treeview(self.nova_janela, columns=self.colunas, show="headings")
        self.tree.heading("Numero", text="Numero")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereco", text="Endereço")
        self.tree.heading("CPF", text="CPF")
        self.tree.pack()

        self.atualizar_treeview()

    def editar_cliente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um cliente para editar.", parent=self.nova_janela)
            return

        item_id = selected_item[0]
        numero = self.tree.item(item_id, 'values')[0]

        cliente = next((c for c in self.clientes if c.numero == numero), None)
        if cliente:
            self.label_numcliente_valor.config(text=cliente.numero)

            self.entrada_nome.delete(0, tk.END)
            self.entrada_nome.insert(0, cliente.nome)

            self.entrada_endereco.delete(0, tk.END)
            self.entrada_endereco.insert(0, cliente.endereco)

            self.entrada_cpf.delete(0, tk.END)
            self.entrada_cpf.insert(0, cliente.cpf)

            self.botao_adicionar.config(command=lambda: self.atualizar_cliente(numero))
            self.botao_adicionar.config(text="Atualizar Cliente")

    def atualizar_cliente(self, numero):
        novo_nome = self.entrada_nome.get()
        novo_endereco = self.entrada_endereco.get()
        novo_cpf = self.entrada_cpf.get()

        if novo_nome and novo_endereco:
            for cliente in self.clientes:
                if cliente.numero == numero:
                    cliente.nome = novo_nome
                    cliente.endereco = novo_endereco
                    cliente.cpf = novo_cpf
                    break

            self.label_numcliente_valor.config(text="O seu número de identificação será gerado automaticamente")
            self.entrada_nome.delete(0, tk.END)
            self.entrada_endereco.delete(0, tk.END)
            self.entrada_cpf.delete(0, tk.END)
            
            self.salvar_clientes()
            self.atualizar_treeview()
            self.botao_adicionar.config(text="Adicionar Cliente")
            self.botao_adicionar.config(command=self.adicionar_cliente)

            messagebox.showinfo("Cliente Atualizado", "O cliente foi atualizado com sucesso.", parent=self.nova_janela)
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.", parent=self.nova_janela)

    def remover_cliente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um cliente para remover.", parent=self.nova_janela)
            return

        item_id = selected_item[0]
        nome_cliente = self.tree.item(item_id, 'values')[1]
        contas_associadas = [conta for conta in self.contas if conta.titular == nome_cliente]

        if contas_associadas:
            messagebox.showwarning("Cliente possui contas", "Não é possível remover este cliente, pois ele possui contas associadas.", parent=self.nova_janela)
            return

        self.clientes = [cliente for cliente in self.clientes if cliente.nome != nome_cliente]
        self.salvar_clientes()
        self.atualizar_treeview()
        messagebox.showinfo("Cliente Removido", "O cliente foi removido com sucesso.", parent=self.nova_janela)

    def adicionar_cliente(self):
        numero = self.gerar_numero_conta()
        nome = self.entrada_nome.get()
        endereco = self.entrada_endereco.get()
        cpf = self.entrada_cpf.get()

        if nome and endereco and cpf:
            novo_cliente = Cliente(numero, nome, endereco, cpf)
            self.clientes.append(novo_cliente)
            
            self.label_numcliente_valor = tk.Label(text="O seu número de identificação será gerado automaticamente")
            self.entrada_nome.delete(0, tk.END)
            self.entrada_endereco.delete(0, tk.END)
            self.entrada_cpf.delete(0, tk.END)

            self.atualizar_treeview()
            self.salvar_clientes()
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.", parent=self.nova_janela)

    def atualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for cliente in self.clientes:
            self.tree.insert("", "end", values=(cliente.numero, cliente.nome, cliente.endereco, cliente.cpf))