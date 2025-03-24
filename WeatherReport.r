#Importando as libs
library(httr)
library(jsonlite)
library(dplyr)
library(tidyr)

#Usando a URL para pegar os dados da API
getapi = GET('https://my.meteoblue.com/packages/basic-day?apikey=JZLlQU0wpFKyrjeS&lat=-23.5475&lon=-46.6361&asl=769&format=json') #DIA TODO
# getapi = GET('https://my.meteoblue.com/packages/basic-1h?apikey=JZLlQU0wpFKyrjeS&lat=-23.5475&lon=-46.6361&asl=769&format=json') #1 HORA

#Lendo o JSON disponibilizado pela API
dados <- fromJSON(rawToChar(getapi$content))

#Criando a média de cada variável e arredondando o resultado
temp  <- round(mean(dados$data_day$temperature_instant), digits = 2)
chance_chuva <- round(mean(dados$data_day$precipitation_probability), digits = 2)
chuva <- round(mean(dados$data_day$precipitation), digits = 2)
vento <- round(mean(dados$data_day$windspeed_mean), digits = 2)

#Criando DF utilizando os dados adquiridos na API 
resultado <- data.frame(temperatura = temp, chance_de_chuva = chance_chuva, qtd_chuva = chuva, velocidade_vento = vento)
print(resultado)
