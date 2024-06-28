import os
from lxml import etree

def extrair_informacoes_orientador(file_path):
    try:
        nome_arquivo = os.path.basename(file_path).split(".")[0]  # Obtém o nome do arquivo sem a extensão
        return nome_arquivo, extrair_areas_conhecimento(etree.parse(file_path).getroot())
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return "Erro ao processar arquivo", set()

def extrair_areas_conhecimento(root):
    areas_conhecimento = set()

    areas = root.xpath("//AREA-DO-CONHECIMENTO-1")
    for area in areas:
        nome_area = area.get("NOME-DA-AREA-DO-CONHECIMENTO")
        sub_area = area.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO")
        especialidade = area.get("NOME-DA-ESPECIALIDADE")
        if nome_area:
            areas_conhecimento.add(nome_area)
        if sub_area:
            areas_conhecimento.add(sub_area)
        if especialidade:
            areas_conhecimento.add(especialidade)

    return areas_conhecimento

# Pasta contendo os arquivos XML
pasta_xml = r"C:\Users\radim\Desktop\ppgmmc"

# Lista para armazenar informações de orientadores e suas áreas de conhecimento
orientadores_areas = []

# Iterar sobre os arquivos XML na pasta
arquivos_xml = [arq for arq in os.listdir(pasta_xml) if arq.endswith(".xml")]
print(f"Número de arquivos XML encontrados: {len(arquivos_xml)}")

for arquivo in arquivos_xml:
    arquivo_path = os.path.join(pasta_xml, arquivo)
    primeiro_nome, areas_conhecimento = extrair_informacoes_orientador(arquivo_path)
    orientadores_areas.append((primeiro_nome, areas_conhecimento))

# Verificar quantos orientadores foram processados
print(f"Número de orientadores processados: {len(orientadores_areas)}")

# Exibir informações dos orientadores e suas áreas de conhecimento no terminal
for i, (orientador, areas) in enumerate(orientadores_areas):
    print(f"Orientador {i+1}: {orientador}")
    for area in areas:
        print(f"  - {area}")
    print("-----\n")
