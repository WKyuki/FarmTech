# Versão do Python: 3.10.0
# Projeto: FarmTech Solutions
# Comando para instalar o pacote no terminal abaixo:
# pip install openpyxl

import json
import openpyxl
from openpyxl import Workbook


# Etapa b: Cálculo de área de plantio para cada cultura.
def calculate_area(shape, length, width=None):
    """Calcula a área com base no formato, comprimento e largura do terreno."""
    if shape == "retângulo":
        return length * width
    elif shape == "triângulo":
        return 0.5 * length * width
    elif shape == "círculo":
        return 3.1415 * (length ** 2)
    else:
        print("Formato inválido")
        return 0

# Etapa c: Cálculo do manejo de insumos para cada cultura.
def calculate_inputs_per_crop(area, crop):
    """Calcula o total de insumos necessários para a lavoura de acordo com a área e cultura plantada."""

    crops_inputs_catalog = {
    'soja' : {'nitrogênio' : 0.0120, 'fósforo' : 0.0400, 'potássio' : 0.005, 'boro' : 0.0002, 'cobre' : 0.0002, 'manganês' : 0.0006, 'molibdênio' : 0.00004, 'zinco': 0.0006},
    'milho' : {'nitrogênio' : 0.0, 'fósforo' : 0.0500, 'potássio' : 0.005, 'boro' : 0.0002, 'cobre' : 0.0002, 'manganês' : 0.0006, 'molibdênio' : 0.00004, 'zinco': 0.0006},
    'trigo' : {'nitrogênio' : 0.0040, 'fósforo' : 0.0300, 'potássio' : 0.005, 'boro' : 0.0002, 'cobre' : 0.0002, 'manganês' : 0.0006, 'molibdênio' : 0.00004, 'zinco': 0.0006}
    }
    """Relação de quantidades de nutrientes para cada cultura"""

    crop_inputs = {}

    for nutrient, valor in crops_inputs_catalog[crop].items():
        resultado = valor*area
        crop_inputs[nutrient] = resultado
    
    return crop_inputs

# Etapa d: Dados em vetores.
crops = []  # Armazena em um dicionário os dados de cada lavoura.
available_crops = ["milho", "soja", "trigo"] # Relação de culturas suportadas pelo sistema
available_shapes = ["retângulo", "círculo", "triângulo"] # Relação de formatos de terreno suportadas pelo sistema

# Etapa e: Menu de opções.
def main_menu():
    try:
        # Carregue os dados existentes, se houver
        global crops
        crops = load_data()
    except ValueError:
        print("Error loading data.")

    while True:  # Etapa f: Comando de loop e decisão com base no menu de opções.
        print("\n--- FarmTech Solutions Menu ---")
        print("1. Cadastrar nova lavoura")
        print("2. Visualizar lavouras")
        print("3. Atualizar dados da lavoura")
        print("4. Apagar dados")
        print("5. Exportar para Excel")
        print("6. Salvar e sair")

        try:
            choice = int(input("\nEscolha uma opção: "))

            if choice == 1:
                input_data()
            elif choice == 2:
                display_data()
            elif choice == 3:
                update_data()
            elif choice == 4:
                delete_data()
            elif choice == 5:
                export_to_excel()
            # # Etapa e: Menu de opções - Sair do programa
            elif choice == 6:
                save_data()  # Extra: Recurso de persistência de dados.
                print("Finalizando o programa.")
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except ValueError:
            print("Opção inválida. Selecione um número entre 1 e 6.")

# Etapa e: Menu de opções - Entrada de dados.
def input_data():
    try:
        crop_name = input("Digite a cultura que será plantada (milho, soja, trigo): ").lower()
        while (crop_name not in available_crops): # Valida se a cultura digitada é suportada pelo sistema
            print('Nome de cultura inválido')
            crop_name = input("Por favor, selecione uma cultura entre as opções (milho, soja, trigo): ").lower()
        
        shape = input("Selecione o formato da área de plantio (retângulo, triângulo ou círculo): ").lower()
        while (shape not in available_shapes): # Valida se o formato de terrno digitado é suportado pelo sistema
            print('Formato inválido')
            shape = input("Por favor, selecione um formato entre as opções (retângulo, triângulo ou círculo): ").lower()

        length = float(input("Digite o comprimento em m (ou raio caso seja um círculo): "))
        
        width = None
        if shape != "círculo":
            width = float(input("Digite a largura em m: "))
            area = calculate_area(shape, length, width)
        else:
            area = calculate_area(shape, length)
        
        crop_inputs = calculate_inputs_per_crop(area, crop_name)
        
        # Armazene todas as informações em um dicionário
        crop_data = {
            "name": crop_name,
            "shape": shape,
            "length": length,
            "width": width,
            "area": area,
            "crop_inputs" : crop_inputs
        }
        crops.append(crop_data)
        
    except ValueError:
        print("Invalid input. Please provide numeric values where expected.")

# Etapa e: Menu de opções - Saída de dados no terminal.
def display_data():
    print("\nDados atuais:")
    for i, crop in enumerate(crops):
        
        if (crop['shape'] == "círculo"):
        
            print(f"""
Lavoura {i+1} 
Cultura: {crop['name']} 
Formato: {crop['shape']} 
Raio: {crop['length']}m  
Área: {crop['area']}m²
Insumos necessários para adubação:""")
        
        else:

            print(f"""
Lavoura {i+1} 
Cultura: {crop['name']} 
Formato: {crop['shape']} 
Comprimento: {crop['length']}m 
Largura: {crop['width']}m 
Área: {crop['area']}m²
Insumos necessários para adubação:""")
            
        for nutriente, valor in crop['crop_inputs'].items():
            print(f"-> Quantidade de {nutriente}: {valor:.4f} Kg")

# Etapa e: Menu de opções - Atualização de dados.
def update_data():
    try:
        index = (int(input("Digite o índice da lavoura que será atualizada: "))-1)
        if 0 <= index < len(crops):
            new_crop_name = input("Digite o nome da nova cultura que será plantada (milho, soja, trigo): ")
            while (new_crop_name not in available_crops): # Valida se a cultura digitada é suportada pelo sistema
                print('Nome de cultura inválido')
                new_crop_name = input("Por favor, selecione uma cultura entre as opções (milho, soja, trigo): ").lower()
            crops[index]["name"] = new_crop_name

            # Atualizar forma e recalcular com base na nova forma
            shape = input("Selecione o novo formato da área de plantio (retângulo, triângulo ou círculo): ").lower()
            while (shape not in available_shapes): # Valida se o formato digitado é suportado pelo sistema
                print('Formato inválido')
                shape = input("Por favor, selecione um formato entre as opções (retângulo, triângulo ou círculo): ").lower()
            crops[index]["shape"] = shape  # Atualizar a forma armazenada

            length = float(input("Digite o novo comprimento: "))
            crops[index]["length"] = length

            if shape != "círculo":
                width = float(input("Digite a nova largura: "))
                crops[index]["width"] = width
                area = calculate_area(shape, length, width)
            else:
                crops[index]["width"] = None  # Nenhuma "largura" aplicável para círculo
                area = calculate_area(shape, length)
            crops[index]["area"] = area

            crops[index]["crop_inputs"] = calculate_inputs_per_crop(area, new_crop_name)
            
            print("Lavoura atualizada com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Índice inválido. Por favor selecione um valor numérico válido Please provide numeric values where expected.")

# Etapa e: Menu de opções - Deleção de dados do vetor de dados.
def delete_data():
    try:
        index = (int(input("Digite o índice da lavoura para deletar: "))-1)
        if 0 <= index < len(crops):
            del crops[index]
            print("Lavoura deletada com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Índice inválido. Por favor selecione um valor numérico válido Please provide numeric values where expected.")

# Extra: Menu de opções - Saída de dados para um arquivo em excel.
def export_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Farm Data"

    # Escrever cabeçalhos
    headers = ["Cultura", "Formato", "Comprimento", "Largura", "Área"]
    nutrientes = ["nitrogênio", "fósforo", "potássio", "boro", "cobre", "manganês", "molibdênio", "zinco"]
    headers.extend([f"Quantidade de {n} (Kg)" for n in nutrientes])
    ws.append(headers)

    # Escrever dados
    for crop in crops:
        row_data = [
            crop["name"], 
            crop["shape"], 
            crop["length"],
            crop["width"], 
            crop["area"]
        ]
        # Adicionar valores dos insumos
        for nutriente in nutrientes:
            row_data.append(crop["crop_inputs"][nutriente])
        ws.append(row_data)

    output_path = "farm_data.xlsx"
    wb.save(output_path)
    print(f"Dados exportados com sucesso para {output_path}.")

# Extra: Carregue dados existentes de um arquivo JSON, se disponível.
def load_data():
    """Carrega os dados existentes para um arquivo JSON, se disponível, para persistência entre sessões."""
    try:
        with open('farm_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Extra: Salve os dados atuais em um arquivo JSON para preservar informações entre as sessões.
def save_data():
    """Salva os dados atuais para um arquivo JSON para preservar dados entre sessões."""
    with open('farm_data.json', 'w') as file:
        json.dump(crops, file)
    print("Dados salvos com sucesso.")

if __name__ == "__main__":
    main_menu()