##########################################################################################################################################################
"""
Este código Python analisa arquivos XML para extrair informações sobre orientadores e suas áreas de conhecimento,
e gera um relatório em formato PDF com essas informações. 

1. Função `extrair_informacoes_orientador`:
   - Abre e analisa um arquivo XML.
   - Obtém o nome do arquivo (sem a extensão) que representa o nome do orientador.
   - Chama a função `extrair_areas_conhecimento` para obter as áreas de conhecimento do orientador.
   - Retorna o nome do orientador e um conjunto de áreas de conhecimento.

2. Função `extrair_areas_conhecimento`:
   - Recebe a raiz do documento XML.
   - Extrai as áreas de conhecimento (Área, Sub-área e Especialidade) e adiciona essas informações a um conjunto.
   - Retorna o conjunto de áreas de conhecimento.

3. Script principal:
   - Define o caminho para a pasta contendo os arquivos XML.
   - Inicializa uma lista para armazenar informações de orientadores e suas áreas de conhecimento.
   - Itera sobre os arquivos XML na pasta:
     - Chama a função `extrair_informacoes_orientador` para obter o nome do orientador e suas áreas de conhecimento.
     - Armazena essas informações na lista.
   - Verifica e imprime o número de arquivos XML encontrados e processados.
   - Cria um documento PDF utilizando a biblioteca `reportlab`.
   - Adiciona informações dos orientadores e suas áreas de conhecimento ao PDF, organizando o layout e criando novas páginas conforme necessário.
   - Salva o PDF com o nome especificado.

"""
########################################################################################################################################################

import os
from lxml import etree
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extrair_informacoes_orientador(file_path):
    try:
        nome_arquivo = os.path.basename(file_path).split(".")[0]  # Obtém o nome do arquivo sem a extensão
        return nome_arquivo, extrair_areas_conhecimento(etree.parse(file_path).getroot())
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return "Erro ao processar arquivo", set()

def extrair_areas_conhecimento(root):
    areas_conhecimento = set()

    areas = root.xpath("//AREA-DO-CONHECIMENTO-1")
    for area in areas:
        nome_area = area.get("NOME-DA-AREA-DO-CONHECIMENTO")
        sub_area = area.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO")
        especialidade = area.get("NOME-DA-ESPECIALIDADE")
        if nome_area:
            areas_conhecimento.add(nome_area)
        if sub_area:
            areas_conhecimento.add(sub_area)
        if especialidade:
            areas_conhecimento.add(especialidade)

    return areas_conhecimento

# Pasta contendo os arquivos XML
pasta_xml = r"C:\Users\radim\Desktop\todos_curriculos"

# Lista para armazenar informações de orientadores e suas áreas de conhecimento
orientadores_areas = []

# Iterar sobre os arquivos XML na pasta
arquivos_xml = [arq for arq in os.listdir(pasta_xml) if arq.endswith(".xml")]
print(f"Número de arquivos XML encontrados: {len(arquivos_xml)}")

for arquivo in arquivos_xml:
    arquivo_path = os.path.join(pasta_xml, arquivo)
    primeiro_nome, areas_conhecimento = extrair_informacoes_orientador(arquivo_path)
    orientadores_areas.append((primeiro_nome, areas_conhecimento))

# Verificar quantos orientadores foram processados
print(f"Número de orientadores processados: {len(orientadores_areas)}")

# Criar PDF
c = canvas.Canvas("areas_todo_lattes.pdf", pagesize=letter)

# Adicionar informações dos orientadores e suas áreas de conhecimento ao PDF
y = 750
for i, (orientador, areas) in enumerate(orientadores_areas):
    y -= 20
    if y < 50:  # Se a posição y está muito baixa, iniciar uma nova página
        c.showPage()
        y = 750
    c.drawString(100, y, f"Orientador {i+1}: {orientador}")
    for area in areas:
        y -= 20
        if y < 50:  # Se a posição y está muito baixa, iniciar uma nova página
            c.showPage()
            y = 750
        c.drawString(120, y, f"- {area}")

c.save()
