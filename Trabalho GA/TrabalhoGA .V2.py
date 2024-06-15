import csv
import os
import platform
import time
from datetime import datetime

class Quarto:
    def __init__(self, numero:int, categoria, diaria=float, consumo=list):
        self.__numero = numero
        self.__categoria = categoria
        self.__diaria = diaria
        self.__consumo = consumo

    @property
    def numero(self):
        return self.__numero
    @property
    def categoria(self):
        return self.__categoria
    @property
    def diaria(self):
        return self.__diaria
    @property
    def consumo(self):
        return self.__consumo

    def adiciona_consumo(self, codigo):
        self.__consumo.append(codigo)

    def lista_consumo(self, pousada):
        fproduto, fvalor = "PRODUTO:", "VALOR:"
        print(f"{fproduto:<12}  {fvalor}")
        for codigo in self.__consumo:
            produto = pousada.encontra_produto(codigo)
            print(f"{produto.nome:<12}  R${produto.preco:.2f}")

    def valor_total_consumo(self, pousada):
        valor_total = 0.0
        for codigo in self.__consumo:
            produto = pousada.encontra_produto(codigo)
            valor_total += produto.preco
        return valor_total
    
    def limpa_consumo(self):
        self.__consumo = []

class Reserva:
    def __init__(self, cliente, dia_inicio:datetime, dia_fim:datetime, status:str, quarto=Quarto):
        self.__cliente = cliente
        self.__status = status #Os status das reservas são: A/C/I/O - Ativa, Cancelada, Check-In, Check-Out.
        self.__dia_inicio = dia_inicio
        self.__dia_fim = dia_fim
        self.__quarto = quarto

    @property
    def cliente(self):
        return self.__cliente
    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        self.__status = status
    @property
    def dia_inicio(self):
        return self.__dia_inicio
    @dia_inicio.setter
    def dia_inicio(self, dia_inicio):
        self.__dia_inicio = dia_inicio
    @property
    def dia_fim(self):
        return self.__dia_fim
    @dia_fim.setter
    def dia_fim(self, dia_fim):
        self.__dia_fim = dia_fim
    @property
    def quarto(self):
        return self.__quarto
    @quarto.setter
    def quarto(self, quarto):
        self.__quarto = quarto
    
class Produto:
    def __init__(self, codigo:int, nome, preco=float):
        self.__codigo = codigo
        self.__nome = nome
        self.__preco = preco

    @property
    def codigo(self):
        return self.__codigo
    @property
    def nome(self):
        return self.__nome
    @property
    def preco(self):
        return self.__preco

class Pousada:
    def __init__(self, nome, contato):
        self.__nome = nome
        self.__contato = contato
        self.__quartos = []
        self.__reservas = []
        self.__produtos = []

    @property
    def reservas(self):
        return self.__reservas
    @property
    def quartos(self):
        return self.__quartos
    @property
    def nome(self):
        return self.__nome
    @property
    def produtos(self):
        return self.__produtos
    
    # Busca e retorna o objeto do tipo Quarto equivalente ao numero do quarto que é passado como parametro, retorna None se não encontrar.
    def encontra_quarto(self, numero):
        for quarto in self.__quartos:
            if quarto.numero == int(numero):
                return quarto
        return None
  
    #Busca e retorna o objeto do tipo Produto equivalente ao código do produto que é passado como parametro, retorna None se não encontrar.
    def encontra_produto(self, codigo):
        for produto in self.__produtos:
            if produto.codigo == int(codigo):
                return produto
        return None
    
    def consulta_disponibilidade(self, dt_inicio, dt_fim, quarto):
        for reserva in self.__reservas:
            if reserva.quarto == quarto:
                if (reserva.dia_inicio >= dt_inicio and reserva.dia_inicio <= dt_fim) and reserva.status in ["A","I"]:
                    return False
                elif (reserva.dia_fim >= dt_fim and reserva.dia_fim <= dt_fim) and reserva.status in ["A","I"]:
                    return False
        return True
                
    def consulta_reserva(self, cliente=None, dt_inicio=None, dt_fim=None, quarto=None):
        reservas_list = []
        for reserva in self.__reservas:
            if not cliente and not dt_inicio and not dt_fim and not quarto:
                continue
            elif (not cliente or cliente.lower() == reserva.cliente.lower())\
                and (not dt_inicio or dt_inicio == reserva.dia_inicio)\
                and (not dt_fim or dt_fim == reserva.dia_fim)\
                and (not quarto or int(quarto) == reserva.quarto.numero)\
                and reserva.status == "A":
                reservas_list.append(reserva)
        if reservas_list:
            return reservas_list
        else:
            return None

    def realiza_reserva(self, cliente, dt_inicio, dt_fim, quarto):
        reserva = Reserva(cliente, dt_inicio, dt_fim, "A", quarto)
        self.__reservas.append(reserva)

    def cancela_reserva(self, cliente):
        reservas = self.consulta_reserva(cliente)
        if reservas:
            for reserva in reservas:
                reserva.status = "C"
            return True
        else:
            return None

    def realiza_checkin(self, cliente):
        reservas = self.consulta_reserva(cliente)
        if reservas:
            for reserva in reservas:
                reserva.status = "I"
            return True
        else:
            return None

    def calcula_dias(self, data_inicio, data_fim):
        dias_total = 1+(data_fim - data_inicio).days
        return dias_total
        
    def consulta_checkin(self, cliente=None, dt_inicio=None, dt_fim=None, quarto=None):
        reservas_list = []
        for reserva in self.__reservas:
            if not cliente and not dt_inicio and not dt_fim and not quarto:
                continue
            elif (not cliente or cliente.lower() == reserva.cliente.lower())\
                and (not dt_inicio or dt_inicio == reserva.dia_inicio)\
                and (not dt_fim or dt_fim == reserva.dia_fim)\
                and (not quarto or int(quarto) == reserva.quarto.numero)\
                and reserva.status == "I":
                reservas_list.append(reserva)
        if reservas_list:
            return reservas_list
        else:
            return None
        
    def realiza_checkout(self, cliente):
        reservas = self.consulta_checkin(cliente)
        if reservas:
            for reserva in reservas:
                reserva.status = "O"
            return True
        else:
            return None
        
    def lista_produto(self):
        print("Código, Produto, Preço:")
        for produto in self.__produtos:
            print(f"{produto.codigo}.{produto.nome}: {produto.preco}")
                
    # Retorna uma lista com os objetos do tipo Quarto, Reserva e Produto a partir dos valores de atributo contido nos arquivos CSV de cada um.
    def deserializar(self, arquivo):
        with open(arquivo) as f:
            reader = csv.reader(f)
            dados = list(reader)
        match arquivo:
            case "quarto.csv":
                quartos_list = []
                for linha in dados:
                    numero = linha[0]
                    categoria = linha[1]
                    diaria = linha[2]
                    consumo = [int(linha[i]) for i in range(3, len(linha))] # <-- Loop que transforma qualquer coisa apos o 3 valor em um lista
                    quarto = Quarto(int(numero), str(categoria), float(diaria), consumo)
                    quartos_list.append(quarto)
                return quartos_list
            case "reserva.csv":
                reservas_list = []
                for linha in dados:
                    cliente, dia_inicio, dia_fim, status, numero_quarto = linha
                    data_inicio = datetime.strptime(dia_inicio, "%d-%m-%Y").date()
                    data_fim = datetime.strptime(dia_fim, "%d-%m-%Y").date()
                    quarto = self.encontra_quarto(numero_quarto)
                    reserva = Reserva(str(cliente), data_inicio, data_fim, str(status), quarto)
                    reservas_list.append(reserva)
                return reservas_list
            case "produto.csv":
                produtos_list = []
                for linha in dados:
                    codigo, nome, preco = linha
                    produto = Produto(int(codigo), str(nome), float(preco))
                    produtos_list.append(produto)
                return produtos_list
            
    # Atribui os objetos Quarto, Reserva e Produto deserializados as suas listas na pousada
    def carrega_dados(self):
        self.__quartos = []
        quartos = self.deserializar("quarto.csv")
        for obj in quartos:
            self.__quartos.append(obj)

        self.__reservas = []
        reservas = self.deserializar("reserva.csv")
        for obj in reservas:
            self.__reservas.append(obj)

        self.__produtos = []
        produtos = self.deserializar("produto.csv")
        for obj in produtos:
            self.__produtos.append(obj)

    # Retorna uma matriz com os valores dos atributos de objetos do tipo Quarto, e Reserva
    def serializar(self, arquivo):
        match arquivo:
            case "quarto.csv":
                quartos_list = []
                for quarto in self.__quartos:
                    linha = [quarto.numero, quarto.categoria, quarto.diaria]
                    for consumo in quarto.consumo:      # <-- Loop para serializar a lista de consumo que está no objeto quarto
                        linha.append(consumo)
                    quartos_list.append(linha)
                return quartos_list
            case "reserva.csv":
                reservas_list = []
                for reserva in self.__reservas:
                    data_inicio = reserva.dia_inicio.strftime("%d-%m-%Y")
                    data_fim = reserva.dia_fim.strftime("%d-%m-%Y")
                    linha = [reserva.cliente, data_inicio, data_fim, reserva.status, reserva.quarto.numero]
                    reservas_list.append(linha)
                return(reservas_list)
    
    # Escreve os atributos dos objetos Quarto e Resserva serializados nos seus arquivos CSV
    def salva_dados(self):
        quartos = self.serializar("quarto.csv")
        with open("quarto.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(quartos)

        reservas = self.serializar("reserva.csv")
        reservas_ativas = []
        for reserva in reservas:
            if reserva[3] not in ["C","O"]:
                reservas_ativas.append(reserva)
        with open("reserva.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(reservas_ativas)

# Imprime a frase passada no parametro e adiciona reticencias que aparecem uma de cada vez.
def imprime_com_retincencias(msg):
    print(msg, end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="")
    time.sleep(0.5)

# Verifica se o sistema operacional é windows e utiliza o comando "cls" para limpar a tela, caso não for windows, utiliza o comando "clear".
def limpar_tela():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Imprime o menu de opções
def mostra_menu():
    print("1 - Consulta disponibilidade")
    print("2 - Consulta reserva")
    print("3 - Realizar reserva")
    print("4 - Cancelar reserva")
    print("5 - Realizar check-in")
    print("6 - Realizar check-out")
    print("7 - Registrar consumo")
    print("8 - Salvar")
    print("0 - Sair")

# Retorna um objeto do tipo Pousada usando os valores do CSV como atributos
def deserializa_pousada(arquivo):
    with open(arquivo) as f:
        reader = csv.reader(f)
        dados = list(reader)
    pousada_nome = dados[0][0]
    pousada_contato = dados[0][1]
    return Pousada(pousada_nome,pousada_contato)

def data_eh_valida(str_data):
    try:
        datetime.strptime(str_data, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def main():
    pousada = deserializa_pousada("pousada.csv")
    pousada.carrega_dados()

    while True:
        limpar_tela()
        print(f"====== Pousada {pousada.nome} ======")
        mostra_menu()

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            limpar_tela()
            print("====== Consulta de disponibilidade ======")
            while True:
                str_dt_inicio = input("Data inicial da reserva (DD-MM-AAAA): ")
                str_dt_fim = input("Data final da reserva (DD-MM-YYYY): ")
                if data_eh_valida(str_dt_inicio) and data_eh_valida(str_dt_fim):
                    dt_inicio = datetime.strptime(str_dt_inicio, "%d-%m-%Y").date()
                    dt_fim = datetime.strptime(str_dt_fim, "%d-%m-%Y").date()
                    break
                else:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi possivel verificar a data, certifique-se que é uma data valida no formato correto (DD-MM-AAAA)\n")
            while True:
                num_quarto = input("Numero do quarto: ")
                if not num_quarto or num_quarto.isalpha():
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o número de um quarto\n")
                else:
                    quarto = pousada.encontra_quarto(num_quarto)
                    if quarto:
                        break
                    else:
                        print("\n\033[31m" + "ERRO: " + "\033[0m" + "Esse quarto não existe\n")
            if pousada.consulta_disponibilidade(dt_inicio, dt_fim, quarto):
                if quarto.categoria == "S":
                    categoria = "Standart"
                elif quarto.categoria == "M":
                    categoria = "Master"
                else:
                    categoria = "Premium"
                print("\n\033[32m" + "Quarto disponivel :)" + "\033[0m")
                print(f"Numero: {quarto.numero}")
                print(f"Categoria: {quarto.categoria}")
                print(f"Valor da diaria: R${quarto.diaria:.2f}")
                input("\nPressione Enter para voltar ao menu...")
            else:
                imprime_com_retincencias("\nQuarto indisponivel nesa data")

        elif escolha == "2":
            limpar_tela()
            print("====== Consulta de reserva ======")
            while True:
                cliente = input("Nome do cliente: ")
                while True:
                    str_dt_inicio = input("Data inicial reserva (DD-MM-YYYY): ")
                    if data_eh_valida(str_dt_inicio):
                        dt_inicio = datetime.strptime(str_dt_inicio, "%d-%m-%Y").date()
                        break
                    elif not str_dt_inicio:
                        dt_inicio = None
                        break
                    else:
                        print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi possivel verificar a data, certifique-se que é uma data valida no formato correto (DD-MM-AAAA)\n")
                while True:
                    str_dt_fim = input("Data final reserva (DD-MM-YYYY): ")
                    if data_eh_valida(str_dt_fim):
                        dt_fim = datetime.strptime(str_dt_fim, "%d-%m-%Y").date()
                        break
                    elif not str_dt_fim:
                        dt_fim = None
                        break
                    else:
                        print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi possivel verificar a data, certifique-se que é uma data valida no formato correto (DD-MM-AAAA)\n")
                while True:
                    quarto = input("Numero do quarto: ")
                    if not quarto:
                        break
                    elif pousada.encontra_quarto(quarto):
                        break
                    else:
                        print("\n\033[31m" + "ERRO: " + "\033[0m" + "Esse quarto não existe\n")
                reservas = pousada.consulta_reserva(cliente, dt_inicio, dt_fim, quarto)
                if not cliente and not dt_inicio and not dt_fim and not quarto:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Pelo menos uma informação deve ser fornecida\n")
                elif reservas:
                    for reserva in reservas:
                        if reserva.quarto.categoria == "S":
                            categoria = "Standart"
                        elif reserva.quarto.categoria == "M":
                            categoria = "Master"
                        else:
                            categoria = "Premium"
                        print("\n\033[32m" + "Reservas encontadas:" + "\033[0m")
                        print(f"Cliente: {reserva.cliente}")
                        print(f"Periodo: {reserva.dia_inicio} até {reserva.dia_fim}")
                        print("Quarto:")
                        print(f"    Numero: {reserva.quarto.numero}")
                        print(f"    Categoria: {reserva.quarto.categoria}")
                        print(f"    Diaria: R${reserva.quarto.diaria:.2f}\n")
                    input("Pressione Enter para voltar ao menu...")
                    break
                else:
                    imprime_com_retincencias("\nNão foram encontradas reservas ativas")
                    break
                
        elif escolha == "3":
            limpar_tela()
            print("====== Realizar reserva ======")
            while True:
                cliente = input("Informe o nome do cliente: ")
                if not cliente:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o nome do cliente\n")
                else:
                    break
            while True:
                str_dt_inicio = input("Data inicial da reserva: ")
                str_dt_fim = input("Data final da reserva: ")
                if data_eh_valida(str_dt_inicio) and data_eh_valida(str_dt_fim):
                    dt_inicio = datetime.strptime(str_dt_inicio, "%d-%m-%Y").date()
                    dt_fim = datetime.strptime(str_dt_inicio, "%d-%m-%Y").date()
                    break
                else:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi possivel verificar a data, certifique-se que é uma data valida no formato correto (DD-MM-AAAA)\n")
            while True:
                num_quarto = input("Numero do quarto: ")
                if not num_quarto or num_quarto.isalpha():
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o número de um quarto\n")
                else:
                    quarto = pousada.encontra_quarto(num_quarto)
                    if quarto:
                        break
                    else:
                        print("\n\033[31m" + "ERRO: " + "\033[0m" + "Esse quarto não existe\n")
            if pousada.consulta_reserva(cliente, None, None, None):
                imprime_com_retincencias("\nCliente já possui reserva ativa")
            elif not pousada.consulta_disponibilidade(dt_inicio, dt_fim, quarto):
                imprime_com_retincencias("\nQuarto esta indisponivel nessa data")
            else:
                pousada.realiza_reserva(cliente, dt_inicio, dt_fim, quarto)
                print("\n\033[32m" + "Reserva realizada com sucesso" + "\033[0m")
                input("\nPressione Enter para voltar ao menu...")

        elif escolha == "4":
            limpar_tela()
            print("====== Cancelamento de reserva ======")
            while True:
                cliente = input("Informe o nome do cliente: ")
                if not cliente:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o nome do cliente\n")
                else:
                    break
            if pousada.cancela_reserva(cliente):
                print("\n\033[32m" + "Reserva Cacncelada com sucesso" + "\033[0m")
                input("\nPressione Enter para voltar ao menu...")
            else:
                imprime_com_retincencias(f"\nNão existe reserva ativa no nome de {cliente}")

        elif escolha == "5":
            limpar_tela()
            print("====== Registrar check-in ======")
            time.sleep(1)
            while True:
                cliente = input("Informe o nome do cliente: ")
                if not cliente:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o nome do cliente\n")
                else:
                    reservas = pousada.consulta_reserva(cliente)
                    if reservas is not None:   
                        reserva = reservas[0]
                        break
                    else: # GABRIEL: adicionada essa linha para tratar valores None na variável reserva
                        break
            if pousada.realiza_checkin(cliente):     
                print("\n\033[32m" + "Check-in realizado com sucesso" + "\033[0m")
                print(f"Periodo: {reserva.dia_inicio} até {reserva.dia_fim}")
                print(f"Quantidade de dias: {pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)}")
                print(f"Valor total (diárias): R${pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)*reserva.quarto.diaria:.2f}")
                print("Quarto:")
                print(f"    Numero: {reserva.quarto.numero}")
                print(f"    Categoria: {reserva.quarto.categoria}")
                print(f"    Valor da diaria: R${reserva.quarto.diaria:.2f}")
                input("\nPressione Enter para voltar ao menu...")
            else:
                print(f"\nNão existe reserva ativa no nome de {cliente}")
                input("\nPressione Enter para voltar ao menu...")

        elif escolha == "6":
            limpar_tela()
            print("Registrar check-out...")
            time.sleep(1)
            while True:
                cliente = input("Informe o nome do cliente: ")
                if not cliente:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o nome do cliente\n")
                else:
                    reservas = pousada.consulta_checkin(cliente)
                    if reservas is not None:
                        reserva = reservas[0]
                        break
                    else: 
                        break
            if pousada.realiza_checkout(cliente):     #<-- ADICIONAR LISTA DE CONSUMO
                print("\n\033[32m" + "Check-out realizado com sucesso" + "\033[0m")
                print(f"Periodo: {reserva.dia_inicio} até {reserva.dia_fim}")
                print(f"Quantidade de dias: {pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)}")
                print(f"Valor diárias: R${pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)*reserva.quarto.diaria:.2f}")
                print(f"Valor consumo (copa): R${reserva.quarto.valor_total_consumo(pousada):.2f}")
                print(f"Valor Total: R${reserva.quarto.valor_total_consumo(pousada)+(pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)*reserva.quarto.diaria):.2f}")
                reserva.quarto.limpa_consumo()
                input("\nPressione Enter para voltar ao menu...")
                print(f"Valor consumo (copa): R${reserva.quarto.valor_total_consumo(pousada):.2f}")               

            else:
                print(f"\nNão existe check-in ativo no nome de {cliente}")
                input("\nPressione Enter para voltar ao menu...")

        
        elif escolha == "7":
            limpar_tela()
            print("Registrar consumo...")
            time.sleep(1)
            while True:
                cliente = input("Informe o nome do cliente: ")
                if not cliente:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o nome do cliente\n")
                else:
                    reservas = pousada.consulta_checkin(cliente)
                    if reservas is not None:
                        reserva = reservas[0]
                        break
                    else: 
                        break
            pousada.lista_produto()
            time.sleep(1)
            cod_produto = 0
            while cod_produto <= len(pousada.produtos) or cod_produto >= 0: #<-- AJUSTAR REGISTRO DE CONSUMO
                cod_produto = input("\nInforme o código do produto ou 0 para sair: ")
                if cod_produto is 0:
                    break
                elif cod_produto > len(pousada.produtos) or cod_produto < 0:
                    cod_produto = input("\nInforme um código válido: ")
                else:
                    
                    reserva.quarto.adiciona_consumo(cod_produto)
                    print(f"{pousada.encontra_produto(cod_produto)} Adicionado(a) ")
                    cod_produto = input("\nInforme o código do produto ou 0 para sair: ")

            

        elif escolha == "8":
            pousada.salva_dados()
            imprime_com_retincencias("\nSalvando dados")
            pousada.carrega_dados()
        elif escolha == "0":
            imprime_com_retincencias("\nSaindo")
            break    

if __name__ == '__main__':
    main()