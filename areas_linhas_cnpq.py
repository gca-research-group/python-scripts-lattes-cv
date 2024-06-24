############################################################################################################################################################
"""
Este código Python faz a extração de informações sobre áreas de conhecimento de arquivos XML que contêm currículos lattes,
e gera um único arquivo PDF organizado com esses dados. 

1. Função `extract_areas_of_knowledge`:
   - Abre e analisa um arquivo XML.
   - Extrai informações das áreas de conhecimento (Grande Área, Área, Sub-área e Especialidade) para os seguintes níveis:
     - Graduação
     - Mestrado
     - Doutorado
     - Pós-Doutorado
     - Linhas de Pesquisa
   - Retorna os dados extraídos em um formato estruturado.

2. Função `create_pdf`:
   - Cria um documento PDF utilizando a biblioteca `reportlab`.
   - Adiciona o nome do arquivo "Orientador" como título em negrito.
   - Organiza as áreas de conhecimento em seções, com cada detalhe (Grande Área, Área, Sub-área, Especialidade) listado em parágrafos.
   - Insere espaçamentos adequados para melhorar a legibilidade.
   - Gera o PDF final contendo todos os dados extraídos de múltiplos arquivos XML.

3. Função `main`:
   - Busca todos os arquivos XML na pasta especificada (`input_folder`).
   - Chama a função `extract_areas_of_knowledge` para cada arquivo XML encontrado e armazena os resultados.
   - Chama a função `create_pdf` para gerar o PDF final com todos os dados extraídos.
   - Define os caminhos para a pasta de entrada e o arquivo PDF de saída.
"""
#############################################################################################################################################################

import os
import glob
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def extract_areas_of_knowledge(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Adicionar namespaces se necessário
    namespaces = {'': 'http://www.w3.org/1999/xhtml'}  
    
    data = {
        "filename": os.path.basename(xml_file), 
        "graducao": [], 
        "mestrado": [], 
        "doutorado": [], 
        "pos_doutorado": [], 
        "linhas_pesquisa": []
    }
    
    def get_areas_of_knowledge(element):
        areas = []
        for area in element.findall('.//AREAS-DO-CONHECIMENTO/AREA-DO-CONHECIMENTO-1'):
            area_data = {
                "grande_area": area.get("NOME-GRANDE-AREA-DO-CONHECIMENTO"),
                "area": area.get("NOME-DA-AREA-DO-CONHECIMENTO"),
                "sub_area": area.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO"),
                "especialidade": area.get("NOME-DA-ESPECIALIDADE")
            }
            areas.append(area_data)
        return areas

    # Extraindo dados de formação acadêmica e linhas de pesquisa
    for formacao in root.findall(".//GRADUACAO"):
        data["graducao"].extend(get_areas_of_knowledge(formacao))

    for formacao in root.findall(".//MESTRADO"):
        data["mestrado"].extend(get_areas_of_knowledge(formacao))

    for formacao in root.findall(".//DOUTORADO"):
        data["doutorado"].extend(get_areas_of_knowledge(formacao))

    for formacao in root.findall(".//POS-DOUTORADO"):
        data["pos_doutorado"].extend(get_areas_of_knowledge(formacao))

    for pesquisa in root.findall(".//LINHA-DE-PESQUISA"):
        data["linhas_pesquisa"].extend(get_areas_of_knowledge(pesquisa))

    return data

def create_pdf(data, output_pdf):
    # Criando o documento PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for entry in data:
        # Adicionando título com o nome do arquivo
        story.append(Paragraph(f"<b>Orientador: {entry['filename']}</b>", styles['Heading2']))
        
        def add_section(title, items):
            if items:
                story.append(Paragraph(f"<b>{title}</b>", styles['Heading3']))
                for item in items:
                    # Adicionando detalhes das áreas de conhecimento
                    story.append(Paragraph(f"<b>Grande Área:</b> {item['grande_area']}", styles['Normal']))
                    story.append(Paragraph(f"<b>Área:</b> {item['area']}", styles['Normal']))
                    story.append(Paragraph(f"<b>Sub-área:</b> {item['sub_area']}", styles['Normal']))
                    story.append(Paragraph(f"<b>Especialidade:</b> {item['especialidade']}", styles['Normal']))
                    story.append(Spacer(1, 0.1 * inch))
        
        # Adicionando seções ao PDF
        add_section("Formação em Graduação", entry["graducao"])
        add_section("Mestrado", entry["mestrado"])
        add_section("Doutorado", entry["doutorado"])
        add_section("Pós-Doutorado", entry["pos_doutorado"])
        add_section("Linhas de Pesquisa", entry["linhas_pesquisa"])
        story.append(Spacer(1, 0.2 * inch))  # Adicionando um espaço menor entre diferentes arquivos

    doc.build(story)

def main(input_folder, output_pdf):
    # Procurando todos os arquivos XML na pasta especificada
    xml_files = glob.glob(os.path.join(input_folder, "*.xml"))
    extracted_data = []

    for xml_file in xml_files:
        extracted_data.append(extract_areas_of_knowledge(xml_file))

    # Criando o PDF com os dados extraídos
    create_pdf(extracted_data, output_pdf)

if __name__ == "__main__":
    input_folder = r"C:\Users\radim\Desktop\todos_curriculos"
    output_pdf = r"C:\Users\radim\Desktop\areas_linhas_cnpq.pdf"
    main(input_folder, output_pdf)
