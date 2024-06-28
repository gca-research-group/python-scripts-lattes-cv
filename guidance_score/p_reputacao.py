import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# Função para extrair participações em bancas
def extract_participations(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    participations = {
        'graduacao': 0,
        'mestrado': 0,
        'doutorado': 0
    }
    
    for participacao in root.findall('.//DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO'):
        participations['graduacao'] += 1
    
    for participacao in root.findall('.//DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO'):
        participations['mestrado'] += 1
    
    for participacao in root.findall('.//DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO'):
        participations['doutorado'] += 1
            
    total_participations = participations['graduacao'] + participations['mestrado'] + participations['doutorado']
    return total_participations

# Função para extrair informações de coautores
def extrair_coautores(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        coautores = set()

        # Buscar artigos publicados dentro de ARTIGOS-PUBLICADOS
        for artigo in root.findall('.//ARTIGO-PUBLICADO'):
            # Extrair nomes dos coautores
            for autor in artigo.findall('.//AUTORES'):
                nome_autor = autor.get('NOME-COMPLETO-DO-AUTOR', 'N/A')
                coautores.add(nome_autor)

        return len(coautores)

    except ET.ParseError as e:
        print(f"Erro ao analisar o arquivo XML: {xml_path}, erro: {e}")
        return 0

# Função para calcular a pontuação de reputação
def calcular_pontuacao(participacoes, coautores, min_b, max_b, min_c, max_c, w1=0.5, w2=0.5):
    normalized_b = (participacoes - min_b) / (max_b - min_b) if max_b > min_b else 0
    normalized_c = (coautores - min_c) / (max_c - min_c) if max_c > min_c else 0
    return w1 * normalized_b + w2 * normalized_c

# Caminho para a pasta contendo os arquivos XML
caminho_pasta = r'C:\Users\radim\Desktop\ppgmmc'

# Dicionário para armazenar os resultados por arquivo
participacoes_list = []
coautores_list = []
resultados_por_arquivo = {}

# Verificar se a pasta existe e se contém arquivos XML
if os.path.exists(caminho_pasta):
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            participacoes = extract_participations(caminho_arquivo)
            coautores = extrair_coautores(caminho_arquivo)
            participacoes_list.append(participacoes)
            coautores_list.append(coautores)
            resultados_por_arquivo[arquivo] = {
                'Participacoes': participacoes,
                'Coautores': coautores
            }

    # Calcular min e max
    min_b = min(participacoes_list)
    max_b = max(participacoes_list)
    min_c = min(coautores_list)
    max_c = max(coautores_list)

    # Calcular pontuações de reputação e imprimir resultados no terminal
    for nome_arquivo, dados_arquivo in resultados_por_arquivo.items():
        participacoes = dados_arquivo['Participacoes']
        coautores = dados_arquivo['Coautores']
        pontuacao = calcular_pontuacao(participacoes, coautores, min_b, max_b, min_c, max_c)
        print(f"Arquivo XML: {nome_arquivo}")
        print(f"Total de participações em bancas: {participacoes}")
        print(f"Total de coautores: {coautores}")
        print(f"Pontuação de reputação: {pontuacao:.2f}")
        print("-" * 40)
else:
    print(f"Pasta não encontrada: {caminho_pasta}")
