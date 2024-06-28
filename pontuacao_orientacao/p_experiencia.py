import os
import xml.etree.ElementTree as ET
import numpy as np

# Função para contar orientações concluídas em um arquivo XML
def count_orientacoes_concluidas(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    orientacoes_concluidas = {
        'iniciacao_cientifica': 0,
        'graduacao': 0,
        'mestrado': 0,
        'doutorado': 0
    }

    orientacoes_map = {
        'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO': 'mestrado',
        'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO': 'doutorado'
    }

    for termo_orientacao, categoria in orientacoes_map.items():
        orientacoes_concluidas[categoria] += len(list(root.iter(termo_orientacao)))

    for orientacao in root.iter('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS'):
        natureza = orientacao.attrib.get('NATUREZA', '').upper()
        if natureza == 'INICIACAO_CIENTIFICA':
            orientacoes_concluidas['iniciacao_cientifica'] += 1
        elif natureza == 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO':
            orientacoes_concluidas['graduacao'] += 1

    return orientacoes_concluidas

# Função para contar orientações em andamento em um arquivo XML
def count_orientacoes_andamento(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    orientacoes_andamento = {
        'iniciacao_cientifica': 0,
        'graduacao': 0,
        'mestrado': 0,
        'doutorado': 0
    }

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Iniciação Científica':
            orientacoes_andamento['iniciacao_cientifica'] += 1

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Graduação':
            orientacoes_andamento['graduacao'] += 1

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Dissertação de mestrado':
            orientacoes_andamento['mestrado'] += 1

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Tese de doutorado':
            orientacoes_andamento['doutorado'] += 1

    return orientacoes_andamento

# Função para calcular o fator de qualidade Q
def calcular_fator_qualidade(P_r, P_max):
    return P_r / P_max if P_max != 0 else 0

# Função para calcular a pontuação de experiência baseada na equação fornecida
def calcular_pontuacao_equacao(concluida, andamento, Q, pesos, limites):
    experiencia = {
        'graduacao': concluida['graduacao'] + andamento['graduacao'],
        'mestrado': concluida['mestrado'] + andamento['mestrado'],
        'doutorado': concluida['doutorado'] + andamento['doutorado']
    }

    G, M, D = limites

    pe = ((experiencia['graduacao'] * pesos['graduacao'] / G) +
          (experiencia['mestrado'] * pesos['mestrado'] / M) +
          (experiencia['doutorado'] * pesos['doutorado'] / D)) * Q

    return pe

# Função para extrair o número de publicações de um arquivo XML
def extrair_numero_publicacoes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return len(list(root.iter('ARTIGO-PUBLICADO')))

# Caminho dos arquivos XML
path = r'C:\Users\radim\Desktop\ppgmmc'

# Pesos e limites
pesos = {
    'graduacao': 4,
    'mestrado': 6,
    'doutorado': 10
}
limites = [50, 30, 20]  # Limites superiores para graduação, mestrado e doutorado

# Lista para armazenar o número de publicações de cada orientador
numeros_publicacoes = []

# Contadores para pastas e arquivos
total_pastas = 0
total_arquivos = 0

# Processar cada arquivo XML para extrair o número de publicações
for root_dir, dirs, files in os.walk(path):
    total_pastas += len(dirs)
    for xml_file in files:
        if xml_file.endswith(".xml"):
            full_path = os.path.join(root_dir, xml_file)
            numeros_publicacoes.append(extrair_numero_publicacoes(full_path))
            total_arquivos += 1

# Calcular P_max como o percentil 90 dos números de publicações
P_max = np.percentile(numeros_publicacoes, 90)
print(f"P_max (Percentil 90 das publicações): {P_max}")

# Processar cada arquivo XML novamente para calcular a pontuação de experiência
for root_dir, dirs, files in os.walk(path):
    for xml_file in files:
        if xml_file.endswith(".xml"):
            full_path = os.path.join(root_dir, xml_file)
            orientador_nome = os.path.splitext(xml_file)[0]

            concluida = count_orientacoes_concluidas(full_path)
            andamento = count_orientacoes_andamento(full_path)

            # Exemplo de número de publicações em revistas
            P_r = extrair_numero_publicacoes(full_path)
            Q = calcular_fator_qualidade(P_r, P_max)

            pontuacao_experiencia = calcular_pontuacao_equacao(concluida, andamento, Q, pesos, limites)

            # Imprimir informações no terminal para depuração
            print(f"Orientador: {orientador_nome}")
            print(f"Número de Artigos Publicados: {P_r}")
            print(f"Experiência em Graduação: {concluida['graduacao'] + andamento['graduacao']}")
            print(f"Experiência em Mestrado: {concluida['mestrado'] + andamento['mestrado']}")
            print(f"Experiência em Doutorado: {concluida['doutorado'] + andamento['doutorado']}")
            print(f"Pontuação da Experiência: {pontuacao_experiencia:.2f}")
            print("-" * 40)

# Imprimir o total de pastas e arquivos varridos
print(f"Total de pastas varridas: {total_pastas}")
print(f"Total de arquivos XML varridos: {total_arquivos}")
