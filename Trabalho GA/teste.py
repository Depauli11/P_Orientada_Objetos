from datetime import datetime

str_data_inicio = "1-2-2020"
str_data_fim = "1-3-2020"

data_inicio = datetime.strptime(str_data_inicio, "%d-%m-%Y")
data_fim = datetime.strptime(str_data_fim, "%d-%m-%Y")

print((data_fim - data_inicio).days)
