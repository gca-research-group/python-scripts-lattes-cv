import os
import xml.etree.ElementTree as ET
from fpdf import FPDF

def contar_itens(tag_name, root):
    return len(root.findall(f".//{tag_name}"))

def extract_participations(root):
    participations = {
        'bancas de graduacao': contar_itens("DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO", root),
        'bancas de mestrado': contar_itens("DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO", root),
        'bancas de doutorado': contar_itens("DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO", root)
    }
    return participations

def count_orientacoes_concluidas(root):
    orientacoes_concluidas = {
        'iniciacao_cientifica': 0,
        'graduacao': 0,
        'mestrado': 0,
        'doutorado': 0
    }

    orientacoes_map = {
        'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO': 'mestrado',
        'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO': 'doutorado'
    }

    for termo_orientacao, categoria in orientacoes_map.items():
        orientacoes_concluidas[categoria] += len(list(root.iter(termo_orientacao)))

    for orientacao in root.iter('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS'):
        natureza = orientacao.attrib.get('NATUREZA', '').upper()
        if natureza == 'INICIACAO_CIENTIFICA':
            orientacoes_concluidas['iniciacao_cientifica'] += 1
        elif natureza == 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO':
            orientacoes_concluidas['graduacao'] += 1

    return orientacoes_concluidas

def count_orientacoes_andamento(root):
    orientacoes_andamento = {
        'iniciacao_cientifica': 0,
        'graduacao': 0,
        'mestrado': 0,
        'doutorado': 0
    }

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Iniciação Científica':
            orientacoes_andamento['iniciacao_cientifica'] += 1

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Graduação':
            orientacoes_andamento['graduacao'] += 1

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Dissertação de mestrado':
            orientacoes_andamento['mestrado'] += 1

    for orientacao in root.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
        natureza = orientacao.attrib.get('NATUREZA', '')
        if natureza == 'Tese de doutorado':
            orientacoes_andamento['doutorado'] += 1

    return orientacoes_andamento

def calcular_pontuacao(experiencia, pesos, tempos):
    n_total = sum(experiencia.values())
    if n_total == 0:
        return 0

    pontuacao = 0
    for i, nivel in enumerate(["iniciacao_cientifica", "graduacao", "mestrado", "doutorado"]):
        pontuacao += (pesos[i] * tempos[i] * experiencia[nivel]) / n_total
    
    return pontuacao

def analisar_arquivo(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
        return None
    except ET.ParseError:
        print(f"Erro ao parsear o arquivo: {file_path}")
        return None

    contagens = {
        "formacao_do_orientador": {
            "graduacoes": contar_itens("GRADUACAO", root),
            "especializacoes": contar_itens("ESPECIALIZACAO", root),
            "mestrados": contar_itens("MESTRADO", root),
            "doutorados": contar_itens("DOUTORADO", root),
            "pos_doutorados": contar_itens("POS-DOUTORADO", root)
        },
        "areas_de_atuacao": contar_itens("AREA-DE-ATUACAO", root),
        "premios_titulos": contar_itens("PREMIO-TITULO", root),
        "artigos_completos_publicados": contar_itens("ARTIGO-PUBLICADO", root),
        "livros_publicados_ou_organizados": contar_itens("LIVROS-PUBLICADOS-OU-ORGANIZADOS", root),
        "capitulos_livros_publicados": contar_itens("CAPITULO-DE-LIVRO-PUBLICADO", root),
        "apresentacoes_trabalho": contar_itens("APRESENTACAO-DE-TRABALHO", root),
        "participacao_eventos": contar_itens("PARTICIPACAO-EM-EVENTO", root),
        "organizacao_eventos": contar_itens("ORGANIZACAO-DE-EVENTO", root),
        "patentes": contar_itens("PATENTE", root),
        "softwares": contar_itens("SOFTWARE", root),
        "projetos_tecnicos": contar_itens("PROJETO-TECNICO", root),
        "trabalhos_tecnicos": contar_itens("TRABALHO-TECNICO", root),
        "trabalhos_artisticos": contar_itens("TRABALHO-ARTISTICO", root),
        "linhas_de_pesquisa": contar_itens("LINHA-DE-PESQUISA", root),
        "idiomas": contar_itens("IDIOMA", root)
    }
    
    participacoes = extract_participations(root)
    contagens.update(participacoes)

    orientacoes_concluidas = count_orientacoes_concluidas(root)
    orientacoes_andamento = count_orientacoes_andamento(root)
    
    contagens.update({
        "orientacoes_concluidas": orientacoes_concluidas,
        "orientacoes_andamento": orientacoes_andamento
    })

    experiencia = {
        'iniciacao_cientifica': orientacoes_concluidas['iniciacao_cientifica'] + orientacoes_andamento['iniciacao_cientifica'],
        'graduacao': orientacoes_concluidas['graduacao'] + orientacoes_andamento['graduacao'],
        'mestrado': orientacoes_concluidas['mestrado'] + orientacoes_andamento['mestrado'],
        'doutorado': orientacoes_concluidas['doutorado'] + orientacoes_andamento['doutorado']
    }
    
    pesos = [1, 2, 3, 4]
    tempos = [1, 1, 2, 4]
    contagens['pontuacao_experiencia'] = calcular_pontuacao(experiencia, pesos, tempos)

    return contagens

def gerar_relatorio_pdf(resultados):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Análise de XML", ln=True, align='C')

    for file_name, contagens in resultados.items():
        pdf.ln(10)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=f"Arquivo: {file_name}", ln=True)
        pdf.set_font("Arial", size=12)
        
        # Exibir formação do orientador
        pdf.cell(200, 10, txt="Formação do Orientador:", ln=True)
        for chave, valor in contagens["formacao_do_orientador"].items():
            pdf.cell(200, 10, txt=f"{chave}: {valor} itens", ln=True)
        
        # Separar orientações concluídas e em andamento
        pdf.cell(200, 10, txt="Orientações Concluídas:", ln=True)
        for chave, valor in contagens["orientacoes_concluidas"].items():
            pdf.cell(200, 10, txt=f"{chave}: {valor} itens", ln=True)
        
        pdf.cell(200, 10, txt="Orientações em Andamento:", ln=True)
        for chave, valor in contagens["orientacoes_andamento"].items():
            pdf.cell(200, 10, txt=f"{chave}: {valor} itens", ln=True)

        # Exibir participações em bancas
        pdf.cell(200, 10, txt="Participações em Bancas:", ln=True)
        for chave, valor in contagens.items():
            if chave in ["bancas de graduacao", "bancas de mestrado", "bancas de doutorado"]:
                pdf.cell(200, 10, txt=f"{chave}: {valor} itens", ln=True)
        
        # Exibir demais contagens
        for chave, valor in contagens.items():
            if chave not in ["formacao_do_orientador", "orientacoes_concluidas", "orientacoes_andamento", "bancas de graduacao", "bancas de mestrado", "bancas de doutorado"]:
                pdf.cell(200, 10, txt=f"{chave}: {valor} itens", ln=True)

    pdf.output("relatorio_agrupado.pdf")
    print("Relatório gerado: relatorio_agrupado.pdf")

def exibir_resultados(resultados):
    total_contagens = {}
    total_arquivos = len(resultados)
    
    for file_name, contagens in resultados.items():
        print(f"\nArquivo: {file_name}")
        
        print("Formação do Orientador:")
        for chave, valor in contagens["formacao_do_orientador"].items():
            print(f"{chave}: {valor} itens")
            total_contagens[chave] = total_contagens.get(chave, 0) + valor
        
        print("Orientações Concluídas:")
        for chave, valor in contagens["orientacoes_concluidas"].items():
            print(f"{chave}: {valor} itens")
            total_contagens[chave] = total_contagens.get(chave, 0) + valor
        
        print("Orientações em Andamento:")
        for chave, valor in contagens["orientacoes_andamento"].items():
            print(f"{chave}: {valor} itens")
            total_contagens[chave] = total_contagens.get(chave, 0) + valor

        print("Participações em Bancas:")
        for chave, valor in contagens.items():
            if chave in ["bancas de graduacao", "bancas de mestrado", "bancas de doutorado"]:
                print(f"{chave}: {valor} itens")
                total_contagens[chave] = total_contagens.get(chave, 0) + valor
        
        for chave, valor in contagens.items():
            if chave not in ["formacao_do_orientador", "orientacoes_concluidas", "orientacoes_andamento", "bancas de graduacao", "bancas de mestrado", "bancas de doutorado"]:
                print(f"{chave}: {valor} itens")
                total_contagens[chave] = total_contagens.get(chave, 0) + valor
    
    print("\nTotais de todos os arquivos analisados:")
    for chave, valor in total_contagens.items():
        print(f"{chave}: {valor} itens")
    
    print(f"\nTotal de arquivos XML analisados: {total_arquivos}")

def main():
    folder_path = r'C:\Users\radim\Desktop\ppgmmc'

    resultados = {}
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xml"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Analisando arquivo: {file_path}")
            contagens = analisar_arquivo(file_path)
            if contagens:
                resultados[file_name] = contagens

    exibir_resultados(resultados)

    gerar_pdf = input("\nDeseja gerar o relatório em PDF? (s/n): ").strip().lower()
    if gerar_pdf == 's':
        gerar_relatorio_pdf(resultados)

if __name__ == "__main__":
    main()
