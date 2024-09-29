import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class ContaPoupancaMenu:
    def __init__(self, master):
        self.janela = master
        self.contas = self.carregar_contas_poupanca()
        self.bancos = self.carregar_bancos()

    def carregar_contas_poupanca(self):
        if os.path.exists('bancoapp/contas.json'):
            with open('bancoapp/contas.json', 'r', encoding='utf-8') as f:
                contas_data = json.load(f)
                return [conta for conta in contas_data if conta['tipo'] == "Conta Poupança"]
        return []

    def carregar_bancos(self):
        if os.path.exists('bancoapp/bancos.json'):
            with open('bancoapp/bancos.json', 'r', encoding='utf-8') as f:
                bancos_data = json.load(f)
                # Usar o nome do banco como chave, normalizando a string
                return {banco['nome_banco'].strip().lower(): float(banco['taxa_juro']) for banco in bancos_data}
        return {}

    def rendimento(self):
        self.nova_janela = tk.Toplevel(self.janela)
        self.nova_janela.title("Contas Poupança")
        self.nova_janela.config(bg="#D3D3D3")
        self.nova_janela.grab_set()

        self.label_info = tk.Label(self.nova_janela, text="Contas Poupança", bg="#D3D3D3", fg='black')
        self.label_info.pack(pady=10)

        self.botao_aplicar_rendimento = tk.Button(self.nova_janela, text="Aplicar Rendimento", command=self.aplicar_rendimento)
        self.botao_aplicar_rendimento.pack(pady=10)

        colunas = ("Numero", "Titular", "Saldo", "Banco")
        self.tree = ttk.Treeview(self.nova_janela, columns=colunas, show="headings")
        self.tree.heading("Numero", text="Número")
        self.tree.heading("Titular", text="Titular")
        self.tree.heading("Saldo", text="Saldo")
        self.tree.heading("Banco", text="Banco")
        self.tree.pack(pady=10, fill='both', expand=True)

        self.atualizar_treeview()

    def atualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for conta in self.contas:
            self.tree.insert('', 'end', values=(conta['numero'], conta['titular'], conta['saldo'], conta['banco']))
            
    def aplicar_rendimento(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma conta poupança.")
            return

        item_id = selected_item[0]
        numero_conta = self.tree.item(item_id, 'values')[0]

        # Encontrar a conta selecionada
        conta_selecionada = next((c for c in self.contas if c['numero'] == numero_conta), None)
        if conta_selecionada:
            nome_banco_conta = conta_selecionada['banco'].strip().lower()  # Normalizar o nome do banco
            taxa_juro = self.bancos.get(nome_banco_conta, 0)

            if taxa_juro:
                saldo_atual = float(conta_selecionada['saldo'])
                novo_saldo = saldo_atual * (1 + taxa_juro / 100)
                conta_selecionada['saldo'] = f"{novo_saldo:.2f}"

                self.salvar_contas()
                self.atualizar_treeview()
                messagebox.showinfo("Rendimento Aplicado", "O rendimento foi aplicado com sucesso.")
            else:
                messagebox.showwarning("Banco Não Encontrado", f"Banco '{conta_selecionada['banco']}' não encontrado para a conta.")
        else:
            messagebox.showwarning("Conta Não Encontrada", "Não foi possível encontrar a conta selecionada.")

    def salvar_contas(self):
        if os.path.exists('bancoapp/contas.json'):
            with open('bancoapp/contas.json', 'r', encoding='utf-8') as f:
                contas_data = json.load(f)

            # Atualiza as contas poupança no arquivo original
            for conta in contas_data:
                if conta['tipo'] == "Conta Poupança":
                    for c in self.contas:
                        if c['numero'] == conta['numero']:
                            conta['saldo'] = c['saldo']

            # Salva as contas atualizadas no arquivo JSON
            with open('bancoapp/contas.json', 'w', encoding='utf-8') as f:
                json.dump(contas_data, f, indent=4, ensure_ascii=False)
