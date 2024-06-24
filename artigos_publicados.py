#########################################################################################################################################################
"""
Este código Python analisa arquivos XML para extrair informações sobre artigos publicados e seus autores,
e gera um relatório em formato PDF com essas informações. 

1. Função `extrair_informacoes`:
   - Abre e analisa um arquivo XML.
   - Conta o número total de artigos publicados.
   - Extrai os nomes dos autores de cada artigo publicado e conta a quantidade de vezes que cada autor aparece.
   - Retorna um dicionário com o total de artigos publicados e um dicionário com os autores e suas respectivas contagens.

2. Função `gerar_pdf`:
   - Cria um documento PDF utilizando a biblioteca `FPDF`.
   - Adiciona um título ao PDF.
   - Para cada arquivo XML processado, adiciona o nome do arquivo, o total de artigos publicados e uma lista dos autores com suas contagens.
   - Salva o PDF com o nome especificado.

3. Script principal:
   - Define o caminho para a pasta contendo os arquivos XML.
   - Verifica se a pasta existe e contém arquivos XML.
   - Inicializa um dicionário para armazenar os resultados de cada arquivo.
   - Processa cada arquivo XML na pasta:
     - Chama a função `extrair_informacoes` para obter os dados do arquivo.
     - Armazena os dados no dicionário de resultados.
   - Chama a função `gerar_pdf` para criar o relatório em PDF com os dados extraídos.
   - Imprime uma mensagem de sucesso ao final do processo.

"""
############################################################################################################################################################




import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from fpdf import FPDF

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

# Função para gerar o PDF com as informações extraídas
def gerar_pdf(resultados, caminho_saida):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adiciona título ao PDF
    pdf.cell(200, 10, txt="Artigos Publicados e Coautorias", ln=True, align="C")
    pdf.ln(10)

    # Adiciona informações de cada arquivo ao PDF
    for nome_arquivo, dados_arquivo in resultados.items():
        pdf.cell(200, 10, txt=f"Arquivo XML: {nome_arquivo}", ln=True)
        pdf.cell(200, 10, txt=f"Total de artigos publicados: {dados_arquivo['Total de Artigos']}", ln=True)
        pdf.cell(200, 10, txt="Autores dos Artigos:", ln=True)
        for autor, quantidade in sorted(dados_arquivo['Autores'].items(), key=lambda item: item[1], reverse=True):
            pdf.cell(200, 10, txt=f"  - Autor: {autor}, Quantidade: {quantidade}", ln=True)
        pdf.ln(10)

    # Salva o PDF
    pdf.output(caminho_saida)

# Caminho para a pasta contendo os arquivos XML
caminho_pasta = r'C:\Users\radim\Desktop\todos_curriculos'

# Dicionário para armazenar os resultados por arquivo
resultados_por_arquivo = {}

# Verificar se a pasta existe e se contém arquivos XML
if os.path.exists(caminho_pasta):
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            print(f"Analisando arquivo: {caminho_arquivo}")
            resultados_por_arquivo[arquivo] = extrair_informacoes(caminho_arquivo)

    # Gerar o PDF com as informações extraídas
    caminho_saida_pdf = r'C:\Users\radim\Desktop\artigos_publicados.pdf'
    gerar_pdf(resultados_por_arquivo, caminho_saida_pdf)
    print("PDF gerado com sucesso!")
else:
    print(f"Pasta não encontrada: {caminho_pasta}")
