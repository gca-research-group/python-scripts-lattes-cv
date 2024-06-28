import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# Função para extrair informações de artigos publicados de um arquivo XML
def extrair_informacoes(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        total_artigos = 0
        autores = defaultdict(int)

        # Buscar artigos publicados dentro de ARTIGOS-PUBLICADOS
        for artigo in root.findall('.//ARTIGO-PUBLICADO'):
            total_artigos += 1

            # Extrair nomes dos autores
            for autor in artigo.findall('.//AUTORES'):
                nome_autor = autor.get('NOME-COMPLETO-DO-AUTOR', 'N/A')
                autores[nome_autor] += 1

        return {
            'Total de Artigos': total_artigos,
            'Autores': dict(autores)
        }

    except ET.ParseError as e:
        print(f"Erro ao analisar o arquivo XML: {xml_path}, erro: {e}")
        return None

# Caminho para a pasta contendo os arquivos XML
caminho_pasta = r'C:\Users\radim\Desktop\ppgmmc'

# Dicionário para armazenar os resultados por arquivo
resultados_por_arquivo = {}

# Verificar se a pasta existe e se contém arquivos XML
if os.path.exists(caminho_pasta):
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            print(f"Analisando arquivo: {caminho_arquivo}")
            resultados_por_arquivo[arquivo] = extrair_informacoes(caminho_arquivo)

    # Exibir os resultados no terminal
    for nome_arquivo, dados_arquivo in resultados_por_arquivo.items():
        if dados_arquivo:
            print(f"Arquivo XML: {nome_arquivo}")
            print(f"Total de artigos publicados: {dados_arquivo['Total de Artigos']}")
            print("Autores dos Artigos:")
            for autor, quantidade in sorted(dados_arquivo['Autores'].items(), key=lambda item: item[1], reverse=True):
                print(f"  - Autor: {autor}, Quantidade: {quantidade}")
            print("-----\n")
else:
    print(f"Pasta não encontrada: {caminho_pasta}")

