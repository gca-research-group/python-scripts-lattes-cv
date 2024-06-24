############################################################################################################################################################
"""
Este código Python analisa arquivos XML contendo informações sobre a participação de professores em bancas de graduação, mestrado e doutorado,
e gera um relatório em formato PDF com essas informações.

1. Função `extract_participations`:
   - Abre e analisa um arquivo XML.
   - Conta o número de participações em bancas de graduação, mestrado e doutorado.
   - Retorna um dicionário com essas contagens.

2. Função `generate_pdf_from_xml`:
   - Cria um documento PDF utilizando a biblioteca `reportlab`.
   - Percorre todos os arquivos XML em um diretório especificado.
   - Para cada arquivo XML, chama a função `extract_participations` para obter as contagens de participações em bancas.
   - Adiciona o nome do professor (extraído do nome do arquivo) e as contagens de participações no PDF.
   - Gera novas páginas no PDF conforme necessário para evitar ultrapassar os limites da página.
   - Salva o PDF com o nome especificado.

3. Script principal:
   - Define o diretório contendo os arquivos XML e o nome do arquivo PDF de saída.
   - Chama a função `generate_pdf_from_xml` para criar o relatório em PDF.
   - Imprime o número total de arquivos XML lidos e processados.

"""
############################################################################################################################################################

import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
            
    return participations

def generate_pdf_from_xml(directory, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    y = 750

    total_xml_files = 0
    processed_xml_files = 0

    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            total_xml_files += 1
            file_path = os.path.join(directory, filename)
            professor_name = os.path.splitext(filename)[0]  # Extracting professor name from filename
            participations = extract_participations(file_path)
            
            # Calculate total participations for the professor
            total_participations = participations['graduacao'] + participations['mestrado'] + participations['doutorado']
            
            print(f"Analisando o arquivo XML: {filename}")
            print(f"Participações do Professor {professor_name}:")
            print(f"Graduação: {participations['graduacao']}")
            print(f"Mestrado: {participations['mestrado']}")
            print(f"Doutorado: {participations['doutorado']}")
            print(f"Total de Participações: {total_participations}")
            print()
            
            c.drawString(50, y, f"Professor: {professor_name}")
            y -= 20
            c.drawString(50, y, "Participações em Bancas:")
            y -= 20
            c.drawString(70, y, f"Graduação: {participations['graduacao']}")
            y -= 15
            c.drawString(70, y, f"Mestrado: {participations['mestrado']}")
            y -= 15
            c.drawString(70, y, f"Doutorado: {participations['doutorado']}")
            y -= 15
            c.drawString(70, y, f"Total de Participações: {total_participations}")
            y -= 35
            processed_xml_files += 1

            if y <= 50:
                c.showPage()
                y = 750

    c.save()

    print(f"Total de arquivos XML lidos: {total_xml_files}")
    print(f"Total de arquivos XML executados: {processed_xml_files}")

directory = r'C:\Users\radim\Desktop\ppgmmc'
output_file = r'C:\Users\radim\Desktop\participacao_bancas.pdf'
generate_pdf_from_xml(directory, output_file)
