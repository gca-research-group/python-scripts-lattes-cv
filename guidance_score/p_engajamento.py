#####################################################################
#Este código analisa arquivos XML para calcular a pontuação de engajamento acadêmico com base em atividades de ensino, pesquisa e extensão. A função #`get_teaching_score` conta disciplinas únicas ensinadas, `get_research_score` conta atividades de pesquisa, e `get_extension_score` conta atividades de #extensão e serviços técnicos. A função `calculate_engagement_score` combina essas pontuações usando pesos definidos (`omega_e`, `omega_p`, `omega_x`). O #script percorre todos os arquivos XML em uma pasta especificada, calcula as pontuações para cada arquivo e exibe os resultados..
#####################################################################

import xml.etree.ElementTree as ET
import os

# Função para extrair pontuação de ensino sem duplicar contagens
def get_teaching_score(root):
    disciplinas = set()  # Usar um conjunto para evitar duplicatas
    for ensino in root.findall(".//ATIVIDADES-DE-ENSINO/ENSINO"):
        for disciplina in ensino.findall("DISCIPLINA"):
            disciplinas.add(disciplina.text)  # Adicionar o nome da disciplina ao conjunto
    return len(disciplinas)  # Retornar o número de disciplinas únicas

# Função para extrair pontuação de pesquisa
def get_research_score(root):
    research_score = 0
    for activity in root.findall(".//ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO/PESQUISA-E-DESENVOLVIMENTO"):
        research_score += 1
    return research_score

# Função para extrair pontuação de extensão
def get_extension_score(root):
    extension_score = 0
    for activity in root.findall(".//ATIVIDADES-DE-SERVICO-TECNICO-ESPECIALIZADO/SERVICO-TECNICO-ESPECIALIZADO"):
        extension_score += 1
    for training in root.findall(".//ATIVIDADES-DE-TREINAMENTO-MINISTRADO/TREINAMENTO-MINISTRADO"):
        extension_score += 1
    for extension in root.findall(".//ATIVIDADES-DE-EXTENSAO-UNIVERSITARIA/EXTENSAO-UNIVERSITARIA"):
        extension_score += 1
    return extension_score

# Função para calcular a pontuação de engajamento
def calculate_engagement_score(omega_e, omega_p, omega_x, pe, pp, px):
    return omega_e * pe + omega_p * pp + omega_x * px

# Caminho da pasta com os arquivos XML
directory_path = "C:\\Users\\radim\\Desktop\\ppgmmc"

# Definir os pesos
omega_e = 0.4  # Peso para ensino
omega_p = 0.4  # Peso para pesquisa
omega_x = 0.2  # Peso para extensão

# Iterar sobre todos os arquivos XML na pasta e subpastas
for root_dir, sub_dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith(".xml"):
            file_path = os.path.join(root_dir, file)
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            pe = get_teaching_score(root)
            pp = get_research_score(root)
            px = get_extension_score(root)
            
            engagement_score = calculate_engagement_score(omega_e, omega_p, omega_x, pe, pp, px)

            # Exibir resultados para cada arquivo
            print("Arquivo:", file)
            print("Pontuação de Ensino (PE):", pe)
            print("Pontuação de Pesquisa (PP):", pp)
            print("Pontuação de Extensão (PX):", px)
            print("Pontuação de Engajamento:", engagement_score)
            print()  # Linha em branco para separar resultados
