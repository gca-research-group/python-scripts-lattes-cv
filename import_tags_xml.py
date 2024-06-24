import xml.etree.ElementTree as ET

def extract_tags(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    tags = set()

    def recurse(node):
        tags.add(node.tag)
        for child in node:
            recurse(child)
    
    recurse(root)
    
    return tags

# Caminho do arquivo XML
xml_file_path = r'C:\Users\radim\Desktop\frantz.xml'
tags = extract_tags(xml_file_path)
tags = sorted(tags)

# Imprimindo as tags
for tag in tags:
    print(tag)
