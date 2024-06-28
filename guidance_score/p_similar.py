import os
import glob
import xml.etree.ElementTree as ET

def extract_knowledge_areas(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    areas = []
    
    def get_areas_of_knowledge(element):
        for area in element.findall('.//AREA-DO-CONHECIMENTO-1'):
            grande_area = area.get("NOME-GRANDE-AREA-DO-CONHECIMENTO")
            area_nome = area.get("NOME-DA-AREA-DO-CONHECIMENTO")
            sub_area = area.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO")
            especialidade = area.get("NOME-DA-ESPECIALIDADE")
            
            areas.append({
                'grande_area': grande_area,
                'area': area_nome,
                'sub_area': sub_area,
                'especialidade': especialidade
            })

    for formacao in root.findall('.//GRADUACAO'):
        get_areas_of_knowledge(formacao)

    for formacao in root.findall('.//MESTRADO'):
        get_areas_of_knowledge(formacao)

    for formacao in root.findall('.//DOUTORADO'):
        get_areas_of_knowledge(formacao)

    for formacao in root.findall('.//POS-DOUTORADO'):
        get_areas_of_knowledge(formacao)
    
    return areas

def compare_areas(area1, area2):
    score = 0
    if area1['grande_area'] == area2['grande_area']:
        score += 1
        if area1['area'] == area2['area']:
            score += 2
            if area1['sub_area'] == area2['sub_area']:
                score += 3
                if area1['especialidade'] == area2['especialidade']:
                    score += 5
    return score

def main(reference_xml, folder_path):
    reference_areas = extract_knowledge_areas(reference_xml)
    xml_files = glob.glob(os.path.join(folder_path, '*.xml'))
    results = []

    for xml_file in xml_files:
        current_areas = extract_knowledge_areas(xml_file)
        total_score = 0
        for area1 in reference_areas:
            for area2 in current_areas:
                score = compare_areas(area1, area2)
                total_score += score
        
        if total_score > 0:
            results.append({
                'file_name': os.path.basename(xml_file),
                'total_score': total_score
            })

    results.sort(key=lambda x: x['total_score'], reverse=True)

    # Imprimir resultados no terminal
    print("Resultados da Comparação de Áreas de Conhecimento")
    print("=" * 50)
    for result in results:
        print(f"Arquivo: {result['file_name']} - Pontuação Total: {result['total_score']}")
        print("-" * 50)

if __name__ == "__main__":
    reference_xml = r'C:\Users\radim\Desktop\Miriam Ines Marchi.xml'
    folder_path = r'C:\Users\radim\Desktop\ppgmmc'
    main(reference_xml, folder_path)
