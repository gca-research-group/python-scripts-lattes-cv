import os
import glob
import xml.etree.ElementTree as ET

def extract_areas_of_knowledge(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
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
    
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def print_individual_summary(entry):
    if not entry:
        print("Nenhum dado encontrado.")
        return

    print(f"Orientador: {entry['filename']}")
    
    def print_section(title, items):
        if items:
            print(f"{title}:")
            for item in items:
                print(f"  Grande Área: {item['grande_area']}")
                print(f"  Área: {item['area']}")
                print(f"  Sub-área: {item['sub_area']}")
                print(f"  Especialidade: {item['especialidade']}")
                print("")

    print_section("Formação em Graduação", entry["graducao"])
    print_section("Mestrado", entry["mestrado"])
    print_section("Doutorado", entry["doutorado"])
    print_section("Pós-Doutorado", entry["pos_doutorado"])
    print_section("Linhas de Pesquisa", entry["linhas_pesquisa"])
    print("-----\n")

def main(input_folder):
    # Procurando todos os arquivos XML na pasta especificada
    xml_files = glob.glob(os.path.join(input_folder, "*.xml"))
    
    if not xml_files:
        print("Nenhum arquivo XML encontrado no diretório especificado.")
        return

    print(f"Arquivos encontrados: {len(xml_files)}")
    
    for xml_file in xml_files:
        print(f"Processando arquivo: {xml_file}")
        data = extract_areas_of_knowledge(xml_file)
        print_individual_summary(data)

if __name__ == "__main__":
    input_folder = r"C:\Users\radim\Desktop\ppgmmc"
    main(input_folder)
