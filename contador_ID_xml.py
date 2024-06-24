import csv

def count_lattes_ids(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        ids = list(reader)
        return len(ids)

file_path = r'C:\Users\radim\Desktop\R358737.csv'  # caminho do arquivo de IDs
total_ids = count_lattes_ids(file_path)
print(f"Total de currículos Lattes cadastrados: {total_ids}")
