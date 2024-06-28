import os
import xml.etree.ElementTree as ET

def count_orientacoes_concluidas(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    orientacoes_concluidas = {
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
            orientacoes_concluidas['graduacao'] += 1

    return orientacoes_concluidas

def count_orientacoes_andamento(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    orientacoes_andamento = {
        'graduacao': 0,
        'mestrado': 0,
        'doutorado': 0
    }

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Iniciação Científica':
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

def calcular_taxa_conclusao(concluidas, andamento):
    taxas_conclusao = {}
    for nivel in ['graduacao', 'mestrado', 'doutorado']:
        total_orientacoes = concluidas[nivel] + andamento[nivel]
        if total_orientacoes > 0:
            taxa_conclusao = concluidas[nivel] / total_orientacoes
        else:
            taxa_conclusao = 0
        taxas_conclusao[nivel] = taxa_conclusao
    return taxas_conclusao

def calcular_pontuacao_qualidade(concluidas, andamento, pesos):
    taxas_conclusao = calcular_taxa_conclusao(concluidas, andamento)
    pontuacao_qualidade = 0

    for nivel in ['graduacao', 'mestrado', 'doutorado']:
        total_orientacoes = concluidas[nivel] + andamento[nivel]
        if total_orientacoes > 0:
            pontuacao_qualidade += (pesos[nivel] * taxas_conclusao[nivel] * concluidas[nivel]) / total_orientacoes
    
    return pontuacao_qualidade

def processar_arquivos_xml(diretorio, pesos):
    resultados = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            concluida = count_orientacoes_concluidas(caminho_arquivo)
            andamento = count_orientacoes_andamento(caminho_arquivo)
            pontuacao_qualidade = calcular_pontuacao_qualidade(concluida, andamento, pesos)
            
            resultado = {
                'arquivo': arquivo,
                'concluida': concluida,
                'andamento': andamento,
                'pontuacao_qualidade': pontuacao_qualidade
            }
            resultados.append(resultado)

    return resultados

def exibir_resultados_terminal(resultados):
    print("Pontuação da Qualidade por Nível de Orientação")
    print("=" * 40)

    for resultado in resultados:
        print(f"Arquivo: {resultado['arquivo']}")
        print(f"  Graduação: {resultado['concluida']['graduacao']} concluídas, {resultado['andamento']['graduacao']} em andamento")
        print(f"  Mestrado: {resultado['concluida']['mestrado']} concluídas, {resultado['andamento']['mestrado']} em andamento")
        print(f"  Doutorado: {resultado['concluida']['doutorado']} concluídas, {resultado['andamento']['doutorado']} em andamento")
        print(f"  Pontuação de Qualidade: {resultado['pontuacao_qualidade']:.2f}")
        print("-" * 40)

def main():
    diretorio_xml = r'C:\Users\radim\Desktop\ppgmmc'
    pesos = {
        'graduacao': 1,
        'mestrado': 2,
        'doutorado': 3
    }
    resultados = processar_arquivos_xml(diretorio_xml, pesos)

    if resultados:
        exibir_resultados_terminal(resultados)
    else:
        print("Nenhum arquivo XML encontrado no diretório.")

if __name__ == "__main__":
    main()
