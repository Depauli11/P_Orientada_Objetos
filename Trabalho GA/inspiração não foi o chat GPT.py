import csv
from datetime import datetime

class Quarto:
    def __init__(self, numero, tipo, disponivel=True, consumo=list):
        self.numero = numero
        self.tipo = tipo
        self.disponivel = disponivel
        self.consumo = consumo

    def __str__(self):
        return f"Quarto {self.numero} - Tipo: {self.tipo}, Disponível: {'Sim' if self.disponivel else 'Não'}"

class Reserva:
    def __init__(self, cliente, quarto, data_inicial, data_final, ativa=True):
        self.cliente = cliente
        self.quarto = quarto
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.ativa = ativa

    def verificar_disponibilidade(self, data):
        """Verifica se a reserva está ativa e se a data está dentro do período da reserva."""
        return self.ativa and self.data_inicial <= data <= self.data_final

    def __str__(self):
        return f"Reserva para {self.cliente} - Quarto: {self.quarto.numero}, Data: {self.data_inicial} até {self.data_final}"

class Cliente:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class Pousada:
    def __init__(self):
        self.quartos = []
        self.reservas = []
        self.produtos = []

    def salvar_dados(self):
        """Salva os dados em arquivos CSV."""
        self.salvar_quartos("quarto.csv")
        self.salvar_reservas("reserva.csv")
        self.salvar_produtos("produto.csv")

    def salvar_quartos(self, filename):
        """Salva os dados dos quartos em um arquivo CSV."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for quarto in self.quartos:
                writer.writerow([quarto.numero, quarto.tipo, quarto.disponivel])

    def salvar_reservas(self, filename):
        """Salva os dados das reservas em um arquivo CSV."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for reserva in self.reservas:
                writer.writerow([reserva.cliente.nome, reserva.quarto.numero, reserva.data_inicial.strftime("%Y-%m-%d"), reserva.data_final.strftime("%Y-%m-%d"), reserva.ativa])

    def salvar_produtos(self, filename):
        """Salva os dados dos produtos em um arquivo CSV."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for produto in self.produtos:
                writer.writerow([produto.nome, produto.preco])

    def carregar_dados(self):
        """Carrega os dados dos arquivos CSV."""
        self.carregar_quartos("quarto.csv")
        self.carregar_reservas("reserva.csv")
        self.carregar_produtos("produto.csv")

    def carregar_quartos(self, filename):
        """Carrega os dados dos quartos do arquivo CSV."""
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                numero, tipo, disponivel, consumo = row
                quarto = Quarto(int(numero), tipo, disponivel=="True", consumo)
                self.quartos.append(quarto)

    def carregar_reservas(self, filename):
        """Carrega os dados das reservas do arquivo CSV."""
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                cliente_nome, quarto_numero, data_inicial_str, data_final_str, ativa_str = row
                cliente = Cliente(cliente_nome)
                quarto = self.encontrar_quarto_por_numero(int(quarto_numero))
                data_inicial = datetime.strptime(data_inicial_str, "%Y-%m-%d").date()
                data_final = datetime.strptime(data_final_str, "%Y-%m-%d").date()
                ativa = ativa_str == "True"
                reserva = Reserva(cliente, quarto, data_inicial, data_final, ativa)
                self.reservas.append(reserva)

    def carregar_produtos(self, filename):
        """Carrega os dados dos produtos do arquivo CSV."""
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                nome, preco = row
                produto = Produto(nome, float(preco))
                self.produtos.append(produto)

    def encontrar_quarto_por_numero(self, numero):
        """Encontra um quarto pelo número."""
        for quarto in self.quartos:
            if quarto.numero == numero:
                return quarto
        return None

    def consultar_disponibilidade(self, data, numero_quarto):
        """Consulta a disponibilidade de um quarto em uma data específica."""
        quarto = self.encontrar_quarto_por_numero(numero_quarto)
        if not quarto:
            return "Quarto não encontrado."
        
        for reserva in self.reservas:
            if reserva.quarto == quarto and reserva.verificar_disponibilidade(data):
                return f"Quarto não disponível. Reservado por {reserva.cliente} de {reserva.data_inicial} a {reserva.data_final}"
        
        return f"Quarto disponível: {quarto}"

    def consultar_reserva(self, data=None, nome_cliente=None, numero_quarto=None):
        """Consulta reservas com base nos parâmetros fornecidos."""
        resultados = []
        for reserva in self.reservas:
            if (not data or reserva.data_inicial <= data <= reserva.data_final) and \
               (not nome_cliente or nome_cliente.lower() in reserva.cliente.nome.lower()) and \
               (not numero_quarto or reserva.quarto.numero == numero_quarto):
                resultados.append(reserva)
        
        if resultados:
            return resultados
        else:
            return "Nenhuma reserva encontrada."

# Teste do sistema
if __name__ == "__main__":
    pousada = Pousada()
    pousada.carregar_dados()

    while True:
        print("\nMenu:")
        print("1 Consultar disponibilidade")
        print("2 Consultar reserva")
        print("3 Realizar reserva")
        print("4 Cancelar reserva")
        print("5 Realizar check-in")
        print("6 Realizar check-out")
        print("7 Registrar consumo")
        print("8 Salvar")
        print("0 Sair")

        opcao = input("Digite a opção desejada: ")

        if opcao == "1":
            data = input("Digite a data (YYYY-MM-DD): ")
            numero_quarto = int(input("Digite o número do quarto: "))
            data = datetime.strptime(data, "%Y-%m-%d").date()
            print(pousada.consultar_disponibilidade(data, numero_quarto))
        
        elif opcao == "2":
            data = input("Digite a data (YYYY-MM-DD) (opcional): ")
            if data:
                data = datetime.strptime(data, "%Y-%m-%d").date()
            nome_cliente = input("Digite o nome do cliente (opcional): ")
            numero_quarto = input("Digite o número do quarto (opcional): ")
            if numero_quarto:
                numero_quarto = int(numero_quarto)
            print(pousada.consultar_reserva(data, nome_cliente, numero_quarto))

        elif opcao == "3":
            cliente_nome = input("Digite o nome do cliente: ")
            numero_quarto = int(input("Digite o número do quarto: "))
            data_inicial = input("Digite a data inicial da reserva (YYYY-MM-DD): ")
            data_final = input("Digite a data final da reserva (YYYY-MM-DD): ")
            
            cliente = Cliente(cliente_nome)
            quarto = pousada.encontrar_quarto_por_numero(numero_quarto)
            data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d").date()
            data_final = datetime.strptime(data_final, "%Y-%m-%d").date()
            
            reserva = Reserva(cliente, quarto, data_inicial, data_final)
            pousada.reservas.append(reserva)
            print("Reserva realizada com sucesso.")

        elif opcao == "4":
            nome_cliente = input("Digite o nome do cliente: ")
            
            for reserva in pousada.reservas:
                if reserva.cliente.nome.lower() == nome_cliente.lower():
                    reserva.ativa = False
                    print("Reserva cancelada com sucesso.")
                    break
            else:
                print("Nenhuma reserva encontrada para esse cliente.")

        elif opcao == "5":
            nome_cliente = input("Digite o nome do cliente: ")
            
            for reserva in pousada.reservas:
                if reserva.cliente.nome.lower() == nome_cliente.lower() and reserva.ativa:
                    reserva.ativa = False
                    print("Check-in realizado com sucesso.")
                    break
            else:
                print("Nenhuma reserva ativa encontrada para esse cliente.")

        elif opcao == "6":
            nome_cliente = input("Digite o nome do cliente: ")
            
            for reserva in pousada.reservas:
                if reserva.cliente.nome.lower() == nome_cliente.lower() and not reserva.ativa:
                    valor_diarias = (reserva.data_final - reserva.data_inicial).days * 100  # Valor da diária fictício
                    valor_consumo = sum(produto.preco for produto in reserva.cliente.consumos)
                    valor_total = valor_diarias + valor_consumo
                    
                    print("Check-out realizado com sucesso.")
                    print(f"Valor das diárias: R${valor_diarias:.2f}")
                    print(f"Valor do consumo: R${valor_consumo:.2f}")
                    print(f"Valor total a ser pago: R${valor_total:.2f}")
                    
                    reserva.ativa = False
                    reserva.cliente.consumos = []
                    break
            else:
                print("Nenhuma reserva em check-out encontrada para esse cliente.")

        elif opcao == "7":
            nome_cliente = input("Digite o nome do cliente: ")
            
            for reserva in pousada.reservas:
                if reserva.cliente.nome.lower() == nome_cliente.lower() and reserva.ativa:
                    for produto in pousada.produtos:
                        print(f"{produto.nome}: R${produto.preco:.2f}")
                    
                    produto_nome = input("Digite o nome do produto: ")
                    
                    for produto in pousada.produtos:
                        if produto.nome.lower() == produto_nome.lower():
                            reserva.cliente.consumos.append(produto)
                            print("Consumo registrado com sucesso.")
                            break
                    else:
                        print("Produto não encontrado.")
                    break
            else:
                print("Nenhuma reserva ativa encontrada para esse cliente.")

        elif opcao == "8":
            pousada.salvar_dados()
            print("Dados salvos com sucesso.")

        elif opcao == "0":
            print("Saindo...")
            break
