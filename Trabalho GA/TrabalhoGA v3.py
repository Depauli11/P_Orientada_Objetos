import csv
import os
import platform
import time
from datetime import datetime

class Quarto:
    """Classe representando um Quarto"""
    def __init__(self, numero:int, categoria, diaria=float, consumo=list):
        self.__numero = numero
        self.__categoria = categoria
        self.__diaria = diaria
        self.__consumo = consumo

    @property
    def numero(self):
        """Método getter - quarto.numero"""
        return self.__numero
    @property
    def categoria(self):
        """Método getter - quarto.categoria"""
        return self.__categoria
    @property
    def diaria(self):
        """Método getter - quarto.diaria"""
        return self.__diaria
    @property
    def consumo(self):
        """Método getter - quarto.consumo"""
        return self.__consumo

    def adiciona_consumo(self, codigo, qtd):
        """Método que adiciona um código de produto a 
        uma lista (consumo) x vezes quantidade passada como parâmetro"""
        for i in range(qtd):
            self.__consumo.append(codigo)

    def lista_consumo(self, pousada):
        """Método que printa na tela a lista de consumo do objeto Quarto instanciado"""
        for codigo in self.__consumo:
            produto = pousada.encontra_produto(codigo)
            print(f"   {produto.nome}: R${produto.preco:.2f}")

    def valor_total_consumo(self, pousada):
        """Método que calcula o consumo  total, iterando (for) por todos os códigos 
        do atributo __consumo (lista de códigos)."""
        valor_total = 0.0
        for codigo in self.__consumo:
            produto = pousada.encontra_produto(codigo)
            valor_total += produto.preco
        return valor_total

    def limpa_consumo(self):
        """Método que limpa o atributo consumo (lista)"""
        self.__consumo = []

class Reserva:
    """Classe representando uma Reserva"""
    def __init__(self, cliente, dia_inicio:datetime, dia_fim:datetime, status:str, quarto=Quarto):
        self.__cliente = cliente
        self.__status = status 
        self.__dia_inicio = dia_inicio
        self.__dia_fim = dia_fim
        self.__quarto = quarto

    @property
    def cliente(self):
        """Método getter - reserva.cliente"""
        return self.__cliente

    @property
    def status(self):
        """Método getter - reserva.status"""
        return self.__status

    @property
    def dia_inicio(self):
        """Método getter - reserva.dia_inicio"""
        return self.__dia_inicio

    @property
    def dia_fim(self):
        """Método getter - reserva.dia_fim"""
        return self.__dia_fim

    @property
    def quarto(self):
        """Método getter - reserva.quarto"""
        return self.__quarto

    @cliente.setter
    def cliente(self, cliente):
        """Método setter - cliente"""
        self.__cliente = cliente

    @status.setter
    def status(self, status):
        """Método setter - status"""
        self.__status = status

    @dia_inicio.setter
    def dia_inicio(self, dia_inicio):
        """Método setter - dia_inicio"""
        self.__dia_inicio = dia_inicio

    @dia_fim.setter
    def dia_fim(self, dia_fim):
        """Método setter - dia_fim"""
        self.__dia_fim = dia_fim

    @quarto.setter
    def quarto(self, quarto):
        """Método setter - quarto"""
        self.__quarto = quarto

class Produto:
    """Classe representando um Produto"""
    def __init__(self, codigo:int, nome, preco=float):
        self.__codigo = codigo
        self.__nome = nome
        self.__preco = preco

    @property
    def codigo(self):
        """Método getter - produto.codigo"""
        return self.__codigo
    @property
    def nome(self):
        """Método getter - produto.nome"""
        return self.__nome
    @property
    def preco(self):
        """Método getter - produto.preco"""
        return self.__preco

class Pousada:
    """Classe representando uma Pousada"""
    def __init__(self, nome, contato):
        self.__nome = nome
        self.__contato = contato
        self.__quartos = []
        self.__reservas = []
        self.__produtos = []

    @property
    def reservas(self):
        """Método getter - pousada.reservas"""
        return self.__reservas
    @property
    def quartos(self):
        """Método getter - pousada.quartos"""
        return self.__quartos
    @property
    def nome(self):
        """Método getter - pousada.nome"""
        return self.__nome
    @property
    def produtos(self):
        """Método getter - pousada.produtos"""
        return self.__produtos

    def encontra_quarto(self, numero):
        """ Método que busca e retorna o objeto do tipo Quarto equivalente ao número 
        do quarto que é passado como parametro, retorna None se não encontrar."""
        for quarto in self.__quartos:
            if quarto.numero == int(numero):
                return quarto
        return None

    def encontra_produto(self, codigo):
        """ Método que Busca e retorna o objeto do tipo Produto equivalente ao código 
        do produto que é passado como parametro, retorna None se não encontrar."""
        for produto in self.__produtos:
            if produto.codigo == int(codigo):
                return produto
        return None

    def consulta_disponibilidade(self, dt_inicio, dt_fim, quarto):
        """ Método que verifica a disponibilidade de um quarto 
        em um intervalo de datas específico."""
        for reserva in self.__reservas:
            if reserva.quarto == quarto:
                if (reserva.dia_inicio >= dt_inicio and reserva.dia_inicio <= dt_fim) \
                        and reserva.status in ["A","I"]:
                    return False
                elif (reserva.dia_fim >= dt_fim and reserva.dia_fim <= dt_fim) \
                        and reserva.status in ["A","I"]:
                    return False
        return True

    def consulta_reserva(self, cliente=None, dt_inicio=None, dt_fim=None, quarto=None):
        """Método que consulta as reservas ativas baseadas em critérios opcionais: 
        cliente, data de início, data de fim e numero do quarto."""
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
        """Método que cria e adiciona uma nova reserva à lista de reservas da pousada."""
        reserva = Reserva(cliente, dt_inicio, dt_fim, "A", quarto)
        self.__reservas.append(reserva)

    def cancela_reserva(self, cliente):
        """Método que muda o status das reservas de um cliente para Cancelada, dentro da 
        lista de reservas da pousada."""
        reservas = self.consulta_reserva(cliente)
        if reservas:
            for reserva in reservas:
                reserva.status = "C"
            return True
        else:
            return None

    def realiza_checkin(self, cliente):
        """Método que realiza o check-in das reservas ativas de um cliente especificado."""
        reservas = self.consulta_reserva(cliente)
        if reservas:
            for reserva in reservas:
                reserva.status = "I"
            return True
        else:
            return None

    def calcula_dias(self, data_inicio, data_fim):
        """Método que calcula a quantidade total de dias entre a data de início e a data de fim."""
        dias_total = 1+(data_fim - data_inicio).days
        return dias_total

    def consulta_checkin(self, cliente=None, dt_inicio=None, dt_fim=None, quarto=None):
        """Método que consulta todas as reservas com status de check-in com base nos critérios 
        opcionais do cliente, data de início, data de fim e número do quarto."""
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
        """Método que realiza o check-out das reservas com status de check-in de um cliente"""
        reservas = self.consulta_checkin(cliente)
        if reservas:
            for reserva in reservas:
                reserva.status = "O"
            return True
        else:
            return None

    def lista_produto(self):
        """Método que lista todos os produtos do atributo (lista) __produtos"""
        print("Código, Produto, Preço:")
        for produto in self.__produtos:
            print(f"{produto.codigo}.{produto.nome}: {produto.preco}")

    def deserializar(self, arquivo):
        """Retorna uma lista com os objetos do tipo Quarto, Reserva e Produto 
        a partir dos valores de atributo contido nos arquivos CSV de cada um."""
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
                    consumo = [int(linha[i]) for i in range(3, len(linha))] #Loop que transforma tudo após o 3 valor em lista
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

    def carrega_dados(self):
        """Atribui os objetos Quarto, Reserva e Produto deserializados as suas listas na pousada."""
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

    def serializar(self, arquivo):
        """Retorna uma matriz com os valores dos atributos de objetos do tipo Quarto, e Reserva."""
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
                    return reservas_list

    def salva_dados(self):
        """Escreve os atributos dos objetos Quarto e Resserva serializados nos seus arquivos CSV"""
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

def imprime_com_retincencias(msg):
    """Imprime a frase passada no parametro e adiciona reticencias que aparecem uma de cada vez."""
    print(msg, end="", flush=True)
    for i in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    time.sleep(0.3)
    print("")

def limpar_tela():
    """Verifica se o sistema operacional é windows e utiliza o comando "cls" para limpar a tela, 
    caso não for windows, utiliza o comando "clear"."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostra_menu():
    """Imprime o menu de opções."""
    print("1 - Consulta disponibilidade")
    print("2 - Consulta reserva")
    print("3 - Realizar reserva")
    print("4 - Cancelar reserva")
    print("5 - Realizar check-in")
    print("6 - Realizar check-out")
    print("7 - Registrar consumo")
    print("8 - Salvar")
    print("0 - Sair")

def deserializa_pousada(arquivo):
    """Retorna um objeto do tipo Pousada usando os valores do CSV como atributos."""
    with open(arquivo) as f:
        reader = csv.reader(f)
        dados = list(reader)
    pousada_nome = dados[0][0]
    pousada_contato = dados[0][1]
    return Pousada(pousada_nome,pousada_contato)

def data_eh_valida(str_data):
    """Valida se a data esta no formato correto dd-mm-YY"""
    try:
        datetime.strptime(str_data, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def main():
    """Main"""
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
                imprime_com_retincencias("\nQuarto indisponivel nesta data")
                input("\nPressione Enter para voltar ao menu...")

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
                    input("\nPressione Enter para voltar ao menu...")
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
                input("\nPressione Enter para voltar ao menu...")
            elif not pousada.consulta_disponibilidade(dt_inicio, dt_fim, quarto):
                imprime_com_retincencias("\nQuarto esta indisponivel nessa data")
                input("\nPressione Enter para voltar ao menu...")
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
                print("\n\033[32m" + "Reserva Cancelada com sucesso" + "\033[0m")
                input("\nPressione Enter para voltar ao menu...")
            else:
                imprime_com_retincencias(f"\nNão existe reserva ativa no nome de {cliente}")
                input("\nPressione Enter para voltar ao menu...")

        elif escolha == "5":
            limpar_tela()
            print("====== Registrar check-in ======")
            while True:
                cliente = input("Informe o nome do cliente: ")
                if not cliente:
                    print("\n\033[31m" + "ERRO: " + "\033[0m" + "Não foi digitado o nome do cliente\n")
                else:
                    reservas = pousada.consulta_reserva(cliente)
                    if reservas is not None:   
                        reserva = reservas[0]
                        break
                    else: 
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
                imprime_com_retincencias(f"\nNão existe reserva ativa no nome de {cliente}")
                input("\nPressione Enter para voltar ao menu...")

        elif escolha == "6":
            limpar_tela()
            print("Registrar check-out...")
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
            if pousada.realiza_checkout(cliente):     
                print("\n\033[32m" + "Check-out realizado com sucesso" + "\033[0m")
                print(f"Periodo: {reserva.dia_inicio} até {reserva.dia_fim}")
                print(f"Quantidade de dias: {pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)}")
                print(f"Valor diárias: R${pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)*reserva.quarto.diaria:.2f}")
                print(f"Valor consumo (copa): R${reserva.quarto.valor_total_consumo(pousada):.2f}")
                reserva.quarto.lista_consumo(pousada)
                print(f"Valor Total: R${reserva.quarto.valor_total_consumo(pousada)+(pousada.calcula_dias(reserva.dia_inicio, reserva.dia_fim)*reserva.quarto.diaria):.2f}")
                reserva.quarto.limpa_consumo()
                input("\nPressione Enter para voltar ao menu...")
                
            else:
                imprime_com_retincencias(f"\nNão existe check-in ativo no nome de {cliente}")
                input("\nPressione Enter para voltar ao menu...")

        
        elif escolha == "7":
            limpar_tela()
            print("Registrar consumo...")
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
            if pousada.consulta_checkin(cliente):   
                pousada.lista_produto()
                cod_produto = input("\nInforme o código do produto ou pressione Enter para sair: ")
                qtd = int(input("Informe a quantidade: "))
                while cod_produto is not "":   
                    while int(cod_produto) <= len(pousada.produtos) and int(cod_produto) > 0: 
                        if int(cod_produto) > len(pousada.produtos) or int(cod_produto) <= 0:
                            cod_produto = input("\nInforme um código válido: ")
                            qtd = int(input("Informe a quantidade: "))
                        else:
                            reserva.quarto.adiciona_consumo(cod_produto, qtd)
                            produto = pousada.encontra_produto(int(cod_produto))
                            print(f"{produto.nome} x{qtd} adicionado(a) ")
                            break
                    cod_produto = input("\nInforme o código de outro produto ou pressione Enter para sair: ")
                    if cod_produto is not "":
                        qtd = int(input("Informe a quantidade: "))
                        continue

            else:
                imprime_com_retincencias(f"\nNão existe check-in ativo no nome de {cliente}")
                input("\nPressione Enter para voltar ao menu...")

        elif escolha == "8":
            pousada.salva_dados()
            imprime_com_retincencias("\nSalvando dados")
            pousada.carrega_dados()
        elif escolha == "0":
            imprime_com_retincencias("\nSaindo")
            break

if __name__ == '__main__':
    main()
