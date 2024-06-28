import os
import glob
import xml.etree.ElementTree as ET

def extract_areas_of_knowledge(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    data = {
        "filename": os.path.basename(xml_file), 
        "graduacao": [], 
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
        data["graduacao"].extend(get_areas_of_knowledge(formacao))

    for formacao in root.findall(".//MESTRADO"):
        data["mestrado"].extend(get_areas_of_knowledge(formacao))

    for formacao in root.findall(".//DOUTORADO"):
        data["doutorado"].extend(get_areas_of_knowledge(formacao))

    for formacao in root.findall(".//POS-DOUTORADO"):
        data["pos_doutorado"].extend(get_areas_of_knowledge(formacao))

    for pesquisa in root.findall(".//LINHA-DE-PESQUISA"):
        data["linhas_pesquisa"].extend(get_areas_of_knowledge(pesquisa))

    return data

def print_data(data):
    for entry in data:
        # Imprimindo título com o nome do arquivo
        print(f"Orientador: {entry['filename']}")
        print("-" * 40)
        
        def add_section(title, items):
            if items:
                print(f"{title}")
                for item in items:
                    # Imprimindo detalhes das áreas de conhecimento
                    print(f"  Grande Área: {item['grande_area']}")
                    print(f"  Área: {item['area']}")
                    print(f"  Sub-área: {item['sub_area']}")
                    print(f"  Especialidade: {item['especialidade']}")
                    print()

        # Adicionando seções
        add_section("Formação em Graduação", entry["graduacao"])
        add_section("Mestrado", entry["mestrado"])
        add_section("Doutorado", entry["doutorado"])
        add_section("Pós-Doutorado", entry["pos_doutorado"])
        add_section("Linhas de Pesquisa", entry["linhas_pesquisa"])
        print("-" * 40)

def main(input_folder):
    # Procurando todos os arquivos XML na pasta especificada
    xml_files = glob.glob(os.path.join(input_folder, "*.xml"))
    extracted_data = []

    for xml_file in xml_files:
        extracted_data.append(extract_areas_of_knowledge(xml_file))

    # Imprimindo os dados extraídos no terminal
    print_data(extracted_data)

if __name__ == "__main__":
    input_folder = r"C:\Users\radim\Desktop\ppgmmc"
    main(input_folder)
