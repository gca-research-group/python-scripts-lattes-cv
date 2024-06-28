import os
import xml.etree.ElementTree as ET

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

##### Caminho dos arquivos XML #####
path = r'C:\Users\radim\Desktop\ppgmmc'

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

        # Exibir informações no terminal
        print(f"Orientador: {orientador_nome}")
        print("Experiência:")
        print(f"  Experiência em Iniciação Científica: {experiencia['iniciacao_cientifica']}")
        print(f"  Experiência em Graduação: {experiencia['graduacao']}")
        print(f"  Experiência em Mestrado: {experiencia['mestrado']}")
        print(f"  Experiência em Doutorado: {experiencia['doutorado']}")
        print("-----\n")
