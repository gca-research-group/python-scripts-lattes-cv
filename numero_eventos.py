#########################################################################################################################################################
"""
Este código Python faz a contagem de eventos de participação em congressos por ano a partir de arquivos XML,
e gera um relatório em formato PDF com essas informações.

1. Função `contar_eventos_por_ano`:
   - Abre e analisa um arquivo XML.
   - Extrai o ano de participação em congressos de cada evento encontrado.
   - Conta a quantidade de eventos por ano e armazena essas informações em um dicionário.
   - Retorna o dicionário contendo a contagem de eventos por ano.

2. Função `processar_arquivos_xml`:
   - Percorre todos os arquivos XML em um diretório especificado.
   - Para cada arquivo XML encontrado, chama a função `contar_eventos_por_ano` e armazena os resultados.
   - Adiciona a contagem total de eventos para cada arquivo.
   - Retorna um dicionário contendo os resultados de todos os arquivos processados.

3. Função `gerar_pdf`:
   - Cria um documento PDF utilizando a biblioteca `FPDF`.
   - Adiciona um título ao PDF.
   - Para cada arquivo processado, adiciona o nome do arquivo e a contagem de eventos por ano.
   - Adiciona a contagem total de eventos para cada arquivo.
   - Salva o PDF com o nome especificado.

4. Função `main`:
   - Define o diretório contendo os arquivos XML.
   - Chama a função `processar_arquivos_xml` para obter os resultados da contagem de eventos.
   - Se houver resultados, chama a função `gerar_pdf` para criar o relatório em PDF.
   - Imprime uma mensagem de sucesso ou erro, dependendo se foram encontrados arquivos XML no diretório.

"""
##########################################################################################################################################################

import os
from fpdf import FPDF
import xml.etree.ElementTree as ET
from collections import defaultdict

def contar_eventos_por_ano(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        eventos_por_ano = defaultdict(int)

        for participacao in root.findall('.//PARTICIPACAO-EM-CONGRESSO'):
            ano = participacao.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-CONGRESSO').get('ANO', 'Ano desconhecido')
            eventos_por_ano[ano] += 1

        return dict(eventos_por_ano)

    except Exception as e:
        print(f"Erro ao contar eventos por ano no arquivo XML {xml_file}: {e}")
        return None

def processar_arquivos_xml(diretorio):
    resultados = {}

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            eventos_por_ano = contar_eventos_por_ano(caminho_arquivo)
            if eventos_por_ano is not None:
                resultados[arquivo] = eventos_por_ano
                resultados[arquivo]['Total'] = sum(eventos_por_ano.values())

    return resultados

def exibir_resultados_terminal(resultados):
    print("Participação em Congressos por Ano")
    print("=" * 40)

    for arquivo, eventos_por_ano in resultados.items():
        print(f"Arquivo: {arquivo}")
        for ano, quantidade in eventos_por_ano.items():
            if ano != 'Total':
                print(f"Ano: {ano}, Quantidade de Eventos: {quantidade}")
        print(f"Total de Eventos: {eventos_por_ano['Total']}")
        print("-" * 40)

def gerar_pdf(resultados, nome_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Participação em Congressos por Ano", ln=True, align="C")
    pdf.ln(10)

    for arquivo, eventos_por_ano in resultados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Arquivo: {arquivo}", ln=True, align="L")

        pdf.set_font("Arial", size=12)
        for ano, quantidade in eventos_por_ano.items():
            if ano != 'Total':
                pdf.cell(200, 10, f"Ano: {ano}, Quantidade de Eventos: {quantidade}", ln=True, align="L")
        pdf.cell(200, 10, f"Total de Eventos: {eventos_por_ano['Total']}", ln=True, align="L")
        pdf.ln(10)

    pdf.output(nome_pdf)

def main():
    diretorio_xml = r'C:\Users\radim\Desktop\ppgmmc'
    resultados = processar_arquivos_xml(diretorio_xml)

    if resultados:
        exibir_resultados_terminal(resultados)
        nome_pdf = 'participacao_eventos.pdf'
        gerar_pdf(resultados, nome_pdf)
        print(f"PDF {nome_pdf} gerado com sucesso.")
    else:
        print("Nenhum arquivo XML encontrado no diretório.")

if __name__ == "__main__":
    main()
