library(jsonlite)
library(dplyr)
library(tidyr)
# Instalar os pacotes
# install.packages("jsonlite")
# install.packages("dplyr")
# install.packages("tidyr")

# Pegando os dados do JSON
dados <- fromJSON("./farm_data.json")

# Transforma os insumos em colunas separadas
dados_com_insumos <- dados %>%
  unnest_wider(crop_inputs)

# Calculando Média e Desvio
resultado <- dados_com_insumos %>%
  select(nitrogênio:zinco) %>%  # Seleciona as colunas de insumos
  summarise(across(everything(), 
                   list(média = ~mean(. , na.rm = TRUE), 
                        desvio = ~sd(. , na.rm = TRUE)))) %>%
  pivot_longer(cols = everything(), 
               names_to = c("insumo", "estatística"), 
               names_sep = "_") %>%
  pivot_wider(names_from = estatística, values_from = value)

resultado_formatado <- resultado %>%
  mutate(across(where(is.numeric), ~sprintf("%.2f", .)))
print(resultado_formatado)