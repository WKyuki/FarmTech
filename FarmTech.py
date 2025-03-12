# Versão do Python: 3.10.0
# Projeto: FarmTech Solutions
# Comando para instalar o pacote no terminal abaixo:
# pip install openpyxl

import json
import openpyxl
from openpyxl import Workbook

# Etapa a: Informações das culturas
# Cultura 1: Milho
# Formato da área: Retângulo (inglês: rectangle)
# Comprimento: 100 m                                    Calculo automatico:
# Largura: 50 m                                        Comprimento x Largura
# Taxa de aplicação: 10 ml/m                            Calculo automatico:
# Número de linhas: 5                         área x taxa de aplicação x número de linhas

# Cultura 2: Soja
# Formato da área: Triângulo (inglês: triangle)
# Comprimento: 80 m                                    Calculo automatico:
# Largura: 40 m                                       Comprimento x Largura
# Taxa de aplicação: 8 ml/m                            Calculo automatico:
# Número de linhas: 3                         área x taxa de aplicação x número de linhas

# Etapa b: Cálculo de área de plantio para cada cultura.
def calculate_area(shape, length, width=None):
    """Calculates area based on shape and dimensions."""
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
def calculate_inputs_per_crop(area, application_rate, num_rows):
    """Calculates the total input needed for a crop based on area, rate, and rows."""
    return area * application_rate * num_rows

# Etapa d: Dados em vetores.
crops = []  # Will store dictionaries with crop data.
areas = []
input_management = []

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
        print("1. Detalhar dados da lavoura")
        print("2. Visualizar dados da lavoura")
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
        crop_name = input("Digite o nome da lavoura: ")
        
        shape = input("Selecione o formato da área de plantio (retângulo, triângulo ou círculo): ").lower()
        length = float(input("Digite o comprimento (ou raio caso seja um círculo): "))
        
        width = None
        if shape != "círculo":
            width = float(input("Digite a largura: "))
            area = calculate_area(shape, length, width)
        else:
            area = calculate_area(shape, length)
        
        application_rate = float(input("Digite a taxa de aplicação de água (ml/m): "))
        num_rows = int(input("Digite o número de linhas: "))
        total_inputs = calculate_inputs_per_crop(area, application_rate, num_rows)
        
        # Armazene todas as informações em um dicionário
        crop_data = {
            "name": crop_name,
            "shape": shape,
            "length": length,
            "width": width,
            "area": area,
            "application_rate": application_rate,
            "num_rows": num_rows,
            "total_inputs": total_inputs
        }
        crops.append(crop_data)
        
    except ValueError:
        print("Invalid input. Please provide numeric values where expected.")

# Etapa e: Menu de opções - Saída de dados no terminal.
def display_data():
    print("\nCurrent data:")
    for i, crop in enumerate(crops):
        print(f"Crop: {crop['name']}, Shape: {crop['shape']}, Length: {crop['length']}, Width: {crop['width']}, Area: {crop['area']}, Application Rate: {crop['application_rate']}, Rows: {crop['num_rows']}, Total Inputs: {crop['total_inputs']}")

# Etapa e: Menu de opções - Atualização de dados.
def update_data():
    try:
        index = int(input("Enter index to update: "))
        if 0 <= index < len(crops):
            new_crop_name = input("Enter new crop name: ")
            crops[index]["name"] = new_crop_name

            # Atualizar forma e recalcular com base na nova forma
            shape = input("Enter new shape of the area (rectangle/triangle/circle): ").lower()
            crops[index]["shape"] = shape  # Atualizar a forma armazenada

            length = float(input("Enter new length: "))
            crops[index]["length"] = length

            if shape != "circle":
                width = float(input("Enter new width: "))
                crops[index]["width"] = width
                area = calculate_area(shape, length, width)
            else:
                crops[index]["width"] = None  # Nenhuma "largura" aplicável para círculo
                area = calculate_area(shape, length)
            crops[index]["area"] = area

            application_rate = float(input("Enter new application rate: "))
            crops[index]["application_rate"] = application_rate
            num_rows = int(input("Enter new number of rows: "))
            crops[index]["num_rows"] = num_rows
            crops[index]["total_inputs"] = calculate_inputs_per_crop(area, application_rate, num_rows)
            
            print("Data updated successfully.")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please provide numeric values where expected.")

# Etapa e: Menu de opções - Deleção de dados do vetor de dados.
def delete_data():
    try:
        index = int(input("Enter index to delete: "))
        if 0 <= index < len(crops):
            del crops[index]
            print("Data deleted successfully.")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please enter a valid index.")

# Extra: Menu de opções - Saída de dados para um arquivo em excel.
def export_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Farm Data"

    # Escrever cabeçalhos
    headers = ["Crop Name", "Shape", "Length", "Width", "Area", "Application Rate", "Rows", "Total Inputs"]
    ws.append(headers)

    # Escrever dados
    for crop in crops:
        ws.append([
            crop["name"], crop["shape"], crop["length"],
            crop["width"], crop["area"], crop["application_rate"],
            crop["num_rows"], crop["total_inputs"]
        ])

    output_path = "farm_data.xlsx"
    wb.save(output_path)
    print(f"Data exported to {output_path} successfully.")

# Extra: Carregue dados existentes de um arquivo JSON, se disponível.
def load_data():
    """Loads existing data from a JSON file, if available, for persistence across sessions."""
    try:
        with open('farm_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Extra: Salve os dados atuais em um arquivo JSON para preservar informações entre as sessões.
def save_data():
    """Saves current data to a JSON file to preserve information between sessions."""
    with open('farm_data.json', 'w') as file:
        json.dump(crops, file)
    print("Data saved successfully.")

if __name__ == "__main__":
    main_menu()