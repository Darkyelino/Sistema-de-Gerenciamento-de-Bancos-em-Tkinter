# Atualizações e Melhorias do Sistema de Gerenciamento de Banco com Tkinter

Este documento detalha as atualizações realizadas no Sistema de Gerenciamento de Bancos em Tkinter desenvolvido para a disciplina de TESI no curso de Sistemas de Informação na UFAC. As alterações incluem a adição de novas funcionalidades, correções de bugs e melhorias na organização do código. A seguir, descrevemos cada mudança em detalhes, relacionando-a diretamente com o comportamento do sistema e os códigos envolvidos.

1. Novas Funcionalidades
    - Interface Gráfica com Tkinter:
      O sistema agora possui uma interface gráfica completa, implementada usando o módulo Tkinter. A interface inicial é definida na classe Tela, localizada no arquivo main.py. A classe configura a janela principal da aplicação com tamanho, título e uma imagem de boas-vindas:

```
self.janela.title("Sistema Bancário Siri")
self.janela.geometry("700x500")
self.janela.config(bg="#D3D3D3")
self.img = tk.PhotoImage(file='bancoapp/siri.png')  # Adição da imagem de boas-vindas.
```
A interface inclui menus para navegação e instanciamento de novas janelas para gerenciar Banco, Conta, e Cliente, com cada funcionalidade sendo tratada em janelas separadas.

2. Menu de Entidades e Ações
    - Menus: O menu principal da aplicação é criado na função home da classe Tela, onde se utilizam Menu e add_cascade para vincular submenus às entidades Banco, Conta, Cliente, além de ações como Depósito & Saque e Render:

```
self.menu_entidades = tk.Menu(self.menu_barra, tearoff=0)
self.menu_barra.add_cascade(label="Menu", menu=self.menu_entidades)
self.menu_entidades.add_command(label="Banco", command=self.banco_menu.banco)
self.menu_entidades.add_command(label="Conta", command=self.conta_menu.conta)
self.menu_entidades.add_command(label="Cliente", command=self.cliente_menu.cliente)
```
Cada comando no menu é vinculado a uma função que instância uma nova janela, oferecendo ao usuário uma interface intuitiva para manipular as diferentes entidades.

3. Cadastro e Gerenciamento de Bancos
    - Bancos: A classe BancoMenu é responsável por gerenciar o cadastro, edição e exclusão de bancos. As funcionalidades implementadas incluem:
      - Adicionar Banco: A função adicionar_banco verifica se o número do banco já existe e, em seguida, cria um novo banco com base nos valores dos campos Entry. O método salva as informações no arquivo bancoapp/bancos.json.
      - Salvar e Carregar Dados de Bancos: Os métodos salvar_bancos e carregar_bancos realizam a persistência dos dados em um arquivo JSON. Isso garante que as informações sejam mantidas entre diferentes sessões.

```
if self.banco_existente(numero_banco):
    messagebox.showwarning("Número de Banco Duplicado", "O número do banco já existe.")
```
```
def salvar_bancos(self):
    with open('bancoapp/bancos.json', 'w') as f:
        bancos_data = [{'numero_banco': banco.numero_banco, 'nome_banco': banco.nome_banco, 'taxa_juro': banco.taxa_juro, 'desconto': banco.desconto} for banco in self.bancos]
        json.dump(bancos_data, f, indent=4)
```
Esses métodos também são utilizados para atualizar a Treeview que exibe todos os bancos cadastrados na interface gráfica.

4. Cadastro e Gerenciamento de Contas
    - Contas: A classe ContaMenu implementa o gerenciamento de contas bancárias, permitindo adicionar, editar e excluir contas. As principais funções incluem:
      - Adicionar Conta: A função adicionar_conta gera um número único automaticamente e atribui a conta a um cliente e banco específico. Utiliza um Combobox para garantir a seleção correta do cliente e banco.
      - Saque e Depósito: O método saquedeposito é utilizado para registrar operações financeiras nas contas, com a possibilidade de aplicar uma taxa de desconto para Conta Corrente. Cada operação é registrada em um arquivo .txt associado à conta:


```
self.tipo_conta = ttk.Combobox(self.nova_janela, values=["Conta Corrente", "Conta Poupança"], state="readonly")
```
```
self.registrar_operacao(conta, "Depósito", valor)
```
Esse sistema garante que o usuário tenha um histórico de todas as operações realizadas, com as informações de saldo e valor do depósito/saldo atualizados após cada operação.

5. Cadastro e Gerenciamento de Clientes
    - Clientes: O gerenciamento de clientes é feito pela classe ClienteMenu. Cada cliente possui um número único e é associado a um CPF e endereço. As funcionalidades implementadas incluem:
      - Adicionar Cliente: Utiliza entradas Entry para registrar o nome, endereço e CPF. O número de cliente é gerado automaticamente por meio do método gerar_numero_conta().
      - Verificação de Dependências: Antes de excluir um cliente, a aplicação verifica se há contas associadas a ele. Caso existam, a remoção é bloqueada.

```
self.clientes.append(Cliente(numero, nome, endereco, cpf))
```
```
contas_associadas = [conta for conta in self.contas if conta.titular == nome_cliente]
```
Essa verificação é feita para manter a integridade das informações e evitar inconsistências nos dados.
6. Função de Rendimento para Contas Poupança
    - Rendimento: A classe ContaPoupancaMenu permite aplicar rendimento sobre o saldo das contas poupança. A taxa de juros é definida para cada banco e aplicada apenas a contas do tipo Conta Poupança:
```
novo_saldo = saldo_atual * (1 + taxa_juro / 100)
```
Após aplicar o rendimento, a atualização do saldo é persistida no arquivo JSON contas.json e exibida na Treeview do sistema.

7. Correções de Bugs
  - Correção no Salvamento de Dados: Ajuste no salvamento e carregamento de dados, garantindo que alterações realizadas em uma sessão sejam mantidas e recuperadas corretamente.
  - Exclusão de Contas e Clientes: Correção da lógica de exclusão, verificando condições específicas (saldo zerado para contas e ausência de contas para clientes).

8. Refatorações no Código
  - Melhorias na Estrutura das Classes: Organização das classes Banco, Conta e Cliente para facilitar o entendimento e manutenção. Métodos auxiliares foram criados para lidar com tarefas específicas, como carregar e salvar arquivos JSON.
  - Utilização de Combobox para Seleção Dinâmica: Substituição de entradas Entry por Combobox para campos de seleção, melhorando a usabilidade e eliminando erros de digitação pelo usuário.

9. Detalhes Técnicos e Estrutura do Projeto
O projeto foi organizado conforme a seguinte estrutura:

```
└── bancoapp/
    ├── banco_menu.py            # Módulo de gerenciamento de bancos
    ├── cliente_menu.py          # Módulo de gerenciamento de clientes
    ├── conta_menu.py            # Módulo de gerenciamento de contas
    ├── rendimento.py            # Módulo para operações de rendimento de contas poupança
    ├── saquedeposito.py         # Módulo para operações de saque e depósito
    ├── main.py                  # Arquivo principal da aplicação
    ├── bancos.json          # Dados de bancos
    ├── contas.json          # Dados de contas
    ├── clientes.json        # Dados de clientes
    └── siri.png             # Imagem usada na interface gráfica do sistema
```
