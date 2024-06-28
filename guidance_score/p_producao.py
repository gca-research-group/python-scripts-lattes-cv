import os
import xml.etree.ElementTree as ET
import numpy as np

def extrair_dados_publicacoes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    publicacoes = []
    for artigo in root.findall('.//ARTIGO-PUBLICADO'):
        # Supondo que o fator de impacto e o percentil estão armazenados como atributos no XML
        fator_impacto = float(artigo.find('.//FACTOR-DE-IMPACTO').text)
        percentil = float(artigo.find('.//PERCENTIL').text)
        publicacoes.append((fator_impacto, percentil))

    return publicacoes

def calcular_pontuacao_producao(publicacoes, h_index):
    pontuacao = 0
    for fator_impacto, percentil in publicacoes:
        pontuacao += fator_impacto * h_index * percentil
    return pontuacao

def main():
    diretorio_xml = r'C:\Users\radim\Desktop\ppgmmc'
    h_index = 10  # Suponha um h-index fixo ou calcule a partir dos dados

    for arquivo in os.listdir(diretorio_xml):
        if arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(diretorio_xml, arquivo)
            publicacoes = extrair_dados_publicacoes(caminho_arquivo)
            pontuacao_producao = calcular_pontuacao_producao(publicacoes, h_index)

            print(f"Arquivo: {arquivo}")
            print(f"Pontuação da Produção Científica: {pontuacao_producao:.2f}")
            print("-" * 40)

if __name__ == "__main__":
    main()
