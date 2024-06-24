############################################################################################################################################################
"""
Este código Python analisa arquivos XML para contar o número de orientações concluídas e em andamento,
calcula uma pontuação de experiência com base em pesos e tempos específicos, e gera um relatório em formato PDF com essas informações.

1. Função `count_orientacoes_concluidas`:
   - Abre e analisa um arquivo XML.
   - Conta o número de orientações concluídas para mestrado e doutorado.
   - Conta o número de outras orientações concluídas, diferenciando entre iniciação científica e graduação.
   - Retorna um dicionário com essas contagens.

2. Função `count_orientacoes_andamento`:
   - Abre e analisa um arquivo XML.
   - Conta o número de orientações em andamento para iniciação científica, graduação, mestrado e doutorado.
   - Retorna um dicionário com essas contagens.

3. Função `calcular_pontuacao`:(peso x tempo x experiencia)/total de experiencia

peso é atribuído a cada nível educacional (iniciação científica, graduação, mestrado, doutorado). 
tempo é em anos atribuído a cada nível educacional. 
experiência é o número de orientações concluídas e em andamento para cada nível educacional. 
n é o número total de níveis educacionais considerados. 
total de experiência é a soma total do número de orientações concluídas e em andamento em todos os níveis educacionais.

   - Calcula a pontuação da experiência com base nas contagens de orientações, pesos e tempos fornecidos.
   - Retorna a pontuação calculada.

4. Script principal:
   - Define o diretório contendo os arquivos XML.
   - Inicializa o documento PDF utilizando a biblioteca `FPDF`.
   - Define os pesos e tempos para cada nível de orientação.
   - Processa cada arquivo XML no diretório:
     - Extrai o nome do orientador a partir do nome do arquivo.
     - Conta as orientações concluídas e em andamento.
     - Calcula a experiência total e a pontuação da experiência.
     - Adiciona essas informações ao PDF.
   - Salva o PDF com o nome especificado.

"""
############################################################################################################################################################

import xml.etree.ElementTree as ET
import os
from fpdf import FPDF

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

# Função para calcular a pontuação da experiência
def calcular_pontuacao(experiencia, pesos, tempos):
    n_total = sum(experiencia.values())
    if n_total == 0:
        return 0

    pontuacao = 0
    for i, nivel in enumerate(["iniciacao_cientifica", "graduacao", "mestrado", "doutorado"]):
        pontuacao += (pesos[i] * tempos[i] * experiencia[nivel]) / n_total
    
    return pontuacao

##### Caminho dos arquivos XML #####
path = r'C:\Users\radim\Desktop\todos_curriculos'

# Inicialização do PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Pesos e tempos
pesos = [1, 2, 3, 4]  # Pesos para iniciação científica, graduação, mestrado, doutorado
tempos = [1, 1, 2, 4]  # Tempos em anos para iniciação científica, graduação, mestrado, doutorado

# Processar cada arquivo XML
for xml_file in os.listdir(path):
    if xml_file.endswith(".xml"):
        full_path = os.path.join(path, xml_file)
        orientador_nome = os.path.splitext(xml_file)[0]

        concluida = count_orientacoes_concluidas(full_path)
        andamento = count_orientacoes_andamento(full_path)

        experiencia = {
            'iniciacao_cientifica': concluida['iniciacao_cientifica'] + andamento['iniciacao_cientifica'],
            'graduacao': concluida['graduacao'] + andamento['graduacao'],
            'mestrado': concluida['mestrado'] + andamento['mestrado'],
            'doutorado': concluida['doutorado'] + andamento['doutorado']
        }
        pontuacao_experiencia = calcular_pontuacao(experiencia, pesos, tempos)

        # Adicionar informações ao PDF
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=f"Orientador: {orientador_nome}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="Experiência:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Experiência em Iniciação Científica: {experiencia['iniciacao_cientifica']}", ln=True)
        pdf.cell(200, 10, txt=f"Experiência em Graduação: {experiencia['graduacao']}", ln=True)
        pdf.cell(200, 10, txt=f"Experiência em Mestrado: {experiencia['mestrado']}", ln=True)
        pdf.cell(200, 10, txt=f"Experiência em Doutorado: {experiencia['doutorado']}", ln=True)
        pdf.cell(200, 10, txt=f"Pontuação da Experiência: {pontuacao_experiencia:.2f}", ln=True)
        pdf.ln(10)

# Salvar o PDF
pdf.output(r'C:\Users\radim\Desktop\calculo_orientacoes.pdf')
