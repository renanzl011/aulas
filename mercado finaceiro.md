import time
import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

usuarios = {}
acoes_disponiveis = []
usuario_logado = None

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input(Fore.CYAN + "\nPressione Enter para continuar...")

def imprimir_cabecalho(titulo):
    limpar_tela()
    print(Fore.YELLOW + "="*50)
    print(Fore.YELLOW + Style.BRIGHT + titulo.center(50))
    print(Fore.YELLOW + "="*50 + Style.RESET_ALL)

def imprimir_rodape():
    print(Fore.YELLOW + "="*50 + Style.RESET_ALL)

def imprimir_menu(opcoes):
    print(Fore.CYAN + "-"*50)
    for key, desc in opcoes.items():
        print(Fore.GREEN + f" {key} - {Style.BRIGHT}{desc}")
    print(Fore.CYAN + "-"*50)

def mensagem_erro(msg):
    print(Fore.RED + Style.BRIGHT + f"\n❌ Erro: {msg}")
    pausar()

def mensagem_sucesso(msg):
    print(Fore.GREEN + Style.BRIGHT + f"\n✅ {msg}")
    pausar()

def menu_login():
    global usuario_logado
    while True:
        imprimir_cabecalho("MERCADO FINANCEIRO VIRTUAL")
        print(Fore.CYAN + "1 - Entrar")
        print(Fore.CYAN + "2 - Cadastrar Novo Usuário")
        print(Fore.CYAN + "0 - Sair")
        imprimir_rodape()
        escolha = input(Fore.WHITE + "Escolha uma opção: ")

        if escolha == '1':
            usuario = input(Fore.WHITE + "Usuário: ").strip()
            senha = input(Fore.WHITE + "Senha: ").strip()
            if usuario in usuarios and usuarios[usuario]['senha'] == senha:
                usuario_logado = usuario
                mensagem_sucesso(f"Bem-vindo, {usuario}!")
                menu_principal()
            else:
                mensagem_erro("Usuário ou senha incorretos!")

        elif escolha == '2':
            usuario = input(Fore.WHITE + "Novo nome de usuário: ").strip()
            if usuario in usuarios:
                mensagem_erro("Usuário já existe!")
                continue
            senha = input(Fore.WHITE + "Crie uma senha: ").strip()
            usuarios[usuario] = {
                'senha': senha,
                'saldo': 10000.0,
                'carteira': {}
            }
            mensagem_sucesso(f"Usuário '{usuario}' criado com R$ 10.000,00 de saldo!")

        elif escolha == '0':
            print(Fore.MAGENTA + "\nSaindo... Até logo!")
            break
        else:
            mensagem_erro("Opção inválida!")


def menu_principal():
    while True:
        saldo = usuarios[usuario_logado]['saldo']
        imprimir_cabecalho(f"Menu Principal - {usuario_logado}")
        print(Fore.CYAN + f"Saldo Atual: {Fore.YELLOW}R$ {saldo:,.2f}\n")
        opcoes = {
            '1': "Cadastrar Ação",
            '2': "Ver Ações Disponíveis",
            '3': "Comprar Ação",
            '4': "Vender Ação",
            '5': "Ver Minha Carteira",
            '0': "Sair"
        }
        imprimir_menu(opcoes)
        escolha = input(Fore.WHITE + "Escolha uma opção: ")

        if escolha == '1':
            cadastrar_acao()
        elif escolha == '2':
            ver_acoes()
        elif escolha == '3':
            comprar_acao()
        elif escolha == '4':
            vender_acao()
        elif escolha == '5':
            ver_carteira()
        elif escolha == '0':
            print(Fore.MAGENTA + "\nDeslogando...")
            time.sleep(1)
            break
        else:
            mensagem_erro("Opção inválida!")

def cadastrar_acao():
    imprimir_cabecalho("Cadastrar Nova Ação")
    nome = input(Fore.WHITE + "Nome da ação: ").strip()
    if not nome:
        mensagem_erro("Nome inválido.")
        return
    try:
        preco = float(input(Fore.WHITE + "Preço da ação (R$): "))
        if preco <= 0:
            mensagem_erro("Preço deve ser positivo.")
            return
    except ValueError:
        mensagem_erro("Preço inválido.")
        return
    desconto = input(Fore.WHITE + "Tem desconto de 10%? (s/n): ").strip().lower() == 's'

    for acao in acoes_disponiveis:
        if acao['nome'].lower() == nome.lower():
            mensagem_erro("Ação já cadastrada!")
            return

    acoes_disponiveis.append({'nome': nome, 'preco': preco, 'desconto': desconto})
    mensagem_sucesso(f"Ação '{nome}' cadastrada com sucesso!")

def ver_acoes():
    imprimir_cabecalho("Ações Disponíveis")
    if not acoes_disponiveis:
        print(Fore.YELLOW + "Nenhuma ação cadastrada.")
    else:
        print(f"{'Nº':<4}{'Nome':<20}{'Preço (R$)':<15}{'Desconto':<10}")
        print(Fore.YELLOW + "-"*50)
        for i, acao in enumerate(acoes_disponiveis, 1):
            desconto_str = Fore.GREEN + "10%" if acao['desconto'] else Fore.RED + "Não"
            print(f"{i:<4}{acao['nome']:<20}R$ {acao['preco']:<13.2f}{desconto_str}")
    imprimir_rodape()
    pausar()
    
def ver_carteira():
    imprimir_cabecalho("Minha Carteira")
    carteira = usuarios[usuario_logado]['carteira']

    if not carteira:
        print(Fore.YELLOW + "Sua carteira está vazia.")
    else:
        print(f"{'Nº':<4}{'Ação':<20}{'Quantidade':<12}{'Preço Unit. (R$)':<18}{'Valor Total (R$)':<18}")
        print(Fore.YELLOW + "-"*70)

        total_geral = 0.0
        for i, (nome, qtd) in enumerate(carteira.items(), 1):
            
            preco_unit = next((acao['preco'] for acao in acoes_disponiveis if acao['nome'] == nome), None)
            if preco_unit is None:
                preco_unit = 0.0 

            valor_total = preco_unit * qtd
            total_geral += valor_total

            print(f"{i:<4}{nome:<20}{qtd:<12}{preco_unit:>15.2f}  R$  {valor_total:>15.2f}")

        print(Fore.YELLOW + "-"*70)
        print(Fore.CYAN + Style.BRIGHT + f"Valor Total da Carteira: R$ {total_geral:,.2f}")

    imprimir_rodape()
    pausar()

def comprar_acao():
    imprimir_cabecalho("Comprar Ação")
    if not acoes_disponiveis:
        print(Fore.YELLOW + "Nenhuma ação disponível para compra.")
        pausar()
        return

    ver_acoes()
    nome = input(Fore.WHITE + "Digite o nome da ação para comprar: ").strip()
    acao = None
    for a in acoes_disponiveis:
        if a['nome'].lower() == nome.lower():
            acao = a
            break
    if not acao:
        mensagem_erro("Ação não encontrada.")
        return

    try:
        quantidade = int(input(Fore.WHITE + "Quantidade: "))
        if quantidade <= 0:
            mensagem_erro("Quantidade deve ser positiva.")
            return
    except ValueError:
        mensagem_erro("Quantidade inválida.")
        return

    preco_unit = acao['preco']
    if acao['desconto']:
        preco_unit *= 0.9 

    total = preco_unit * quantidade
    saldo = usuarios[usuario_logado]['saldo']

    if saldo < total:
        mensagem_erro(f"Saldo insuficiente! Precisa de R$ {total:.2f}, mas tem R$ {saldo:.2f}")
        return

    usuarios[usuario_logado]['saldo'] -= total
    carteira = usuarios[usuario_logado]['carteira']
    carteira[acao['nome']] = carteira.get(acao['nome'], 0) + quantidade

    mensagem_sucesso(f"Comprou {quantidade}x {acao['nome']} por R$ {total:.2f}")

def vender_acao():
    imprimir_cabecalho("Vender Ação")
    carteira = usuarios[usuario_logado]['carteira']
    if not carteira:
        mensagem_erro("Você não possui ações para vender.")
        return

    print(f"{'Nº':<4}{'Ação':<20}{'Quantidade':<10}")
    print(Fore.YELLOW + "-"*40)
    for idx, (nome, qtd) in enumerate(carteira.items(), 1):
        print(f"{idx:<4}{nome:<20}{qtd:<10}")

    try:
        escolha = int(input(Fore.WHITE + "Escolha o número da ação para vender: ")) - 1
        if escolha < 0 or escolha >= len(carteira):
            mensagem_erro("Opção inválida!")
            return
    except ValueError:
        mensagem_erro("Opção inválida!")
        return

    nome_acao = list(carteira.keys())[escolha]
    quantidade_possui = carteira[nome_acao]
    preco_unit = next(acao['preco'] for acao in acoes_disponiveis if acao['nome'] == nome_acao)

    try:
        quantidade_venda = int(input(Fore.WHITE + f"Quantidade de {nome_acao} para vender (Você possui {quantidade_possui}): "))
        if quantidade_venda <= 0 or quantidade_venda > quantidade_possui:
            mensagem_erro("Quantidade inválida para venda.")
            return
    except ValueError:
        mensagem_erro("Quantidade inválida.")
        return

    total_venda = preco_unit * quantidade_venda
    usuarios[usuario_logado]['saldo'] += total_venda
    carteira[nome_acao] -= quantidade_venda

if __name__ == "__main__":
    menu_login()
