import os
import xml.etree.ElementTree as ET
from collections import Counter
from fpdf import FPDF

def extract_areas_from_lattes(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    data = {
        'grandes_areas_conhecimento': [],
        'areas_conhecimento': [],
        'sub_areas_conhecimento': [],
        'especialidades': []
    }

    # Áreas de Atuação
    for area in root.findall(".//AREAS-DE-ATUACAO/AREA-DE-ATUACAO"):
        grandes_area = area.attrib.get('NOME-GRANDE-AREA-DO-CONHECIMENTO')
        if grandes_area:
            data['grandes_areas_conhecimento'].append(grandes_area)
        area_conhecimento = area.attrib.get('NOME-DA-AREA-DO-CONHECIMENTO')
        if area_conhecimento:
            data['areas_conhecimento'].append(area_conhecimento)
        sub_area = area.attrib.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO')
        if sub_area:
            data['sub_areas_conhecimento'].append(sub_area)
        especialidade = area.attrib.get('NOME-DA-ESPECIALIDADE')
        if especialidade:
            data['especialidades'].append(especialidade)
    
    return data

def process_all_files(directory):
    summary = {
        'grandes_areas_conhecimento': Counter(),
        'areas_conhecimento': Counter(),
        'sub_areas_conhecimento': Counter(),
        'especialidades': Counter()
    }

    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            data = extract_areas_from_lattes(file_path)
            for key in summary:
                summary[key].update(data[key])
    
    return summary

def print_summary(summary):
    for key, counter in summary.items():
        total_items = sum(counter.values())
        print(f"{key.replace('_', ' ')}: {total_items} itens")
        for item, count in counter.items():
            percentage = (count / total_items) * 100 if total_items > 0 else 0
            print(f"  - {item}: {count} vezes ({percentage:.2f}%)")

def save_summary_to_pdf(summary, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, counter in summary.items():
        total_items = sum(counter.values())
        pdf.cell(200, 10, txt=f"{key.replace('_', ' ')}: {total_items} itens", ln=True)
        for item, count in counter.items():
            percentage = (count / total_items) * 100 if total_items > 0 else 0
            pdf.cell(200, 10, txt=f"  - {item}: {count} vezes ({percentage:.2f}%)", ln=True)
    
    pdf.output(file_path)

# Exemplo de uso
directory_path = r'C:\Users\radim\Desktop\ppgmmc'
summary_data = process_all_files(directory_path)

# Exibir resultados
print_summary(summary_data)

# Perguntar ao usuário se deseja salvar em PDF
save_to_pdf = input("Deseja salvar o resumo em um arquivo PDF? (s/n): ").lower()
if save_to_pdf == 's':
    pdf_file_path = r'C:\Users\radim\Desktop\summary.pdf'
    save_summary_to_pdf(summary_data, pdf_file_path)
    print(f"Resumo salvo em {pdf_file_path}")
